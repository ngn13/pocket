#!/usr/bin/python3
#!/usr/bin/python

from shells import Shells
from sys import argv
from os import system
import argparse
from colorama import Style, Fore, init
init(autoreset=True)

class logger:
	def error(text):
		print(Fore.RED + Style.BRIGHT + "[-] " + Fore.RESET + Style.NORMAL + text)
	def info(text):
		print(Fore.BLUE + Style.BRIGHT + "[*] " + Fore.RESET + Style.NORMAL + text)
	def success(text):
		print(Fore.GREEN + Style.BRIGHT + "[+] " + Fore.RESET + Style.NORMAL + text)

class Pocket:
	def __init__(self):
		self.shells = Shells()

		self.parser = argparse.ArgumentParser(
                    prog = "pocket",
                    description = "Reverse shells in your pocket",
                    epilog = "Check https://github.com/ngn13/pocket for more information")
		self.parser.add_argument("IP", help="IP address of the attacker")
		self.parser.add_argument("port", help="Port of the attacker")   
		self.parser.add_argument("-s", "--shell", help="Name of the shell")      
		self.parser.add_argument("-m", "--msfvenom", help="Name of the msfvenom shell") 
		self.parser.add_argument("-l", "--listener", help="Name of the listener")
		self.parser.add_argument("-r", "--run", help="Run the listener", action='store_true')
		self.parser.add_argument("-e", "--encode", help="URL encode the shell", action='store_true')
		self.args = self.parser.parse_args()

	def encode(self, string):
		# from https://gist.github.com/Paradoxis/6336c2eaea20a591dd36bb1f5e227da2
		return "".join("%{0:0>2}".format(format(ord(char), "x")) for char in string)

	def list_keys(self, keys):
		strkeys = ""

		for key in keys:
			strkeys += key + (", " if list(keys).index(key) != len(keys)-1 else "")
		
		print(strkeys)

	def run(self):
		shell = self.shells.reverse["bash"]
		listener = self.shells.listener["nc"]

		if self.args.shell and self.args.msfvenom:
			logger.error("Use either msfvenom shells or normal shells")
			exit()

		if self.args.shell:
			try:
				shell = self.shells.reverse[self.args.shell]
			except:
				logger.error("Invalid shell, here is the list of shells that you can use:")
				self.list_keys(self.shells.reverse)
				exit()
		
		if self.args.listener: 
			try:
				listener = self.shells.listener[self.args.listener]
			except:
				logger.error("Invalid listener, here is the list of listeners that you can use:")
				self.list_keys(self.shells.listener)
				exit()
		
		if self.args.msfvenom:
			try:
				shell = self.shells.msfvenom[self.args.msfvenom]
			except:
				logger.error("Invalid msfvenom shell, here is the list of msfvenom shells that you can use:")
				self.list_keys(self.shells.msfvenom)
				exit()

		shell = shell.replace("[ip]", self.args.IP)
		shell = shell.replace("[port]", self.args.port)
		listener = listener.replace("[ip]", self.args.IP)
		listener = listener.replace("[port]", self.args.port)

		logger.success("Your shell is ready to go!")
		print(Fore.YELLOW + Style.BRIGHT + "Shell: " + Fore.RESET + Style.NORMAL + f"{shell if not self.args.encode else self.encode(shell)}")
		print(Fore.YELLOW + Style.BRIGHT + "Listener: " + Fore.RESET + Style.NORMAL + f"{listener}")

		if self.args.run:
			try:
				logger.info("Starting up the listener...")
				system(listener)
			except KeyboardInterrupt:
				print("[-] Abort.")
				exit()

if __name__ == "__main__":
	pocket = Pocket()
	pocket.run()