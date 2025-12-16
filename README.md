# Uptime Kuma Installation Guide (Docker Compose on Raspberry Pi)

This README provides step-by-step instructions for installing and running Uptime Kuma using Docker Compose on a Raspberry Pi (or any Linux system). This method is lightweight, easy to update, and perfect for monitoring your smart home devices via ping and TCP ports.

## Prerequisites

- A Raspberry Pi running Raspberry Pi OS (64-bit recommended).
- Basic terminal access.

## Step 1: Install Docker (if not already installed)

```bash
sudo apt update && sudo apt upgrade -y

# Install Docker using the official convenience script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your current user to the docker group (log out and back in, or reboot afterward)
sudo usermod -aG docker $USER
```

## Step 2: Set Up Uptime Kuma with Docker Compose

```bash
# Create a directory for Uptime Kuma
mkdir ~/uptime-kuma && cd ~/uptime-kuma

# Create the docker-compose.yml file
nano docker-compose.yml
```

Paste the following content into `docker-compose.yml`:

```yaml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:latest
    container_name: uptime-kuma
    volumes:
      - uptime-kuma-data:/app/data
    ports:
      - 3001:3001
    restart: unless-stopped

volumes:
  uptime-kuma-data:
```

**Note**: The `version` field is no longer required in modern Docker Compose and has been omitted.

Save and exit (Ctrl+O → Enter → Ctrl+X in nano).

## Step 3: Start Uptime Kuma

```bash
docker compose up -d
```

Uptime Kuma will now run in the background and auto-start on boot/reboot.

## Access the Dashboard

Open a web browser on any device on your network and go to:

```
http://<your-rpi-ip>:3001
```

(e.g., `http://192.168.1.250:3001`)

On first access, create your admin username and password.

## Example Screenshots

Here are some visuals of what you'll see:

- [uptimekuma.org](https://uptimekuma.org)
- [uptimekuma.org](https://uptimekuma.org)
- [betterstack.com](https://betterstack.com)
- [linuxiac.com](https://linuxiac.com)
- [flywp.com](https://flywp.com)

## Adding Monitors

- **Ping monitors**: For basic device reachability (ICMP).
- **Port monitors**: For TCP services (e.g., SSH on port 22, web interfaces on 80).

Click **Add New Monitor** and select the type.

## Bulk Import Monitors (Automated Setup)

Instead of manually adding monitors one by one, you can use the included Python script to bulk import all your devices from a YAML configuration file.

### Step 1: Install Python Dependencies

```bash
# Install required Python packages
pip3 install -r requirements.txt
```

### Step 2: Configure Your Devices

Edit `config/devices.yaml` to match your network setup. The file already includes a template based on your network devices. Each monitor entry supports:

- `name`: Display name for the monitor
- `ip`: IP address to monitor
- `type`: Monitor type (`ping` or `port`)
- `ports`: List of ports to monitor (required if type is `port`)
- `location`, `manufacturer`, `mac`, `notes`: Optional metadata

Example:
```yaml
monitors:
  - name: "RPI5 Prod Server"
    ip: "192.168.1.250"
    type: "port"
    ports: [21, 22, 1883, 3000, 8086, 5900]
    notes: "Water Monitor - Primary"
```

### Step 3: Run the Import Script

```bash
python3 add_monitors.py
```

The script will:
1. Prompt for your Uptime Kuma URL (defaults to `http://192.168.1.250:3001`)
2. Ask for your username and password
3. Read `config/devices.yaml`
4. Create all monitors automatically (ping monitors for devices without ports, port monitors for each specified port)

**Note**: The script will create separate monitors for each port. For example, if a device has ports `[22, 80, 443]`, it will create 3 separate port monitors.

## Updating Uptime Kuma

To get the latest version:

```bash
cd ~/uptime-kuma
docker compose pull
docker compose up -d
```

This pulls the new image and restarts the container with zero downtime.

## Stopping or Removing

- **Stop**: `docker compose down`
- **Remove data (caution!)**: `docker volume rm uptime-kuma-data`

---

Enjoy your self-hosted monitoring dashboard! If you need help adding your specific devices/ports, let me know.
