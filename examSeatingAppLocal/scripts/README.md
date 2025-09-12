# Build Scripts

## Create Deployment Package

### Windows
```bash
build.bat
```

### Linux
```bash
./build.sh
```

This will create a zip file with timestamp that contains everything needed for deployment.

## What it creates:
- Builds the Vue.js UI
- Copies all API files
- Creates setup scripts for Windows and Linux
- Packages everything into a zip file

## Server Requirements:

### Minimum Installation Required:
- **Python 3.8+** (with pip)
- **Network access** (for downloading Python packages)

### Windows Server:
```bash
# Download and install Python from python.org
# Make sure to check "Add Python to PATH" during installation
python --version  # Should show Python 3.8+
```

### Linux Server:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# CentOS/RHEL
sudo yum install python3 python3-pip

# Verify installation
python3 --version  # Should show Python 3.8+
```

### Network Ports:
- **Port 8000**: API Server
- **Port 3001**: UI Server
- Make sure these ports are open in firewall

## Usage:
1. **Build**: Run the build script on your development machine
2. **Transfer**: Copy the generated zip file to your server
3. **Deploy**: Unzip and run the setup script on the server
4. **Access**: Open http://server-ip:3001 in browser

## Validate Server is Running:

### Check if Services are Running:

**Windows:**
```bash
# Check if processes are running
tasklist | findstr python

# Check specific ports
netstat -an | findstr :8000
netstat -an | findstr :3001

# Check Task Scheduler
schtasks /query /tn "ExamSeatingApp"
```

**Linux:**
```bash
# Check systemd services
sudo systemctl status exam-seating-api
sudo systemctl status exam-seating-ui

# Check if ports are listening
sudo netstat -tlnp | grep :8000
sudo netstat -tlnp | grep :3001

# Or using ss command
ss -tlnp | grep :8000
ss -tlnp | grep :3001
```

### Test API and UI:

**From Server:**
```bash
# Test API
curl http://localhost:8000
curl http://localhost:8000/health

# Test UI (should return HTML)
curl http://localhost:3001
```

**From Network:**
```bash
# Replace YOUR_SERVER_IP with actual server IP
curl http://YOUR_SERVER_IP:8000
curl http://YOUR_SERVER_IP:3001
```

**Browser Test:**
- API: `http://YOUR_SERVER_IP:8000` (should show JSON message)
- UI: `http://YOUR_SERVER_IP:3001` (should show login page)

### Troubleshooting:

**If services not running:**
- **Windows**: Run `start_all.bat` manually
- **Linux**: `sudo systemctl start exam-seating-api exam-seating-ui`

**Check logs:**
- **Linux**: `sudo journalctl -u exam-seating-api -f`

**Firewall issues:**
- **Windows**: Check Windows Defender Firewall
- **Linux**: `sudo ufw allow 8000` and `sudo ufw allow 3001`