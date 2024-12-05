#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: system_info.py
# Project: SSH-Sentinel
# File Created: Thursday, 5th December 2024 1:43:35 pm
# Author: Daniel Rodríguez Cabrera (daniel8rc@gmail.com)
# Version: 1.0.0
# -----
# Last Modified: Thursday, 5th December 2024 2:07:51 pm
# Modified By: Daniel Rodríguez Cabrera
# -----
# Copyright (c) 2024 - 2025 daniel8rc@gmail.com copying, distribution or modification not authorised in writing is prohibited.
###
from loguru import logger


class SystemInfo:
    """
    Clase para parsear y obtener información del sistema desde los comandos SSH.
    """

    @logger.catch
    @staticmethod
    def parse_system_info(data):
        import re

        # Diccionario para almacenar las variables
        variables = {}

        # Procesar línea por línea
        lines = data.split("\n")

        # Expresión regular para capturar el nombre de la variable y el valor
        regex = r"([\w\(\)/]+):\s+([\d\.]+)\s*(kB)?"

        for line in lines:
            # Parsear líneas con formato "Variable: Value kB"
            match = re.match(regex, line)
            if match:
                var_name, value, unit = match.groups()
                value = float(value)

                # Convertir kB a MB o GB si aplica
                if unit == "kB":
                    if value >= 1_048_576:  # Convertir a GB
                        value = value / 1_048_576
                        variables[var_name] = f"{value:.2f} GB"
                    elif value >= 1024:  # Convertir a MB
                        value = value / 1024
                        variables[var_name] = f"{value:.2f} MB"
                    else:
                        variables[var_name] = f"{value:.2f} kB"
                else:
                    variables[var_name] = value

            elif re.match(r"^[\d\.]+\s[\d\.]+\s[\d\.]+\s\d+/\d+\s\d+$", line.strip()):
                parts = line.split()
                variables["LoadAvg1"] = float(parts[0])
                variables["LoadAvg5"] = float(parts[1])
                variables["LoadAvg15"] = float(parts[2])
                variables["RunningProcesses"] = parts[3]
                variables["LastPID"] = int(parts[4])

        return {
            "total_memory": variables.get("MemTotal", "0 GB"),
            "free_memory": variables.get("MemAvailable", "0 GB"),
            "used_memory": f"{float(variables.get('MemTotal', '0').split()[0]) - float(variables.get('MemAvailable', '0').split()[0]):.2f} GB",
            "load_average": {
                "1min": variables.get("LoadAvg1", 0),
                "5min": variables.get("LoadAvg5", 0),
                "15min": variables.get("LoadAvg15", 0),
            },
        }
