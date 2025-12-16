#!/usr/bin/env python3
"""
Uptime Kuma Monitor Configuration Script
Reads devices.yaml and creates monitors in Uptime Kuma via API
"""

import yaml
import sys
import getpass
from pathlib import Path

try:
    from uptime_kuma_api import UptimeKumaApi, MonitorType
except ImportError:
    print("Error: uptime-kuma-api package not installed.")
    print("Install it with: pip install uptime-kuma-api")
    sys.exit(1)


def load_config(config_path):
    """Load the YAML configuration file"""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)


def create_monitors(api, config, base_url):
    """Create monitors in Uptime Kuma based on configuration"""
    created = 0
    skipped = 0
    errors = 0
    
    print(f"\nConnecting to Uptime Kuma at {base_url}...")
    
    try:
        # Get username and password
        username = input("Enter Uptime Kuma username: ").strip()
        password = getpass.getpass("Enter Uptime Kuma password: ")
        
        # Login to Uptime Kuma
        api.login(username, password)
        print("✓ Successfully logged in\n")
        
    except Exception as e:
        print(f"Error logging in: {e}")
        sys.exit(1)
    
    # Process each monitor configuration
    for monitor_config in config.get('monitors', []):
        name = monitor_config.get('name')
        ip = monitor_config.get('ip')
        monitor_type = monitor_config.get('type', 'ping').lower()
        ports = monitor_config.get('ports', [])
        notes = monitor_config.get('notes', '')
        
        if not name or not ip:
            print(f"⚠ Skipping monitor with missing name or IP: {monitor_config}")
            skipped += 1
            continue
        
        try:
            if monitor_type == 'ping':
                # Create ping monitor
                monitor_name = f"{name} (Ping)"
                api.add_monitor(
                    type=MonitorType.PING,
                    name=monitor_name,
                    hostname=ip,
                    description=notes
                )
                print(f"✓ Created ping monitor: {monitor_name} ({ip})")
                created += 1
                
            elif monitor_type == 'port':
                if not ports:
                    # If no ports specified, create a ping monitor instead
                    monitor_name = f"{name} (Ping)"
                    api.add_monitor(
                        type=MonitorType.PING,
                        name=monitor_name,
                        hostname=ip,
                        description=notes
                    )
                    print(f"✓ Created ping monitor (no ports specified): {monitor_name} ({ip})")
                    created += 1
                else:
                    # Create a port monitor for each port
                    for port in ports:
                        monitor_name = f"{name} - Port {port}"
                        api.add_monitor(
                            type=MonitorType.PORT,
                            name=monitor_name,
                            hostname=ip,
                            port=port,
                            description=f"{notes} - Port {port}"
                        )
                        print(f"✓ Created port monitor: {monitor_name} ({ip}:{port})")
                        created += 1
            else:
                print(f"⚠ Unknown monitor type '{monitor_type}' for {name}, skipping")
                skipped += 1
                
        except Exception as e:
            print(f"✗ Error creating monitor for {name}: {e}")
            errors += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Created: {created}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors:  {errors}")
    print(f"{'='*60}\n")
    
    # Disconnect
    api.disconnect()
    print("Disconnected from Uptime Kuma")


def main():
    """Main function"""
    # Determine config file path
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config' / 'devices.yaml'
    
    # Get Uptime Kuma URL
    print("Uptime Kuma Monitor Configuration Script")
    print("=" * 60)
    default_url = "http://192.168.1.250:3001"
    base_url = input(f"Enter Uptime Kuma URL [{default_url}]: ").strip()
    if not base_url:
        base_url = default_url
    
    # Load configuration
    print(f"\nLoading configuration from {config_path}...")
    config = load_config(config_path)
    monitor_count = len(config.get('monitors', []))
    print(f"✓ Found {monitor_count} monitor configurations\n")
    
    # Initialize API
    api = UptimeKumaApi(base_url)
    
    # Create monitors
    create_monitors(api, config, base_url)


if __name__ == '__main__':
    main()

