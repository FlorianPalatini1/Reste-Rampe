#!/bin/bash

# GroceryMate - Frontend & Manual Testing Script
# Usage: bash frontend/tests/manual_tests.sh

BASE_URL="http://127.0.0.1:5174"
API_URL="http://127.0.0.1:8000/api"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}GroceryMate - Frontend Testing Checklist${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}\n"

echo -e "${YELLOW}Before starting: Ensure backend and frontend are running${NC}"
echo -e "Backend: curl http://127.0.0.1:8000/docs"
echo -e "Frontend: Open ${BASE_URL} in browser\n"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ TEST 1: REGISTRATION FLOW                             ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}\n"

echo "Steps:"
echo "1. Navigate to ${BASE_URL}/register"
echo "2. Enter:"
echo "   - Email: newuser_$(date +%s)@test.com"
echo "   - Username: testuser_$(date +%s)"
echo "   - Password: TestPassword123!"
echo "3. Click 'Registrieren' / 'Register'"
echo ""
echo "Expected Results:"
echo -e "  ${GREEN}✓${NC} Page redirects to Dashboard"
echo -e "  ${GREEN}✓${NC} User avatar shows in top-right"
echo -e "  ${GREEN}✓${NC} localStorage contains 'auth_token'"
echo ""
echo "Verification in DevTools:"
echo "  - Press F12, go to Application → Local Storage"
echo "  - Look for 'auth_token' key"
echo "  - Value should look like: eyJhbGciOiJ..."
echo ""
read -p "Did Test 1 PASS? (y/n): " test1_result

echo -e "\n${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ TEST 2: LOGIN FLOW                                    ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}\n"

echo "Steps:"
echo "1. If logged in, click 'Logout'"
echo "2. Navigate to ${BASE_URL}/login"
echo "3. Enter:"
echo "   - Username/Email: demo@gm.test"
echo "   - Password: demo123"
echo "4. Click 'Anmelden' / 'Login'"
echo ""
echo "Expected Results:"
echo -e "  ${GREEN}✓${NC} Page redirects to Dashboard"
echo -e "  ${GREEN}✓${NC} User avatar shows (TE for tester101)"
echo -e "  ${GREEN}✓${NC} localStorage contains 'auth_token'"
echo ""
read -p "Did Test 2 PASS? (y/n): " test2_result

echo -e "\n${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ TEST 3: INVALID LOGIN                                 ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}\n"

echo "Steps:"
echo "1. Navigate to ${BASE_URL}/login"
echo "2. Enter:"
echo "   - Username: demo@gm.test"
echo "   - Password: wrongpassword"
echo "3. Click 'Anmelden' / 'Login'"
echo ""
echo "Expected Results:"
echo -e "  ${RED}✗${NC} NOT redirected to Dashboard"
echo -e "  ${GREEN}✓${NC} Error message displayed"
echo -e "  ${GREEN}✓${NC} Stays on login page"
echo -e "  ${GREEN}✓${NC} localStorage does NOT have 'auth_token'"
echo ""
read -p "Did Test 3 PASS? (y/n): " test3_result

echo -e "\n${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ TEST 4: PROTECTED ROUTES                              ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}\n"

echo "Steps:"
echo "1. Click 'Logout' button"
echo "2. Verify localStorage no longer has 'auth_token' (DevTools → Application)"
echo "3. Manually navigate to:"
echo "   - ${BASE_URL}/ingredients"
echo "   - ${BASE_URL}/recipes"
echo "   - ${BASE_URL}/shopping"
echo ""
echo "Expected Results:"
echo -e "  ${RED}✗${NC} NOT shown protected pages"
echo -e "  ${GREEN}✓${NC} Redirected to ${BASE_URL}/login for each"
echo ""
echo "4. Now login as demo@gm.test / demo123"
echo "5. Try accessing same routes again"
echo ""
echo "Expected Results:"
echo -e "  ${GREEN}✓${NC} All routes now accessible"
echo ""
read -p "Did Test 4 PASS? (y/n): " test4_result

echo -e "\n${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ TEST 5: DATA ISOLATION                                ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}\n"

echo "Steps (User A):"
echo "1. Login as: demo@gm.test / demo123"
echo "2. Go to Zutaten (Ingredients)"
echo "3. Create new ingredient:"
echo "   - Name: 'Secret Ingredient A - $(date +%s)'"
echo "   - Category: Vegetables"
echo "   - Location: Fridge"
echo "   - Quantity: 1"
echo "   - Unit: kg"
echo "4. Click Save"
echo ""
echo "Steps (User B):"
echo "1. Click Logout"
echo "2. Register new user:"
echo "   - Email: userb_$(date +%s)@test.com"
echo "   - Username: userb_$(date +%s)"
echo "   - Password: UserBPass123!"
echo "3. Go to Zutaten (Ingredients)"
echo ""
echo "Expected Results:"
echo -e "  ${RED}✗${NC} 'Secret Ingredient A' is NOT visible"
echo -e "  ${GREEN}✓${NC} Only User B's ingredients shown (likely empty or their own)"
echo ""
echo "4. Logout and login again as User A (demo@gm.test)"
echo "5. Go to Zutaten"
echo ""
echo "Expected Results:"
echo -e "  ${GREEN}✓${NC} 'Secret Ingredient A' is visible again"
echo -e "  ${RED}✗${NC} No User B ingredients visible"
echo ""
read -p "Did Test 5 PASS? (y/n): " test5_result

