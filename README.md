# hll_name_banned

Este bot de hell let loose únicamente funciona con dependecia del rcon de https://github.com/MarechJ/hll_rcon_tool.
El objetivo del bot es ayudar a los moderadores de los servers controlando los nombres de los usuarios del servidor.

---

## Funcionamiento del Bot

El bot realiza las siguientes tareas:

2. **Monitoreo de usuarios:** Revisa los nombres de los usuarios que ingresan al servidor para verificar si cumplen con los criterios establecidos.
3. **Advertencias:** Si un nombre no es válido, el bot envía una advertencia al usuario indicando el problema y sugiriendo cambiar el nombre.
4. **Baneo:** Si el usuario no cambia su nombre después de un número configurable de advertencias, el bot puede proceder a realizar un baneo permanente.

---

## Configuración de Conexión

- `URLS_RCON=`: URLs del servidor RCON donde se ejecuta el bot. Si el servidor es mas de uno constara de una cadena separada por comas. Ej:https://serve1,https://server2
- `USER_RCON=`: Usuario para autenticar en el servidor RCON.
- `PASSWORD_RCON=`: Contraseña para autenticar en el servidor RCON.

## Endpoints de la API (conexiones por defecto del rcon) 

- `URL_LOGIN=/api/login`: Endpoint utilizado para autenticar el bot en el sistema.
- `URL_GET_PLAYERS=/api/get_players`: Endpoint para obtener la lista de jugadores actualmente conectados al servidor.
- `URL_MESSAGE=/api/message_player`: Endpoint para enviar mensajes directos a los jugadores.
- `URL_POST_PLAYER_COMMENT=/api/post_player_comment`: Endpoint para agregar un comentario sobre un jugador en el sistema.
- `URL_ADD_BLACKLIST=/api/add_blacklist_record`: Endpoint para agregar un jugador a la lista negra.

## Mensajes y Respuestas

- `MSG_WARNING=Tu nombre de Steam no está permitido en este servidor. El nombre debe ser legible y con caracteres latinos para facilitar la administración. Mantenerlo puede implicar que seas baneado.`
  - Mensaje de advertencia enviado al jugador cuando su nombre no cumple con los estándares.

- `ERROR_LOGIN_MSG=Error al hacer login en`
  - Mensaje mostrado cuando ocurre un error al intentar autenticar en el servidor.

- `ERROR_IN_MSG=Error en`
  - Mensaje genérico para registrar errores en las operaciones del bot.

- `MSG_TO_MSG=Mensaje enviado a`
  - Mensaje de confirmación que indica que se envió un mensaje a un jugador.

- `UNEXPECTED_ERROR_MSG=Error inesperado en name_banned`
  - Mensaje de error registrado cuando ocurre una excepción inesperada en la funcionalidad de baneo de nombres.

- `BAN_MSG=El nombre de tu usuario de Steam no es válido, abre ticket en la comunidad.`
  - Mensaje enviado al jugador cuando es baneado debido a un nombre no válido.

- `REASON_MSG=Nombre no válido`
  - Razón registrada al banear a un jugador.

- `SUCCESSFUL_BAN_MSG=Permabaneado:`
  - Mensaje registrado cuando un baneo se realiza con éxito.

## Configuración de Advertencias y Baneo

- `NUM_WARNINGS=3`
  - Número de advertencias que el bot enviará antes de proceder al baneo.

- `ENABLE_BAN=false`
  - Configuración para habilitar o deshabilitar el baneo. Si está configurado como `false`, el bot solo enviará advertencias pero no aplicará baneos.

- `REGEX=[A-Za-z0-9.^_ÑñÄËÏÖÜäëïöüÂÊÎÔÛâêîôûÁÉÍÓÚáéíóú➡\-\|]{3}`
  - Expresión regular en la que se basara el criterio de monitorización

---

## Notas Adicionales

- Asegúrate de que las credenciales (usuario y contraseña) sean correctas y que el servidor RCON esté configurado para aceptar conexiones del bot.
- Si `ENABLE_BAN` está configurado como `false`, el bot funcionará únicamente en modo de advertencia.

---

## Ejemplo de Archivo `.env`

```env
URLS_RCON=https://servidor1-rcon.com,https://servidor2-rcon.com,https://servidor3-rcon.com
USER_RCON=usuario
PASSWORD_RCON=contraseña
URL_LOGIN=/api/login
URL_GET_PLAYERS=/api/get_players
URL_MESSAGE=/api/message_player
URL_POST_PLAYER_COMMENT=/api/post_player_comment
URL_ADD_BLACKLIST=/api/add_blacklist_record
MSG_WARNING=Tu nombre de Steam no está permitido en este servidor. El nombre debe ser legible y con caracteres latinos para facilitar la administración. Mantenerlo puede implicar que seas baneado.
ERROR_LOGIN_MSG=Error al hacer login en
ERROR_IN_MSG=Error en
MSG_TO_MSG=Mensaje enviado a
UNEXPECTED_ERROR_MSG=Error inesperado en name_banned
BAN_MSG=El nombre de tu usuario de Steam no es válido, abre ticket en la comunidad.
REASON_MSG=Nombre no válido
SUCCESSFUL_BAN_MSG=Permabaneado:
NUM_WARNINGS=3
ENABLE_BAN=false
REGEX=[A-Za-z0-9.^_ÑñÄËÏÖÜäëïöüÂÊÎÔÛâêîôûÁÉÍÓÚáéíóú➡\-\|]{3}
```

