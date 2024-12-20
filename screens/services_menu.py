#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: services_menu.py
# Project: SSH-Sentinel
# File Created: Thursday, 5th December 2024 1:42:27 pm
# Author: Daniel Rodríguez Cabrera (daniel8rc@gmail.com)
# Version: 1.0.0
# -----
# Last Modified: Thursday, 19th December 2024 7:16:35 pm
# Modified By: Daniel Rodríguez Cabrera
# -----
# Copyright (c) 2024 - 2025 daniel8rc@gmail.com copying, distribution or modification not authorised in writing is prohibited.
###
import threading
import time
import customtkinter as ctk
from screens.base_screen import BaseScreen
from loguru import logger


class ServicesMenuScreen(BaseScreen):
    """
    Pantalla que muestra la lista de servicios del servidor.
    """

    def __init__(self, root, server, ssh_manager, on_service_selected, on_back):
        super().__init__(root)
        self.server = server
        self.ssh_manager = ssh_manager
        self.on_service_selected = on_service_selected
        self.on_back = on_back

        self.setup_ui()

    def setup_ui(self):
        """
        Configura los elementos de la interfaz de usuario.
        """
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            self.frame,
            text="Seleccione un servicio para administrar:",
            font=("Helvetica", 18, "bold"),
        )
        title.pack(pady=10)

        for service in self.server["services"]:
            service_name = service["name"]
            service_status_label = ctk.CTkLabel(
                self.frame,
                text=f"{service_name}: Comprobando...",
                font=("Helvetica", 14),
                fg_color="red",
            )
            service_status_label.pack(pady=5)
            threading.Thread(
                target=self.update_service_status,
                args=(service, service_status_label),
                daemon=True,
            ).start()

            btn = ctk.CTkButton(
                self.frame,
                text=service_name,
                command=lambda s=service: self.on_service_selected(s),
                font=("Helvetica", 14),
            )
            btn.pack(pady=5, padx=20, fill="x")

        back_btn = ctk.CTkButton(
            self.frame,
            text="Volver",
            command=self.on_back,
            font=("Helvetica", 14),
        )
        back_btn.pack(pady=20)

    def update_service_status(self, service, label):
        """
        Actualiza el estado de un servicio periódicamente.
        """
        while True:
            try:
                stdin, stdout, stderr = self.ssh_manager.execute_command(
                    f"systemctl is-active {service['name']}"
                )
                status = stdout.read().decode().strip()
                if status == "active":
                    if label.winfo_exists():
                        label.configure(
                            fg_color="green", text=f"{service['name']}: Activo"
                        )
                else:
                    if label.winfo_exists():
                        label.configure(
                            fg_color="red", text=f"{service['name']}: Inactivo"
                        )
            except Exception as e:
                logger.error(
                    f"No se pudo actualizar el estado del servicio {service['name']}: {e}"
                )
            time.sleep(5)
