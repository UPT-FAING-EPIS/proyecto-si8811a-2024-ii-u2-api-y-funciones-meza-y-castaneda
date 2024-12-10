import pytest
import sys
from utils.device_utils import is_mobile
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

def test_is_mobile():
    # Prueba para una cadena de usuario de navegador de iPhone
    assert is_mobile("Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X)")

    # Prueba para una cadena de usuario de navegador de Android
    assert is_mobile("Mozilla/5.0 (Linux; Android 10; SM-G991B)")

    # Prueba para cadenas de usuario de navegador que no representan dispositivos móviles
    assert not is_mobile("Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    assert not is_mobile("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)")

    # Prueba con una cadena de usuario de navegador que representa un iPad
    assert not is_mobile("Mozilla/5.0 (iPad; CPU OS 14_3 like Mac OS X)")

    # Prueba con una cadena de usuario de navegador de dispositivo móvil genérico
    assert is_mobile("Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; GT-I9300 Build/GRJ22)")

    # Prueba con una cadena de usuario de navegador de navegador de consola (común en pruebas automatizadas)
    assert not is_mobile("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36")
