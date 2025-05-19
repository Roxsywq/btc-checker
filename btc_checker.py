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
STATS_INTERVAL = 1  # Seconds between stats updates
SAVE_FILE = "found.txt"

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(Fore.YELLOW + Style.BRIGHT + """
╔═════════════════════════════════════════╗
║   BTC Wallet Scanner [Optimized v2.0]   ║
╚═════════════════════════════════════════╝
""")
    print(Fore.CYAN + f"Workers: {MAX_WORKERS} | Timeout: {REQUEST_TIMEOUT}s")
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
            return int(response.text) / 1e8
    except requests.RequestException:
        time.sleep(1)  # Brief pause if API fails
    return 0

def save_wallet(private, address, balance):
    with open(SAVE_FILE, 'a') as f:
        f.write(f"{private} | {address} | {balance} BTC\n")
    print(Fore.GREEN + f"[SAVED] {address} | {balance} BTC")

def worker(results_queue, count_queue):
    while True:
        try:
            private = generate_private_key()
            public = private_to_public_key(private)
            address = public_key_to_address(public)
            balance = check_balance(address)
            
            if balance > 0:
                results_queue.put(('FOUND', private, address, balance))
            count_queue.put(1)
        except Exception as e:
            print(Fore.RED + f"Worker error: {str(e)}")
            time.sleep(1)

def display_stats(start_time, total_checked, found_count):
    elapsed = time.time() - start_time
    speed = total_checked / elapsed if elapsed > 0 else 0
    stats = (Fore.CYAN + 
             f"Checked: {total_checked:,} | " +
             f"Speed: {speed:,.1f} addr/sec | " +
             f"Found: {found_count} | " +
             f"Running: {time.strftime('%H:%M:%S', time.gmtime(elapsed))}")
    print(stats, end='\r')

def main():
    banner()
    
    # Initialize found.txt if it doesn't exist
    if not os.path.exists(SAVE_FILE):
        open(SAVE_FILE, 'w').close()
    
    # Create queues for communication
    manager = multiprocessing.Manager()
    results_queue = manager.Queue()
    count_queue = manager.Queue()
    
    # Start worker processes
    processes = []
    for _ in range(MAX_WORKERS):
        p = multiprocessing.Process(target=worker, args=(results_queue, count_queue))
        p.daemon = True
        p.start()
        processes.append(p)
    
    start_time = time.time()
    last_stats = start_time
    total_checked = 0
    found_count = 0
    
    try:
        while True:
            now = time.time()
            
            # Update counters
            while not count_queue.empty():
                total_checked += count_queue.get()
            
            # Display stats every second
            if now - last_stats >= STATS_INTERVAL:
                display_stats(start_time, total_checked, found_count)
                last_stats = now
            
            # Process found wallets
            while not results_queue.empty():
                msg, private, address, balance = results_queue.get()
                if msg == 'FOUND':
                    found_count += 1
                    print(Fore.GREEN + f"\n[FOUND] {address} | Balance: {balance} BTC")
                    save_wallet(private, address, balance)
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print(Fore.RED + "\nStopping workers...")
        for p in processes:
            p.terminate()
        
        # Final stats
        elapsed = time.time() - start_time
        print(Fore.YELLOW + "\nFinal Statistics:")
        print(Fore.CYAN + f"Total addresses checked: {total_checked:,}")
        print(Fore.CYAN + f"Total wallets found: {found_count}")
        print(Fore.CYAN + f"Average speed: {total_checked/elapsed:,.1f} addresses/sec")
        print(Fore.CYAN + f"Run time: {time.strftime('%H:%M:%S', time.gmtime(elapsed))}")
        print(Fore.GREEN + f"\nFound wallets saved to: {SAVE_FILE}")

if __name__ == "__main__":
    main()
