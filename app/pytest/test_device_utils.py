import pytest
from app.utils.device_utils import is_mobile

def test_is_mobile():
    assert is_mobile("Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X)")
    assert is_mobile("Mozilla/5.0 (Linux; Android 10; SM-G991B)")
    assert not is_mobile("Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    assert not is_mobile("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)")
