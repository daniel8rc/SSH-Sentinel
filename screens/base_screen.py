#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: base_screen.py
# Project: SSH-Sentinel
# File Created: Thursday, 5th December 2024 1:42:01 pm
# Author: Daniel Rodríguez Cabrera (daniel8rc@gmail.com)
# Version: 1.0.0
# -----
# Last Modified: Thursday, 5th December 2024 2:07:51 pm
# Modified By: Daniel Rodríguez Cabrera
# -----
# Copyright (c) 2024 - 2025 daniel8rc@gmail.com copying, distribution or modification not authorised in writing is prohibited.
###
from loguru import logger


class BaseScreen:
    """
    Clase base para las pantallas, maneja el limpiado de la ventana.
    """

    def __init__(self, root):
        self.root = root
        self.clear_window()

    def clear_window(self):
        """
        Limpia todos los widgets de la ventana principal.
        """
        for widget in self.root.winfo_children():
            widget.destroy()
