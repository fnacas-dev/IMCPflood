import random
import threading
import time
from icmplib import ping, SocketAddressError

def generate_ipv4():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Simplificamos em uma única função que recebe o IP do alvo
def send_ping(id_thread, ip_alvo):
    print(f"[Thread {id_thread}] Starting pings to {ip_alvo}...")

    try:    
        resultado = ping(ip_alvo, count=1000, payload_size=120, interval=0.01, timeout=0.001, privileged=True)
        print(f"[Thread {id_thread}] Concluded. Packets send: {resultado.packets_sent} | Received: {resultado.packets_received}")
    except SocketAddressError:
        print(f"[Thread-{id_thread}] Address Error: {SocketAddressError}")
    except Exception as e:
        print(f"Unexpected error: {e}")


while True:
    ip = input("You want to generate a random IPv4, or set manually an IP? \nPress Y for random, or set manually the IP. \nHere's an example: 190.168.15.10\n> ").strip()

    if ip.lower() == 'y':
        host = generate_ipv4()
        print(f'Right! Random IPv4 generated: {host}. Starting in a few seconds...')
        break
    elif 7 <= len(ip) <= 15: # Garante um tamanho mínimo para um IP válido (ex: 1.1.1.1)
        host = ip
        print(f'Right! Manual IP set to: {host}. Starting in a few seconds...')
        break
    else:
        print('The manual set IP is invalid or empty. \nTry again.\n')

print('--- STARTED ---')

while True:
    try:
        threads_list = []
        rounds = 0
        
        for i in range(1, 5):
            t = threading.Thread(target=send_ping, args=(i, host))
            threads_list.append(t)
            t.start()

        for t in threads_list:
            t.join()

        rounds += 1
        print(f'Round {round} Concluded')
        time.sleep(0.5)
    except KeyboardInterrupt:
        print('\nBye son of a bitch.')
        break

print('--- CLOSING ---')
