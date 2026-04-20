from flask import Flask, request
from datetime import datetime
import socket

app = Flask(__name__)

def get_container_ip():
    """Zwraca realne IP kontenera/poda, niezależnie od środowiska."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Nie wysyła pakietów — tylko ustawia routing
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "Could not get container IP"
    finally:
        s.close()

@app.route('/api')
def get_info():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    container_ip = get_container_ip()
    # remote_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    remote_ip = request.headers.get("Cf-Connecting-Ip") or \
                request.headers.get("X-Forwarded-For", request.remote_addr)

    return (
        f"date: {current_time}<br>"
        f"container IP: {container_ip}<br>"
        f"your IP: {remote_ip}"
    )

@app.route('/debug')
def get_debug():
    headers = "<br>".join([f"{k}: {v}" for k, v in request.headers.items()])
    return headers

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
