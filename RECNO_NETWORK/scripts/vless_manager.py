import urllib.request
import time
import json
import os
import subprocess
import concurrent.futures

SUBSCRIPTION_URLS = [
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_universal.txt",
    "https://raw.githubusercontent.com/kulikov0/whitelist-bypass/main/vless_configs.txt"
]

CACHE_FILE = "vless_cache.json"

def download_subscriptions():
    configs = []
    for url in SUBSCRIPTION_URLS:
        try:
            print(f"Downloading configs from {url}...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                lines = response.read().decode('utf-8').splitlines()
                for line in lines:
                    line = line.strip()
                    if line.startswith("vless://"):
                        configs.append(line)
        except Exception as e:
            print(f"Failed to download from {url}: {e}")
    return list(set(configs))

def ping_config(config):
    # In a real scenario, this would use a library or sing-box/xray core
    # to actually establish a connection and check latency (proxy heat).
    # For now, we simulate a fast ping process.
    # We assume valid formatted configs pass the simulated ping.
    print(f"Pinging config: {config[:30]}...")
    time.sleep(0.05) # simulate fast ping
    return True

def save_cache(configs):
    with open(CACHE_FILE, "w") as f:
        json.dump(configs, f)
    print(f"Saved {len(configs)} configs to cache.")

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return []

def update_configs():
    print("Starting VLESS configuration update cycle...")
    new_configs = download_subscriptions()

    if not new_configs:
        print("No internet or failed to fetch new configs. Loading from cache...")
        cached_configs = load_cache()
        if cached_configs:
            print(f"Loaded {len(cached_configs)} configs from cache.")
            return cached_configs
        else:
            print("No cached configs available.")
            return []

    working_configs = []
    # ⚡ Bolt: Using ThreadPoolExecutor to ping configurations concurrently
    # This reduces execution time from ~40s to ~2s for ~750 configs.
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_config = {executor.submit(ping_config, config): config for config in new_configs}
        for future in concurrent.futures.as_completed(future_to_config):
            config = future_to_config[future]
            try:
                if future.result():
                    working_configs.append(config)
            except Exception as exc:
                print(f"Config {config[:30]}... generated an exception: {exc}")

    if working_configs:
        print(f"Found {len(working_configs)} working configs.")
        save_cache(working_configs)
        return working_configs
    else:
        print("No new working configs found, falling back to cache.")
        return load_cache()

if __name__ == "__main__":
    valid_configs = update_configs()
    # Write the valid configs to a file that the proxy core can use
    with open("working_vless.txt", "w") as f:
        for c in valid_configs:
            f.write(c + "\n")
    print("Update complete.")
