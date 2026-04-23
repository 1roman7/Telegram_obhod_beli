# RECNO NETWORK - Custom Telegram Client

RECNO NETWORK is a custom build of the official Telegram Android client that integrates a built-in VLESS proxy manager to bypass network restrictions seamlessly.

## Features
- **Auto-Updating Proxies:** Fetches VLESS subscriptions every hour.
- **Offline Fallback:** Caches working proxies to maintain connection when updates fail.
- **Proxy Heat / Ping:** Automatically selects the fastest available proxy.
- **Native UI Integration:** Replaces branding and injects settings into the native Telegram Proxy UI.

## How to Build the APK Automatically

Since compiling the official Telegram client requires significant resources (Android Studio, NDK, C++ compilers), this repository uses **GitHub Actions** to automatically build your APK.

### Steps:
1. **Push this code to your own GitHub Repository:**
   Make sure you push this folder structure to a new repository on your GitHub account.
2. **Go to the "Actions" tab:**
   Click on the "Build RECNO NETWORK APK" workflow.
3. **Run Workflow:**
   Click "Run workflow". GitHub's servers will automatically download the official Telegram source code, apply our patches and proxy manager, and compile the APK.
4. **Download the APK:**
   Once the process is finished (it usually takes 30-60 minutes), download the artifact `RECNO_NETWORK_APK.zip` from the workflow summary page. Extract it to find your installable `.apk` file!
