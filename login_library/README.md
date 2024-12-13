# Login Library

**Login Library** es una librería de Python que facilita la autenticación de usuarios utilizando **Microsoft** y **Google OAuth2**. Además, incluye soporte para generar y manejar **JWTs** (JSON Web Tokens). Su diseño modular permite integrar la autenticación en cualquier proyecto de manera rápida y reutilizable.

---

## Características

- Autenticación con **Microsoft** usando MSAL (Microsoft Authentication Library).
- Autenticación con **Google OAuth2**.
- Generación y validación de **JWTs**.
- Detección de dispositivos móviles mediante el `User-Agent`.

---

## Instalación

### Requisitos previos

1. Python 3.7 o superior.
2. Configuración de aplicaciones en los servicios de autenticación:
   - **Microsoft:** Registra tu aplicación en [Azure AD](https://portal.azure.com/).
   - **Google:** Registra tu aplicación en [Google Cloud Console](https://console.cloud.google.com/).

### Instalación de la librería

#### Desde PyPI
Si tu librería está publicada en PyPI, instálala usando:

```bash
pip install login-library
```

Si estás trabajando localmente, puedes instalarla desde la carpeta del proyecto:
```bash
pip install .
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