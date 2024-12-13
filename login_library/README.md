# Login Library

**Login Library** es una librería de Python que facilita la autenticación de usuarios utilizando **Microsoft** y **Google OAuth2**. Además, incluye soporte para generar y manejar **JWTs** (JSON Web Tokens). Su diseño modular permite integrar la autenticación en cualquier proyecto de manera rápida y reutilizable.

---

## Características

- Autenticación con **Microsoft** usando MSAL (Microsoft Authentication Library).
- Autenticación con **Google OAuth2**.
- Generación y validación de **JWTs**.
- Detección de dispositivos móviles mediante el `User-Agent`.

---

## Facilidades

### **Facilidades para Microsoft**
La librería simplifica la autenticación con Microsoft utilizando MSAL, generando automáticamente la URL de inicio de sesión y gestionando el intercambio de códigos por tokens de acceso. Esto permite acceder fácilmente a recursos como Microsoft Graph API, ideal para aplicaciones que necesitan autenticar usuarios o interactuar con servicios de Microsoft 365 de forma segura y eficiente.

### **Facilidades para Google**
La librería abstrae el flujo OAuth2 de Google, generando la URL de inicio de sesión y gestionando la obtención de tokens de acceso y `id_token`. Es perfecta para integrar el inicio de sesión con Google y acceder a APIs como Google Drive o Gmail, proporcionando una experiencia de autenticación sencilla y segura.

---

## Instalación

### Requisitos previos

1. Python 3.7 o superior.
2. Configuración de aplicaciones en los servicios de autenticación:
   - **Microsoft:** Registra tu aplicación en [Azure AD](https://portal.azure.com/).
   - **Google:** Registra tu aplicación en [Google Cloud Console](https://console.cloud.google.com/).

### Instalación de la librería

1. Instalar desde el archivo de distribución local (dist/)

```bash
pip install dist/login_library-0.1.0-py3-none-any.whl
pip install dist/login-library-0.1.0.tar.gz
```

## Uso

### Configuración inicial

Configura las siguientes **variables de entorno** antes de usar la librería:

#### Para Microsoft
- `CLIENT_ID`: ID de cliente de tu aplicación en Azure.
- `CLIENT_SECRET`: Secreto del cliente.
- `AUTHORITY`: URL de autorización de Azure (por ejemplo: `https://login.microsoftonline.com/common`).
- `REDIRECT_PATH`: Ruta para la redirección después de iniciar sesión.

#### Para Google
- `GOOGLE_CLIENT_ID`: ID de cliente de tu aplicación en Google.
- `GOOGLE_CLIENT_SECRET`: Secreto del cliente.
- `GOOGLE_DISCOVERY_URL`: URL para descubrir los endpoints de Google OAuth (por defecto: `https://accounts.google.com/.well-known/openid-configuration`).

#### Para JWT
- `JWT_SECRET_KEY`: Clave secreta para firmar los tokens JWT.

### Cómo definir las variables de entorno

Puedes definir estas variables en tu terminal utilizando el siguiente comando:

```bash
export CLIENT_ID="tu-client-id"
export CLIENT_SECRET="tu-client-secret"
export AUTHORITY="https://login.microsoftonline.com/common"
export REDIRECT_PATH="/authorized"
export JWT_SECRET_KEY="super-secret-key"
export GOOGLE_CLIENT_ID="tu-google-client-id"
export GOOGLE_CLIENT_SECRET="tu-google-client-secret"
export GOOGLE_DISCOVERY_URL="https://accounts.google.com/.well-known/openid-configuration"
```

### Ejemplo de Uso

#### Autenticación con Microsoft

```python
from login_library.msal_auth import MicrosoftAuth

# Configurar credenciales
ms_auth = MicrosoftAuth(
    client_id="tu-client-id",
    client_secret="tu-client-secret",
    authority="https://login.microsoftonline.com/common",
    redirect_path="/authorized",
    scope=["User.Read"]
)

# Obtener URL de inicio de sesión
auth_url = ms_auth.get_auth_url("http://localhost:5000/authorized")
print(f"Inicia sesión visitando esta URL: {auth_url}")

# Intercambiar el código por un token
authorization_code = input("Ingresa el código de autorización recibido: ")
token_response = ms_auth.acquire_token(authorization_code, "http://localhost:5000/authorized")

if "access_token" in token_response:
    print(f"Token de acceso: {token_response['access_token']}")
else:
    print("Error en la autenticación:", token_response)
```
#### Autenticación con Google
```python

from login_library.google_auth import GoogleAuth
# Configurar credenciales
google_auth = GoogleAuth(
    client_id="tu-google-client-id",
    client_secret="tu-google-client-secret",
    discovery_url="https://accounts.google.com/.well-known/openid-configuration"
)

# Obtener URL de inicio de sesión
auth_url = google_auth.get_auth_url("http://localhost:5000/authorized")
print(f"Inicia sesión visitando esta URL: {auth_url}")

# Intercambiar el código por un token
authorization_code = input("Ingresa el código de autorización recibido: ")
token_response = google_auth.acquire_token(authorization_code, "http://localhost:5000/authorized")

if "id_token" in token_response:
    print(f"Token de acceso: {token_response['id_token']}")
else:
    print("Error en la autenticación:", token_response)
```

### Errores Comunes y Soluciones

1. **Error `invalid_grant` durante la autenticación**
   - **Causa:** El código de autorización expiró o no coincide el `redirect_uri`.
   - **Solución:** Verifica que el `redirect_uri` configurado en tu código coincida exactamente con el registrado en Azure o Google.

2. **Error `AADSTS50011`**
   - **Causa:** El `redirect_uri` no está configurado correctamente en Azure.
   - **Solución:** Agrega la URI correcta en la sección de "Redirect URIs" de la configuración de tu aplicación en Azure.

3. **Error `ModuleNotFoundError: No module named 'login_library'`**
   - **Causa:** La librería no está instalada correctamente.
   - **Solución:** Asegúrate de instalar la librería con:
     ```bash
     pip install -e .
     ```

4. **Error al instalar dependencias**
   - **Causa:** Versiones incompatibles de Python o dependencias.
   - **Solución:** Verifica que estás usando Python 3.7 o superior y que las dependencias están actualizadas.
