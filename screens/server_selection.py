#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: server_selection.py
# Project: SSH-Sentinel
# File Created: Thursday, 5th December 2024 1:42:08 pm
# Author: Daniel Rodríguez Cabrera (daniel8rc@gmail.com)
# Version: 1.0.0
# -----
# Last Modified: Thursday, 5th December 2024 2:07:51 pm
# Modified By: Daniel Rodríguez Cabrera
# -----
# Copyright (c) 2024 - 2025 daniel8rc@gmail.com copying, distribution or modification not authorised in writing is prohibited.
###
import customtkinter as ctk
from screens.base_screen import BaseScreen
from loguru import logger


class ServerSelectionScreen(BaseScreen):
    """
    Pantalla para seleccionar un servidor al cual conectar.
    """

    def __init__(self, root, servers, on_server_selected):
        super().__init__(root)
        self.servers = servers
        self.on_server_selected = on_server_selected
        self.setup_ui()

    def setup_ui(self):
        """
        Configura los elementos de la interfaz de usuario.
        """
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            self.frame,
            text="Seleccione un servidor para conectar:",
            font=("Helvetica", 18, "bold"),
        )
        title.pack(pady=20)

        for server in self.servers:
            btn = ctk.CTkButton(
                self.frame,
                text=server["name"],
                command=lambda s=server: self.on_server_selected(s),
                font=("Helvetica", 14),
            )
            btn.pack(pady=10, padx=20, fill="x")
