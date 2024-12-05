#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: journal_viewer.py
# Project: SSH-Sentinel
# File Created: Thursday, 5th December 2024 1:42:46 pm
# Author: Daniel Rodríguez Cabrera (daniel8rc@gmail.com)
# Version: 1.0.0
# -----
# Last Modified: Thursday, 5th December 2024 2:07:51 pm
# Modified By: Daniel Rodríguez Cabrera
# -----
# Copyright (c) 2024 - 2025 daniel8rc@gmail.com copying, distribution or modification not authorised in writing is prohibited.
###
import threading
import time
import customtkinter as ctk
from screens.base_screen import BaseScreen
from loguru import logger


class JournalViewer(BaseScreen):
    """
    Pantalla para mostrar los logs de journalctl de un servicio.
    """

    def __init__(self, root, service, ssh_manager, on_back):
        super().__init__(root)
        self.service = service
        self.ssh_manager = ssh_manager
        self.on_back = on_back

        self.setup_ui()
        threading.Thread(target=self.fetch_journalctl, daemon=True).start()

    def setup_ui(self):
        """
        Configura los elementos de la interfaz de usuario.
        """
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            self.frame,
            text=f"Journalctl de {self.service['name']}",
            font=("Helvetica", 18, "bold"),
        )
        title.pack(pady=10)

        self.journal_text = ctk.CTkTextbox(self.frame, width=800, height=800)
        self.journal_text.pack(fill="both", expand=True)

        back_btn = ctk.CTkButton(
            self.frame,
            text="Volver",
            command=self.on_back,
            font=("Helvetica", 14),
        )
        back_btn.pack(pady=20)

    def fetch_journalctl(self):
        """
        Obtiene los logs de journalctl del servidor.
        """
        try:
            command = f"journalctl -fu {self.service['name']}"
            stdin, stdout, stderr = self.ssh_manager.execute_command(command)
            while True:
                line = stdout.readline()
                if line:
                    self.journal_text.insert("end", line)
                    self.journal_text.see("end")
                else:
                    time.sleep(0.1)
        except Exception as e:
            logger.error(f"No se pudieron obtener los logs de journalctl: {e}")
