# mpeg-streamer

## Setting Up `mpeg-streamer.service` on Linux

This guide covers setting up a `systemd` service to automatically start an MPEG streamer on Linux reboot.

### Step 1: Create the `mpeg-streamer.service` File

1. Open a terminal.
2. Create a new service file for the MPEG streamer:
```bash
sudo nano /etc/systemd/system/mpeg-streamer.service
```
3. Add the following content to the file, replacing placeholders as needed:
```ini
[Unit]
Description=MPEG Streamer
After=network.target

[Service]
User=arrow
WorkingDirectory=/home/arrow/mpeg-streamer
ExecStart=python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```
4. Save and close the file by pressing CTRL + X, then Y, and Enter.

### Reload systemd and Enable the Service

1. Reload the `systemd` configuration to apply the new service:
```bash
sudo systemctl daemon-reload
```
2. Enable the `mpeg-streamer` service to start on boot:
```bash
sudo systemctl enable mpeg-streamer
```
3. Start the mpeg-streamer service immediately (optional):
```bash
sudo systemctl start mpeg-streamer
```
4. Check the status to ensure it’s running:
```bash
sudo systemctl status mpeg-streamer

```