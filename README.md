
🩸 BlackNet Recon - Advanced Penetration Testing Toolkit
**BlackNet Recon** is a powerful, interactive, and centralized penetration testing framework designed for ethical hackers, bug bounty hunters, and security researchers. It bridges the gap between static cheat sheets and active exploitation by providing an interactive UI to orchestrate heavy-duty security tools effortlessly.

## 🌟 Key Features

* **🔀 Reverse Shell Generator:** Instantly generate payloads for 16+ languages (Bash, Python, PHP, Netcat, etc.) with automatic Base64, URL, and Hex encoding variants.
* **⚡ Live Command Executor:** Run system commands, network scans, and interact with your OS directly from the BlackNet interface without switching terminals.
* **🧬 Smart Hash Identifier:** Paste any hash to instantly identify its type, corresponding Hashcat mode (`-m`), and John the Ripper format.
* **🔐 Encode/Decode Utility:** Built-in fast conversions for Base64, URL, Hex, ROT13, HTML Entities, MD5, SHA1, and SHA256.
* **📋 Comprehensive Port Reference:** A built-in cheat sheet covering 50+ common ports, services, and associated attack vectors.
* **🛠️ Massive Tool Arsenal Reference:** Categorized execution guides and payloads for Nmap, SQLmap, Bettercap, Metasploit, Recon-ng, Hashcat, and more.

## 📸 Screenshots
<img width="1903" height="676" alt="feature of recon" src="https://github.com/user-attachments/assets/499f0c80-b48d-4f39-80f0-9d1e33b82070" />
<img width="1910" height="919" alt="blacknet" src="https://github.com/user-attachments/assets/194f7be2-8f14-4417-96df-21ff48670a23" />

## 🚀 Installation & Usage

BlackNet Recon comes with an automated installer script that handles virtual environments and dependencies (like the `rich` UI library) to ensure it runs flawlessly on any modern Linux distribution without breaking system packages.


### Quick Start

1. **Clone the repository:**

   ```git clone https://github.com/MRBLADESTALKER/blacknet-recon.git ```

### Prerequisites
* Python 3.x
* GitMake the launcher executable:
    Bash

    ```chmod +x blacknet.sh```

    Run the tool:
    Bash

    ```./blacknet.sh```

    Note: For tools that require raw socket access (like Nmap SYN scans or Bettercap ARP spoofing), run the toolkit with root privileges:
    Bash

    ```sudo ./blacknet.sh```

Important: Ensure both blacknet.sh and recon.py remain in the same directory.
⚠️ Disclaimer

LEGAL NOTICE: This toolkit is strictly for authorized penetration testing, CTF competitions, and educational research. Unauthorized use against systems you do not own or do not have explicit written permission to test is illegal and may result in criminal prosecution. The author assumes NO liability and is not responsible for any misuse or damage caused by this program.
📞 Contact & Support

Author: Mr. Blade Stalker

Telegram: @mrbladestalker35

Feel free to reach out for bug reports, feature requests, or collaboration opportunities! If you find this tool useful, don't forget to ⭐ star the repository!
