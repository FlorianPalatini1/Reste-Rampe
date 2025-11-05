"""
Monitoring Dashboard Backend API
Provides real-time Mailcow monitoring data and statistics
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import json
import asyncio
import time
from datetime import datetime, timedelta
import httpx
from enum import Enum
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ======================== MODELS ========================

class StatusEnum(str, Enum):
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class QuotaData(BaseModel):
    mailbox: str
    used_mb: float
    total_mb: float
    usage_percent: float
    status: StatusEnum

class APIHealth(BaseModel):
    status: StatusEnum
    response_time_ms: float
    timestamp: str
    error_message: Optional[str] = None

class MailboxSummary(BaseModel):
    total_mailboxes: int
    total_quota_mb: float
    total_used_mb: float
    average_usage_percent: float
    status: StatusEnum
    mailboxes: List[QuotaData]

class ForwardingRule(BaseModel):
    source: str
    destinations: List[str]
    active: bool

class SystemStats(BaseModel):
    api_health: APIHealth
    mailbox_summary: MailboxSummary
    forwarding_rules: List[ForwardingRule]
    collection_timestamp: str
    update_interval_seconds: int

class HistoricalData(BaseModel):
    timestamp: str
    total_used_mb: float
    average_usage_percent: float
    mailbox_count: int

# ======================== FASTAPI APP ========================

app = FastAPI(title="Monitoring Dashboard Backend", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for monitoring
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================== CONFIGURATION ========================

MAILCOW_API_URL = os.getenv("MAILCOW_API_URL", "https://mailcow.example.com/api/v1")
MAILCOW_API_KEY = os.getenv("MAILCOW_API_KEY", "")
MAILCOW_VERIFY_SSL = os.getenv("MAILCOW_VERIFY_SSL", "false").lower() == "true"
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"  # Enable demo mode by default

# In-memory storage for historical data
historical_data: List[Dict[str, Any]] = []
last_update = None
current_stats = None

# ======================== HELPER FUNCTIONS ========================

async def make_api_request(endpoint: str, timeout: int = 10) -> tuple[Optional[Any], Optional[str]]:
    """Make authenticated request to Mailcow API"""
    try:
        url = f"{MAILCOW_API_URL}{endpoint}"
        headers = {"X-API-Key": MAILCOW_API_KEY}
        
        async with httpx.AsyncClient(verify=MAILCOW_VERIFY_SSL, timeout=timeout) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), None
    except httpx.RequestError as e:
        return None, f"Request error: {str(e)}"
    except httpx.HTTPStatusError as e:
        return None, f"HTTP error {e.response.status_code}"
    except Exception as e:
        return None, f"Error: {str(e)}"

def get_demo_mailboxes() -> List[Dict[str, Any]]:
    """Generate demo mailbox data for testing"""
    import random
    return [
        {
            "username": "admin@reste-rampe.tech",
            "bytes": int(2.5 * 1024 * 1024 * 1024),  # 2.5 GB
            "quota": int(5 * 1024 * 1024 * 1024),     # 5 GB quota
            "active": 1
        },
        {
            "username": "info@reste-rampe.tech",
            "bytes": int(1.2 * 1024 * 1024 * 1024),   # 1.2 GB
            "quota": int(3 * 1024 * 1024 * 1024),     # 3 GB quota
            "active": 1
        },
        {
            "username": "support@reste-rampe.tech",
            "bytes": int(0.8 * 1024 * 1024 * 1024),   # 0.8 GB
            "quota": int(2 * 1024 * 1024 * 1024),     # 2 GB quota
            "active": 1
        },
        {
            "username": "noreply@reste-rampe.tech",
            "bytes": int(0.1 * 1024 * 1024 * 1024),   # 0.1 GB
            "quota": int(1 * 1024 * 1024 * 1024),     # 1 GB quota
            "active": 1
        },
    ]

def calculate_quota_status(usage_percent: float) -> StatusEnum:
    """Determine status based on quota usage"""
    if usage_percent >= 90:
        return StatusEnum.CRITICAL
    elif usage_percent >= 75:
        return StatusEnum.WARNING
    else:
        return StatusEnum.HEALTHY

def get_overall_status(mailboxes: List[QuotaData]) -> StatusEnum:
    """Determine overall status based on mailboxes"""
    if not mailboxes:
        return StatusEnum.HEALTHY
    
    statuses = [m.status for m in mailboxes]
    if StatusEnum.CRITICAL in statuses:
        return StatusEnum.CRITICAL
    elif StatusEnum.WARNING in statuses:
        return StatusEnum.WARNING
    else:
        return StatusEnum.HEALTHY

# ======================== API ENDPOINTS ========================

@app.get("/health")
async def health_check():
    """Simple health check"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/health", response_model=APIHealth)
async def api_health():
    """Check Mailcow API health"""
    start_time = time.time()
    
    data, error = await make_api_request("/status")
    response_time_ms = (time.time() - start_time) * 1000
    
    if error:
        return APIHealth(
            status=StatusEnum.CRITICAL,
            response_time_ms=response_time_ms,
            timestamp=datetime.utcnow().isoformat(),
            error_message=error
        )
    
    return APIHealth(
        status=StatusEnum.HEALTHY,
        response_time_ms=response_time_ms,
        timestamp=datetime.utcnow().isoformat(),
        error_message=None
    )