echo -e "\n${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ TEST 6: TOKEN EXPIRATION (Optional/Manual)            ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}\n"

echo "Option A - Manual Token Expiration (Immediate Test):"
echo "1. Login as demo@gm.test"
echo "2. Open DevTools (F12) → Console"
echo "3. Run:"
echo "   localStorage.setItem('auth_token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjAwMDAwMDB9.invalid');"
echo "4. Refresh page or navigate to /ingredients"
echo ""
echo "Expected Results:"
echo -e "  ${RED}✗${NC} NOT shown ingredients"
echo -e "  ${GREEN}✓${NC} Redirected to login"
echo ""
echo "Option B - Natural Expiration:"
echo "1. Login at time T"
echo "2. Wait 1 hour + 1 minute"
echo "3. Try accessing protected route"
echo ""
echo "Expected Results:"
echo -e "  ${GREEN}✓${NC} Redirected to login (same as Option A)"
echo ""
read -p "Did Test 6 PASS? (y/n): " test6_result

echo -e "\n${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ TEST 7: LOGOUT                                        ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}\n"

echo "Steps:"
echo "1. Login as demo@gm.test / demo123"
echo "2. Verify on Dashboard"
echo "3. Click 'Logout' button (top-right)"
echo ""
echo "Expected Results:"
echo -e "  ${GREEN}✓${NC} Redirected to ${BASE_URL}/login"
echo -e "  ${GREEN}✓${NC} localStorage NO LONGER has 'auth_token'"
echo ""
echo "4. Click browser BACK button"
echo ""
echo "Expected Results:"
echo -e "  ${RED}✗${NC} NOT going back to Dashboard"
echo -e "  ${GREEN}✓${NC} Stays on login page (router prevents access)"
echo ""
echo "5. Manually navigate to ${BASE_URL}/ingredients"
echo ""
echo "Expected Results:"
echo -e "  ${GREEN}✓${NC} Redirected to login"
echo ""
read -p "Did Test 7 PASS? (y/n): " test7_result

echo -e "\n${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ SECURITY CHECK 1: PASSWORD HASHING                    ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}\n"

echo "Steps:"
echo "1. Connect to PostgreSQL:"
echo "   docker exec -it postgres psql -U grocery_user -d grocery_db"
echo ""
echo "2. Run query:"
echo "   SELECT id, email, username, hashed_password FROM public.user LIMIT 5;"
echo ""
echo "Expected Results:"
echo -e "  ${GREEN}✓${NC} All hashed_password values start with \$2b\$ or \$2y\$ (bcrypt)"
echo -e "  ${RED}✗${NC} NO passwords are plain text (like password123)"
echo -e "  ${RED}✗${NC} NO passwords are MD5 or SHA hashes"
echo ""
echo "Example of CORRECT output:"
echo "  | 1 | demo@gm.test | demo | \$2b\$12\$abcdefg1234567890...xyz |"
echo ""
read -p "Did Security Check 1 PASS? (y/n): " sec1_result

echo -e "\n${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ SECURITY CHECK 2: TOKEN IN AUTHORIZATION HEADER       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}\n"

echo "Steps:"
echo "1. Login as demo@gm.test / demo123"
echo "2. Open DevTools (F12) → Network tab"
echo "3. Go to Zutaten (Ingredients) page"
echo "4. Look for request to: GET .../api/ingredients/"
echo "5. Click on it, go to 'Headers' tab"
echo "6. Scroll to 'Request Headers'"
echo ""
echo "Expected Results:"
echo -e "  ${GREEN}✓${NC} Authorization header present:"
echo "   Authorization: Bearer eyJhbGciOiJIUzI1NiI..."
echo -e "  ${RED}✗${NC} NO token in URL query parameters"
echo -e "  ${RED}✗${NC} NO token in cookies"
echo ""
read -p "Did Security Check 2 PASS? (y/n): " sec2_result

echo -e "\n${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ SECURITY CHECK 3: JWT CLAIMS                          ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}\n"

