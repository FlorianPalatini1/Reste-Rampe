#!/usr/bin/env python3
"""
Mailcow API Integration Test Script

Tests Mailcow REST API connectivity and operations:
- Connection test
- Create mailbox
- Get mailbox details
- Get quota
- Add forwarding
- Delete forwarding
- Delete mailbox
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.mailcow_api import MailcowAPI


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def test_connection():
    """Test API connection"""
    print_header("1. Testing Mailcow API Connection")
    
    mailcow = MailcowAPI()
    
    print(f"API URL: {mailcow.base_url}")
    print(f"Domain: {mailcow.domain}")
    print(f"API Key: {'*' * 20}...{mailcow.api_key[-4:] if mailcow.api_key else 'NOT SET'}")
    
    if not mailcow.api_key:
        print("\n❌ ERROR: MAILCOW_API_KEY environment variable not set!")
        return False
    
    success = mailcow.test_connection()
    if success:
        print("✅ Connection successful!")
        return True
    else:
        print("❌ Connection failed!")
        return False


def test_mailbox_operations():
    """Test mailbox CRUD operations"""
    print_header("2. Testing Mailbox Operations")
    
    mailcow = MailcowAPI()
    test_username = "testuser123"
    test_password = "Test@1234567890"
    
    # Create
    print(f"\nCreating test mailbox: {test_username}@{mailcow.domain}")
    success = mailcow.create_mailbox(
        username=test_username,
        password=test_password,
        display_name="Test User",
        quota_mb=1024,
    )
    if success:
        print("✅ Mailbox created successfully")
    else:
        print("❌ Failed to create mailbox")
        return False
    
    # Get details
    print(f"\nFetching mailbox details...")
    details = mailcow.get_mailbox_details(test_username)
    if details:
        print("✅ Mailbox details retrieved:")
        print(f"   - Email: {details.get('username')}")
        print(f"   - Active: {details.get('active') == 1}")
        print(f"   - Quota: {int(details.get('quota', 0) / (1024*1024))}MB")
        print(f"   - Messages: {details.get('messages', 0)}")
    else:
        print("❌ Failed to fetch mailbox details")
        return False
    
    # Get quota
    print(f"\nGetting mailbox quota...")
    quota = mailcow.get_mailbox_quota(test_username)
    if quota:
        print("✅ Quota retrieved:")
        print(f"   - Total: {int(quota['quota_total'] / (1024*1024))}MB")
        print(f"   - Used: {int(quota['quota_used'] / (1024*1024))}MB")
        print(f"   - Percent: {quota['quota_percent']}%")
    else:
        print("❌ Failed to fetch quota")
        return False
    
    # Delete
    print(f"\nDeleting mailbox: {test_username}@{mailcow.domain}")
    success = mailcow.delete_mailbox(test_username)
    if success:
        print("✅ Mailbox deleted successfully")
    else:
        print("❌ Failed to delete mailbox")
        return False
    
    return True


def test_forwarding():
    """Test forwarding rules"""
    print_header("3. Testing Email Forwarding")
    
    mailcow = MailcowAPI()
    test_username = "testfwd123"
    test_password = "Test@1234567890"
    test_forward_dest = "user@gmail.com"
    
    # Create mailbox
    print(f"\nCreating mailbox for forwarding test: {test_username}@{mailcow.domain}")
    success = mailcow.create_mailbox(
        username=test_username,
        password=test_password,
        display_name="Forwarding Test",
    )
    if not success:
        print("❌ Failed to create mailbox")
        return False
    print("✅ Mailbox created")
    
    # Add forwarding
    print(f"\nAdding forwarding rule: {test_username}@{mailcow.domain} → {test_forward_dest}")
    success = mailcow.add_forwarding(
        username=test_username,
        forward_to=test_forward_dest,
        keep_local=True,
    )
    if success:
        print("✅ Forwarding rule added")
    else:
        print("❌ Failed to add forwarding rule")
        mailcow.delete_mailbox(test_username)
        return False
    
    # Get forwarding rules
    print(f"\nFetching forwarding rules...")
    rules = mailcow.get_forwarding_rules(test_username)
    if rules:
        print(f"✅ Forwarding rules retrieved: {rules}")
    else:
        print("❌ Failed to fetch forwarding rules")
        mailcow.delete_mailbox(test_username)
        return False
    
    # Remove forwarding
    print(f"\nRemoving forwarding rule...")
    success = mailcow.remove_forwarding(test_username, test_forward_dest)
    if success:
        print("✅ Forwarding rule removed")
    else:
        print("❌ Failed to remove forwarding rule")
        mailcow.delete_mailbox(test_username)
        return False
    
    # Delete mailbox
    print(f"\nCleaning up: deleting mailbox")
    mailcow.delete_mailbox(test_username)
    print("✅ Cleanup complete")
    
    return True


def test_password_change():
    """Test password change"""
    print_header("4. Testing Password Change")
    
    mailcow = MailcowAPI()
    test_username = "testpwd123"
    old_password = "Test@1234567890"
    new_password = "NewTest@1234567890"
    
    # Create mailbox
    print(f"\nCreating mailbox: {test_username}@{mailcow.domain}")
    success = mailcow.create_mailbox(
        username=test_username,
        password=old_password,
        display_name="Password Test",
    )
    if not success:
        print("❌ Failed to create mailbox")
        return False
    print("✅ Mailbox created")
    
    # Change password
    print(f"\nChanging password...")
    success = mailcow.set_mailbox_password(test_username, new_password)
    if success:
        print("✅ Password changed successfully")
    else:
        print("❌ Failed to change password")
        mailcow.delete_mailbox(test_username)
        return False
    
    # Cleanup
    print(f"\nCleaning up: deleting mailbox")
    mailcow.delete_mailbox(test_username)
    print("✅ Cleanup complete")
    
    return True


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  MAILCOW REST API INTEGRATION TEST".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    tests = [
        ("Connection", test_connection),
        ("Mailbox Operations", test_mailbox_operations),
        ("Email Forwarding", test_forwarding),
        ("Password Change", test_password_change),
    ]
    
    results = {}
    
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with exception:")
            print(f"   {str(e)}")
            results[name] = False
    
    # Summary
    print_header("Test Summary")
    for name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(results.values())
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if all_passed:
        print("\n🎉 All tests passed! Mailcow API integration is working correctly.")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check Mailcow API configuration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
