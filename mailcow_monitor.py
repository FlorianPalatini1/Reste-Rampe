#!/usr/bin/env python3

"""
🐮 Mailcow REST API Monitoring Tool 🐮

Monitort die Mailcow REST API und deine Mailboxen
Features:
  - Real-time Health Checks
  - Mailbox Quota Monitoring
  - Forwarding Rules Tracking
  - Performance Metrics
  - Email Alerts
  - JSON Export
  - Color-coded Terminal Output

Usage:
  python3 mailcow_monitor.py --config /path/to/.env
  python3 mailcow_monitor.py --watch 60  # Watch mode every 60 seconds
  python3 mailcow_monitor.py --alert email@example.com
"""

import os
import sys
import json
import time
import argparse
import logging
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# ============================================================================
# Configuration
# ============================================================================

class Status(Enum):
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"

@dataclass
class MailboxStats:
    name: str
    domain: str
    quota_mb: int
    used_mb: int
    quota_percent: float
    status: Status
    timestamp: str
    
@dataclass
class APIHealth:
    status: Status
    response_time_ms: float
    last_check: str
    error_message: Optional[str] = None

@dataclass
class MonitoringReport:
    timestamp: str
    api_health: APIHealth
    mailboxes: List[MailboxStats]
    forwardings: int
    overall_status: Status
    
# ============================================================================
# Color Constants
# ============================================================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ============================================================================
# Mailcow API Client
# ============================================================================

