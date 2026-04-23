# RECNO NETWORK Architecture

Integrating a completely new proxy protocol (VLESS) into an existing native C++ network stack (tgnet) is highly complex. To ensure stability and fast performance, RECNO NETWORK uses a "Local Bridge" architecture.

## How It Works

1. **VlessManager (Python/Java)**
   - Downloads subscription lists (e.g., from `https://raw.githubusercontent.com/zieng2/wl/main/vless_universal.txt`).
   - Parses the `vless://` URLs.
   - Pings the servers to check for "heat" (latency/availability).
   - Saves the working configurations locally to a cache file.

2. **Core Integration (Proxy-Core)**
   - Instead of rewriting Telegram's C++ network layer, RECNO NETWORK bundles a proxy core (like Xray-core or sing-box).
   - The selected VLESS config is passed to the proxy core.
   - The proxy core establishes the VLESS connection to the remote server and opens a **local SOCKS5 port** on the device (e.g., `127.0.0.1:10808`).

3. **Telegram Native Client Patching**
   - The script `patch_telegram.sh` modifies the native Java/C++ code of Telegram.
   - It changes the UI branding to "RECNO NETWORK".
   - It injects a command into `ApplicationLoader` to start the VLESS update/connection background service on boot.
   - It tells Telegram to automatically connect to the local SOCKS5 port (`127.0.0.1:10808`), seamlessly bridging the official client through the VLESS connection.

This approach ensures that the client remains stable and compatible with all official Telegram updates, while providing the powerful anti-censorship features of VLESS.
