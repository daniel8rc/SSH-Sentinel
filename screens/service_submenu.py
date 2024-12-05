#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: service_submenu.py
# Project: SSH-Sentinel
# File Created: Thursday, 5th December 2024 1:42:35 pm
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
from screens.journal_viewer import JournalViewer
from screens.log_viewer import LogViewer
from loguru import logger


class ServiceSubmenuScreen(BaseScreen):
    """
    Pantalla que muestra las opciones para un servicio seleccionado.
    """

    def __init__(self, root, service, ssh_manager, on_back):
        super().__init__(root)
        self.service = service
        self.ssh_manager = ssh_manager
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
            text=f"Servicio: {self.service['name']}",
            font=("Helvetica", 18, "bold"),
        )
        title.pack(pady=10)

        btn_logs = ctk.CTkButton(
            self.frame,
            text="Ver Logs",
            command=self.view_logs,
            font=("Helvetica", 14),
        )
        btn_logs.pack(pady=5, fill="x")

        btn_journalctl = ctk.CTkButton(
            self.frame,
            text="Ver Journalctl",
            command=self.view_journalctl,
            font=("Helvetica", 14),
        )
        btn_journalctl.pack(pady=5, fill="x")

        btn_restart = ctk.CTkButton(
            self.frame,
            text="Reiniciar Servicio",
            command=self.restart_service,
            font=("Helvetica", 14),
        )
        btn_restart.pack(pady=5, fill="x")

        btn_stop = ctk.CTkButton(
            self.frame,
            text="Detener Servicio",
            command=self.stop_service,
            font=("Helvetica", 14),
        )
        btn_stop.pack(pady=5, fill="x")

        btn_start = ctk.CTkButton(
            self.frame,
            text="Iniciar Servicio",
            command=self.start_service,
            font=("Helvetica", 14),
        )
        btn_start.pack(pady=5, fill="x")

        back_btn = ctk.CTkButton(
            self.frame,
            text="Volver",
            command=self.on_back,
            font=("Helvetica", 14),
        )
        back_btn.pack(pady=20)

    def view_logs(self):
        """
        Abre el visor de logs para los logs del servicio.
        """
        LogViewer(self.root, self.service, self.ssh_manager, self.on_back)

    def view_journalctl(self):
        """
        Abre el visor de journalctl para los logs del servicio.
        """
        JournalViewer(self.root, self.service, self.ssh_manager, self.on_back)

    def restart_service(self):
        """
        Reinicia el servicio.
        """
        command = f'echo {self.ssh_manager.current_server["password"]} | sudo -S systemctl restart {self.service["name"]}'
        self.ssh_manager.execute_command(command)

    def stop_service(self):
        """
        Detiene el servicio.
        """
        command = f'echo {self.ssh_manager.current_server["password"]} | sudo -S systemctl stop {self.service["name"]}'
        self.ssh_manager.execute_command(command)

    def start_service(self):
        """
        Inicia el servicio.
        """
        command = f'echo {self.ssh_manager.current_server["password"]} | sudo -S systemctl start {self.service["name"]}'
        self.ssh_manager.execute_command(command)
