#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: server_status.py
# Project: SSH-Sentinel
# File Created: Thursday, 5th December 2024 1:42:22 pm
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
from utils.system_info import SystemInfo


class ServerStatusScreen(BaseScreen):
    """
    Pantalla que muestra el estado después de conectar a un servidor.
    """

    def __init__(self, root, server, ssh_manager, on_services_button_clicked):
        super().__init__(root)
        self.server = server
        self.ssh_manager = ssh_manager
        self.on_services_button_clicked = on_services_button_clicked

        self.status_label = None
        self.services_btn = None

        self.setup_ui()
        self.connect_ssh()

    def setup_ui(self):
        """
        Configura los elementos de la interfaz de usuario.
        """
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            self.frame,
            text=f"Conectando a {self.server['name']}...",
            font=("Helvetica", 18, "bold"),
        )
        title.pack(pady=10)

        self.status_label = ctk.CTkLabel(
            self.frame,
            text="Por favor espere mientras se conecta...",
            font=("Helvetica", 14),
        )
        self.status_label.pack(pady=10)

        self.services_btn = ctk.CTkButton(
            self.frame,
            text="Servicios",
            command=self.on_services_button_clicked,
            state="disabled",
            font=("Helvetica", 14),
        )
        self.services_btn.pack(pady=20)

    def connect_ssh(self):
        """
        Inicia la conexión SSH al servidor.
        """
        self.ssh_manager.connect(
            self.server, on_success=self.on_ssh_connected, on_failure=self.on_ssh_failed
        )

    def on_ssh_connected(self):
        """
        Callback cuando la conexión SSH es exitosa.
        """
        self.status_label.configure(text=f"Conectado a {self.server['name']}")
        self.services_btn.configure(state="normal")
        self.start_system_status_thread()

    def on_ssh_failed(self):
        """
        Callback cuando la conexión SSH falla.
        """
        self.status_label.configure(text=f"No se pudo conectar a {self.server['name']}")
        self.services_btn.configure(state="disabled")

    def start_system_status_thread(self):
        """
        Inicia un hilo para actualizar el estado del sistema periódicamente.
        """
        threading.Thread(target=self.update_system_status, daemon=True).start()

    def update_system_status(self):
        """
        Actualiza la información del estado del sistema periódicamente.
        """
        while True:
            stdin, stdout, stderr = self.ssh_manager.execute_command(
                "cat /proc/uptime; cat /proc/meminfo; cat /proc/loadavg"
            )
            if stdout:
                output = stdout.read().decode()
                system_info = SystemInfo.parse_system_info(output)

                formatted_output = (
                    f"{'Información del Sistema':^40}\n"
                    f"{'-'*40}\n"
                    f"{'Memoria Total':<15}: {system_info['total_memory']}\n"
                    f"{'Memoria Usada':<15}: {system_info['used_memory']}\n"
                    f"{'Memoria Libre':<15}: {system_info['free_memory']}\n"
                    f"{'Promedio de Carga':<15}: 1min={system_info['load_average']['1min']}, "
                    f"5min={system_info['load_average']['5min']}, "
                    f"15min={system_info['load_average']['15min']}\n"
                    f"{'-'*40}"
                )
                if self.status_label.winfo_exists():
                    self.status_label.configure(text=formatted_output)
            else:
                logger.error("No se pudo obtener el estado del sistema.")
            time.sleep(5)  # Actualizar cada 5 segundos
