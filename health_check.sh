#!/bin/bash
# 📊 Reste-Rampe Health Check & Monitoring Script

set -e

echo "🔍 Reste-Rampe Health Check - $(date)"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counter
HEALTHY=0
ISSUES=0

# ==================== DOCKER CONTAINERS ====================
echo "📦 Docker Container Status:"
echo "--------------------------"

cd /home/newuser/Reste-Rampe

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose not found!${NC}"
    ISSUES=$((ISSUES+1))
else
    echo -e "${GREEN}✅ docker-compose available${NC}"
    HEALTHY=$((HEALTHY+1))
fi

# Get container status
BACKEND_STATUS=$(docker-compose ps reste-rampe-backend --format="{{.State}}" 2>/dev/null || echo "unknown")
FRONTEND_STATUS=$(docker-compose ps reste-rampe-frontend --format="{{.State}}" 2>/dev/null || echo "unknown")
DB_STATUS=$(docker-compose ps reste-rampe-db --format="{{.State}}" 2>/dev/null || echo "unknown")

# Backend
if [[ "$BACKEND_STATUS" == *"Up"* ]]; then
    echo -e "${GREEN}✅ Backend: Running${NC}"
    HEALTHY=$((HEALTHY+1))
else
    echo -e "${RED}❌ Backend: $BACKEND_STATUS${NC}"
    ISSUES=$((ISSUES+1))
fi

# Frontend
if [[ "$FRONTEND_STATUS" == *"Up"* ]]; then
    echo -e "${GREEN}✅ Frontend: Running${NC}"
    HEALTHY=$((HEALTHY+1))
else
    echo -e "${RED}❌ Frontend: $FRONTEND_STATUS${NC}"
    ISSUES=$((ISSUES+1))
fi

# Database
if [[ "$DB_STATUS" == *"Up"* ]]; then
    echo -e "${GREEN}✅ Database: Running${NC}"
    HEALTHY=$((HEALTHY+1))
else
    echo -e "${RED}❌ Database: $DB_STATUS${NC}"
    ISSUES=$((ISSUES+1))
fi

echo ""

# ==================== API HEALTH ====================
echo "🔗 API Health Check:"
echo "-------------------"

API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health)

if [ "$API_RESPONSE" == "200" ]; then
    echo -e "${GREEN}✅ API responding (HTTP $API_RESPONSE)${NC}"
    HEALTHY=$((HEALTHY+1))
else
    echo -e "${RED}❌ API not responding (HTTP $API_RESPONSE)${NC}"
    ISSUES=$((ISSUES+1))
fi

echo ""

# ==================== DATABASE HEALTH ====================
echo "🗄️  Database Health Check:"
echo "------------------------"

DB_CHECK=$(docker-compose exec -T db pg_isready -U reste 2>/dev/null || echo "failed")

if [[ "$DB_CHECK" == *"accepting"* ]]; then
    echo -e "${GREEN}✅ Database accepting connections${NC}"
    HEALTHY=$((HEALTHY+1))
else
    echo -e "${RED}❌ Database connection problem${NC}"
    ISSUES=$((ISSUES+1))
fi

# Count users
USER_COUNT=$(docker-compose exec -T db psql -U reste -d reste-rampe-db -t -c "SELECT COUNT(*) FROM users;" 2>/dev/null || echo "unknown")
echo "   Users in database: $USER_COUNT"

echo ""

# ==================== DISK SPACE ====================
echo "💾 Disk Space:"
echo "--------------"

DISK_USAGE=$(df -h /home | tail -1 | awk '{print $5}')
DISK_AVAILABLE=$(df -h /home | tail -1 | awk '{print $4}')

echo "   Used: $DISK_USAGE"
echo "   Available: $DISK_AVAILABLE"

if [[ "${DISK_USAGE%\%}" -gt 80 ]]; then
    echo -e "${YELLOW}⚠️  Disk usage above 80%!${NC}"
    ISSUES=$((ISSUES+1))
else
    echo -e "${GREEN}✅ Disk usage OK${NC}"
    HEALTHY=$((HEALTHY+1))
fi

echo ""

# ==================== DOCKER RESOURCE USAGE ====================
echo "📈 Resource Usage:"
echo "-----------------"

echo "Backend:"
docker stats --no-stream reste-rampe-backend 2>/dev/null | tail -1 | awk '{printf "  CPU: %s | Memory: %s\n", $3, $4}' || echo "  (unable to retrieve)"

echo "Frontend:"
docker stats --no-stream reste-rampe-frontend 2>/dev/null | tail -1 | awk '{printf "  CPU: %s | Memory: %s\n", $3, $4}' || echo "  (unable to retrieve)"

echo "Database:"
docker stats --no-stream reste-rampe-db 2>/dev/null | tail -1 | awk '{printf "  CPU: %s | Memory: %s\n", $3, $4}' || echo "  (unable to retrieve)"

echo ""

# ==================== LOG ERRORS ====================
echo "📋 Recent Errors in Logs:"
echo "------------------------"

BACKEND_ERRORS=$(docker-compose logs backend 2>/dev/null | grep -i "error" | tail -3 || echo "No errors found")
if [ ! -z "$BACKEND_ERRORS" ] && [ "$BACKEND_ERRORS" != "No errors found" ]; then
    echo -e "${YELLOW}⚠️  Backend errors:${NC}"
    echo "$BACKEND_ERRORS"
    ISSUES=$((ISSUES+1))
else
    echo -e "${GREEN}✅ No backend errors${NC}"
    HEALTHY=$((HEALTHY+1))
fi

echo ""

# ==================== SUMMARY ====================
echo "=================================="
echo "📊 Health Check Summary:"
echo "-----------------------"
echo -e "Healthy: ${GREEN}$HEALTHY${NC}"
echo -e "Issues:  ${RED}$ISSUES${NC}"

if [ $ISSUES -eq 0 ]; then
    echo -e "\n${GREEN}✅ Everything looks good!${NC}"
    exit 0
else
    echo -e "\n${RED}⚠️  There are $ISSUES issue(s) to address${NC}"
    exit 1
fi
