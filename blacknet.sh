#!/usr/bin/env bash

# Colors for output
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

echo -e "${RED}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}║${NC} ${CYAN}      BlackNet Recon - Auto-Installer & Launcher         ${NC} ${RED}║${NC}"
echo -e "${RED}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# 1. Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python3 is not installed. Please install python3 to continue.${NC}"
    exit 1
fi

# 2. Check for pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo -e "${YELLOW}[!] pip is not installed. Attempting to install pip...${NC}"
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y python3-pip python3-venv
    elif command -v pacman &> /dev/null; then
        sudo pacman -Sy --noconfirm python-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-pip
    else
        echo -e "${RED}[!] Could not automatically install pip. Please install python3-pip manually.${NC}"
        exit 1
    fi
fi

# 3. Ensure python3-venv is installed (specifically for Debian/Ubuntu/Parrot OS)
if command -v apt-get &> /dev/null; then
    if ! dpkg -s python3-venv &> /dev/null; then
        echo -e "${YELLOW}[*] Installing python3-venv for environment isolation...${NC}"
        sudo apt-get install -y python3-venv
    fi
fi

# 4. Set up Virtual Environment to bypass "externally-managed-environment" errors
VENV_DIR=".blacknet_venv"
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${CYAN}[*] Creating Python Virtual Environment to prevent package conflicts...${NC}"
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo -e "${RED}[!] Failed to create virtual environment. Ensure 'python3-venv' is installed.${NC}"
        exit 1
    fi
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# 5. Install the required Python dependencies
echo -e "${CYAN}[*] Checking/Installing dependencies inside virtual environment...${NC}"
pip install --upgrade pip --quiet
pip install rich --quiet

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[+] Dependencies installed successfully!${NC}"
else
    echo -e "${RED}[!] Failed to install dependencies. Check your internet connection.${NC}"
    deactivate
    exit 1
fi

# 6. Verify recon.py exists
SCRIPT_NAME="recon.py"
if [ ! -f "$SCRIPT_NAME" ]; then
    echo -e "${RED}[!] Error: $SCRIPT_NAME not found in the current directory.${NC}"
    echo -e "${YELLOW}[*] Please make sure blacknet.sh and recon.py are in the same folder.${NC}"
    deactivate
    exit 1
fi

# Make the python script executable
chmod +x "$SCRIPT_NAME"

# 7. Launch the tool
echo -e "${GREEN}[+] Launching BlackNet Recon...${NC}"
sleep 1

# If the script is run with sudo, pass sudo down to python so tools like bettercap/nmap work correctly
if [ "$EUID" -eq 0 ]; then
    python3 "$SCRIPT_NAME"
else
    echo -e "${YELLOW}[!] Warning: You are not running as root. Some network scans (like nmap SYN) may require sudo privileges.${NC}"
    python3 "$SCRIPT_NAME"
fi

# Deactivate venv upon exit
deactivate