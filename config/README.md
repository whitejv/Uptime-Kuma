# Monitor Configuration

This directory contains the YAML configuration file for Uptime Kuma monitors.

## devices.yaml

This file defines all devices and ports to monitor on your network. Each monitor entry can have:

- `name`: Display name for the monitor
- `ip`: IP address to monitor
- `type`: Monitor type (`ping` or `port`)
- `ports`: List of ports to monitor (required if type is `port`)
- `location`: Physical location (optional)
- `manufacturer`: Device manufacturer (optional)
- `mac`: MAC address (optional)
- `notes`: Additional notes (optional)

## Editing the Configuration

To add or modify monitors, edit `devices.yaml`:

```yaml
monitors:
  - name: "Device Name"
    ip: "192.168.1.100"
    type: "port"
    ports: [22, 80, 443]
    notes: "Description"
```

Then run the `add_monitors.py` script to apply changes.

