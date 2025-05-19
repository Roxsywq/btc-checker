import os
import time
import random
import hashlib
import requests
import base58
import ecdsa
from colorama import init, Fore, Style

init(autoreset=True)

def banner():
    os.system('clear')
    print(Fore.YELLOW + Style.BRIGHT + """
    ╔═════════════════════════════════════════╗
    ║      BTC Wallet Checker [Termux UI]    ║
    ╚═════════════════════════════════════════╝
    """)

def generate_private_key():
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(64))

def private_to_public_key(private_key_hex):
    private_key_bytes = bytes.fromhex(private_key_hex)
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()
    return public_key

def public_key_to_address(public_key):
    sha256 = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160', sha256).digest()
    network_byte = b'\x00' + ripemd160
    checksum = hashlib.sha256(hashlib.sha256(network_byte).digest()).digest()[:4]
    address_bytes = network_byte + checksum
    return base58.b58encode(address_bytes).decode()

def check_balance(address):
    try:
        url = f'https://blockchain.info/q/addressbalance/{address}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            balance = int(response.text) / 1e8
            return balance
    except:
        pass
    return 0

def main_loop():
    count = 0
    while True:
        count += 1
        private = generate_private_key()
        public = private_to_public_key(private)
        address = public_key_to_address(public)
        balance = check_balance(address)

        if balance > 0:
            print(Fore.GREEN + f"[{count}] Bulundu! {address} -> {balance} BTC")
            with open('found.txt', 'a') as f:
                f.write(f'{private} | {address} | {balance} BTC\n')
        else:
            print(Fore.CYAN + f"[{count}] {address} | Bakiye: 0 BTC")

        time.sleep(0.5)

if __name__ == "__main__":
    banner()
    print(Fore.MAGENTA + "Başlatılıyor... CTRL+C ile durdurabilirsin.")
    time.sleep(2)
    main_loop()
