# SSH Sentinel

SSH Sentinel es una aplicación de escritorio desarrollada en Python que permite gestionar y monitorear servidores SSH de manera eficiente. Con una interfaz gráfica intuitiva, SSH Sentinel facilita la conexión, supervisión y administración de servicios en servidores remotos, proporcionando herramientas para visualizar logs, controlar servicios y obtener información del sistema en tiempo real.

## Características

- **Conexión a Múltiples Servidores:** Gestiona conexiones SSH a varios servidores desde una sola interfaz.
- **Autenticación Segura:** Soporta autenticación mediante contraseña y claves SSH.
- **Gestión de Servicios:** Inicia, detén y reinicia servicios en el servidor remoto con un solo clic.
- **Visualización de Logs:** Visualiza y filtra logs de servicios en tiempo real.
- **Monitoreo del Sistema:** Obtén información actualizada sobre el uso de memoria, carga del sistema y más.
- **Interfaz Amigable:** Diseño intuitivo utilizando `customtkinter` para una experiencia de usuario mejorada.
- **Actualizaciones en Tiempo Real:** Información y estado de servicios actualizados automáticamente sin necesidad de refrescar manualmente.

## Capturas de Pantalla

_(pendiente)_

## Instalación

### Prerrequisitos

- **Python 3.7 o superior** instalado en tu sistema.
- Las siguientes librerías de Python:
  - `customtkinter`
  - `paramiko`
  - `loguru`

### Clonar el Repositorio

```bash
git clone https://github.com/daniel8rc/SSH-Sentinel.git
cd ssh-sentinel
```

### Crear un Entorno Virtual (Opcional pero Recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Configuración

Antes de ejecutar la aplicación, es necesario configurar los servidores y servicios que deseas gestionar.

### Archivo `config.json`

Edita el archivo `config.json` y agrega la información de tus servidores y servicios. El formato es el siguiente:

```json
{
  "servers": [
    {
      "name": "Servidor 1",
      "host": "192.168.1.100",
      "username": "usuario",
      "password": "contraseña",
      "services": [
        {
          "name": "nginx",
          "log_path": "/var/log/nginx/error.log"
        },
        {
          "name": "mysql",
          "log_path": "/var/log/mysql/error.log"
        }
      ]
    },
    {
      "name": "Servidor 2",
      "host": "192.168.1.101",
      "username": "usuario",
      "password": "contraseña",
      "services": [
        {
          "name": "apache2",
          "log_path": "/var/log/apache2/error.log"
        }
      ]
    }
  ]
}
```

**Nota:** Por razones de seguridad, considera usar autenticación mediante claves SSH y almacenar contraseñas de manera segura.

## Ejecución

Una vez configurado, puedes iniciar la aplicación ejecutando:

```bash
python main.py
```

## Uso

1. **Seleccionar Servidor:** Al iniciar la aplicación, selecciona el servidor al que deseas conectarte.
2. **Conexión SSH:** La aplicación intentará establecer una conexión SSH con el servidor seleccionado.
3. **Menú de Servicios:** Una vez conectado, podrás ver y gestionar los servicios configurados en ese servidor.
4. **Acciones sobre Servicios:**
   - **Ver Logs:** Visualiza los logs del servicio en tiempo real y aplica filtros según tus necesidades.
   - **Ver Journalctl:** Observa los logs del sistema relacionados con el servicio.
   - **Iniciar/Detener/Reiniciar Servicio:** Controla el estado del servicio directamente desde la aplicación.

## Contribución

¡Las contribuciones son bienvenidas! Si deseas colaborar con SSH Sentinel, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama con la nueva característica o corrección de errores: `git checkout -b mi-nueva-rama`.
3. Realiza tus cambios y haz commit de ellos: `git commit -m 'Agrego nueva característica'`.
4. Sube tus cambios a tu repositorio fork: `git push origin mi-nueva-rama`.
5. Abre un Pull Request en GitHub.

## Roadmap

- [ ] Implementar autenticación mediante claves SSH.
- [ ] Añadir soporte para editar la configuración desde la interfaz gráfica.
- [ ] Mejorar la interfaz de usuario con más opciones de personalización.
- [ ] Soporte para múltiples conexiones simultáneas.
- [ ] Integración con sistemas de notificaciones para alertas en tiempo real.
- [ ] Añadir pruebas unitarias y de integración.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Desarrollado por [Daniel8rc](https://github.com/daniel8rc). Si tienes alguna pregunta o sugerencia, no dudes en contactarme.

## Agradecimientos

- A todos los contribuidores y testers que han ayudado a mejorar SSH Sentinel.
- A las comunidades de Python y open-source por su apoyo y recursos.

¡Gracias por usar SSH Sentinel! 🚀
