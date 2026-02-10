import time
from login import login

access_token = None
token = 0
def ensure_token(username, password):
    """Đảm bảo token truy cập hợp lệ."""
    global access_token, token
    if access_token is None or time.time() > token:
        access_token = login(username, password)
        token = time.time() + 1700 
    return access_token
