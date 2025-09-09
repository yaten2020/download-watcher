# Download Watcher (macOS)

A simple Python + `launchd` setup to automatically move certain files from the `~/Downloads` folder to a designated location.

## Features
- Watches your Downloads folder every minute
- Moves files matching:
  - `mindmap*.json`
  - `*.mmp`
- Skips files still being downloaded
- Logs activity to `~/Library/Logs/download_watcher.log`

## Setup / Install / Uninstall

1. Clone this repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/download-watcher.git
   cd download-watcher
   mkdir -p ~/Scripts
   cp download_watcher.py ~/Scripts/
   chmod +x ~/Scripts/download_watcher.py
   ```

2. Modify the files to make them compatible with your Mac:
   - **com.user.download-watcher.plist**
     - Replace `"ykumar"` (my username) with your username
     - Modify your Python path (`which python3`) with your own, e.g.  
       `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3`
     - This is set to launch every **60 seconds** (line 15) — adjust as needed
   - **download_watcher.py**
     - Add more file extensions and their destination folders in the Python dictionary called `RULES` (around line 11)

3. Copy the Python script to `~/Scripts`:
   ```bash
   mkdir -p ~/Scripts
   cp download_watcher.py ~/Scripts/
   chmod +x ~/Scripts/download_watcher.py
   ```

4. Copy the LaunchAgent to `~/Library/LaunchAgents`:
   ```bash
   cp com.user.download-watcher.plist ~/Library/LaunchAgents/
   ```

5. Load the agent:
   ```bash
   launchctl load -w ~/Library/LaunchAgents/com.user.download-watcher.plist
   ```

6. Check logs here:
   ```bash
   tail -f ~/Library/Logs/download_watcher.log
   ```

7. To stop it and/or uninstall:
   ```bash
   launchctl unload -w ~/Library/LaunchAgents/com.user.download-watcher.plist
   rm ~/Library/LaunchAgents/com.user.download-watcher.plist
   rm ~/Scripts/download_watcher.py
   ```
