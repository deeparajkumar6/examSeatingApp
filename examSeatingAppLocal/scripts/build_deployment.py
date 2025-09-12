#!/usr/bin/env python3
"""
Build script to create deployment package for Exam Seating App
Creates a zip file with all necessary files for deployment
"""

import os
import shutil
import subprocess
import zipfile
from datetime import datetime

def run_command(command, cwd=None):
    """Run shell command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command {command}: {e}")
        return False

def create_deployment_package():
    """Create deployment package"""
    print("Building Exam Seating App Deployment Package...")
    
    # Get current directory (we're in scripts folder, so go up one level)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    ui_dir = os.path.join(base_dir, "UI")
    api_dir = os.path.join(base_dir, "fastapi_app")
    
    # Create deployment directory
    deploy_dir = os.path.join(base_dir, "deployment")
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    print("Building UI...")
    # Build UI
    if not run_command("npm run build", cwd=ui_dir):
        print("Failed to build UI")
        return False
    
    print("Copying files...")
    
    # Copy API files
    api_dest = os.path.join(deploy_dir, "api")
    shutil.copytree(api_dir, api_dest, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    
    # Copy built UI files
    ui_build_src = os.path.join(ui_dir, "dist")
    ui_dest = os.path.join(deploy_dir, "ui")
    if os.path.exists(ui_build_src):
        shutil.copytree(ui_build_src, ui_dest)
    else:
        print("UI build files not found")
        return False
    
    # Create scripts directory
    scripts_dir = os.path.join(deploy_dir, "scripts")
    os.makedirs(scripts_dir)
    
    # Create config directory
    config_dir = os.path.join(deploy_dir, "config")
    os.makedirs(config_dir)
    
    print("Creating deployment scripts...")
    create_deployment_scripts(deploy_dir)
    
    print("Creating zip package...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"exam_seating_app_deployment_{timestamp}.zip"
    zip_path = os.path.join(script_dir, zip_name)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, deploy_dir)
                zipf.write(file_path, arc_name)
    
    # Cleanup deployment directory
    shutil.rmtree(deploy_dir)
    
    print(f"Deployment package created: {zip_name}")
    print(f"Location: {zip_path}")
    print("\nDeployment Instructions:")
    print("1. Copy the zip file to your server")
    print("2. Unzip the file")
    print("3. Run setup script:")
    print("   Windows: setup_windows.bat")
    print("   Linux: sudo ./setup_linux.sh")
    
    return True

def create_deployment_scripts(deploy_dir):
    """Create all deployment scripts"""
    scripts_dir = os.path.join(deploy_dir, "scripts")
    config_dir = os.path.join(deploy_dir, "config")
    
    # API startup script
    create_api_startup_script(deploy_dir)
    
    # UI server script
    create_ui_server_script(deploy_dir)
    
    # Windows setup script
    create_windows_setup_script(scripts_dir)
    
    # Linux setup script
    create_linux_setup_script(scripts_dir)
    
    # Windows start script
    create_windows_start_script(scripts_dir)
    
    # Linux start script
    create_linux_start_script(scripts_dir)
    
    # Configuration file
    create_config_file(config_dir)
    
    # README
    create_readme(deploy_dir)

def create_api_startup_script(deploy_dir):
    """Create API startup script"""
    script_content = '''#!/usr/bin/env python3
"""
Exam Seating App API Server
"""
import os
import sys
import uvicorn
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def main():
    """Start the API server"""
    print("🚀 Starting Exam Seating App API Server...")
    print("📍 API will be available at: http://localhost:8000")
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\\n🛑 API Server stopped")
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    with open(os.path.join(deploy_dir, "api", "start_server.py"), "w", encoding="utf-8") as f:
        f.write(script_content)

def create_ui_server_script(deploy_dir):
    """Create UI server script"""
    script_content = '''#!/usr/bin/env python3
"""
Exam Seating App UI Server
"""
import os
import sys
import http.server
import socketserver
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for SPA routing"""
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def do_GET(self):
        # Handle SPA routing - serve index.html for non-file requests
        if not os.path.exists(self.translate_path(self.path)) and not self.path.startswith('/assets'):
            self.path = '/index.html'
        return super().do_GET()

