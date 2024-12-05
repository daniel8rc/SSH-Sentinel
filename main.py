#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: main.py
# Project: SSH-Sentinel
# File Created: Thursday, 5th December 2024 1:43:12 pm
# Author: Daniel Rodríguez Cabrera (daniel8rc@gmail.com)
# Version: 1.0.0
# -----
# Last Modified: Thursday, 5th December 2024 2:07:51 pm
# Modified By: Daniel Rodríguez Cabrera
# -----
# Copyright (c) 2024 - 2025 daniel8rc@gmail.com copying, distribution or modification not authorised in writing is prohibited.
###
import json
import customtkinter as ctk
from loguru import logger
from screens.server_selection import ServerSelectionScreen
from screens.server_status import ServerStatusScreen
from screens.services_menu import ServicesMenuScreen
from screens.service_submenu import ServiceSubmenuScreen
from utils.ssh_manager import SSHConnectionManager


class MainApp:
    """
    Clase principal de la aplicación SSH Server Manager.
    """

    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("800x600")
        self.root.title("SSH Server Manager")

        self.config = self.load_config("config.json")
        self.ssh_manager = SSHConnectionManager()
        self.current_screen = None

        self.show_server_selection_screen()

        self.root.mainloop()

    def load_config(self, file_path):
        """
        Carga la configuración desde un archivo JSON.
        """
        with open(file_path, "r") as file:
            return json.load(file)

    def show_server_selection_screen(self):
        """
        Muestra la pantalla de selección de servidor.
        """
        self.current_screen = ServerSelectionScreen(
            self.root, self.config["servers"], self.on_server_selected
        )

    def on_server_selected(self, server):
        """
        Callback cuando un servidor es seleccionado.
        """
        self.current_server = server
        self.show_server_status_screen(server)

    def show_server_status_screen(self, server):
        """
        Muestra la pantalla de estado del servidor después de conectar.
        """
        self.current_screen = ServerStatusScreen(
            self.root, server, self.ssh_manager, self.on_services_button_clicked
        )

    def on_services_button_clicked(self):
        """
        Callback cuando el botón de Servicios es clickeado.
        """
        self.show_services_menu()

    def show_services_menu(self):
        """
        Muestra la pantalla del menú de servicios.
        """
        self.current_screen = ServicesMenuScreen(
            self.root,
            self.current_server,
            self.ssh_manager,
            self.on_service_selected,
            self.show_server_selection_screen,
        )

    def on_service_selected(self, service):
        """
        Callback cuando un servicio es seleccionado.
        """
        self.show_service_submenu(service)

    def show_service_submenu(self, service):
        """
        Muestra la pantalla del submenú del servicio seleccionado.
        """
        self.current_screen = ServiceSubmenuScreen(
            self.root, service, self.ssh_manager, self.show_services_menu
        )


if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Establece el modo de apariencia
    ctk.set_default_color_theme("blue")  # Establece el tema de color

    app = MainApp()
