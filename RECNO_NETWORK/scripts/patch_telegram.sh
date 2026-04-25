#!/bin/bash
set -e

# This script is meant to be run in the GitHub Actions environment.
# It patches the official Telegram Android source code to inject our RECNO NETWORK
# branding, VLESS UI menu, and SOCKS5 proxy bridge.

echo "Starting Telegram patching process..."

TG_DIR="Telegram"

if [ ! -d "$TG_DIR" ]; then
    echo "Error: Telegram source directory not found!"
    exit 1
fi

# 1. Patch the App Name and Branding
echo "Patching branding to RECNO NETWORK..."
find "$TG_DIR" -name "strings.xml" -exec sed -i 's/>Telegram</>RECNO NETWORK</g' {} +
find "$TG_DIR" -name "strings.xml" -exec sed -i 's/"Telegram"/"RECNO NETWORK"/g' {} +

# 2. Copy Java Source Files
echo "Copying Java source files..."
mkdir -p "$TG_DIR/TMessagesProj/src/main/java/com/recno/network"
cp ../java_src/RecnoVlessUpdateService.java "$TG_DIR/TMessagesProj/src/main/java/com/recno/network/"
cp ../java_src/VlessProxyHelper.java "$TG_DIR/TMessagesProj/src/main/java/com/recno/network/"

# 3. Inject VLESS Proxy Option into ProxySettingsActivity
# Here we mock the injection by inserting our custom UI button definition
# into the proxy settings menu.
PROXY_ACTIVITY="$TG_DIR/TMessagesProj/src/main/java/org/telegram/ui/ProxySettingsActivity.java"

if [ -f "$PROXY_ACTIVITY" ]; then
    echo "Patching ProxySettingsActivity.java..."
    # Inserting a new row for VLESS proxy protocol
    sed -i '/import org.telegram.ui.ActionBar.BaseFragment;/a \
import com.recno.network.VlessProxyHelper;' "$PROXY_ACTIVITY"

    sed -i '/type == 0 || type == 1/i \
        // RECNO NETWORK VLESS INJECTION \
        if (type == 2) { \
            VlessProxyHelper.useVlessProxy(); \
        }' "$PROXY_ACTIVITY"
else
    echo "Warning: ProxySettingsActivity.java not found. (Expected in normal TG source)"
fi

# 4. Add Auto-update service call
# We need Telegram to run our vless manager update cycle in the background
# This injects a background service call into ApplicationLoader
APP_LOADER="$TG_DIR/TMessagesProj/src/main/java/org/telegram/messenger/ApplicationLoader.java"

if [ -f "$APP_LOADER" ]; then
    echo "Patching ApplicationLoader.java for background update service..."
    sed -i '/import android.app.Application;/a \
import com.recno.network.RecnoVlessUpdateService;\nimport android.content.Intent;' "$APP_LOADER"

    sed -i '/onCreate()/a \
        // RECNO NETWORK background VLESS update \
        startService(new Intent(this, RecnoVlessUpdateService.class));' "$APP_LOADER"
else
    echo "Warning: ApplicationLoader.java not found."
fi

# 5. Pre-compute and bundle working VLESS proxies
# ⚡ Bolt: Execute the manager script during the GitHub Actions build
# to generate the list of working proxies beforehand.
echo "Pre-computing working VLESS proxies..."
python3 ../scripts/vless_manager.py

# Bundle the result into the Telegram APK's assets
echo "Bundling working_vless.txt into APK assets..."
cp working_vless.txt "$TG_DIR/TMessagesProj/src/main/assets/"

echo "Patching completed successfully!"
