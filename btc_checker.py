import os
import time
import random
import hashlib
import requests
import base58
import ecdsa
import multiprocessing
from colorama import init, Fore, Style

init(autoreset=True)

# Configuration
MAX_WORKERS = multiprocessing.cpu_count() * 2  # Optimal worker count
API_URL = "https://blockchain.info/q/addressbalance/"
REQUEST_TIMEOUT = 15
BATCH_SIZE = 100  # Number of addresses to check before displaying progress

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(Fore.YELLOW + Style.BRIGHT + """
╔═════════════════════════════════════════╗
║      BTC Wallet Checker ROXSYWQ                ║
╚═════════════════════════════════════════╝
""")
    print(Fore.CYAN + f"Using {MAX_WORKERS} parallel workers")
    print(Fore.MAGENTA + "Press CTRL+C to stop\n")

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
        response = requests.get(f"{API_URL}{address}", timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            balance = int(response.text) / 1e8
            return balance
    except requests.RequestException:
        pass
    return 0

def worker(results_queue, count_queue):
    while True:
        private = generate_private_key()
        public = private_to_public_key(private)
        address = public_key_to_address(public)
        balance = check_balance(address)
        
        if balance > 0:
            results_queue.put((private, address, balance))
        count_queue.put(1)

def main():
    banner()
    
    # Create queues for communication
    results_queue = multiprocessing.Queue()
    count_queue = multiprocessing.Queue()
    
    # Start worker processes
    processes = []
    for _ in range(MAX_WORKERS):
        p = multiprocessing.Process(target=worker, args=(results_queue, count_queue))
        p.daemon = True
        p.start()
        processes.append(p)
    
    total_checked = 0
    last_print = time.time()
    
    try:
        while True:
            # Display progress periodically
            if time.time() - last_print >= 1.0:
                # Get count of checked addresses
                while not count_queue.empty():
                    total_checked += count_queue.get()
                
                print(Fore.CYAN + f"Checked: {total_checked:,} addresses | Speed: {total_checked / (time.time() - start_time):.1f} addr/sec", end='\r')
                last_print = time.time()
            
            # Check for found wallets
            while not results_queue.empty():
                private, address, balance = results_queue.get()
                print(Fore.GREEN + f"\n[FOUND] {address} -> {balance} BTC")
                with open('found.txt', 'a') as f:
                    f.write(f'{private} | {address} | {balance} BTC\n')
    
    except KeyboardInterrupt:
        print(Fore.RED + "\nStopping workers...")
        for p in processes:
            p.terminate()
        print(Fore.YELLOW + f"Total addresses checked: {total_checked:,}")

if __name__ == "__main__":
    start_time = time.time()
    main()
