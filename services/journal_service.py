#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: journal_service.py
# Project: SSH-Sentinel
# File Created: Wednesday, 4th December 2024 1:44:28 am
# Author: Daniel Rodríguez Cabrera (daniel8rc@gmail.com)
# Version: 1.0.0
# -----
# Last Modified: Thursday, 5th December 2024 2:07:51 pm
# Modified By: Daniel Rodríguez Cabrera
# -----
# Copyright (c) 2024 - 2025 daniel8rc@gmail.com copying, distribution or modification not authorised in writing is prohibited.
###

import subprocess

class JournalService:
    def __init__(self, service_name):
        self.service_name = service_name

    def display_journal_logs(self):
        command = ["journalctl", "-f", "-u", self.service_name]
        try:
            subprocess.run(command)
        except KeyboardInterrupt:
            print("\nExiting journalctl viewer.")
