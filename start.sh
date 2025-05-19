#!/data/data/com.termux/files/usr/bin/bash

# Bağımlılıklar
echo "[*] Gerekli paketler yükleniyor..."
pkg update -y && pkg upgrade -y
pkg install python git -y
pip install requests ecdsa base58 colorama

# Script başlat
echo "[*] BTC Checker başlatılıyor..."
python btc_checker.py
