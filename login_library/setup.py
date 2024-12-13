from setuptools import setup, find_packages

setup(
    name="login-library",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "msal",
        "oauthlib",
        "requests",
        "PyJWT"
    ],
    author="Marco",
    description="Librería para autenticación con Microsoft y Google usando Flask.",
    url="https://github.com/UPT-FAING-EPIS/proyecto-si8811a-2024-ii-u2-api-y-funciones-meza-y-castaneda/login-library",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
