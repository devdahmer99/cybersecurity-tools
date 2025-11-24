#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        OSINT FRAMEWORK - ADVANCED TOOLKIT                      ║
║                              Created by devdahmer99                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import re
import json
import time
import socket
import requests
import dns.resolver
import whois
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, quote_plus
from datetime import datetime
from colorama import Fore, Back, Style, init
from bs4 import BeautifulSoup
import argparse

# Inicializa colorama para Windows
init(autoreset=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÕES GLOBAIS
# ══════════════════════════════════════════════════════════════════════════════

VERSION = "1.0.0"
AUTHOR = "devdahmer99"
TOOL_NAME = "DAHMER OSINT"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

# ══════════════════════════════════════════════════════════════════════════════
# CORES E ESTILOS
# ══════════════════════════════════════════════════════════════════════════════

class Colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT
    DIM = Style.DIM

# ══════════════════════════════════════════════════════════════════════════════
# BANNER E INTERFACE
# ══════════════════════════════════════════════════════════════════════════════

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Colors.GREEN}                                                                              
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                        {Colors.CYAN}██████╗  █████╗ ██╗  ██╗███╗   ███╗███████╗██████╗ 
        ⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀                                        {Colors.CYAN}██╔══██╗██╔══██╗██║  ██║████╗ ████║██╔════╝██╔══██╗
        ⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀                                        {Colors.CYAN}██║  ██║███████║███████║██╔████╔██║█████╗  ██████╔╝
        ⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀                                        {Colors.CYAN}██║  ██║██╔══██║██╔══██║██║╚██╔╝██║██╔══╝  ██╔══██╗
        ⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⡿⠋⠉⠛⠛⠛⠛⠉⠙⢿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀                                        {Colors.CYAN}██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
        ⠀⠀⣼⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣧⠀⠀                                        {Colors.CYAN}╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
        ⠀⠀⣿⣿⣿⣿⣿⣿⠏⠀⢠⣤⣤⣤⣤⣤⣤⡄⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⠀⠀       
        ⠀⠀⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⠀⠀            {Colors.RED}█▀█ █▀ █ █▄░█ ▀█▀   ▀█▀ █▀█ █▀█ █░░ █▄▀ █ ▀█▀{Colors.RESET}
        ⠀⠀⢿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡿⠀⠀            {Colors.RED}█▄█ ▄█ █ █░▀█ ░█░   ░█░ █▄█ █▄█ █▄▄ █░█ █ ░█░{Colors.RESET}
        ⠀⠀⠸⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⠇⠀⠀
        ⠀⠀⠀⢻⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⡟⠀⠀⠀       {Colors.YELLOW}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{Colors.RESET}
        ⠀⠀⠀⠀⠻⣿⣿⣿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⠟⠀⠀⠀⠀       {Colors.WHITE}  Advanced OSINT Framework for Penetration Testing{Colors.RESET}
        ⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀       {Colors.WHITE}  Red Team Operations & Intelligence Gathering{Colors.RESET}
        ⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠀⠀⠀       {Colors.YELLOW}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{Colors.RESET}
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠛⠛⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                                                    {Colors.DIM}Created by {Colors.CYAN}{AUTHOR}{Colors.RESET}
                                                                    {Colors.DIM}Version: {Colors.GREEN}{VERSION}{Colors.RESET}
    """
    print(banner)

def print_separator():
    print(f"{Colors.YELLOW}{'═' * 90}{Colors.RESET}")

def print_module_header(module_name):
    clear_screen()
    print(f"""
{Colors.CYAN}╔{'═' * 88}╗
║{Colors.WHITE}{Colors.BOLD} {module_name.center(86)} {Colors.CYAN}║
╠{'═' * 88}╣
║{Colors.GREEN} {'DAHMER OSINT FRAMEWORK'.center(86)} {Colors.CYAN}║
║{Colors.DIM}{Colors.WHITE} {f'Developer: {AUTHOR} | Version: {VERSION}'.center(86)} {Colors.CYAN}║
╚{'═' * 88}╝{Colors.RESET}
""")

def print_status(status, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if status == "info":
        print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} [{Colors.BLUE}INFO{Colors.RESET}] {message}")
    elif status == "success":
        print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} [{Colors.GREEN}SUCCESS{Colors.RESET}] {message}")
    elif status == "warning":
        print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} [{Colors.YELLOW}WARNING{Colors.RESET}] {message}")
    elif status == "error":
        print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} [{Colors.RED}ERROR{Colors.RESET}] {message}")
    elif status == "found":
        print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} [{Colors.GREEN}FOUND{Colors.RESET}] {message}")
    elif status == "not_found":
        print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} [{Colors.RED}NOT FOUND{Colors.RESET}] {message}")

def print_menu():
    print(f"""
{Colors.CYAN}┌──────────────────────────────────────────────────────────────────────────────────────────┐
│{Colors.WHITE}{Colors.BOLD}                                    MAIN MENU                                            {Colors.CYAN}│
├──────────────────────────────────────────────────────────────────────────────────────────┤{Colors.RESET}
│                                                                                          │
│   {Colors.GREEN}[1]{Colors.RESET} 📧  Email Harvester         {Colors.DIM}- Coleta emails de domínios{Colors.RESET}                       │
│   {Colors.GREEN}[2]{Colors.RESET} 🌐  Subdomain Enumerator    {Colors.DIM}- Descobre subdomínios{Colors.RESET}                            │
│   {Colors.GREEN}[3]{Colors.RESET} 🔍  WHOIS Lookup            {Colors.DIM}- Informações de registro de domínio{Colors.RESET}              │
│   {Colors.GREEN}[4]{Colors.RESET} 👤  Username OSINT          {Colors.DIM}- Busca username em redes sociais{Colors.RESET}                 │
│   {Colors.GREEN}[5]{Colors.RESET} 📄  Metadata Extractor      {Colors.DIM}- Extrai metadados de arquivos{Colors.RESET}                    │
│   {Colors.GREEN}[6]{Colors.RESET} 🎯  Google Dorker           {Colors.DIM}- Automatiza Google Dorks{Colors.RESET}                         │
│   {Colors.GREEN}[7]{Colors.RESET} 📍  IP Geolocation          {Colors.DIM}- Geolocalização e info de IPs{Colors.RESET}                    │
│   {Colors.GREEN}[8]{Colors.RESET} 🔗  Full Recon              {Colors.DIM}- Reconhecimento completo de alvo{Colors.RESET}                 │
│                                                                                          │
│   {Colors.RED}[0]{Colors.RESET} 🚪  Exit                     {Colors.DIM}- Sair do framework{Colors.RESET}                               │
│                                                                                          │
{Colors.CYAN}└──────────────────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}
""")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 1: EMAIL HARVESTER
# ══════════════════════════════════════════════════════════════════════════════

class EmailHarvester:
    def __init__(self, domain):
        self.domain = domain
        self.emails = set()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def search_bing(self):
        """Busca emails usando Bing"""
        print_status("info", f"Buscando emails no Bing para {self.domain}...")
        try:
            for page in range(0, 50, 10):
                url = f"https://www.bing.com/search?q=%40{self.domain}&first={page}"
                response = self.session.get(url, timeout=10)
                emails = re.findall(r'[\w\.-]+@' + re.escape(self.domain), response.text)
                for email in emails:
                    self.emails.add(email.lower())
                time.sleep(1)
        except Exception as e:
            print_status("error", f"Erro no Bing: {str(e)}")
    
    def search_duckduckgo(self):
        """Busca emails usando DuckDuckGo"""
        print_status("info", f"Buscando emails no DuckDuckGo para {self.domain}...")
        try:
            url = f"https://duckduckgo.com/html/?q=%40{self.domain}"
            response = self.session.get(url, timeout=10)
            emails = re.findall(r'[\w\.-]+@' + re.escape(self.domain), response.text)
            for email in emails:
                self.emails.add(email.lower())
        except Exception as e:
            print_status("error", f"Erro no DuckDuckGo: {str(e)}")
    
    def search_pgp_servers(self):
        """Busca emails em servidores PGP"""
        print_status("info", f"Buscando emails em servidores PGP...")
        pgp_servers = [
            f"https://keyserver.ubuntu.com/pks/lookup?search={self.domain}&op=index",
        ]
        for server in pgp_servers:
            try:
                response = self.session.get(server, timeout=10)
                emails = re.findall(r'[\w\.-]+@[\w\.-]+\.' + re.escape(self.domain.split('.')[-1]), response.text)
                for email in emails:
                    if self.domain in email:
                        self.emails.add(email.lower())
            except:
                pass
    
    def generate_common_emails(self):
        """Gera emails comuns baseados em padrões"""
        print_status("info", "Gerando emails baseados em padrões comuns...")
        common_prefixes = [
            'admin', 'info', 'contact', 'support', 'sales', 'marketing',
            'hr', 'careers', 'jobs', 'webmaster', 'postmaster', 'abuse',
            'security', 'noc', 'helpdesk', 'billing', 'accounts', 'press',
            'media', 'investor', 'legal', 'privacy', 'compliance', 'ceo',
            'cto', 'cfo', 'coo', 'office', 'reception', 'hello', 'hi',
            'team', 'feedback', 'enquiries', 'inquiries', 'general'
        ]
        for prefix in common_prefixes:
            self.emails.add(f"{prefix}@{self.domain}")
    
    def verify_email(self, email):
        """Verifica se o email existe via MX lookup"""
        try:
            domain = email.split('@')[1]
            records = dns.resolver.resolve(domain, 'MX')
            return True
        except:
            return False
    
    def run(self):
        """Executa todas as buscas"""
        print_module_header("📧 EMAIL HARVESTER")
        print(f"\n{Colors.CYAN}[*] Target Domain: {Colors.WHITE}{self.domain}{Colors.RESET}\n")
        print_separator()
        
        self.search_bing()
        self.search_duckduckgo()
        self.search_pgp_servers()
        self.generate_common_emails()
        
        print_separator()
        print(f"\n{Colors.GREEN}[+] Emails encontrados: {len(self.emails)}{Colors.RESET}\n")
        
        for email in sorted(self.emails):
            print(f"    {Colors.CYAN}→{Colors.RESET} {email}")
        
        # Salvar resultados
        self.save_results()
        return self.emails
    
    def save_results(self):
        """Salva resultados em arquivo"""
        filename = f"emails_{self.domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            for email in sorted(self.emails):
                f.write(f"{email}\n")
        print_status("success", f"Resultados salvos em {filename}")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 2: SUBDOMAIN ENUMERATOR
# ══════════════════════════════════════════════════════════════════════════════

class SubdomainEnumerator:
    def __init__(self, domain):
        self.domain = domain
        self.subdomains = set()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
        # Wordlist de subdomínios comuns
        self.wordlist = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'ns2',
            'ns3', 'ns4', 'dns', 'dns1', 'dns2', 'mx', 'mx1', 'mx2', 'remote', 'blog',
            'webdisk', 'server', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'api',
            'dev', 'development', 'stage', 'staging', 'test', 'testing', 'demo', 'beta',
            'alpha', 'portal', 'admin', 'administrator', 'secure', 'vpn', 'gateway',
            'intranet', 'extranet', 'backup', 'bk', 'db', 'database', 'sql', 'mysql',
            'oracle', 'postgres', 'mongodb', 'redis', 'cache', 'cdn', 'static', 'assets',
            'media', 'img', 'images', 'video', 'download', 'downloads', 'upload', 'uploads',
            'shop', 'store', 'ecommerce', 'cart', 'pay', 'payment', 'checkout', 'order',
            'app', 'apps', 'mobile', 'android', 'ios', 'cloud', 'aws', 'azure', 'gcp',
            'jenkins', 'gitlab', 'github', 'bitbucket', 'jira', 'confluence', 'wiki',
            'docs', 'documentation', 'help', 'support', 'ticket', 'tickets', 'forum',
            'community', 'status', 'monitor', 'grafana', 'kibana', 'elastic', 'log',
            'logs', 'analytics', 'track', 'tracking', 'crm', 'erp', 'hr', 'finance',
            'internal', 'private', 'public', 'proxy', 'sso', 'auth', 'login', 'signin',
            'register', 'signup', 'account', 'accounts', 'profile', 'user', 'users',
            'customer', 'customers', 'client', 'clients', 'partner', 'partners', 'vendor',
            'service', 'services', 'soap', 'rest', 'graphql', 'ws', 'websocket', 'socket'
        ]
    
    def dns_bruteforce(self):
        """Bruteforce de subdomínios via DNS"""
        print_status("info", "Iniciando DNS bruteforce...")
        
        def check_subdomain(subdomain):
            full_domain = f"{subdomain}.{self.domain}"
            try:
                dns.resolver.resolve(full_domain, 'A')
                return full_domain
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(check_subdomain, sub): sub for sub in self.wordlist}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.subdomains.add(result)
                    print_status("found", result)
    
    def crtsh_search(self):
        """Busca subdomínios no crt.sh (Certificate Transparency)"""
        print_status("info", "Buscando em Certificate Transparency (crt.sh)...")
        try:
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    name = entry.get('name_value', '')
                    for sub in name.split('\n'):
                        sub = sub.strip().lower()
                        if sub.endswith(self.domain) and '*' not in sub:
                            self.subdomains.add(sub)
                            print_status("found", sub)
        except Exception as e:
            print_status("error", f"Erro no crt.sh: {str(e)}")
    
    def hackertarget_search(self):
        """Busca subdomínios via HackerTarget"""
        print_status("info", "Buscando via HackerTarget...")
        try:
            url = f"https://api.hackertarget.com/hostsearch/?q={self.domain}"
            response = self.session.get(url, timeout=15)
            if response.status_code == 200 and "error" not in response.text.lower():
                for line in response.text.split('\n'):
                    if ',' in line:
                        subdomain = line.split(',')[0].strip()
                        if subdomain:
                            self.subdomains.add(subdomain)
                            print_status("found", subdomain)
        except Exception as e:
            print_status("error", f"Erro no HackerTarget: {str(e)}")
    
    def resolve_subdomain(self, subdomain):
        """Resolve IP de um subdomínio"""
        try:
            answers = dns.resolver.resolve(subdomain, 'A')
            ips = [rdata.address for rdata in answers]
            return ips
        except:
            return []
    
    def run(self):
        """Executa todas as buscas"""
        print_module_header("🌐 SUBDOMAIN ENUMERATOR")
        print(f"\n{Colors.CYAN}[*] Target Domain: {Colors.WHITE}{self.domain}{Colors.RESET}\n")
        print_separator()
        
        self.crtsh_search()
        self.hackertarget_search()
        self.dns_bruteforce()
        
        print_separator()
        print(f"\n{Colors.GREEN}[+] Subdomínios encontrados: {len(self.subdomains)}{Colors.RESET}\n")
        
        # Mostrar resultados com IPs
        print(f"{'Subdomain':<50} {'IP Address':<20}")
        print(f"{'-'*50} {'-'*20}")
        
        for subdomain in sorted(self.subdomains):
            ips = self.resolve_subdomain(subdomain)
            ip_str = ', '.join(ips) if ips else 'N/A'
            print(f"{Colors.CYAN}{subdomain:<50}{Colors.RESET} {ip_str:<20}")
        
        # Salvar resultados
        self.save_results()
        return self.subdomains
    
    def save_results(self):
        """Salva resultados em arquivo"""
        filename = f"subdomains_{self.domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            for subdomain in sorted(self.subdomains):
                f.write(f"{subdomain}\n")
        print_status("success", f"Resultados salvos em {filename}")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 3: WHOIS LOOKUP
# ══════════════════════════════════════════════════════════════════════════════

class WhoisLookup:
    def __init__(self, target):
        self.target = target
        self.info = {}
    
    def lookup(self):
        """Realiza consulta WHOIS"""
        print_module_header("🔍 WHOIS LOOKUP")
        print(f"\n{Colors.CYAN}[*] Target: {Colors.WHITE}{self.target}{Colors.RESET}\n")
        print_separator()
        
        try:
            print_status("info", f"Consultando WHOIS para {self.target}...")
            w = whois.whois(self.target)
            
            self.info = {
                'Domain Name': w.domain_name,
                'Registrar': w.registrar,
                'WHOIS Server': w.whois_server,
                'Creation Date': w.creation_date,
                'Expiration Date': w.expiration_date,
                'Updated Date': w.updated_date,
                'Name Servers': w.name_servers,
                'Status': w.status,
                'Emails': w.emails,
                'Organization': w.org,
                'Address': w.address,
                'City': w.city,
                'State': w.state,
                'Country': w.country,
                'Postal Code': w.zipcode,
                'DNSSEC': w.dnssec,
            }
            
            print_separator()
            print(f"\n{Colors.GREEN}[+] WHOIS Information:{Colors.RESET}\n")
            
            for key, value in self.info.items():
                if value:
                    if isinstance(value, list):
                        value = ', '.join(str(v) for v in value)
                    print(f"    {Colors.CYAN}{key}:{Colors.RESET} {value}")
            
            self.save_results()
            
        except Exception as e:
            print_status("error", f"Erro na consulta WHOIS: {str(e)}")
        
        return self.info
    
    def save_results(self):
        """Salva resultados em arquivo"""
        filename = f"whois_{self.target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.info, f, indent=4, default=str)
        print_status("success", f"Resultados salvos em {filename}")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 4: USERNAME OSINT
# ══════════════════════════════════════════════════════════════════════════════

class UsernameOSINT:
    def __init__(self, username):
        self.username = username
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
        # Sites para verificar
        self.sites = {
            'GitHub': f'https://github.com/{username}',
            'Twitter/X': f'https://twitter.com/{username}',
            'Instagram': f'https://instagram.com/{username}',
            'Facebook': f'https://facebook.com/{username}',
            'LinkedIn': f'https://linkedin.com/in/{username}',
            'Reddit': f'https://reddit.com/user/{username}',
            'YouTube': f'https://youtube.com/@{username}',
            'TikTok': f'https://tiktok.com/@{username}',
            'Pinterest': f'https://pinterest.com/{username}',
            'Tumblr': f'https://{username}.tumblr.com',
            'Medium': f'https://medium.com/@{username}',
            'Dev.to': f'https://dev.to/{username}',
            'Twitch': f'https://twitch.tv/{username}',
            'Steam': f'https://steamcommunity.com/id/{username}',
            'Spotify': f'https://open.spotify.com/user/{username}',
            'SoundCloud': f'https://soundcloud.com/{username}',
            'Flickr': f'https://flickr.com/people/{username}',
            'Vimeo': f'https://vimeo.com/{username}',
            'Dribbble': f'https://dribbble.com/{username}',
            'Behance': f'https://behance.net/{username}',
            'GitLab': f'https://gitlab.com/{username}',
            'Bitbucket': f'https://bitbucket.org/{username}',
            'StackOverflow': f'https://stackoverflow.com/users/{username}',
            'HackerNews': f'https://news.ycombinator.com/user?id={username}',
            'Keybase': f'https://keybase.io/{username}',
            'Telegram': f'https://t.me/{username}',
            'Discord': f'https://discord.com/users/{username}',
            'Slack': f'https://{username}.slack.com',
            'Patreon': f'https://patreon.com/{username}',
            'Substack': f'https://{username}.substack.com',
            'ProductHunt': f'https://producthunt.com/@{username}',
            'AngelList': f'https://angel.co/u/{username}',
            'Crunchbase': f'https://crunchbase.com/person/{username}',
            'About.me': f'https://about.me/{username}',
            'Gravatar': f'https://gravatar.com/{username}',
            'Disqus': f'https://disqus.com/by/{username}',
            'Slideshare': f'https://slideshare.net/{username}',
            'Scribd': f'https://scribd.com/{username}',
            'Goodreads': f'https://goodreads.com/{username}',
            'Last.fm': f'https://last.fm/user/{username}',
            'Myspace': f'https://myspace.com/{username}',
            'VK': f'https://vk.com/{username}',
            'OK.ru': f'https://ok.ru/{username}',
            'Weibo': f'https://weibo.com/{username}',
            'Zhihu': f'https://zhihu.com/people/{username}',
            'HackerOne': f'https://hackerone.com/{username}',
            'BugCrowd': f'https://bugcrowd.com/{username}',
            'TryHackMe': f'https://tryhackme.com/p/{username}',
            'HackTheBox': f'https://app.hackthebox.com/profile/{username}',
            'LeetCode': f'https://leetcode.com/{username}',
            'CodeWars': f'https://codewars.com/users/{username}',
            'Kaggle': f'https://kaggle.com/{username}',
            'Replit': f'https://replit.com/@{username}',
            'CodePen': f'https://codepen.io/{username}',
            'JSFiddle': f'https://jsfiddle.net/user/{username}',
            'Pastebin': f'https://pastebin.com/u/{username}',
            'Imgur': f'https://imgur.com/user/{username}',
            '500px': f'https://500px.com/{username}',
            'DeviantArt': f'https://deviantart.com/{username}',
            'ArtStation': f'https://artstation.com/{username}',
            'Fiverr': f'https://fiverr.com/{username}',
            'Upwork': f'https://upwork.com/freelancers/{username}',
            'Freelancer': f'https://freelancer.com/u/{username}',
            'Etsy': f'https://etsy.com/shop/{username}',
            'eBay': f'https://ebay.com/usr/{username}',
            'Amazon': f'https://amazon.com/gp/profile/{username}',
            'Yelp': f'https://yelp.com/user_details?userid={username}',
            'TripAdvisor': f'https://tripadvisor.com/members/{username}',
            'Airbnb': f'https://airbnb.com/users/show/{username}',
            'Couchsurfing': f'https://couchsurfing.com/people/{username}',
            'Strava': f'https://strava.com/athletes/{username}',
            'Duolingo': f'https://duolingo.com/profile/{username}',
            'Chess.com': f'https://chess.com/member/{username}',
            'Lichess': f'https://lichess.org/@/{username}',
            'Xbox': f'https://xboxgamertag.com/search/{username}',
            'PlayStation': f'https://psnprofiles.com/{username}',
            'Nintendo': f'https://nintendo.com/profile/{username}',
            'Roblox': f'https://roblox.com/users/profile?username={username}',
            'Minecraft': f'https://namemc.com/profile/{username}',
            'Fortnite': f'https://fortnitetracker.com/profile/all/{username}',
            'Apex': f'https://apex.tracker.gg/profile/apex/origin/{username}',
            'Valorant': f'https://tracker.gg/valorant/profile/riot/{username}',
            'League': f'https://op.gg/summoner/userName={username}',
            'Dota2': f'https://dotabuff.com/players/{username}',
            'CSGO': f'https://csgostats.gg/player/{username}',
            'Letterboxd': f'https://letterboxd.com/{username}',
            'Trakt': f'https://trakt.tv/users/{username}',
            'MAL': f'https://myanimelist.net/profile/{username}',
            'AniList': f'https://anilist.co/user/{username}',
            'Wattpad': f'https://wattpad.com/user/{username}',
            'Fanfiction': f'https://fanfiction.net/~{username}',
            'AO3': f'https://archiveofourown.org/users/{username}',
            'Quora': f'https://quora.com/profile/{username}',
            'Ask.fm': f'https://ask.fm/{username}',
            'Mastodon': f'https://mastodon.social/@{username}',
            'Threads': f'https://threads.net/@{username}',
            'Bluesky': f'https://bsky.app/profile/{username}.bsky.social',
        }
    
    def check_site(self, site_name, url):
        """Verifica se o username existe em um site"""
        try:
            response = self.session.get(url, timeout=10, allow_redirects=True)
            
            # Verificação básica de existência
            if response.status_code == 200:
                # Verificações adicionais para evitar falsos positivos
                if 'not found' not in response.text.lower() and \
                   'doesn\'t exist' not in response.text.lower() and \
                   'page not found' not in response.text.lower() and \
                   '404' not in response.text[:1000].lower():
                    return (site_name, url, True)
            return (site_name, url, False)
        except:
            return (site_name, url, None)
    
    def run(self):
        """Executa busca em todos os sites"""
        print_module_header("👤 USERNAME OSINT")
        print(f"\n{Colors.CYAN}[*] Target Username: {Colors.WHITE}{self.username}{Colors.RESET}\n")
        print_separator()
        
        print_status("info", f"Buscando '{self.username}' em {len(self.sites)} plataformas...")
        print()
        
        found_count = 0
        
        with ThreadPoolExecutor(max_workers=30) as executor:
            futures = {executor.submit(self.check_site, name, url): name 
                      for name, url in self.sites.items()}
            
            for future in as_completed(futures):
                site_name, url, exists = future.result()
                
                if exists is True:
                    self.results[site_name] = {'url': url, 'status': 'found'}
                    print_status("found", f"{site_name}: {url}")
                    found_count += 1
                elif exists is False:
                    self.results[site_name] = {'url': url, 'status': 'not_found'}
                else:
                    self.results[site_name] = {'url': url, 'status': 'error'}
        
        print_separator()
        print(f"\n{Colors.GREEN}[+] Perfis encontrados: {found_count}/{len(self.sites)}{Colors.RESET}\n")
        
        self.save_results()
        return self.results
    
    def save_results(self):
        """Salva resultados em arquivo"""
        filename = f"username_{self.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        print_status("success", f"Resultados salvos em {filename}")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 5: METADATA EXTRACTOR
# ══════════════════════════════════════════════════════════════════════════════

class MetadataExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.metadata = {}
    
    def extract_pdf_metadata(self):
        """Extrai metadados de PDF"""
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(self.file_path)
            info = reader.metadata
            if info:
                self.metadata = {
                    'Title': info.get('/Title', 'N/A'),
                    'Author': info.get('/Author', 'N/A'),
                    'Creator': info.get('/Creator', 'N/A'),
                    'Producer': info.get('/Producer', 'N/A'),
                    'Creation Date': info.get('/CreationDate', 'N/A'),
                    'Modification Date': info.get('/ModDate', 'N/A'),
                    'Pages': len(reader.pages),
                }
        except ImportError:
            print_status("error", "PyPDF2 não instalado. Execute: pip install PyPDF2")
        except Exception as e:
            print_status("error", f"Erro ao extrair PDF: {str(e)}")
    
    def extract_image_metadata(self):
        """Extrai metadados de imagem (EXIF)"""
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            
            image = Image.open(self.file_path)
            exif_data = image._getexif()
            
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    self.metadata[tag] = str(value)
            
            self.metadata['Format'] = image.format
            self.metadata['Mode'] = image.mode
            self.metadata['Size'] = f"{image.size[0]}x{image.size[1]}"
            
        except ImportError:
            print_status("error", "Pillow não instalado. Execute: pip install Pillow")
        except Exception as e:
            print_status("error", f"Erro ao extrair imagem: {str(e)}")
    
    def extract_docx_metadata(self):
        """Extrai metadados de DOCX"""
        try:
            from docx import Document
            doc = Document(self.file_path)
            props = doc.core_properties
            
            self.metadata = {
                'Author': props.author or 'N/A',
                'Title': props.title or 'N/A',
                'Subject': props.subject or 'N/A',
                'Keywords': props.keywords or 'N/A',
                'Created': str(props.created) if props.created else 'N/A',
                'Modified': str(props.modified) if props.modified else 'N/A',
                'Last Modified By': props.last_modified_by or 'N/A',
                'Revision': props.revision or 'N/A',
                'Category': props.category or 'N/A',
                'Comments': props.comments or 'N/A',
            }
        except ImportError:
            print_status("error", "python-docx não instalado. Execute: pip install python-docx")
        except Exception as e:
            print_status("error", f"Erro ao extrair DOCX: {str(e)}")
    
    def run(self):
        """Executa extração de metadados"""
        print_module_header("📄 METADATA EXTRACTOR")
        print(f"\n{Colors.CYAN}[*] Target File: {Colors.WHITE}{self.file_path}{Colors.RESET}\n")
        print_separator()
        
        if not os.path.exists(self.file_path):
            print_status("error", "Arquivo não encontrado!")
            return {}
        
        file_ext = os.path.splitext(self.file_path)[1].lower()
        
        # Informações básicas do arquivo
        stat = os.stat(self.file_path)
        self.metadata['File Name'] = os.path.basename(self.file_path)
        self.metadata['File Size'] = f"{stat.st_size} bytes"
        self.metadata['Created'] = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        self.metadata['Modified'] = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        self.metadata['MD5 Hash'] = self.calculate_hash('md5')
        self.metadata['SHA256 Hash'] = self.calculate_hash('sha256')
        
        # Extração específica por tipo
        if file_ext == '.pdf':
            self.extract_pdf_metadata()
        elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp']:
            self.extract_image_metadata()
        elif file_ext == '.docx':
            self.extract_docx_metadata()
        
        print_separator()
        print(f"\n{Colors.GREEN}[+] Metadados extraídos:{Colors.RESET}\n")
        
        for key, value in self.metadata.items():
            print(f"    {Colors.CYAN}{key}:{Colors.RESET} {value}")
        
        self.save_results()
        return self.metadata
    
    def calculate_hash(self, algorithm):
        """Calcula hash do arquivo"""
        hash_func = hashlib.new(algorithm)
        with open(self.file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    
    def save_results(self):
        """Salva resultados em arquivo"""
        filename = f"metadata_{os.path.basename(self.file_path)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.metadata, f, indent=4)
        print_status("success", f"Resultados salvos em {filename}")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 6: GOOGLE DORKER
# ══════════════════════════════════════════════════════════════════════════════

class GoogleDorker:
    def __init__(self, target):
        self.target = target
        self.dorks = {}
        self.results = []
        
        # Categorias de dorks
        self.dork_templates = {
            'Arquivos Sensíveis': [
                f'site:{target} filetype:pdf',
                f'site:{target} filetype:doc OR filetype:docx',
                f'site:{target} filetype:xls OR filetype:xlsx',
                f'site:{target} filetype:ppt OR filetype:pptx',
                f'site:{target} filetype:txt',
                f'site:{target} filetype:sql',
                f'site:{target} filetype:log',
                f'site:{target} filetype:bak',
                f'site:{target} filetype:conf OR filetype:config',
                f'site:{target} filetype:env',
            ],
            'Diretórios Expostos': [
                f'site:{target} intitle:"index of"',
                f'site:{target} intitle:"index of" "parent directory"',
                f'site:{target} intitle:"index of" password',
                f'site:{target} intitle:"index of" backup',
                f'site:{target} intitle:"index of" .git',
            ],
            'Painéis de Admin': [
                f'site:{target} inurl:admin',
                f'site:{target} inurl:login',
                f'site:{target} inurl:wp-admin',
                f'site:{target} inurl:administrator',
                f'site:{target} inurl:phpmyadmin',
                f'site:{target} inurl:cpanel',
                f'site:{target} inurl:webmail',
                f'site:{target} intitle:"dashboard"',
            ],
            'Informações Sensíveis': [
                f'site:{target} "password"',
                f'site:{target} "username" "password"',
                f'site:{target} "api_key" OR "apikey"',
                f'site:{target} "secret_key" OR "secretkey"',
                f'site:{target} "aws_access_key"',
                f'site:{target} "private_key"',
                f'site:{target} intext:"@gmail.com" OR intext:"@yahoo.com"',
                f'site:{target} "confidential"',
            ],
            'Vulnerabilidades': [
                f'site:{target} inurl:".php?id="',
                f'site:{target} inurl:".asp?id="',
                f'site:{target} inurl:"redirect="',
                f'site:{target} inurl:"url="',
                f'site:{target} inurl:"file="',
                f'site:{target} inurl:"path="',
                f'site:{target} inurl:"page="',
                f'site:{target} ext:php intitle:phpinfo "published by the PHP Group"',
            ],
            'Backups e Configs': [
                f'site:{target} filetype:bak',
                f'site:{target} filetype:old',
                f'site:{target} filetype:backup',
                f'site:{target} inurl:backup',
                f'site:{target} "backup" filetype:sql',
                f'site:{target} filetype:xml',
                f'site:{target} filetype:json',
            ],
            'Git e Repositórios': [
                f'site:{target} inurl:.git',
                f'site:{target} filetype:git',
                f'site:{target} ".git/config"',
                f'site:{target} intext:"Index of /.svn"',
            ],
            'Tecnologias': [
                f'site:{target} powered by',
                f'site:{target} "running on"',
                f'site:{target} inurl:readme',
                f'site:{target} filetype:md',
                f'site:{target} "error" OR "warning" OR "notice"',
            ]
        }
    
    def run(self):
        """Executa geração de dorks"""
        print_module_header("🎯 GOOGLE DORKER")
        print(f"\n{Colors.CYAN}[*] Target: {Colors.WHITE}{self.target}{Colors.RESET}\n")
        print_separator()
        
        print(f"\n{Colors.GREEN}[+] Google Dorks gerados para {self.target}:{Colors.RESET}\n")
        
        all_dorks = []
        
        for category, dorks in self.dork_templates.items():
            print(f"\n{Colors.YELLOW}═══ {category} ═══{Colors.RESET}\n")
            for dork in dorks:
                encoded_dork = quote_plus(dork)
                google_url = f"https://www.google.com/search?q={encoded_dork}"
                print(f"    {Colors.CYAN}→{Colors.RESET} {dork}")
                print(f"      {Colors.DIM}{google_url}{Colors.RESET}\n")
                all_dorks.append({
                    'category': category,
                    'dork': dork,
                    'url': google_url
                })
        
        self.save_results(all_dorks)
        return all_dorks
    
    def save_results(self, dorks):
        """Salva resultados em arquivo"""
        filename = f"dorks_{self.target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(dorks, f, indent=4)
        print_status("success", f"Resultados salvos em {filename}")
        
        # Também salva em formato texto para fácil uso
        txt_filename = f"dorks_{self.target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(txt_filename, 'w') as f:
            for dork in dorks:
                f.write(f"{dork['dork']}\n")
        print_status("success", f"Lista de dorks salva em {txt_filename}")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 7: IP GEOLOCATION
# ══════════════════════════════════════════════════════════════════════════════

class IPGeolocation:
    def __init__(self, ip):
        self.ip = ip
        self.info = {}
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def lookup_ipapi(self):
        """Consulta ip-api.com"""
        try:
            url = f"http://ip-api.com/json/{self.ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return data
        except Exception as e:
            print_status("error", f"Erro na consulta ip-api: {str(e)}")
        return {}
    
    def lookup_ipinfo(self):
        """Consulta ipinfo.io"""
        try:
            url = f"https://ipinfo.io/{self.ip}/json"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print_status("error", f"Erro na consulta ipinfo: {str(e)}")
        return {}
    
    def reverse_dns(self):
        """Realiza DNS reverso"""
        try:
            hostname = socket.gethostbyaddr(self.ip)
            return hostname[0]
        except:
            return None
    
    def run(self):
        """Executa geolocalização"""
        print_module_header("📍 IP GEOLOCATION")
        print(f"\n{Colors.CYAN}[*] Target IP: {Colors.WHITE}{self.ip}{Colors.RESET}\n")
        print_separator()
        
        print_status("info", f"Consultando informações para {self.ip}...")
        
        # Consulta múltiplas fontes
        ipapi_data = self.lookup_ipapi()
        ipinfo_data = self.lookup_ipinfo()
        reverse = self.reverse_dns()
        
        # Consolida informações
        self.info = {
            'IP Address': self.ip,
            'Hostname': reverse or ipapi_data.get('reverse', 'N/A'),
            'Continent': ipapi_data.get('continent', 'N/A'),
            'Country': ipapi_data.get('country', ipinfo_data.get('country', 'N/A')),
            'Country Code': ipapi_data.get('countryCode', 'N/A'),
            'Region': ipapi_data.get('regionName', ipinfo_data.get('region', 'N/A')),
            'City': ipapi_data.get('city', ipinfo_data.get('city', 'N/A')),
            'ZIP Code': ipapi_data.get('zip', ipinfo_data.get('postal', 'N/A')),
            'Latitude': ipapi_data.get('lat', 'N/A'),
            'Longitude': ipapi_data.get('lon', 'N/A'),
            'Timezone': ipapi_data.get('timezone', ipinfo_data.get('timezone', 'N/A')),
            'ISP': ipapi_data.get('isp', ipinfo_data.get('org', 'N/A')),
            'Organization': ipapi_data.get('org', 'N/A'),
            'AS Number': ipapi_data.get('as', 'N/A'),
            'AS Name': ipapi_data.get('asname', 'N/A'),
            'Is Mobile': 'Yes' if ipapi_data.get('mobile') else 'No',
            'Is Proxy/VPN': 'Yes' if ipapi_data.get('proxy') else 'No',
            'Is Hosting': 'Yes' if ipapi_data.get('hosting') else 'No',
        }
        
        print_separator()
        print(f"\n{Colors.GREEN}[+] Informações do IP:{Colors.RESET}\n")
        
        for key, value in self.info.items():
            print(f"    {Colors.CYAN}{key}:{Colors.RESET} {value}")
        
        # Mostra mapa
        if self.info.get('Latitude') != 'N/A' and self.info.get('Longitude') != 'N/A':
            maps_url = f"https://www.google.com/maps?q={self.info['Latitude']},{self.info['Longitude']}"
            print(f"\n    {Colors.YELLOW}📍 Google Maps:{Colors.RESET} {maps_url}")
        
        self.save_results()
        return self.info
    
    def save_results(self):
        """Salva resultados em arquivo"""
        filename = f"ip_{self.ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.info, f, indent=4)
        print_status("success", f"Resultados salvos em {filename}")

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 8: FULL RECON
# ══════════════════════════════════════════════════════════════════════════════

class FullRecon:
    def __init__(self, target):
        self.target = target
        self.results = {}
    
    def run(self):
        """Executa reconhecimento completo"""
        print_module_header("🔗 FULL RECONNAISSANCE")
        print(f"\n{Colors.CYAN}[*] Target: {Colors.WHITE}{self.target}{Colors.RESET}\n")
        print_separator()
        
        print_status("info", "Iniciando reconhecimento completo...")
        print_status("warning", "Este processo pode demorar alguns minutos...\n")
        
        # 1. WHOIS
        print(f"\n{Colors.YELLOW}{'═' * 40} WHOIS {'═' * 40}{Colors.RESET}\n")
        whois_lookup = WhoisLookup(self.target)
        self.results['whois'] = whois_lookup.lookup()
        
        input(f"\n{Colors.CYAN}Pressione ENTER para continuar...{Colors.RESET}")
        
        # 2. Subdomains
        print(f"\n{Colors.YELLOW}{'═' * 40} SUBDOMAINS {'═' * 40}{Colors.RESET}\n")
        subdomain_enum = SubdomainEnumerator(self.target)
        self.results['subdomains'] = list(subdomain_enum.run())
        
        input(f"\n{Colors.CYAN}Pressione ENTER para continuar...{Colors.RESET}")
        
        # 3. Emails
        print(f"\n{Colors.YELLOW}{'═' * 40} EMAILS {'═' * 40}{Colors.RESET}\n")
        email_harvester = EmailHarvester(self.target)
        self.results['emails'] = list(email_harvester.run())
        
        input(f"\n{Colors.CYAN}Pressione ENTER para continuar...{Colors.RESET}")
        
        # 4. Google Dorks
        print(f"\n{Colors.YELLOW}{'═' * 40} GOOGLE DORKS {'═' * 40}{Colors.RESET}\n")
        dorker = GoogleDorker(self.target)
        self.results['dorks'] = dorker.run()
        
        # Resumo final
        print_separator()
        print(f"\n{Colors.GREEN}{'═' * 40} RESUMO DO RECONHECIMENTO {'═' * 40}{Colors.RESET}\n")
        
        print(f"""
    {Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗
    ║{Colors.WHITE}                    RECONNAISSANCE SUMMARY                        {Colors.CYAN}║
    ╠══════════════════════════════════════════════════════════════════╣
    ║{Colors.RESET}  Target:              {self.target:<43}{Colors.CYAN}║
    ║{Colors.RESET}  Subdomains Found:    {len(self.results.get('subdomains', [])):<43}{Colors.CYAN}║
    ║{Colors.RESET}  Emails Found:        {len(self.results.get('emails', [])):<43}{Colors.CYAN}║
    ║{Colors.RESET}  Dorks Generated:     {len(self.results.get('dorks', [])):<43}{Colors.CYAN}║
    ╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}
        """)
        
        self.save_results()
        return self.results
    
    def save_results(self):
        """Salva todos os resultados em arquivo"""
        filename = f"full_recon_{self.target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4, default=str)
        print_status("success", f"Relatório completo salvo em {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES
# ══════════════════════════════════════════════════════════════════════════════

def get_user_input(prompt, allow_empty=False):
    """Obtém input do usuário com validação"""
    while True:
        user_input = input(f"\n{Colors.CYAN}[?]{Colors.RESET} {prompt}: ").strip()
        if user_input or allow_empty:
            return user_input
        print_status("warning", "Input não pode ser vazio!")

def pause():
    """Pausa a execução até o usuário pressionar ENTER"""
    input(f"\n{Colors.CYAN}Pressione ENTER para voltar ao menu...{Colors.RESET}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Função principal do framework"""
    
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        choice = input(f"{Colors.GREEN}┌──({Colors.CYAN}{AUTHOR}{Colors.GREEN}㉿{Colors.CYAN}dahmer-osint{Colors.GREEN})-[{Colors.WHITE}~{Colors.GREEN}]\n└─{Colors.WHITE}$ {Colors.RESET}").strip()
        
        try:
            if choice == '1':
                # Email Harvester
                domain = get_user_input("Digite o domínio alvo (ex: example.com)")
                harvester = EmailHarvester(domain)
                harvester.run()
                pause()
                
            elif choice == '2':
                # Subdomain Enumerator
                domain = get_user_input("Digite o domínio alvo (ex: example.com)")
                enumerator = SubdomainEnumerator(domain)
                enumerator.run()
                pause()
                
            elif choice == '3':
                # WHOIS Lookup
                target = get_user_input("Digite o domínio ou IP")
                lookup = WhoisLookup(target)
                lookup.lookup()
                pause()
                
            elif choice == '4':
                # Username OSINT
                username = get_user_input("Digite o username alvo")
                osint = UsernameOSINT(username)
                osint.run()
                pause()
                
            elif choice == '5':
                # Metadata Extractor
                file_path = get_user_input("Digite o caminho do arquivo")
                extractor = MetadataExtractor(file_path)
                extractor.run()
                pause()
                
            elif choice == '6':
                # Google Dorker
                target = get_user_input("Digite o domínio alvo (ex: example.com)")
                dorker = GoogleDorker(target)
                dorker.run()
                pause()
                
            elif choice == '7':
                # IP Geolocation
                ip = get_user_input("Digite o endereço IP")
                geo = IPGeolocation(ip)
                geo.run()
                pause()
                
            elif choice == '8':
                # Full Recon
                target = get_user_input("Digite o domínio alvo para recon completo")
                recon = FullRecon(target)
                recon.run()
                pause()
                
            elif choice == '0':
                # Exit
                clear_screen()
                print(f"""
{Colors.RED}
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║           ██████╗  ██████╗  ██████╗ ██████╗ ██████╗ ██╗   ██╗███████╗  ║
    ║          ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝  ║
    ║          ██║  ███╗██║   ██║██║   ██║██║  ██║██████╔╝ ╚████╔╝ █████╗    ║
    ║          ██║   ██║██║   ██║██║   ██║██║  ██║██╔══██╗  ╚██╔╝  ██╔══╝    ║
    ║          ╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   ███████╗  ║
    ║           ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝  ║
    ║                                                                  ║
    ║                Thanks for using DAHMER OSINT Framework!          ║
    ║                         Stay safe & ethical!                     ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
{Colors.RESET}
                """)
                print(f"    {Colors.DIM}Created by {AUTHOR} | Version {VERSION}{Colors.RESET}\n")
                sys.exit(0)
                
            else:
                print_status("error", "Opção inválida!")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print_status("warning", "\nOperação cancelada pelo usuário!")
            time.sleep(1)
        except Exception as e:
            print_status("error", f"Erro: {str(e)}")
            pause()


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Verifica se está rodando como root (recomendado para algumas funções)
    if os.name != 'nt' and os.geteuid() != 0:
        print(f"{Colors.YELLOW}[!] Algumas funções podem requerer privilégios de root.{Colors.RESET}")
    
    # Argumentos de linha de comando para uso direto
    parser = argparse.ArgumentParser(
        description=f'{TOOL_NAME} - Advanced OSINT Framework by {AUTHOR}',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  python osint_framework.py                    # Modo interativo
  python osint_framework.py -e example.com     # Email harvesting
  python osint_framework.py -s example.com     # Subdomain enumeration
  python osint_framework.py -w example.com     # WHOIS lookup
  python osint_framework.py -u johndoe         # Username OSINT
  python osint_framework.py -g example.com     # Google dorks
  python osint_framework.py -i 8.8.8.8         # IP geolocation
  python osint_framework.py -f example.com     # Full recon
        """
    )
    
    parser.add_argument('-e', '--email', metavar='DOMAIN', help='Email harvesting para o domínio')
    parser.add_argument('-s', '--subdomain', metavar='DOMAIN', help='Enumeração de subdomínios')
    parser.add_argument('-w', '--whois', metavar='TARGET', help='WHOIS lookup')
    parser.add_argument('-u', '--username', metavar='USERNAME', help='Username OSINT')
    parser.add_argument('-m', '--metadata', metavar='FILE', help='Extração de metadados')
    parser.add_argument('-g', '--dorks', metavar='DOMAIN', help='Google dorks generator')
    parser.add_argument('-i', '--ip', metavar='IP', help='IP geolocation')
    parser.add_argument('-f', '--full', metavar='DOMAIN', help='Full reconnaissance')
    parser.add_argument('-v', '--version', action='version', version=f'{TOOL_NAME} v{VERSION}')
    
    args = parser.parse_args()
    
    # Execução via argumentos
    if args.email:
        clear_screen()
        print_banner()
        EmailHarvester(args.email).run()
    elif args.subdomain:
        clear_screen()
        print_banner()
        SubdomainEnumerator(args.subdomain).run()
    elif args.whois:
        clear_screen()
        print_banner()
        WhoisLookup(args.whois).lookup()
    elif args.username:
        clear_screen()
        print_banner()
        UsernameOSINT(args.username).run()
    elif args.metadata:
        clear_screen()
        print_banner()
        MetadataExtractor(args.metadata).run()
    elif args.dorks:
        clear_screen()
        print_banner()
        GoogleDorker(args.dorks).run()
    elif args.ip:
        clear_screen()
        print_banner()
        IPGeolocation(args.ip).run()
    elif args.full:
        clear_screen()
        print_banner()
        FullRecon(args.full).run()
    else:
        # Modo interativo
        main()