def main():
    """Start the UI server"""
    ui_dir = Path(__file__).parent
    os.chdir(ui_dir)
    
    PORT = 3001
    
    print("🚀 Starting Exam Seating App UI Server...")
    print(f"📍 UI will be available at: http://localhost:{PORT}")
    print("🌐 Access from network: http://YOUR_SERVER_IP:3001")
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), CustomHTTPRequestHandler) as httpd:
            httpd.allow_reuse_address = True
            print(f"✅ UI Server running on port {PORT}")
            print(f"🌐 Network access: http://192.168.1.13:{PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\n🛑 UI Server stopped")
    except Exception as e:
        print(f"❌ Error starting UI server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    with open(os.path.join(deploy_dir, "ui", "start_server.py"), "w", encoding="utf-8") as f:
        f.write(script_content)

def create_windows_setup_script(scripts_dir):
    """Create Windows setup script"""
    script_content = '''@echo off
echo 🚀 Setting up Exam Seating App on Windows...

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set APP_DIR=%SCRIPT_DIR%..

echo 📦 Installing Python dependencies...
cd /d "%APP_DIR%\\api"
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo 🔧 Creating Windows services...

REM Create API service batch file
echo @echo off > "%APP_DIR%\\start_api.bat"
echo REM Kill any process using port 8000 >> "%APP_DIR%\\start_api.bat"
echo powershell -Command "Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue ^^^| ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >> "%APP_DIR%\\start_api.bat"
echo cd /d "%APP_DIR%\\api" >> "%APP_DIR%\\start_api.bat"
echo python start_server.py >> "%APP_DIR%\\start_api.bat"

REM Create UI service batch file
echo @echo off > "%APP_DIR%\\start_ui.bat"
echo REM Kill any process using port 3001 >> "%APP_DIR%\\start_ui.bat"
echo powershell -Command "Get-NetTCPConnection -LocalPort 3001 -ErrorAction SilentlyContinue ^^^| ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >> "%APP_DIR%\\start_ui.bat"
echo cd /d "%APP_DIR%\\ui" >> "%APP_DIR%\\start_ui.bat"
echo python start_server.py >> "%APP_DIR%\\start_ui.bat"
echo cd /d "%APP_DIR%\\ui" >> "%APP_DIR%\\start_ui.bat"
echo python start_server.py >> "%APP_DIR%\\start_ui.bat"

REM Create combined start script
echo @echo off > "%APP_DIR%\\start_all.bat"
echo echo 🚀 Starting Exam Seating App... >> "%APP_DIR%\\start_all.bat"
echo start "API Server" cmd /k "%APP_DIR%\\start_api.bat" >> "%APP_DIR%\\start_all.bat"
echo timeout /t 3 /nobreak ^> nul >> "%APP_DIR%\\start_all.bat"
echo start "UI Server" cmd /k "%APP_DIR%\\start_ui.bat" >> "%APP_DIR%\\start_all.bat"
echo echo ✅ Both servers started! >> "%APP_DIR%\\start_all.bat"
echo echo 📍 API: http://localhost:8000 >> "%APP_DIR%\\start_all.bat"
echo echo 📍 UI: http://localhost:3001 >> "%APP_DIR%\\start_all.bat"

echo 🔧 Configuring Windows Firewall...
netsh advfirewall firewall add rule name="Exam Seating App UI" dir=in action=allow protocol=TCP localport=3001
netsh advfirewall firewall add rule name="Exam Seating App API" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall set rule group="Network Discovery" new enable=Yes

echo 📋 Creating startup tasks...
schtasks /create /tn "ExamSeatingApp-API" /tr "\"%APP_DIR%\\start_api.bat\"" /sc onstart /ru "SYSTEM" /rl HIGHEST /f
schtasks /create /tn "ExamSeatingApp-UI" /tr "\"%APP_DIR%\\start_ui.bat\"" /sc onstart /ru "SYSTEM" /rl HIGHEST /f
if %errorlevel% neq 0 (
    echo ⚠️  Could not create startup tasks. You may need to run as Administrator.
    echo 💡 Manual setup: Add start_api.bat and start_ui.bat to Windows startup folder
)

echo 🚀 Starting services now...
start "API Server" "%APP_DIR%\\start_api.bat"
timeout /t 3 /nobreak > nul
start "UI Server" "%APP_DIR%\\start_ui.bat"

echo.
echo ✅ Setup completed!
echo 🚀 To start manually: run start_all.bat
echo 🔄 Auto-start: Configured to start on system boot
echo 📍 API will be available at: http://YOUR_SERVER_IP:8000
echo 📍 UI will be available at: http://YOUR_SERVER_IP:3001
echo.
pause
'''
    
    with open(os.path.join(scripts_dir, "setup_windows.bat"), "w", encoding="utf-8") as f:
        f.write(script_content)

def create_linux_setup_script(scripts_dir):
    """Create Linux setup script"""
    script_content = '''#!/bin/bash
echo "🚀 Setting up Exam Seating App on Linux..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"

echo "📦 Installing Python dependencies..."
cd "$APP_DIR/api"
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo "🔧 Configuring firewall..."
sudo ufw allow 8000/tcp
sudo ufw allow 3001/tcp

echo "🔧 Creating systemd services..."

# Create API service
sudo tee /etc/systemd/system/exam-seating-api.service > /dev/null <<EOF
[Unit]
Description=Exam Seating App API Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR/api
ExecStart=/usr/bin/python3 $APP_DIR/api/start_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create UI service
sudo tee /etc/systemd/system/exam-seating-ui.service > /dev/null <<EOF
[Unit]
Description=Exam Seating App UI Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR/ui
ExecStart=/usr/bin/python3 $APP_DIR/ui/start_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable services
sudo systemctl daemon-reload
sudo systemctl enable exam-seating-api.service
sudo systemctl enable exam-seating-ui.service

# Start services
sudo systemctl start exam-seating-api.service
sudo systemctl start exam-seating-ui.service

echo ""
echo "✅ Setup completed and services started!"
echo "🚀 Services are now running and will auto-start on boot"
echo "📍 API available at: http://$(hostname -I | awk '{print $1}'):8000"
echo "📍 UI available at: http://$(hostname -I | awk '{print $1}'):3001"
echo ""
echo "🔧 Service management commands:"
echo "  Check status: sudo systemctl status exam-seating-api exam-seating-ui"
echo "  Stop services: sudo systemctl stop exam-seating-api exam-seating-ui"
echo "  Start services: sudo systemctl start exam-seating-api exam-seating-ui"
echo "  View logs: sudo journalctl -u exam-seating-api -f"
'''
    
    with open(os.path.join(scripts_dir, "setup_linux.sh"), "w", encoding="utf-8") as f:
        f.write(script_content)
    
    # Make script executable
    os.chmod(os.path.join(scripts_dir, "setup_linux.sh"), 0o755)

def create_windows_start_script(scripts_dir):
    """Create Windows manual start script"""
    script_content = '''@echo off
echo 🚀 Starting Exam Seating App manually...

set SCRIPT_DIR=%~dp0
set APP_DIR=%SCRIPT_DIR%..

start "API Server" cmd /k "%APP_DIR%\\start_api.bat"
timeout /t 3 /nobreak > nul
start "UI Server" cmd /k "%APP_DIR%\\start_ui.bat"

echo ✅ Both servers started!
echo 📍 API: http://localhost:8000
echo 📍 UI: http://localhost:3001
pause
'''
    
    with open(os.path.join(scripts_dir, "start_manual_windows.bat"), "w", encoding="utf-8") as f:
        f.write(script_content)

def create_linux_start_script(scripts_dir):
    """Create Linux manual start script"""
    script_content = '''#!/bin/bash
echo "🚀 Starting Exam Seating App manually..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"

# Start API server in background
cd "$APP_DIR/api"
python3 start_server.py &
API_PID=$!

# Wait a moment
sleep 3

# Start UI server in background
cd "$APP_DIR/ui"
python3 start_server.py &
UI_PID=$!

echo "✅ Both servers started!"
echo "📍 API: http://$(hostname -I | awk '{print $1}'):8000 (PID: $API_PID)"
echo "📍 UI: http://$(hostname -I | awk '{print $1}'):3001 (PID: $UI_PID)"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for interrupt
trap 'kill $API_PID $UI_PID; exit' INT
wait
'''
    
    with open(os.path.join(scripts_dir, "start_manual_linux.sh"), "w", encoding="utf-8") as f:
        f.write(script_content)
    
    # Make script executable
    os.chmod(os.path.join(scripts_dir, "start_manual_linux.sh"), 0o755)

def create_config_file(config_dir):
    """Create configuration file"""
    config_content = '''{
  "api": {
    "host": "0.0.0.0",
    "port": 8000,
    "log_level": "info"
  },
  "ui": {
    "host": "0.0.0.0", 
    "port": 3001
  },
  "database": {
    "path": "database.db"
  }
}'''
    
    with open(os.path.join(config_dir, "settings.json"), "w", encoding="utf-8") as f:
        f.write(config_content)

def create_readme(deploy_dir):
    """Create README file"""
    readme_content = '''# Exam Seating App Deployment

## Quick Start

### Windows
1. Unzip the deployment package
2. Run `scripts/setup_windows.bat` as Administrator
3. Services will start automatically

### Linux  
1. Unzip the deployment package
2. Run `sudo ./scripts/setup_linux.sh`
3. Services will start automatically

## Access Points
- **API**: http://YOUR_SERVER_IP:8000
- **UI**: http://YOUR_SERVER_IP:3001

## Default Login
- Username: `admin`
- Password: `Admin@123`

## Manual Control

### Windows
- Start: `scripts/start_manual_windows.bat`
- Stop: Close the command windows

### Linux
- Start: `./scripts/start_manual_linux.sh`
- Stop: `sudo systemctl stop exam-seating-api exam-seating-ui`
- Status: `sudo systemctl status exam-seating-api exam-seating-ui`

## Troubleshooting

### Check if services are running
**Windows**: Task Manager → Services → Look for ExamSeatingApp
**Linux**: `sudo systemctl status exam-seating-api exam-seating-ui`

### View logs
**Linux**: `sudo journalctl -u exam-seating-api -f`

### Firewall
Make sure ports 8000 and 3001 are open in your firewall.

### Network Access
Replace `YOUR_SERVER_IP` with your actual server IP address.

## File Structure
```
deployment/
├── api/                 # FastAPI backend
├── ui/                  # Built Vue.js frontend  
├── scripts/             # Setup and start scripts
└── config/              # Configuration files
```
'''
    
    with open(os.path.join(deploy_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

if __name__ == "__main__":
    success = create_deployment_package()
    if not success:
        print("❌ Build failed!")
        exit(1)