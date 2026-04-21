from flask import Flask, request
from datetime import datetime
import socket
import requests
import json
import os

app = Flask(__name__)

def get_service_status():
    token_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"
    ca_path = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
    namespace = "k8s-test-app"
    service = "frontend"

    with open(token_path, "r") as f:
        token = f.read()

    url = f"https://kubernetes.default.svc/api/v1/namespaces/{namespace}/services/{service}"

    r = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        verify=ca_path,
        timeout=3
    )

    return r.json()


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

def get_external_ip():
    token_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"
    ca_path = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
    namespace = "k8s-test-app"
    service = "frontend"

    with open(token_path, "r") as f:
        token = f.read()

    url = f"https://kubernetes.default.svc/api/v1/namespaces/{namespace}/services/{service}"

    r = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        verify=ca_path,
        timeout=3
    )

    data = r.json()
    return data["status"]["loadBalancer"]["ingress"][0]["ip"]


@app.route('/api')
def get_info():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    container_ip = get_container_ip()
    # remote_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    remote_ip = request.headers.get("Cf-Connecting-Ip") or \
                request.headers.get("X-Forwarded-For", request.remote_addr)

    return (
        f"date: {current_time}<br><br>"
        f"container IP: {container_ip}<br>"
        f"your IP: {remote_ip}"
    )

@app.route('/debug')
def get_debug():
    # Headers
    headers = "<h2>Headers</h2>" + "<br>".join([f"{k}: {v}" for k, v in request.headers.items()])

    # WSGI environ
    environ = "<h2>WSGI environ</h2>" + "<br>".join([f"{k}: {v}" for k, v in request.environ.items()])

    # Kubernetes service status
    try:
        svc = get_service_status()
        status = svc.get("status", {})
        external_ip = status.get("loadBalancer", {}).get("Ingress", [{}])[0].get("ip", "N/A")

        status_html = (
            "<h2>Kubernetes Service Status</h2>"
            f"<b>External IP:</b> {external_ip}<br><br>"
            "<pre>" + json.dumps(status, indent=2) + "</pre>"
        )
    except Exception as e:
        status_html = f"<h2>Kubernetes Service Status</h2>Error: {e}"

    return headers + "<hr>" + environ + "<hr>" + status_html

#@app.route('/debug')
#def get_debug():
#    import os
#    headers = "<h2>Headers</h2>" + "<br>".join([f"{k}: {v}" for k, v in request.headers.items()])
#    environ = "<h2>WSGI environ</h2>" + "<br>".join([f"{k}: {v}" for k, v in request.environ.items()])
#    return headers + "<hr>" + environ
#    # headers = "<br>".join([f"{k}: {v}" for k, v in request.headers.items()])
#    # return headers

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
