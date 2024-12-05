#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: service_status.py
# Project: SSH-Sentinel
# File Created: Wednesday, 4th December 2024 1:39:23 am
# Author: Daniel Rodríguez Cabrera (daniel8rc@gmail.com)
# Version: 1.0.0
# -----
# Last Modified: Thursday, 5th December 2024 2:07:51 pm
# Modified By: Daniel Rodríguez Cabrera
# -----
# Copyright (c) 2024 - 2025 daniel8rc@gmail.com copying, distribution or modification not authorised in writing is prohibited.
###

import subprocess

class ServiceStatus:
    def __init__(self, service_name):
        self.service_name = service_name

    def check_status(self):
        try:
            result = subprocess.run(
                ["systemctl", "is-active", self.service_name],
                capture_output=True,
                text=True
            )
            is_active = result.stdout.strip() == "active"
            uptime = self.get_uptime() if is_active else "N/A"
            return is_active, uptime
        except Exception as e:
            return False, "Error: " + str(e)

    def get_uptime(self):
        try:
            result = subprocess.run(
                ["systemctl", "show", self.service_name, "--property=ActiveEnterTimestamp"],
                capture_output=True,
                text=True
            )
            timestamp = result.stdout.strip().split("=")[-1]
            return timestamp or "N/A"
        except Exception:
            return "Unknown"

    def start_service(self):
        try:
            subprocess.run(["systemctl", "start", self.service_name], check=True)
            print(f"Service {self.service_name} started successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to start service {self.service_name}: {e}")

    def stop_service(self):
        try:
            subprocess.run(["systemctl", "stop", self.service_name], check=True)
            print(f"Service {self.service_name} stopped successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to stop service {self.service_name}: {e}")

    def restart_service(self):
        try:
            subprocess.run(["systemctl", "restart", self.service_name], check=True)
            print(f"Service {self.service_name} restarted successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to restart service {self.service_name}: {e}")

    
    def get_service_start_time(self):
        try:
            result = subprocess.run(
                ["systemctl", "show", self.service_name, "--property=ExecMainStartTimestamp"],
                capture_output=True,
                text=True
            )
            timestamp = result.stdout.strip().split("=")[-1]
            return timestamp or "N/A"
        except Exception:
            return "Unknown"

