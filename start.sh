#!/data/data/com.termux/files/usr/bin/bash

echo "[*] Installing required packages..."
pkg update -y && pkg upgrade -y
pkg install python git -y
pip install requests ecdsa base58 colorama

echo "[*] Downloading optimized BTC checker..."
curl -O https://raw.githubusercontent.com/yourusername/btc_checker/main/btc_checker.py

echo "[*] Making scripts executable..."
chmod +x btc_checker.py

echo -e "\n[*] Setup complete!"
echo -e "Run the checker with: python btc_checker.py\n"
