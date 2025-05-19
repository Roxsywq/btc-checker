#!/data/data/com.termux/files/usr/bin/bash

echo -e "\033[1;33m[*] Updating packages...\033[0m"
pkg update -y && pkg upgrade -y

echo -e "\033[1;33m[*] Installing dependencies...\033[0m"
pkg install python git -y
pip install requests ecdsa base58 colorama

echo -e "\033[1;33m[*] Downloading BTC checker...\033[0m"
curl -O https://raw.githubusercontent.com/yourusername/btc_checker/main/btc_checker.py

echo -e "\033[1;33m[*] Setting permissions...\033[0m"
chmod +x btc_checker.py

echo -e "\n\033[1;32m[+] Installation complete!\033[0m"
echo -e "\033[1;36mRun the checker with: python btc_checker.py\033[0m"
