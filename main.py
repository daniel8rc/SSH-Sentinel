#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: main.py
# Project: SSH-Sentinel
# File Created: Thursday, 5th December 2024 1:43:12 pm
# Author: Daniel Rodríguez Cabrera (daniel8rc@gmail.com)
# Version: 1.0.0
# -----
# Last Modified: Thursday, 19th December 2024 6:15:32 pm
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
        self.current_server = None  # Inicializar current_server

        # Contenedor superior para botones generales
        self.top_frame = ctk.CTkFrame(self.root)
        self.top_frame.pack(side="top", fill="x")

        # Botón para crear una nueva pestaña
        self.new_tab_button = ctk.CTkButton(
            self.top_frame, text="Crear Nueva Pestaña", command=self.add_new_tab
        )
        self.new_tab_button.pack(side="left", padx=10, pady=5)

        # Botón para cerrar la pestaña actual
        self.close_tab_button = ctk.CTkButton(
            self.top_frame, text="Cerrar Pestaña Actual", command=self.close_current_tab
        )
        self.close_tab_button.pack(side="left", padx=10, pady=5)

        # Contenedor para los botones de pestañas
        self.tab_buttons_frame = ctk.CTkFrame(self.top_frame)
        self.tab_buttons_frame.pack(side="left", padx=10)

        # Contenedor para las pestañas
        self.tabs_frame = ctk.CTkFrame(self.root)
        self.tabs_frame.pack(fill="both", expand=True)

        self.tabs = {}
        self.current_tab = None
        self.tab_count = 0

        # Crear la primera pestaña por defecto
        self.add_new_tab()

        self.root.mainloop()

    def add_new_tab(self):
        """
        Añade una nueva pestaña con el menú principal.
        """
        tab_id = f"Pestaña {self.tab_count + 1}"
        self.tab_count += 1

        # Crear botón para la pestaña
        tab_button = ctk.CTkButton(
            self.tab_buttons_frame,
            text=tab_id,
            command=lambda: self.switch_tab(tab_id),
        )
        tab_button.pack(side="left", padx=5)

        # Crear frame para la pestaña
        tab_frame = ctk.CTkFrame(self.tabs_frame)
        tab_frame.pack(fill="both", expand=True)

        # Contenedor interno para contenido dinámico
        content_frame = ctk.CTkFrame(tab_frame)
        content_frame.pack(fill="both", expand=True)

        self.tabs[tab_id] = {
            "button": tab_button,
            "frame": tab_frame,
            "content_frame": content_frame,  # Almacenar el contenedor de contenido
        }

        self.switch_tab(tab_id)
        ServerSelectionScreen(
            content_frame, self.config["servers"], self.on_server_selected
        )

    def switch_tab(self, tab_id):
        """
        Cambia a la pestaña seleccionada.
        """
        if self.current_tab:
            self.tabs[self.current_tab]["frame"].pack_forget()
        self.current_tab = tab_id
        self.tabs[tab_id]["frame"].pack(fill="both", expand=True)

    def close_current_tab(self):
        """
        Cierra la pestaña actualmente seleccionada.
        """
        if self.current_tab:
            if len(self.tabs) > 1:  # Asegurarse de que queda al menos una pestaña
                tab_data = self.tabs.pop(self.current_tab)
                tab_data["frame"].destroy()
                tab_data["button"].destroy()

                # Cambiar a otra pestaña disponible
                self.current_tab = list(self.tabs.keys())[0]
                self.switch_tab(self.current_tab)

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
        self.current_server = server  # Asignar el servidor actual
        if self.current_tab:
            content_frame = self.tabs[self.current_tab]["content_frame"]
            for widget in content_frame.winfo_children():
                widget.destroy()  # Limpiar el contenido anterior
            self.show_server_status_screen(server, content_frame)

    def show_services_menu(self, frame):
        """
        Muestra la pantalla del menú de servicios en el contenedor dinámico actual.
        """
        if not self.current_server:
            logger.error("No hay servidor seleccionado.")
            return

        self.current_screen = ServicesMenuScreen(
            frame,
            self.current_server,
            self.ssh_manager,
            self.on_service_selected,
            lambda: self.on_server_selected(self.current_server),
        )

    def show_server_status_screen(self, server, frame):
        """
        Muestra la pantalla de estado del servidor dentro del contenedor dinámico actual.
        """
        self.current_screen = ServerStatusScreen(
            frame, server, self.ssh_manager, self.on_services_button_clicked
        )

    def on_services_button_clicked(self):
        """
        Callback cuando el botón de Servicios es clickeado.
        """
        if self.current_tab:
            content_frame = self.tabs[self.current_tab]["content_frame"]
            for widget in content_frame.winfo_children():
                widget.destroy()  # Limpiar el contenido anterior
            self.show_services_menu(content_frame)

    def on_service_selected(self, service):
        """
        Callback cuando un servicio es seleccionado.
        """
        if self.current_tab:
            content_frame = self.tabs[self.current_tab]["content_frame"]
            for widget in content_frame.winfo_children():
                widget.destroy()  # Limpiar el contenido anterior
            self.show_service_submenu(service, content_frame)

    def show_service_submenu(self, service, frame):
        """
        Muestra la pantalla del submenú del servicio seleccionado en el contenedor dinámico actual.
        """
        self.current_screen = ServiceSubmenuScreen(
            frame, service, self.ssh_manager, lambda: self.show_services_menu(frame)
        )


if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Establece el modo de apariencia
    ctk.set_default_color_theme("blue")  # Establece el tema de color

    app = MainApp()
