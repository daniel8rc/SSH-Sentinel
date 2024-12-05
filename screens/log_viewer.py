#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: log_viewer.py
# Project: SSH-Sentinel
# File Created: Thursday, 5th December 2024 1:42:41 pm
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


class LogViewer(BaseScreen):
    """
    Pantalla para mostrar los logs de un servicio.
    """

    def __init__(self, root, service, ssh_manager, on_back):
        super().__init__(root)
        self.service = service
        self.ssh_manager = ssh_manager
        self.on_back = on_back

        self.log_font_size = 14
        self.current_filter = None

        self.setup_ui()
        threading.Thread(target=self.fetch_logs, daemon=True).start()

    def setup_ui(self):
        """
        Configura los elementos de la interfaz de usuario.
        """
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            self.frame,
            text=f"Logs de {self.service['name']}",
            font=("Helvetica", 18, "bold"),
        )
        title.pack(pady=10)

        # Área de texto para los logs
        log_text_frame = ctk.CTkFrame(self.frame)
        log_text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_text = ctk.CTkTextbox(log_text_frame, width=800, height=800)
        self.log_text.pack(fill="both", expand=True)

        # Configuración inicial del tamaño de fuente
        self.log_text._textbox.configure(font=("Courier", self.log_font_size))

        # Input de filtro
        filter_frame = ctk.CTkFrame(self.frame)
        filter_frame.pack(pady=10)

        filter_label = ctk.CTkLabel(filter_frame, text="Filtrar logs:")
        filter_label.pack(side="left", padx=5)

        self.filter_entry = ctk.CTkEntry(filter_frame, width=200)
        self.filter_entry.pack(side="left", padx=5)

        filter_button = ctk.CTkButton(
            filter_frame, text="Aplicar", command=self.apply_filter
        )
        filter_button.pack(side="left", padx=5)

        back_btn = ctk.CTkButton(
            self.frame,
            text="Volver",
            command=self.on_back,
            font=("Helvetica", 14),
        )
        back_btn.pack(side="left", padx=5)

        # Botones para ajustar el tamaño de letra
        button_frame = ctk.CTkFrame(self.frame)
        button_frame.pack(pady=10)

        increase_font_button = ctk.CTkButton(
            button_frame, text="Aumentar Letra", command=self.increase_font
        )
        increase_font_button.pack(side="left", padx=10)

        decrease_font_button = ctk.CTkButton(
            button_frame, text="Disminuir Letra", command=self.decrease_font
        )
        decrease_font_button.pack(side="left", padx=10)

        # Configuración de resaltado de texto
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("warning", foreground="orange")
        self.log_text.tag_config("info", foreground="blue")

    def apply_filter(self):
        """
        Aplica el filtro a los logs.
        """
        self.current_filter = self.filter_entry.get().strip() or None
        self.log_text.delete("1.0", "end")  # Limpia los logs actuales

    def increase_font(self):
        """
        Aumenta el tamaño de letra de los logs.
        """
        self.log_font_size += 2
        self.log_text._textbox.configure(font=("Courier", self.log_font_size))

    def decrease_font(self):
        """
        Disminuye el tamaño de letra de los logs.
        """
        if self.log_font_size > 8:  # Tamaño mínimo
            self.log_font_size -= 2
            self.log_text._textbox.configure(font=("Courier", self.log_font_size))

    def highlight_logs(self, line):
        """
        Resalta las líneas de logs según la severidad.
        """
        if "error" in line.lower() or "critical" in line.lower():
            self.log_text.insert("end", line, "error")
        elif "warning" in line.lower():
            self.log_text.insert("end", line, "warning")
        elif "info" in line.lower():
            self.log_text.insert("end", line, "info")
        else:
            self.log_text.insert("end", line)

    def fetch_logs(self):
        """
        Obtiene los logs del servidor.
        """
        try:
            command = f"tail -f {self.service['log_path']}"
            stdin, stdout, stderr = self.ssh_manager.execute_command(command)
            while True:
                line = stdout.readline()
                if line:
                    # Aplica el filtro si está configurado
                    if (
                        self.current_filter is None
                        or self.current_filter.lower() in line.lower()
                    ):
                        self.highlight_logs(line)
                        self.log_text.see("end")
                else:
                    time.sleep(0.1)
        except Exception as e:
            logger.error(f"No se pudieron obtener los logs: {e}")
