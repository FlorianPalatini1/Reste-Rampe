"""
Mailcow REST API Integration Module

Handles all interactions with Mailcow API for mailbox management,
quotas, forwarding, and admin operations.
"""

import os
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Mailcow API Configuration
MAILCOW_API_URL = os.getenv("MAILCOW_API_URL", "https://mailcow.example.com/api/v1")
MAILCOW_API_KEY = os.getenv("MAILCOW_API_KEY", "")
MAILCOW_DOMAIN = os.getenv("MAILCOW_DOMAIN", "reste-rampe.tech")
MAILCOW_API_TIMEOUT = 10

# Disable SSL verification for self-signed certs (only in dev!)
MAILCOW_VERIFY_SSL = os.getenv("MAILCOW_VERIFY_SSL", "false").lower() == "true"


class MailcowAPI:
    """Mailcow REST API Client"""

    def __init__(self):
        self.base_url = MAILCOW_API_URL.rstrip("/")
        self.api_key = MAILCOW_API_KEY
        self.domain = MAILCOW_DOMAIN
        self.verify_ssl = MAILCOW_VERIFY_SSL

    def _headers(self) -> Dict[str, str]:
        """Generate API headers with auth token"""
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Make authenticated request to Mailcow API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/get/mailbox/all")
            data: JSON body for POST/PUT requests
            params: Query parameters

        Returns:
            Response JSON

        Raises:
            Exception: If API request fails
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=self._headers(),
                timeout=MAILCOW_API_TIMEOUT,
                verify=self.verify_ssl,
            )

            # Log the request
            logger.debug(f"Mailcow API {method} {endpoint}: {response.status_code}")

            if response.status_code == 401:
                logger.error("Mailcow API: Invalid API key")
                raise Exception("Mailcow API: Invalid API key")

            if response.status_code == 403:
                logger.error("Mailcow API: Access denied")
                raise Exception("Mailcow API: Access denied")

            if response.status_code >= 400:
                logger.error(f"Mailcow API Error {response.status_code}: {response.text}")
                raise Exception(f"Mailcow API Error: {response.status_code}")

            return response.json()

        except requests.RequestException as e:
            logger.error(f"Mailcow API request failed: {str(e)}")
            raise Exception(f"Mailcow API connection error: {str(e)}")

    # ==================== MAILBOX OPERATIONS ====================

    def create_mailbox(
        self,
        username: str,
        password: str,
        display_name: Optional[str] = None,
        quota_mb: int = 5120,  # 5GB default
    ) -> bool:
        """
        Create a new mailbox in Mailcow

        Args:
            username: Email username (without domain)
            password: Mailbox password
            display_name: Display name (e.g., "John Doe")
            quota_mb: Quota in megabytes (default 5GB)

        Returns:
            True if successful, False otherwise
        """
        try:
            mailbox_email = f"{username}@{self.domain}"

            payload = {
                "username": mailbox_email,
                "password": password,
                "password2": password,
                "mailbox": mailbox_email,
                "name": display_name or username,
                "quota": quota_mb * 1024 * 1024,  # Convert MB to bytes
                "active": 1,
                "force_pw_update": 0,
                "sogo_access": 1,
            }

            result = self._make_request("POST", "/add/mailbox", data=payload)

            # Mailcow returns {"status": "success", "msg": [...]}
            if isinstance(result, dict) and result.get("status") == "success":
                logger.info(f"Created mailbox: {mailbox_email}")
                return True

            logger.warning(f"Mailbox creation failed: {result}")
            return False

        except Exception as e:
            logger.error(f"Failed to create mailbox for {username}: {str(e)}")
            return False

    def delete_mailbox(self, username: str) -> bool:
        """
        Delete a mailbox from Mailcow

        Args:
            username: Email username (without domain)

        Returns:
            True if successful, False otherwise
        """
        try:
            mailbox_email = f"{username}@{self.domain}"

            payload = {"username": [mailbox_email]}

            result = self._make_request("POST", "/delete/mailbox", data=payload)

            if isinstance(result, dict) and result.get("status") == "success":
                logger.info(f"Deleted mailbox: {mailbox_email}")
                return True

            logger.warning(f"Mailbox deletion failed: {result}")
            return False

        except Exception as e:
            logger.error(f"Failed to delete mailbox for {username}: {str(e)}")
            return False

    def get_mailbox_details(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get mailbox details from Mailcow

        Args:
            username: Email username (without domain)

        Returns:
            Mailbox details dict, or None if not found/error
        """
        try:
            mailbox_email = f"{username}@{self.domain}"

            result = self._make_request("GET", f"/get/mailbox/{mailbox_email}")

            # Mailcow returns list with one item
            if isinstance(result, list) and len(result) > 0:
                return result[0]

            logger.warning(f"Mailbox not found: {mailbox_email}")
            return None

        except Exception as e:
            logger.error(f"Failed to get mailbox details for {username}: {str(e)}")
            return None

    def get_mailbox_quota(self, username: str) -> Optional[Dict[str, int]]:
        """
        Get mailbox quota usage

        Args:
            username: Email username (without domain)

        Returns:
            Dict with 'quota_total' and 'quota_used' in bytes, or None if error
        """
        try:
            details = self.get_mailbox_details(username)
            if not details:
                return None

            # Mailcow returns quota in bytes
            quota_total = details.get("quota", 0)
            quota_used = details.get("bytes", 0)

            return {
                "quota_total": quota_total,
                "quota_used": quota_used,
                "quota_percent": int((quota_used / quota_total * 100)) if quota_total > 0 else 0,
            }

        except Exception as e:
            logger.error(f"Failed to get quota for {username}: {str(e)}")
            return None

    # ==================== FORWARDING OPERATIONS ====================

    def add_forwarding(
        self,
        username: str,
        forward_to: str,
        keep_local: bool = True,
    ) -> bool:
        """
        Add email forwarding rule

        Args:
            username: Email username (without domain)
            forward_to: Destination email address
            keep_local: Keep copy of email on mailbox (default True)

        Returns:
            True if successful, False otherwise
        """
        try:
            mailbox_email = f"{username}@{self.domain}"

            payload = {
                "forwarding": mailbox_email,
                "forwarding_dest": forward_to,
                "keep": 1 if keep_local else 0,
            }

            result = self._make_request("POST", "/add/forwarding", data=payload)

            if isinstance(result, dict) and result.get("status") == "success":
                logger.info(f"Added forwarding: {mailbox_email} → {forward_to}")
                return True

            logger.warning(f"Forwarding creation failed: {result}")
            return False

        except Exception as e:
            logger.error(f"Failed to add forwarding for {username}: {str(e)}")
            return False

    def remove_forwarding(self, username: str, forward_to: str) -> bool:
        """
        Remove email forwarding rule

        Args:
            username: Email username (without domain)
            forward_to: Destination email address to remove

        Returns:
            True if successful, False otherwise
        """
        try:
            mailbox_email = f"{username}@{self.domain}"

            payload = {
                "forwarding": mailbox_email,
                "forwarding_dest": forward_to,
            }

            result = self._make_request("POST", "/delete/forwarding", data=payload)

            if isinstance(result, dict) and result.get("status") == "success":
                logger.info(f"Removed forwarding: {mailbox_email} → {forward_to}")
                return True

            logger.warning(f"Forwarding removal failed: {result}")
            return False

        except Exception as e:
            logger.error(f"Failed to remove forwarding for {username}: {str(e)}")
            return False

    def get_forwarding_rules(self, username: str) -> Optional[List[str]]:
        """
        Get all forwarding rules for a mailbox

        Args:
            username: Email username (without domain)

        Returns:
            List of forwarding destinations, or None if error
        """
        try:
            mailbox_email = f"{username}@{self.domain}"

            result = self._make_request("GET", f"/get/forwarding/{mailbox_email}")

            if isinstance(result, list):
                return [item.get("forwarding_dest") for item in result if item.get("forwarding_dest")]

            return None

        except Exception as e:
            logger.error(f"Failed to get forwarding rules for {username}: {str(e)}")
            return None

    # ==================== PASSWORD OPERATIONS ====================

    def set_mailbox_password(self, username: str, password: str) -> bool:
        """
        Change mailbox password

        Args:
            username: Email username (without domain)
            password: New password

        Returns:
            True if successful, False otherwise
        """
        try:
            mailbox_email = f"{username}@{self.domain}"

            payload = {
                "username": mailbox_email,
                "password": password,
                "password2": password,
            }

            result = self._make_request("POST", "/edit/mailbox", data=payload)

            if isinstance(result, dict) and result.get("status") == "success":
                logger.info(f"Changed password for mailbox: {mailbox_email}")
                return True

            logger.warning(f"Password change failed: {result}")
            return False

        except Exception as e:
            logger.error(f"Failed to change password for {username}: {str(e)}")
            return False

    # ==================== ADMIN OPERATIONS ====================

    def get_all_mailboxes(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get all mailboxes in the domain (Admin only)

        Returns:
            List of mailbox dicts, or None if error
        """
        try:
            result = self._make_request("GET", "/get/mailbox/all")

            if isinstance(result, list):
                # Filter to only our domain
                return [m for m in result if self.domain in m.get("username", "")]

            return None

        except Exception as e:
            logger.error(f"Failed to get all mailboxes: {str(e)}")
            return None

    def disable_mailbox(self, username: str) -> bool:
        """
        Disable a mailbox (Admin only)

        Args:
            username: Email username (without domain)

        Returns:
            True if successful, False otherwise
        """
        try:
            mailbox_email = f"{username}@{self.domain}"

            payload = {
                "username": mailbox_email,
                "active": 0,
            }

            result = self._make_request("POST", "/edit/mailbox", data=payload)

            if isinstance(result, dict) and result.get("status") == "success":
                logger.info(f"Disabled mailbox: {mailbox_email}")
                return True

            return False

        except Exception as e:
            logger.error(f"Failed to disable mailbox for {username}: {str(e)}")
            return False

    def enable_mailbox(self, username: str) -> bool:
        """
        Enable a mailbox (Admin only)

        Args:
            username: Email username (without domain)

        Returns:
            True if successful, False otherwise
        """
        try:
            mailbox_email = f"{username}@{self.domain}"

            payload = {
                "username": mailbox_email,
                "active": 1,
            }

            result = self._make_request("POST", "/edit/mailbox", data=payload)

            if isinstance(result, dict) and result.get("status") == "success":
                logger.info(f"Enabled mailbox: {mailbox_email}")
                return True

            return False

        except Exception as e:
            logger.error(f"Failed to enable mailbox for {username}: {str(e)}")
            return False

    def set_mailbox_quota(self, username: str, quota_mb: int) -> bool:
        """
        Set mailbox quota (Admin only)

        Args:
            username: Email username (without domain)
            quota_mb: Quota in megabytes

        Returns:
            True if successful, False otherwise
        """
        try:
            mailbox_email = f"{username}@{self.domain}"

            payload = {
                "username": mailbox_email,
                "quota": quota_mb * 1024 * 1024,  # Convert MB to bytes
            }

            result = self._make_request("POST", "/edit/mailbox", data=payload)

            if isinstance(result, dict) and result.get("status") == "success":
                logger.info(f"Set quota for {mailbox_email}: {quota_mb}MB")
                return True

            return False

        except Exception as e:
            logger.error(f"Failed to set quota for {username}: {str(e)}")
            return False

    # ==================== CONNECTION TEST ====================

    def test_connection(self) -> bool:
        """
        Test Mailcow API connectivity and authentication

        Returns:
            True if connection successful, False otherwise
        """
        try:
            result = self._make_request("GET", "/get/mailbox/all")
            logger.info("✅ Mailcow API connection successful")
            return True
        except Exception as e:
            logger.error(f"❌ Mailcow API connection failed: {str(e)}")
            return False
