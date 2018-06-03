# xmr-miner

xmr-miner is written in python3 and C. I have published it for Windows and Debian amd64 based systems.
Remote configuration file (eg. pastebin raw file) as input argument is implemented.
Maybe in the future, I will implement x86 and ARM (eg. Raspberry-Pi) versions (recompiling the C library).
Even in the future, maybe I will rewrite it entirely in C++ for speed improvement.

WARNING: C code is published separately in my other repo https://github.com/menekevin/cryptonight

## Command Line Interface
```
xmr-miner [-h] [-f FILE] [-o URL] [-u USERNAME] [-p PASSWORD] [-v VARIANT] [-t THREADS] [-d]

optional arguments:
	-h, --help            				show this help message and exit
	-f FILE, --file FILE  				remote configuration file - eg. https://pastebin.com/raw/TeXtFiLe (required, if not url given)
	-o URL, --url URL     				mining pool - eg: stratum+tcp://mining.pool.com:3333 (required, if not file given)
	-u USERNAME, --username USERNAME	username or wallet address (required, if not file given)
	-p PASSWORD, --password PASSWORD	password (optional)
	-v VARIANT, --variant VARIANT		pow variant 0 (original) or 1 (April 2018 fork) (default = 1)
	-t THREADS, --threads THREADS		mining threads (default = 1)
	-d, --debug

remote configuration file formatting:
	[example with line numbers]:
	1	URL								mining pool - eg: stratum+tcp://mining.pool.com:3333 (required)
	2	USERNAME						username or wallet address (required)
	3	PASSWORD						password (optional)
	4	VARIANT							pow variant 0 (original) or 1 (April 2018 fork) (default = 1)
	5	THREADS							mining threads (default = 1)	
```
## License
The python code is MIT.
