import subprocess

def set_mac_proxy(network_service, proxy_host, proxy_port):
    try:
        # Set Web Proxy (HTTP)
        subprocess.run([
            "networksetup",
            "-setwebproxy",
            network_service,
            proxy_host,
            str(proxy_port)
        ], check=True)

        # Set Secure Web Proxy (HTTPS)
        subprocess.run([
            "networksetup",
            "-setsecurewebproxy",
            network_service,
            proxy_host,
            str(proxy_port)
        ], check=True)

        # Enable both proxies
        subprocess.run([
            "networksetup",
            "-setwebproxystate",
            network_service,
            "on"
        ], check=True)

        subprocess.run([
            "networksetup",
            "-setsecurewebproxystate",
            network_service,
            "on"
        ], check=True)

        print("✅ Proxy settings updated successfully.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to set proxy: {e}")

set_mac_proxy(
    "Wi-Fi",       # or "Ethernet" or your network service name
    "127.0.0.1",   # proxy host
    8080           # proxy port
)
