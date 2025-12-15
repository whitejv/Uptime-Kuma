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
version: '3.8'

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
