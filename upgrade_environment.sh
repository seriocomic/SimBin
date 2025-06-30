#!/bin/bash
set -e

echo "🚀 Upgrading Simbin to latest stable versions..."
echo "================================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Setting Python 3.13.4 for this project${NC}"
pyenv local 3.13.4

echo -e "${YELLOW}Step 2: Backing up current virtual environment${NC}"
if [ -d ".venv" ]; then
    mv .venv .venv.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backed up existing .venv"
fi

echo -e "${YELLOW}Step 3: Creating new virtual environment with Python 3.13.4${NC}"
python -m venv .venv

echo -e "${YELLOW}Step 4: Activating virtual environment${NC}"
source .venv/bin/activate

echo -e "${YELLOW}Step 5: Upgrading pip to latest version${NC}"
pip install --upgrade pip

echo -e "${YELLOW}Step 6: Installing updated requirements${NC}"
pip install -r requirements.txt

echo -e "${YELLOW}Step 7: Running Django system checks${NC}"
python manage.py check

echo -e "${YELLOW}Step 8: Collecting static files${NC}"
python manage.py collectstatic --noinput

echo -e "${GREEN}✅ Upgrade complete!${NC}"
echo ""
echo -e "${GREEN}Your environment is now running:${NC}"
echo "Python: $(python --version)"
echo "Django: $(python -c 'import django; print(django.get_version())')"
echo ""
echo -e "${GREEN}To activate the environment in the future, run:${NC}"
echo "source .venv/bin/activate"
echo ""
echo -e "${GREEN}To test the application locally:${NC}"
echo "python manage.py runserver"