---

This Hell Let Loose bot works exclusively with the RCON dependency from https://github.com/MarechJ/hll_rcon_tool.
The purpose of the bot is to assist server moderators by managing user names on the server.

---

## Bot Functionality

The bot performs the following tasks:

1. **User Monitoring:** Checks the names of users joining the server to ensure they meet established criteria.
2. **Warnings:** If a name is invalid, the bot sends a warning to the user explaining the issue and suggesting they change their name.
3. **Banning:** If the user does not change their name after a configurable number of warnings, the bot may proceed with a permanent ban.

---

## Connection Configuration

- `URLS_RCON=`: URLs of the RCON servers where the bot operates. If there is more than one server, they should be separated by commas. E.g., `https://server1,https://server2`.
- `USER_RCON=`: Username to authenticate with the RCON server.
- `PASSWORD_RCON=`: Password to authenticate with the RCON server.

## API Endpoints (default RCON connections)

- `URL_LOGIN=/api/login`: Endpoint used to authenticate the bot in the system.
- `URL_GET_PLAYERS=/api/get_players`: Endpoint to retrieve the list of players currently connected to the server.
- `URL_MESSAGE=/api/message_player`: Endpoint to send direct messages to players.
- `URL_POST_PLAYER_COMMENT=/api/post_player_comment`: Endpoint to add a comment about a player in the system.
- `URL_ADD_BLACKLIST=/api/add_blacklist_record`: Endpoint to add a player to the blacklist.

## Messages and Responses

- `MSG_WARNING=Your Steam name is not allowed on this server. The name must be readable and use Latin characters to facilitate administration. Keeping it may result in a ban.`
  - Warning message sent to the player when their name does not meet the standards.

- `ERROR_LOGIN_MSG=Error logging into`
  - Message displayed when an error occurs while attempting to authenticate with the server.

- `ERROR_IN_MSG=Error in`
  - Generic message to log errors in the bot's operations.

- `MSG_TO_MSG=Message sent to`
  - Confirmation message indicating that a message was sent to a player.

- `UNEXPECTED_ERROR_MSG=Unexpected error in name_banned`
  - Error message logged when an unexpected exception occurs in the name banning functionality.

- `BAN_MSG=Your Steam user name is invalid. Please open a ticket in the community.`
  - Message sent to the player when they are banned due to an invalid name.

- `REASON_MSG=Invalid name`
  - Reason logged when banning a player.

- `SUCCESSFUL_BAN_MSG=Permanently banned:`
  - Message logged when a ban is successfully executed.

## Warning and Ban Configuration

- `NUM_WARNINGS=3`
  - Number of warnings the bot will send before proceeding with a ban.

- `ENABLE_BAN=false`
  - Configuration to enable or disable banning. If set to `false`, the bot will only send warnings but will not apply bans.

- `REGEX=[A-Za-z0-9.^_ÑñÄËÏÖÜäëïöüÂÊÎÔÛâêîôûÁÉÍÓÚáéíóú➡\-\|]{3}`
  - Regular expression on which the monitoring criteria will be based.
---

## Additional Notes

- Ensure that the credentials (username and password) are correct and that the RCON server is configured to accept connections from the bot.
- If `ENABLE_BAN` is set to `false`, the bot will operate in warning-only mode.

---

## Example `.env` File

```env
URLS_RCON=https://server1-rcon.com,https://server2-rcon.com,https://server3-rcon.com
USER_RCON=username
PASSWORD_RCON=password
URL_LOGIN=/api/login
URL_GET_PLAYERS=/api/get_players
URL_MESSAGE=/api/message_player
URL_POST_PLAYER_COMMENT=/api/post_player_comment
URL_ADD_BLACKLIST=/api/add_blacklist_record
MSG_WARNING=Your Steam name is not allowed on this server. The name must be readable and use Latin characters to facilitate administration. Keeping it may result in a ban.
ERROR_LOGIN_MSG=Error logging into
ERROR_IN_MSG=Error in
MSG_TO_MSG=Message sent to
UNEXPECTED_ERROR_MSG=Unexpected error in name_banned
BAN_MSG=Your Steam user name is invalid. Please open a ticket in the community.
REASON_MSG=Invalid name
SUCCESSFUL_BAN_MSG=Permanently banned:
NUM_WARNINGS=3
ENABLE_BAN=false
REGEX=[A-Za-z0-9.^_ÑñÄËÏÖÜäëïöüÂÊÎÔÛâêîôûÁÉÍÓÚáéíóú➡\-\|]{3}
```
