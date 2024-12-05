#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: file_utils.py
# Project: SSH-Sentinel
# File Created: Wednesday, 4th December 2024 1:44:53 am
# Author: Daniel Rodríguez Cabrera (daniel8rc@gmail.com)
# Version: 1.0.0
# -----
# Last Modified: Thursday, 5th December 2024 2:07:51 pm
# Modified By: Daniel Rodríguez Cabrera
# -----
# Copyright (c) 2024 - 2025 daniel8rc@gmail.com copying, distribution or modification not authorised in writing is prohibited.
###

def validate_file_path(file_path):
    import os
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