echo "Steps:"
echo "1. Login and copy auth_token from localStorage:"
echo "   - DevTools → Application → Local Storage"
echo "   - Copy value of 'auth_token' key"
echo ""
echo "2. Go to https://jwt.io"
echo "3. Paste token in 'Encoded' section"
echo "4. Look at 'Decoded' → 'Payload' section"
echo ""
echo "Expected Results:"
echo -e "  ${GREEN}✓${NC} Payload contains:"
echo "   - 'sub': demo@gm.test (or your user email)"
echo "   - 'exp': Unix timestamp ~1 hour in future"
echo "   - 'iat': Unix timestamp of now"
echo -e "  ${RED}✗${NC} NO password in payload"
echo -e "  ${RED}✗${NC} NO sensitive data exposed"
echo ""
echo "5. To check remaining time, run in console:"
echo "   let token = localStorage.getItem('auth_token');"
echo "   let parts = token.split('.');"
echo "   let payload = JSON.parse(atob(parts[1]));"
echo "   console.log('Expires in:', (payload.exp - Math.floor(Date.now()/1000)), 'seconds');"
echo ""
read -p "Did Security Check 3 PASS? (y/n): " sec3_result

echo -e "\n${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ SECURITY CHECK 4: DATA ACCESS CONTROL                 ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}\n"

echo "Steps:"
echo "1. Login as User A (demo@gm.test)"
echo "2. Create an ingredient 'Secret A' (note the ID from network tab)"
echo "3. Logout and login as User B (or register new)"
echo "4. Open DevTools → Console"
echo ""
echo "5. Try to fetch all ingredients:"
echo "   fetch('/api/ingredients/').then(r => r.json()).then(d => console.log(d))"
echo ""
echo "Expected Results:"
echo -e "  ${GREEN}✓${NC} 'Secret A' is NOT in the response"
echo ""
echo "6. Try to fetch User A's ingredient by ID (let's say ID=123):"
echo "   fetch('/api/ingredients/123').then(r => r.json()).then(d => console.log(d))"
echo ""
echo "Expected Results:"
echo -e "  ${GREEN}✓${NC} Empty response or 404 error"
echo -e "  ${RED}✗${NC} NOT showing User A's ingredient"
echo ""
read -p "Did Security Check 4 PASS? (y/n): " sec4_result

echo -e "\n${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ SECURITY CHECK 5: INVALID TOKEN REJECTION             ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}\n"

echo "Steps:"
echo "1. Login as demo@gm.test"
echo "2. Open DevTools → Console"
echo ""
echo "3. Modify the token:"
echo "   let oldToken = localStorage.getItem('auth_token');"
echo "   let modified = oldToken.slice(0, -5) + 'XXXXX';"
echo "   localStorage.setItem('auth_token', modified);"
echo ""
echo "4. Refresh page or navigate to /ingredients"
echo ""
echo "Expected Results:"
echo -e "  ${RED}✗${NC} NOT showing ingredients"
echo -e "  ${GREEN}✓${NC} Redirected to login"
echo -e "  ${GREEN}✓${NC} Console shows 401 error"
echo ""
read -p "Did Security Check 5 PASS? (y/n): " sec5_result

echo -e "\n${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║ TEST RESULTS SUMMARY                                  ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}\n"

declare -A results
results[1]=$test1_result
results[2]=$test2_result
results[3]=$test3_result
results[4]=$test4_result
results[5]=$test5_result
results[6]=$test6_result
results[7]=$test7_result
results[8]=$sec1_result
results[9]=$sec2_result
results[10]=$sec3_result
results[11]=$sec4_result
results[12]=$sec5_result

passed=0
failed=0

for i in {1..12}; do
    if [ "${results[$i]}" = "y" ] || [ "${results[$i]}" = "Y" ]; then
        ((passed++))
    else
        ((failed++))
    fi
done

echo "Test 1 (Registration):             ${results[1]}"
echo "Test 2 (Login):                    ${results[2]}"
echo "Test 3 (Invalid Login):            ${results[3]}"
echo "Test 4 (Protected Routes):         ${results[4]}"
echo "Test 5 (Data Isolation):           ${results[5]}"
echo "Test 6 (Token Expiration):         ${results[6]}"
echo "Test 7 (Logout):                   ${results[7]}"
echo "Security 1 (Password Hashing):     ${results[8]}"
echo "Security 2 (Token Headers):        ${results[9]}"
echo "Security 3 (JWT Claims):           ${results[10]}"
echo "Security 4 (Data Access):          ${results[11]}"
echo "Security 5 (Invalid Tokens):       ${results[12]}"
echo ""
echo -e "${GREEN}Passed: $passed${NC} | ${RED}Failed: $failed${NC} | Total: 12"
echo ""

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🎉 ALL TESTS PASSED! 🎉${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
else
    echo -e "${RED}═══════════════════════════════════════════════════════${NC}"
    echo -e "${RED}⚠️  ${failed} TESTS FAILED - Review the results above${NC}"
    echo -e "${RED}═══════════════════════════════════════════════════════${NC}"
fi

echo ""
