import os
from pathlib import Path
from platform import platform

def Searchimg(pathdbimagen):	
	if os.path.isfile(Path(pathdbimagen)):
		return Path(pathdbimagen)
	else:
		if 'Windows' in platform():
			return Path("C:\\DBGestionBot\\BotcndRazones\\Imgnofound.png")
		return Path("/mnt/images/Imgnofound.png")