@app.get("/api/mailboxes", response_model=MailboxSummary)
async def get_mailboxes():
    """Get all mailboxes and their quota"""
    try:
        # Use demo data if API key not configured
        if not MAILCOW_API_KEY or MAILCOW_API_KEY == "your_api_key_here" or DEMO_MODE:
            logger.info("Using demo mailbox data (DEMO_MODE=%s, API_KEY=%s)", DEMO_MODE, bool(MAILCOW_API_KEY))
            data = get_demo_mailboxes()
        else:
            data, error = await make_api_request("/mailbox")
            if error:
                logger.warning(f"API error, falling back to demo: {error}")
                data = get_demo_mailboxes()
        
        if not data:
            logger.warning("No mailbox data, using demo")
            data = get_demo_mailboxes()
        
        mailboxes = []
        total_quota = 0.0
        total_used = 0.0
        
        # Parse mailbox data
        if isinstance(data, list):
            for mailbox in data:
                try:
                    if mailbox.get("active") == 1:  # Only active mailboxes
                        used_mb = float(mailbox.get("bytes", 0)) / (1024 * 1024)
                        total_mb = float(mailbox.get("quota", 0)) / (1024 * 1024)
                        
                        if total_mb > 0:
                            usage_percent = (used_mb / total_mb) * 100
                        else:
                            usage_percent = 0
                        
                        status = calculate_quota_status(usage_percent)
                        
                        mailboxes.append(QuotaData(
                            mailbox=mailbox.get("username", "unknown"),
                            used_mb=round(used_mb, 2),
                            total_mb=round(total_mb, 2),
                            usage_percent=round(usage_percent, 1),
                            status=status
                        ))
                        
                        total_quota += total_mb
                        total_used += used_mb
                except Exception as e:
                    logger.error(f"Error processing mailbox {mailbox}: {e}")
                    continue
        
        # Calculate averages
        avg_usage = 0
        if mailboxes and total_quota > 0:
            avg_usage = (total_used / total_quota) * 100
        
        overall_status = get_overall_status(mailboxes)
        
        summary = MailboxSummary(
            total_mailboxes=len(mailboxes),
            total_quota_mb=round(total_quota, 2),
            total_used_mb=round(total_used, 2),
            average_usage_percent=round(avg_usage, 1),
            status=overall_status,
            mailboxes=sorted(mailboxes, key=lambda x: x.usage_percent, reverse=True)
        )
        
        # Store historical data
        store_historical_data(summary)
        logger.info(f"Mailbox summary: {len(mailboxes)} mailboxes, {avg_usage:.1f}% avg usage")
        
        return summary
        
    except Exception as e:
        logger.error(f"FATAL Error fetching mailboxes: {type(e).__name__}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/forwarding", response_model=List[ForwardingRule])
async def get_forwarding_rules():
    """Get all forwarding rules"""
    try:
        data, error = await make_api_request("/forwarding/all")
        
        if error or not data:
            return []
        
        rules = []
        if isinstance(data, list):
            for rule in data:
                # Parse destination addresses (comma-separated)
                destinations = []
                dest_str = rule.get("destination", "")
                if dest_str:
                    destinations = [d.strip() for d in dest_str.split(",")]
                
                rules.append(ForwardingRule(
                    source=rule.get("source", ""),
                    destinations=destinations,
                    active=rule.get("active") == 1
                ))
        
        return rules
        
    except Exception as e:
        logger.error(f"Error fetching forwarding rules: {str(e)}")
        return []

@app.get("/api/stats", response_model=SystemStats)
async def get_system_stats():
    """Get complete system statistics"""
    global current_stats
    
    try:
        logger.info("Collecting system stats...")
        
        # Get API health
        health_data = await api_health()
        logger.info(f"API health: {health_data.status}")
        
        # Get mailbox summary
        mailbox_summary = await get_mailboxes()
        logger.info(f"Mailbox summary: {mailbox_summary.total_mailboxes} mailboxes")
        
        # Get forwarding rules
        forwarding = await get_forwarding_rules()
        logger.info(f"Forwarding rules: {len(forwarding)} rules")
        
        stats = SystemStats(
            api_health=health_data,
            mailbox_summary=mailbox_summary,
            forwarding_rules=forwarding,
            collection_timestamp=datetime.utcnow().isoformat(),
            update_interval_seconds=30
        )
        
        current_stats = stats
        logger.info("Stats collection completed successfully")
        return stats
        
    except Exception as e:
        logger.error(f"FATAL Error collecting stats: {type(e).__name__}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

def store_historical_data(summary: MailboxSummary):
    """Store historical data for trending"""
    global historical_data
    
    data_point = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_used_mb": summary.total_used_mb,
        "average_usage_percent": summary.average_usage_percent,
        "mailbox_count": summary.total_mailboxes
    }
    
    historical_data.append(data_point)
    
    # Keep only last 24 hours of data (one point per 30 seconds = 2880 points)
    if len(historical_data) > 2880:
        historical_data = historical_data[-2880:]

@app.get("/api/history", response_model=List[HistoricalData])
async def get_history(limit: int = 100):
    """Get historical data for trending"""
    recent = historical_data[-limit:] if historical_data else []
    return [HistoricalData(**d) for d in recent]

@app.get("/api/status")
async def get_status():
    """Quick status endpoint"""
    global current_stats
    
    if not current_stats:
        raise HTTPException(status_code=503, detail="No data available yet")
    
    return {
        "overall_status": current_stats.mailbox_summary.status,
        "total_mailboxes": current_stats.mailbox_summary.total_mailboxes,
        "average_usage": current_stats.mailbox_summary.average_usage_percent,
        "api_health": current_stats.api_health.status,
        "timestamp": current_stats.collection_timestamp
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