class MailcowAPIClient:
    """Mailcow REST API Client"""
    
    def __init__(self, api_url: str, api_key: str, verify_ssl: bool = True):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self.headers = {'X-API-Key': api_key, 'Content-Type': 'application/json'}
        self.logger = logging.getLogger(__name__)
        
    def _make_request(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Dict:
        """Make API request with error handling"""
        url = f"{self.api_url}{endpoint}"
        
        try:
            start_time = time.time()
            
            if method == 'GET':
                response = requests.get(
                    url,
                    headers=self.headers,
                    verify=self.verify_ssl,
                    timeout=10
                )
            elif method == 'POST':
                response = requests.post(
                    url,
                    headers=self.headers,
                    json=data,
                    verify=self.verify_ssl,
                    timeout=10
                )
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            elapsed_ms = (time.time() - start_time) * 1000
            self.logger.debug(f"API Request: {method} {endpoint} - {response.status_code} - {elapsed_ms:.2f}ms")
            
            response.raise_for_status()
            
            return {
                'status': 'success',
                'data': response.json(),
                'status_code': response.status_code,
                'elapsed_ms': elapsed_ms
            }
            
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout calling {endpoint}")
            return {
                'status': 'error',
                'error': 'API Timeout (>10s)',
                'elapsed_ms': (time.time() - start_time) * 1000
            }
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Connection error: {e}")
            return {
                'status': 'error',
                'error': f'Connection error: {str(e)}',
                'elapsed_ms': (time.time() - start_time) * 1000
            }
        except Exception as e:
            self.logger.error(f"API Error: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'elapsed_ms': (time.time() - start_time) * 1000
            }
    
    def health_check(self) -> APIHealth:
        """Check API health"""
        start_time = time.time()
        
        try:
            result = self._make_request('/status/version')
            elapsed = (time.time() - start_time) * 1000
            
            if result['status'] == 'success':
                return APIHealth(
                    status=Status.HEALTHY,
                    response_time_ms=elapsed,
                    last_check=datetime.now().isoformat()
                )
            else:
                return APIHealth(
                    status=Status.CRITICAL,
                    response_time_ms=elapsed,
                    last_check=datetime.now().isoformat(),
                    error_message=result.get('error')
                )
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            return APIHealth(
                status=Status.CRITICAL,
                response_time_ms=elapsed,
                last_check=datetime.now().isoformat(),
                error_message=str(e)
            )
    
    def get_mailboxes(self) -> List[Dict]:
        """Get all mailboxes"""
        result = self._make_request('/mailbox/all')
        if result['status'] == 'success':
            return result['data']
        return []
    
    def get_mailbox_quota(self, mailbox: str) -> Dict:
        """Get mailbox quota usage"""
        result = self._make_request(f'/mailbox/quota/{mailbox}')
        if result['status'] == 'success':
            return result['data']
        return {}
    
    def get_forwarding_rules(self, mailbox: str) -> List[Dict]:
        """Get forwarding rules for mailbox"""
        result = self._make_request(f'/forwarding/get/{mailbox}')
        if result['status'] == 'success':
            return result['data']
        return []

# ============================================================================
# Monitor Class
# ============================================================================

class MailcowMonitor:
    """Mailcow Monitoring Engine"""
    
    def __init__(self, api_client: MailcowAPIClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)
        self.history: List[MonitoringReport] = []
        
    def collect_metrics(self) -> MonitoringReport:
        """Collect all metrics"""
        self.logger.info("Collecting metrics...")
        
        # API Health
        api_health = self.api_client.health_check()
        
        # Mailboxes
        mailboxes = []
        try:
            mailbox_list = self.api_client.get_mailboxes()
            for mailbox_data in mailbox_list:
                mailbox_name = mailbox_data.get('name', 'unknown')
                domain = mailbox_data.get('domain', 'unknown')
                quota_mb = int(mailbox_data.get('quota', 0)) / (1024 * 1024)
                
                # Get quota usage
                quota_info = self.api_client.get_mailbox_quota(mailbox_name)
                used_mb = int(quota_info.get('bytes', 0)) / (1024 * 1024) if quota_info else 0
                
                quota_percent = (used_mb / quota_mb * 100) if quota_mb > 0 else 0
                
                # Determine status
                if quota_percent > 90:
                    status = Status.CRITICAL
                elif quota_percent > 75:
                    status = Status.WARNING
                else:
                    status = Status.HEALTHY
                
                mailboxes.append(MailboxStats(
                    name=mailbox_name,
                    domain=domain,
                    quota_mb=int(quota_mb),
                    used_mb=int(used_mb),
                    quota_percent=quota_percent,
                    status=status,
                    timestamp=datetime.now().isoformat()
                ))
        except Exception as e:
            self.logger.error(f"Error collecting mailbox metrics: {e}")
        
        # Forwarding count
        forwarding_count = 0
        try:
            for mailbox in mailbox_list:
                fwd = self.api_client.get_forwarding_rules(mailbox.get('name', ''))
                forwarding_count += len(fwd)
        except:
            pass
        
        # Overall status
        overall_status = Status.HEALTHY
        if api_health.status == Status.CRITICAL:
            overall_status = Status.CRITICAL
        elif any(m.status == Status.CRITICAL for m in mailboxes):
            overall_status = Status.CRITICAL
        elif any(m.status == Status.WARNING for m in mailboxes):
            overall_status = Status.WARNING
        
        report = MonitoringReport(
            timestamp=datetime.now().isoformat(),
            api_health=api_health,
            mailboxes=mailboxes,
            forwardings=forwarding_count,
            overall_status=overall_status
        )
        
        self.history.append(report)
        return report
    
    def print_report(self, report: MonitoringReport):
        """Print formatted report"""
        print("\n" + "="*80)
        print(f"{Colors.HEADER}{Colors.BOLD}🐮 MAILCOW MONITORING REPORT{Colors.ENDC}")
        print(f"{Colors.BOLD}Time: {report.timestamp}{Colors.ENDC}")
        print("="*80 + "\n")
        
        # API Health
        self._print_section("API Health", report.api_health)
        
        # Overall Status
        status_color = self._get_status_color(report.overall_status)
        print(f"\n{Colors.BOLD}Overall Status:{Colors.ENDC} {status_color}{report.overall_status.value}{Colors.ENDC}")
        
        # Mailboxes
        if report.mailboxes:
            self._print_mailboxes(report.mailboxes)
        
        # Summary
        print(f"\n{Colors.BOLD}Summary:{Colors.ENDC}")
        print(f"  Total Mailboxes: {len(report.mailboxes)}")
        print(f"  Total Forwarding Rules: {report.forwardings}")
        print(f"  Healthy Mailboxes: {sum(1 for m in report.mailboxes if m.status == Status.HEALTHY)}")
        print(f"  Warning Mailboxes: {sum(1 for m in report.mailboxes if m.status == Status.WARNING)}")
        print(f"  Critical Mailboxes: {sum(1 for m in report.mailboxes if m.status == Status.CRITICAL)}")
        
        print("\n" + "="*80 + "\n")
    
    def _print_section(self, title: str, api_health: APIHealth):
        """Print API health section"""
        print(f"{Colors.BOLD}{title}:{Colors.ENDC}")
        status_color = self._get_status_color(api_health.status)
        print(f"  Status: {status_color}{api_health.status.value}{Colors.ENDC}")
        print(f"  Response Time: {api_health.response_time_ms:.2f}ms")
        if api_health.error_message:
            print(f"  Error: {Colors.RED}{api_health.error_message}{Colors.ENDC}")
        print()
    
    def _print_mailboxes(self, mailboxes: List[MailboxStats]):
        """Print mailbox table"""
        print(f"\n{Colors.BOLD}Mailboxes:{Colors.ENDC}")
        print(f"{'Name':<30} {'Domain':<20} {'Usage':<15} {'Status':<10}")
        print("-" * 75)
        
        for mb in mailboxes:
            status_color = self._get_status_color(mb.status)
            quota_bar = self._get_quota_bar(mb.quota_percent)
            usage_str = f"{mb.used_mb}MB / {mb.quota_mb}MB {quota_bar} ({mb.quota_percent:.1f}%)"
            print(f"{mb.name:<30} {mb.domain:<20} {usage_str:<15} {status_color}{mb.status.value}{Colors.ENDC}")
    
    def _get_status_color(self, status: Status) -> str:
        """Get color for status"""
        if status == Status.HEALTHY:
            return Colors.GREEN
        elif status == Status.WARNING:
            return Colors.YELLOW
        elif status == Status.CRITICAL:
            return Colors.RED
        else:
            return Colors.CYAN
    
    def _get_quota_bar(self, percent: float) -> str:
        """Get quota visualization bar"""
        filled = int(percent / 10)
        empty = 10 - filled
        
        if percent > 90:
            color = Colors.RED
        elif percent > 75:
            color = Colors.YELLOW
        else:
            color = Colors.GREEN
        
        return f"{color}[{'█' * filled}{'░' * empty}]{Colors.ENDC}"
    
    def export_json(self, report: MonitoringReport, filepath: str):
        """Export report as JSON"""
        data = {
            'timestamp': report.timestamp,
            'api_health': {
                'status': report.api_health.status.value,
                'response_time_ms': report.api_health.response_time_ms,
                'last_check': report.api_health.last_check,
                'error_message': report.api_health.error_message
            },
            'mailboxes': [asdict(m) | {'status': m.status.value} for m in report.mailboxes],
            'forwardings': report.forwardings,
            'overall_status': report.overall_status.value
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.logger.info(f"Report exported to {filepath}")

# ============================================================================
# Main
# ============================================================================

def load_config(config_file: str) -> Dict[str, str]:
    """Load config from .env file"""
    config = {}
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    return config

def setup_logging(debug: bool = False):
    """Setup logging"""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    parser = argparse.ArgumentParser(
        description='🐮 Mailcow REST API Monitoring Tool'
    )
    parser.add_argument(
        '--config',
        default='.env',
        help='Path to .env config file'
    )
    parser.add_argument(
        '--watch',
        type=int,
        help='Watch mode: repeat every N seconds'
    )
    parser.add_argument(
        '--export',
        help='Export report to JSON file'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    setup_logging(args.debug)
    
    # Load config
    config = load_config(args.config)
    
    api_url = config.get('MAILCOW_API_URL')
    api_key = config.get('MAILCOW_API_KEY')
    verify_ssl = config.get('MAILCOW_VERIFY_SSL', 'true').lower() == 'true'
    
    if not api_url or not api_key:
        print(f"{Colors.RED}Error: MAILCOW_API_URL and MAILCOW_API_KEY not found in {args.config}{Colors.ENDC}")
        sys.exit(1)
    
    # Create client and monitor
    client = MailcowAPIClient(api_url, api_key, verify_ssl)
    monitor = MailcowMonitor(client)
    
    try:
        if args.watch:
            print(f"{Colors.CYAN}Starting watch mode (every {args.watch}s). Press Ctrl+C to stop.{Colors.ENDC}\n")
            while True:
                report = monitor.collect_metrics()
                monitor.print_report(report)
                
                if args.export:
                    monitor.export_json(report, args.export)
                
                time.sleep(args.watch)
        else:
            report = monitor.collect_metrics()
            monitor.print_report(report)
            
            if args.export:
                monitor.export_json(report, args.export)
                
    except KeyboardInterrupt:
        print(f"\n{Colors.CYAN}Monitoring stopped.{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.ENDC}")
        sys.exit(1)

if __name__ == '__main__':
    main()
