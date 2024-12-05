#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: log_service.py
# Project: SSH-Sentinel
# File Created: Wednesday, 4th December 2024 1:44:13 am
# Author: Daniel Rodríguez Cabrera (daniel8rc@gmail.com)
# Version: 1.0.0
# -----
# Last Modified: Thursday, 5th December 2024 2:07:51 pm
# Modified By: Daniel Rodríguez Cabrera
# -----
# Copyright (c) 2024 - 2025 daniel8rc@gmail.com copying, distribution or modification not authorised in writing is prohibited.
###
import os
import threading
import json
import time
import urwid
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from services.journal_service import JournalService
from services.service_status import ServiceStatus
import curses
class LogService:
    def __init__(self, log_path):
        self.log_path = log_path
        self.stop_log_display = False
        self.log_lines = []
        self.filtered_lines = []

    def view_logs(self):
        self.stop_log_display = False
        filter_text = ""

        log_handler = LogUpdateHandler(self)
        observer = Observer()
        observer.schedule(log_handler, path=os.path.dirname(self.log_path), recursive=False)
        observer.start()

        try:
            curses.wrapper(self.curses_log_view, filter_text, observer)
        except KeyboardInterrupt:
            self.stop_log_display = True
            observer.stop()
            observer.join()

    def curses_log_view(self, stdscr, filter_text, observer):
        curses.curs_set(0)
        stdscr.clear()

        def refresh_logs():
            max_y, max_x = stdscr.getmaxyx()
            log_window_height = max_y - 3

            stdscr.clear()
            for idx, line in enumerate(self.filtered_lines[-log_window_height:]):
                if idx < log_window_height:
                    stdscr.addstr(idx, 0, line[:max_x - 1])

            stdscr.addstr(log_window_height, 0, f"Filter: {filter_text}")
            stdscr.addstr(log_window_height + 1, 0, "Press ESC to exit, BACKSPACE to delete, ENTER to clear filter")
            stdscr.refresh()

        while not self.stop_log_display:
            refresh_logs()
            stdscr.timeout(1000)  # Wait for 1 second or a key press
            key = stdscr.getch()

            if key == 27:  # ESC key
                self.stop_log_display = True
                observer.stop()
                observer.join()
                break
            elif key == curses.KEY_BACKSPACE or key == 127:
                filter_text = filter_text[:-1]
            elif key == 10:  # Enter key
                filter_text = ""
            elif 32 <= key <= 126:
                filter_text += chr(key)

            # Update filtered lines based on the current filter_text
            self.filtered_lines = [line for line in self.log_lines if filter_text.lower() in line.lower()]

    def update_logs(self, new_line):
        if not self.stop_log_display:
            self.log_lines.append(new_line)
            # Only update filtered lines if the new line matches the current filter
            if not self.filtered_lines or self.filtered_lines and new_line.lower().find(self.filtered_lines[0].lower()) != -1:
                self.filtered_lines.append(new_line)

class LogUpdateHandler(FileSystemEventHandler):
    def __init__(self, log_service):
        self.log_service = log_service

    def on_modified(self, event):
        if event.src_path == self.log_service.log_path:
            with open(self.log_service.log_path, 'r') as log_file:
                lines = log_file.readlines()
                new_lines = lines[len(self.log_service.log_lines):]
                for line in new_lines:
                    self.log_service.update_logs(line.strip())