#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: ssh_manager.py
# Project: SSH-Sentinel
# File Created: Thursday, 5th December 2024 1:43:29 pm
# Author: Daniel Rodríguez Cabrera (daniel8rc@gmail.com)
# Version: 1.0.0
# -----
# Last Modified: Thursday, 5th December 2024 2:07:51 pm
# Modified By: Daniel Rodríguez Cabrera
# -----
# Copyright (c) 2024 - 2025 daniel8rc@gmail.com copying, distribution or modification not authorised in writing is prohibited.
###
import threading
from loguru import logger
import paramiko


class SSHConnectionManager:
    """
    Clase para manejar las conexiones SSH.
    """

    def __init__(self):
        self.ssh_clients = {}
        self.current_server = None

    def connect(self, server, on_success, on_failure):
        """
        Conecta al servidor SSH.
        """

        def threaded_connect():
            try:
                logger.info(f"Conectando a {server['name']}...")
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(
                    server["host"],
                    username=server["username"],
                    password=server["password"],
                )
                self.ssh_clients[server["name"]] = ssh
                logger.info(f"Conectado a {server['name']}")
                self.current_server = server
                on_success()
            except Exception as e:
                logger.error(f"No se pudo conectar a {server['name']}: {e}")
                on_failure()

        threading.Thread(target=threaded_connect, daemon=True).start()

    def execute_command(self, command):
        """
        Ejecuta un comando en el servidor SSH actual.
        """
        if self.current_server and self.current_server["name"] in self.ssh_clients:
            ssh = self.ssh_clients[self.current_server["name"]]
            return ssh.exec_command(command)
        else:
            logger.error("No hay conexión SSH disponible.")
            return None, None, None
