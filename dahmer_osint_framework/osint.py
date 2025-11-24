#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
+------------------------------------------------------------------------------+
|                        OSINT FRAMEWORK - ADVANCED TOOLKIT                    |
|                              Created by devdahmer99                          |
+------------------------------------------------------------------------------+
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
import struct
import zlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, quote_plus
from datetime import datetime
from colorama import Fore, Back, Style, init
import argparse

# Inicializa colorama para Windows
init(autoreset=True)

# ==============================================================================
# CONFIGURAÇÕES GLOBAIS
# ==============================================================================

VERSION = "2.0.0" 
AUTHOR = "devdahmer99"
TOOL_NAME = "DAHMER OSINT"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

# ==============================================================================
# CORES E ESTILOS
# ==============================================================================

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

# ==============================================================================
# BANNER E INTERFACE
# ==============================================================================

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
        ⠀⠀⠀⢻⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⡟⠀⠀⠀       {Colors.YELLOW}----------------------------------------------------------{Colors.RESET}
        ⠀⠀⠀⠀⠻⣿⣿⣿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⠟⠀⠀⠀⠀       {Colors.WHITE}  Advanced OSINT Framework for Penetration Testing{Colors.RESET}
        ⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀       {Colors.WHITE}  Red Team Operations & Intelligence Gathering{Colors.RESET}
        ⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠀⠀⠀       {Colors.YELLOW}----------------------------------------------------------{Colors.RESET}
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠛⠛⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                                                    {Colors.DIM}Created by {Colors.CYAN}{AUTHOR}{Colors.RESET}
                                                                    {Colors.DIM}Version: {Colors.GREEN}{VERSION}{Colors.RESET}
    """
    print(banner)

def print_separator():
    print(f"{Colors.YELLOW}{'-' * 90}{Colors.RESET}")

def print_module_header(module_name):
    clear_screen()
    print(f"""
{Colors.CYAN}+{'-' * 88}+
|{Colors.WHITE}{Colors.BOLD} {module_name.center(86)} {Colors.CYAN}|
+{'-' * 88}+
|{Colors.GREEN} {'DAHMER OSINT FRAMEWORK'.center(86)} {Colors.CYAN}|
|{Colors.DIM}{Colors.WHITE} {f'Developer: {AUTHOR} | Version: {VERSION}'.center(86)} {Colors.CYAN}|
+{'-' * 88}+{Colors.RESET}
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
    elif status == "sensitive":
        print(f"{Colors.DIM}[{timestamp}]{Colors.RESET} [{Colors.RED}SENSITIVE{Colors.RESET}] {message}")

def print_menu():
    print(f"""
{Colors.CYAN}+------------------------------------------------------------------------------------------+
|{Colors.WHITE}{Colors.BOLD}                                    MAIN MENU                                             {Colors.CYAN}|
+------------------------------------------------------------------------------------------+{Colors.RESET}
|                                                                                          |
|   {Colors.GREEN}[1]{Colors.RESET} [?]  Email Harvester         {Colors.DIM}- Coleta emails de dominios{Colors.RESET}                       |
|   {Colors.GREEN}[2]{Colors.RESET} [?]  Subdomain Enumerator    {Colors.DIM}- Descobre subdominios{Colors.RESET}                            |
|   {Colors.GREEN}[3]{Colors.RESET} [?]  WHOIS Lookup            {Colors.DIM}- Informacoes de registro de dominio{Colors.RESET}              |
|   {Colors.GREEN}[4]{Colors.RESET} [?]  Username OSINT          {Colors.DIM}- Busca username em redes sociais{Colors.RESET}                 |
|   {Colors.GREEN}[5]{Colors.RESET} [?]  Metadata Extractor      {Colors.DIM}- Extrai metadados (Advanced){Colors.RESET}                    |
|   {Colors.GREEN}[6]{Colors.RESET} [?]  Google Dorker           {Colors.DIM}- Automatiza Google Dorks{Colors.RESET}                         |
|   {Colors.GREEN}[7]{Colors.RESET} [?]  IP Geolocation          {Colors.DIM}- Geolocalizacao e info de IPs{Colors.RESET}                    |
|   {Colors.GREEN}[8]{Colors.RESET} [?]  Full Recon              {Colors.DIM}- Reconhecimento completo de alvo{Colors.RESET}                 |
|                                                                                          |
|   {Colors.RED}[0]{Colors.RESET} [X]  Exit                     {Colors.DIM}- Sair do framework{Colors.RESET}                               |
|                                                                                          |
{Colors.CYAN}+------------------------------------------------------------------------------------------+{Colors.RESET}
""")

# ==============================================================================
# MÓDULO 1: EMAIL HARVESTER
# ==============================================================================

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
        """Gera emails comuns baseados em padroes"""
        print_status("info", "Gerando emails baseados em padroes comuns...")
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
        print_module_header("EMAIL HARVESTER")
        print(f"\n{Colors.CYAN}[*] Target Domain: {Colors.WHITE}{self.domain}{Colors.RESET}\n")
        print_separator()
        
        self.search_bing()
        self.search_duckduckgo()
        self.search_pgp_servers()
        self.generate_common_emails()
        
        print_separator()
        print(f"\n{Colors.GREEN}[+] Emails encontrados: {len(self.emails)}{Colors.RESET}\n")
        
        for email in sorted(self.emails):
            print(f"    {Colors.CYAN}->{Colors.RESET} {email}")
        
        # Salvar resultados
        self.save_results()
        return self.emails
    
    def save_results(self):
        """Salva resultados em arquivo"""
        filename = f"emails_{self.domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            for email in sorted(self.emails):
                f.write(f"{email}\n")
        print_status("success", f"Resultados salvos em {filename}")

# ==============================================================================
# MÓDULO 2: SUBDOMAIN ENUMERATOR
# ==============================================================================

class SubdomainEnumerator:
    def __init__(self, domain):
        self.domain = domain
        self.subdomains = set()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
        # Wordlist de subdominios comuns
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
        """Bruteforce de subdominios via DNS"""
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
        """Busca subdominios no crt.sh (Certificate Transparency)"""
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
        """Busca subdominios via HackerTarget"""
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
        """Resolve IP de um subdominio"""
        try:
            answers = dns.resolver.resolve(subdomain, 'A')
            ips = [rdata.address for rdata in answers]
            return ips
        except:
            return []
    
    def run(self):
        """Executa todas as buscas"""
        print_module_header("SUBDOMAIN ENUMERATOR")
        print(f"\n{Colors.CYAN}[*] Target Domain: {Colors.WHITE}{self.domain}{Colors.RESET}\n")
        print_separator()
        
        self.crtsh_search()
        self.hackertarget_search()
        self.dns_bruteforce()
        
        print_separator()
        print(f"\n{Colors.GREEN}[+] Subdominios encontrados: {len(self.subdomains)}{Colors.RESET}\n")
        
        # Mostrar resultados com IPs
        print(f"{'Subdominio':<50} {'Endereco IP':<20}")
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
        with open(filename, 'w', encoding='utf-8') as f:
            for subdomain in sorted(self.subdomains):
                f.write(f"{subdomain}\n")
        print_status("success", f"Resultados salvos em {filename}")

# ==============================================================================
# MÓDULO 3: WHOIS LOOKUP
# ==============================================================================

class WhoisLookup:
    def __init__(self, target):
        self.target = target
        self.info = {}
    
    def lookup(self):
        """Realiza consulta WHOIS"""
        print_module_header("WHOIS LOOKUP")
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
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.info, f, indent=4, default=str)
        print_status("success", f"Resultados salvos em {filename}")

# ==============================================================================
# MÓDULO 4: USERNAME OSINT
# ==============================================================================

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
            
            # Verificacao basica de existencia
            if response.status_code == 200:
                # Verificacoes adicionais para evitar falsos positivos
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
        print_module_header("USERNAME OSINT")
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
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=4)
        print_status("success", f"Resultados salvos em {filename}")

# ==============================================================================
# MÓDULO 5: METADATA EXTRACTOR (ADVANCED)
# ==============================================================================

class MetadataExtractor:
    """Extrator avancado de metadados para analise forense e OSINT"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.metadata = {}
        self.sensitive_data = []
        self.warnings = []
        
    # ==========================================================================
    # INFORMACOES BASICAS DO ARQUIVO
    # ==========================================================================
    
    def extract_file_info(self):
        """Extrai informacoes basicas do arquivo"""
        stat = os.stat(self.file_path)
        
        self.metadata['File_Information'] = {
            'File_Name': os.path.basename(self.file_path),
            'File_Path': os.path.abspath(self.file_path),
            'File_Extension': os.path.splitext(self.file_path)[1].lower(),
            'File_Size_Bytes': stat.st_size,
            'File_Size_Human': self._bytes_to_human(stat.st_size),
            'Created_Time': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'Modified_Time': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'Accessed_Time': datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
            'Inode': stat.st_ino,
            'Device': stat.st_dev,
            'Hard_Links': stat.st_nlink,
        }
        
        # Permissoes (Unix)
        if os.name != 'nt':
            try:
                import pwd
                import grp
                self.metadata['File_Information']['Permissions'] = oct(stat.st_mode)[-3:]
                self.metadata['File_Information']['Owner_UID'] = stat.st_uid
                self.metadata['File_Information']['Owner_GID'] = stat.st_gid
                try:
                    self.metadata['File_Information']['Owner_Name'] = pwd.getpwuid(stat.st_uid).pw_name
                    self.metadata['File_Information']['Group_Name'] = grp.getgrgid(stat.st_gid).gr_name
                except:
                    pass
            except ImportError:
                pass
        
        # MIME Type
        try:
            import magic
            mime = magic.Magic(mime=True)
            self.metadata['File_Information']['MIME_Type'] = mime.from_file(self.file_path)
            
            desc = magic.Magic()
            self.metadata['File_Information']['File_Type_Description'] = desc.from_file(self.file_path)
        except ImportError:
            # Fallback sem python-magic
            import mimetypes
            mime_type, _ = mimetypes.guess_type(self.file_path)
            self.metadata['File_Information']['MIME_Type'] = mime_type or 'unknown'
        except Exception as e:
            self.metadata['File_Information']['MIME_Type'] = 'unknown'
    
    # ==========================================================================
    # HASHES MÚLTIPLOS
    # ==========================================================================
    
    def calculate_hashes(self):
        """Calcula multiplos hashes do arquivo"""
        algorithms = {
            'MD5': hashlib.md5(),
            'SHA1': hashlib.sha1(),
            'SHA256': hashlib.sha256(),
            'SHA512': hashlib.sha512(),
        }
        
        with open(self.file_path, 'rb') as f:
            while chunk := f.read(8192):
                for algo in algorithms.values():
                    algo.update(chunk)
        
        self.metadata['Hashes'] = {
            name: algo.hexdigest() for name, algo in algorithms.items()
        }
        
        # SSDEEP (fuzzy hash) se disponivel
        try:
            import ppdeep as ssdeep
            self.metadata['Hashes']['SSDEEP'] = ssdeep.hash_from_file(self.file_path)
        except ImportError:
            self.metadata['Hashes']['SSDEEP'] = 'ssdeep not installed (pip install ssdeep)'
        except Exception:
            pass
        
        # CRC32
        import zlib
        with open(self.file_path, 'rb') as f:
            crc = zlib.crc32(f.read()) & 0xffffffff
            self.metadata['Hashes']['CRC32'] = format(crc, '08x')
    
    # ==========================================================================
    # EXTRAÇÃO DE IMAGENS - MEGA COMPLETA
    # ==========================================================================
    
    def extract_image_metadata(self):
        """Extrai TODOS os metadados possiveis de imagens"""
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS, GPSTAGS, IFD
            
            image = Image.open(self.file_path)
            
            # ==================================================================
            # INFORMACOES BASICAS DA IMAGEM
            # ==================================================================
            
            width, height = image.size
            
            self.metadata['Image_Basic'] = {
                'Format': image.format,
                'Format_Description': image.format_description if hasattr(image, 'format_description') else image.format,
                'Mode': image.mode,
                'Mode_Description': self._get_mode_description(image.mode),
                'Width_Pixels': width,
                'Height_Pixels': height,
                'Megapixels': round((width * height) / 1000000, 2),
                'Aspect_Ratio': f"{width}:{height}",
                'Aspect_Ratio_Decimal': round(width / height, 2) if height else 0,
                'Is_Animated': getattr(image, 'is_animated', False),
                'N_Frames': getattr(image, 'n_frames', 1),
            }
            
            # Bits por pixel
            if image.mode in ['1']:
                bpp = 1
            elif image.mode in ['L', 'P']:
                bpp = 8
            elif image.mode in ['LA']:
                bpp = 16
            elif image.mode in ['RGB', 'YCbCr']:
                bpp = 24
            elif image.mode in ['RGBA', 'CMYK']:
                bpp = 32
            else:
                bpp = 'unknown'
            
            self.metadata['Image_Basic']['Bits_Per_Pixel'] = bpp
            self.metadata['Image_Basic']['Color_Depth'] = f"{bpp}-bit" if isinstance(bpp, int) else bpp
            
            # DPI / Resolucao
            if 'dpi' in image.info:
                self.metadata['Image_Basic']['DPI_X'] = image.info['dpi'][0]
                self.metadata['Image_Basic']['DPI_Y'] = image.info['dpi'][1]
            
            # ==================================================================
            # EXIF DATA COMPLETO
            # ==================================================================
            
            exif_data = {}
            gps_data = {}
            camera_data = {}
            photo_settings = {}
            datetime_data = {}
            author_data = {}
            software_data = {}
            
            # Tentar obter EXIF de diferentes formas
            raw_exif = None
            
            # Metodo 1: _getexif()
            if hasattr(image, '_getexif') and image._getexif():
                raw_exif = image._getexif()
            
            # Metodo 2: getexif() (PIL mais recente)
            if not raw_exif and hasattr(image, 'getexif'):
                raw_exif = image.getexif()
            
            if raw_exif:
                for tag_id, value in raw_exif.items():
                    tag_name = TAGS.get(tag_id, str(tag_id))
                    
                    # Converter bytes
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', errors='replace').strip('\x00')
                        except:
                            value = value.hex()
                    
                    # GPS INFO - LOCALIZACAO
                    if tag_name == 'GPSInfo':
                        gps_data = self._parse_gps_info(value)
                        if gps_data.get('Latitude_Decimal') and gps_data.get('Longitude_Decimal'):
                            lat = gps_data['Latitude_Decimal']
                            lon = gps_data['Longitude_Decimal']
                            gps_data['Google_Maps_URL'] = f"https://www.google.com/maps?q={lat},{lon}"
                            gps_data['OpenStreetMap_URL'] = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=15"
                            
                            self.sensitive_data.append(f"[!] GPS LOCATION FOUND: {lat}, {lon}")
                            self.sensitive_data.append(f"[!] Google Maps: {gps_data['Google_Maps_URL']}")
                    
                    # CAMERA E DISPOSITIVO
                    elif tag_name in ['Make', 'Model', 'BodySerialNumber', 'LensModel', 
                                     'LensSerialNumber', 'CameraOwnerName', 'OwnerName']:
                        camera_data[tag_name] = str(value)
                        
                        if tag_name in ['BodySerialNumber', 'LensSerialNumber', 'CameraOwnerName', 'OwnerName']:
                            self.sensitive_data.append(f"[!] {tag_name}: {value}")
                    
                    # CONFIGURACOES DA FOTO
                    elif tag_name in ['ExposureTime', 'FNumber', 'ISOSpeedRatings', 'ISO',
                                     'FocalLength', 'FocalLengthIn35mmFilm', 'ApertureValue',
                                     'ShutterSpeedValue', 'ExposureBiasValue', 'MaxApertureValue',
                                     'MeteringMode', 'Flash', 'WhiteBalance', 'ExposureProgram',
                                     'ExposureMode', 'DigitalZoomRatio', 'SceneCaptureType']:
                        photo_settings[tag_name] = self._format_exif_value(tag_name, value)
                    
                    # DATAS E HORARIOS
                    elif tag_name in ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized',
                                     'OffsetTime', 'OffsetTimeOriginal', 'OffsetTimeDigitized']:
                        datetime_data[tag_name] = str(value)
                    
                    # AUTOR E COPYRIGHT
                    elif tag_name in ['Artist', 'Copyright', 'ImageDescription', 
                                     'XPAuthor', 'XPTitle', 'XPComment', 'XPKeywords', 'XPSubject']:
                        author_data[tag_name] = str(value)
                        self.sensitive_data.append(f"[!] {tag_name}: {value}")
                    
                    # SOFTWARE
                    elif tag_name in ['Software', 'ProcessingSoftware', 'HostComputer']:
                        software_data[tag_name] = str(value)
                        self.sensitive_data.append(f"[!] {tag_name}: {value}")
                    
                    # Todos os outros
                    else:
                        exif_data[tag_name] = str(value) if not isinstance(value, (int, float)) else value
            
            # Adicionar ao metadata
            if camera_data:
                self.metadata['Camera_Device'] = camera_data
            if photo_settings:
                self.metadata['Photo_Settings'] = photo_settings
            if datetime_data:
                self.metadata['DateTime_Info'] = datetime_data
            if author_data:
                self.metadata['Author_Copyright'] = author_data
            if software_data:
                self.metadata['Software_Info'] = software_data
            if gps_data:
                self.metadata['GPS_Location'] = gps_data
            if exif_data:
                self.metadata['EXIF_Other'] = exif_data
            
            # ==================================================================
            # THUMBNAIL EMBUTIDO
            # ==================================================================
            
            if raw_exif and 513 in raw_exif:  # ThumbnailOffset
                self.metadata['Thumbnail'] = {
                    'Present': True,
                    'Warning': '[!] Thumbnail pode conter versao original antes de crop/edicao!'
                }
                self.sensitive_data.append("[!] THUMBNAIL FOUND - May reveal original image before editing!")
                self.warnings.append("Thumbnail embutido pode revelar informacoes da imagem original")
            
            # ==================================================================
            # ICC PROFILE
            # ==================================================================
            
            if 'icc_profile' in image.info:
                icc = image.info['icc_profile']
                self.metadata['ICC_Profile'] = {
                    'Present': True,
                    'Size_Bytes': len(icc),
                }
                
                # Tentar extrair nome do perfil
                try:
                    # O nome do perfil geralmente esta no offset 128 com 4 bytes de tamanho antes
                    if len(icc) > 132:
                        desc_offset = 128
                        profile_desc = icc[desc_offset:desc_offset+64].decode('utf-8', errors='ignore').strip('\x00')
                        if profile_desc:
                            self.metadata['ICC_Profile']['Profile_Description'] = profile_desc
                except:
                    pass
            
            # ==================================================================
            # XMP METADATA
            # ==================================================================
            
            xmp_data = self._extract_xmp()
            if xmp_data:
                self.metadata['XMP_Metadata'] = xmp_data
            
            # ==================================================================
            # IPTC METADATA
            # ==================================================================
            
            iptc_data = self._extract_iptc(image)
            if iptc_data:
                self.metadata['IPTC_Metadata'] = iptc_data
            
            # ==================================================================
            # PHOTOSHOP METADATA
            # ==================================================================
            
            if 'photoshop' in image.info:
                self.metadata['Photoshop_Data'] = {
                    'Present': True,
                    'Note': 'Imagem foi processada no Adobe Photoshop'
                }
                self.sensitive_data.append("[!] Image was edited in Adobe Photoshop")
            
            image.close()
            
        except ImportError:
            print_status("error", "Pillow nao instalado. Execute: pip install Pillow")
        except Exception as e:
            print_status("error", f"Erro ao extrair metadados de imagem: {str(e)}")
    
    def _parse_gps_info(self, gps_info):
        """Parse GPS info do EXIF"""
        gps_data = {}
        
        try:
            from PIL.ExifTags import GPSTAGS
            
            for tag_id, value in gps_info.items():
                tag_name = GPSTAGS.get(tag_id, str(tag_id))
                
                if isinstance(value, bytes):
                    value = value.decode('utf-8', errors='replace')
                
                gps_data[tag_name] = str(value)
            
            # Converter para decimal
            def to_decimal(coord, ref):
                try:
                    degrees = float(coord[0])
                    minutes = float(coord[1])
                    seconds = float(coord[2])
                    decimal = degrees + (minutes / 60) + (seconds / 3600)
                    if ref in ['S', 'W']:
                        decimal = -decimal
                    return round(decimal, 6)
                except:
                    return None
            
            # Latitude
            if 2 in gps_info and 1 in gps_info:
                lat = to_decimal(gps_info[2], gps_info[1])
                if lat:
                    gps_data['Latitude_Decimal'] = lat
            
            # Longitude
            if 4 in gps_info and 3 in gps_info:
                lon = to_decimal(gps_info[4], gps_info[3])
                if lon:
                    gps_data['Longitude_Decimal'] = lon
            
            # Altitude
            if 6 in gps_info:
                try:
                    alt = float(gps_info[6])
                    gps_data['Altitude_Meters'] = round(alt, 2)
                except:
                    pass
            
            # Timestamp GPS
            if 29 in gps_info:  # GPSDateStamp
                gps_data['GPS_Date'] = str(gps_info[29])
            if 7 in gps_info:  # GPSTimeStamp
                try:
                    h, m, s = gps_info[7]
                    gps_data['GPS_Time'] = f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
                except:
                    pass
            
            # Velocidade
            if 13 in gps_info:  # GPSSpeed
                try:
                    speed = float(gps_info[13])
                    gps_data['GPS_Speed'] = speed
                except:
                    pass
            
            # Direcao
            if 17 in gps_info:  # GPSImgDirection
                try:
                    direction = float(gps_info[17])
                    gps_data['GPS_Direction_Degrees'] = round(direction, 2)
                except:
                    pass
                    
        except Exception as e:
            gps_data['Parse_Error'] = str(e)
        
        return gps_data
    
    def _extract_xmp(self):
        """Extrai metadados XMP do arquivo"""
        xmp_data = {}
        
        try:
            with open(self.file_path, 'rb') as f:
                content = f.read()
            
            # Procurar por XMP
            xmp_start = content.find(b'<x:xmpmeta')
            xmp_end = content.find(b'</x:xmpmeta>')
            
            if xmp_start != -1 and xmp_end != -1:
                xmp_raw = content[xmp_start:xmp_end + 12].decode('utf-8', errors='ignore')
                
                # Extrair campos usando regex
                patterns = {
                    'Creator': r'<dc:creator[^>]*>.*?<rdf:li[^>]*>([^<]+)',
                    'Title': r'<dc:title[^>]*>.*?<rdf:li[^>]*>([^<]+)',
                    'Description': r'<dc:description[^>]*>.*?<rdf:li[^>]*>([^<]+)',
                    'Subject': r'<dc:subject[^>]*>.*?<rdf:li[^>]*>([^<]+)',
                    'Rights': r'<dc:rights[^>]*>.*?<rdf:li[^>]*>([^<]+)',
                    'CreatorTool': r'xmp:CreatorTool[=>"\s]+([^"<]+)',
                    'CreateDate': r'xmp:CreateDate[=>"\s]+([^"<]+)',
                    'ModifyDate': r'xmp:ModifyDate[=>"\s]+([^"<]+)',
                    'MetadataDate': r'xmp:MetadataDate[=>"\s]+([^"<]+)',
                    'Rating': r'xmp:Rating[=>"\s]+([^"<]+)',
                    'Label': r'xmp:Label[=>"\s]+([^"<]+)',
                    'DocumentID': r'xmpMM:DocumentID[=>"\s]+([^"<]+)',
                    'InstanceID': r'xmpMM:InstanceID[=>"\s]+([^"<]+)',
                    'OriginalDocumentID': r'xmpMM:OriginalDocumentID[=>"\s]+([^"<]+)',
                    'Photoshop_ColorMode': r'photoshop:ColorMode[=>"\s]+([^"<]+)',
                    'Photoshop_ICCProfile': r'photoshop:ICCProfile[=>"\s]+([^"<]+)',
                    'CameraRaw_Version': r'crs:Version[=>"\s]+([^"<]+)',
                }
                
                for name, pattern in patterns.items():
                    match = re.search(pattern, xmp_raw, re.DOTALL | re.IGNORECASE)
                    if match:
                        value = match.group(1).strip()
                        xmp_data[name] = value
                        
                        if name in ['Creator', 'DocumentID', 'OriginalDocumentID']:
                            self.sensitive_data.append(f"[!] XMP {name}: {value}")
                
                # Verificar historico de edicao
                if 'stEvt:action' in xmp_raw or 'photoshop:History' in xmp_raw:
                    xmp_data['Has_Edit_History'] = True
                    self.sensitive_data.append("[!] XMP contains edit history!")
                    
                    # Extrair acoes do historico
                    actions = re.findall(r'stEvt:action[=>"\s]+([^"<]+)', xmp_raw)
                    if actions:
                        xmp_data['Edit_Actions'] = list(set(actions))
                
                # Software history
                software_agents = re.findall(r'stEvt:softwareAgent[=>"\s]+([^"<]+)', xmp_raw)
                if software_agents:
                    xmp_data['Software_History'] = list(set(software_agents))
                    for sw in set(software_agents):
                        self.sensitive_data.append(f"[!] Software used: {sw}")
                        
        except Exception as e:
            pass
        
        return xmp_data
    
    def _extract_iptc(self, image):
        """Extrai metadados IPTC"""
        iptc_data = {}
        
        try:
            from PIL import IptcImagePlugin
            
            iptc = IptcImagePlugin.getiptcinfo(image)
            
            if iptc:
                # Mapeamento de tags IPTC comuns
                iptc_tags = {
                    (2, 5): 'ObjectName',
                    (2, 25): 'Keywords',
                    (2, 55): 'DateCreated',
                    (2, 60): 'TimeCreated',
                    (2, 62): 'DigitalCreationDate',
                    (2, 63): 'DigitalCreationTime',
                    (2, 80): 'Byline',
                    (2, 85): 'BylineTitle',
                    (2, 90): 'City',
                    (2, 92): 'Sublocation',
                    (2, 95): 'State',
                    (2, 100): 'CountryCode',
                    (2, 101): 'Country',
                    (2, 105): 'Headline',
                    (2, 110): 'Credit',
                    (2, 115): 'Source',
                    (2, 116): 'CopyrightNotice',
                    (2, 118): 'Contact',
                    (2, 120): 'Caption',
                    (2, 122): 'Writer',
                }
                
                for key, value in iptc.items():
                    tag_name = iptc_tags.get(key, f"Tag_{key}")
                    
                    if isinstance(value, bytes):
                        value = value.decode('utf-8', errors='replace')
                    elif isinstance(value, list):
                        value = [v.decode('utf-8', errors='replace') if isinstance(v, bytes) else str(v) for v in value]
                        value = ', '.join(value)
                    
                    iptc_data[tag_name] = str(value)
                    
                    # Dados sensiveis
                    if tag_name in ['Byline', 'Credit', 'Source', 'Contact', 'City', 'Country']:
                        self.sensitive_data.append(f"[!] IPTC {tag_name}: {value}")
                        
        except Exception as e:
            pass
        
        return iptc_data
    
    def _get_mode_description(self, mode):
        """Retorna descricao do modo de imagem"""
        modes = {
            '1': '1-bit pixels, black and white',
            'L': '8-bit pixels, grayscale',
            'P': '8-bit pixels, palette-mapped',
            'RGB': '3x8-bit pixels, true color',
            'RGBA': '4x8-bit pixels, true color with transparency',
            'CMYK': '4x8-bit pixels, color separation',
            'YCbCr': '3x8-bit pixels, color video format',
            'LAB': '3x8-bit pixels, L*a*b color space',
            'HSV': '3x8-bit pixels, Hue, Saturation, Value',
            'I': '32-bit signed integer pixels',
            'F': '32-bit floating point pixels',
        }
        return modes.get(mode, f'Unknown mode: {mode}')
    
    def _format_exif_value(self, tag_name, value):
        """Formata valores EXIF para melhor legibilidade"""
        try:
            if tag_name == 'ExposureTime':
                if isinstance(value, tuple):
                    return f"1/{int(value[1]/value[0])}s" if value[0] else str(value)
                return f"{value}s"
            
            elif tag_name == 'FNumber':
                if isinstance(value, tuple):
                    return f"f/{value[0]/value[1]:.1f}"
                return f"f/{value}"
            
            elif tag_name == 'FocalLength':
                if isinstance(value, tuple):
                    return f"{value[0]/value[1]:.1f}mm"
                return f"{value}mm"
            
            elif tag_name == 'ISOSpeedRatings':
                return f"ISO {value}"
            
            elif tag_name == 'Flash':
                flash_modes = {
                    0: 'No Flash',
                    1: 'Fired',
                    5: 'Fired, Return not detected',
                    7: 'Fired, Return detected',
                    8: 'On, Did not fire',
                    9: 'On, Fired',
                    13: 'On, Return not detected',
                    15: 'On, Return detected',
                    16: 'Off, Did not fire',
                    24: 'Auto, Did not fire',
                    25: 'Auto, Fired',
                    29: 'Auto, Fired, Return not detected',
                    31: 'Auto, Fired, Return detected',
                }
                return flash_modes.get(value, f"Unknown ({value})")
            
            elif tag_name == 'MeteringMode':
                modes = {
                    0: 'Unknown', 1: 'Average', 2: 'Center-weighted average',
                    3: 'Spot', 4: 'Multi-spot', 5: 'Pattern', 6: 'Partial'
                }
                return modes.get(value, f"Unknown ({value})")
            
            elif tag_name == 'WhiteBalance':
                return 'Auto' if value == 0 else 'Manual'
            
            elif tag_name == 'ExposureProgram':
                programs = {
                    0: 'Not defined', 1: 'Manual', 2: 'Program AE',
                    3: 'Aperture-priority', 4: 'Shutter-priority',
                    5: 'Creative (slow speed)', 6: 'Action (high speed)',
                    7: 'Portrait', 8: 'Landscape'
                }
                return programs.get(value, f"Unknown ({value})")
                
        except:
            pass
        
        return str(value)
    
    # ==========================================================================
    # ANÁLISE DE STRINGS (para encontrar dados ocultos)
    # ==========================================================================
    
    def extract_strings(self, min_length=8):
        """Extrai strings legiveis do arquivo binario"""
        strings_found = {
            'emails': set(),
            'urls': set(),
            'ip_addresses': set(),
            'file_paths': set(),
            'phone_numbers': set(),
            'interesting_strings': set(),
        }
        
        try:
            with open(self.file_path, 'rb') as f:
                content = f.read()
            
            # Encontrar strings ASCII
            ascii_pattern = rb'[\x20-\x7e]{' + str(min_length).encode() + rb',}'
            ascii_strings = re.findall(ascii_pattern, content)
            
            # Encontrar strings UTF-16 (Windows)
            utf16_strings = []
            try:
                utf16_pattern = rb'(?:[\x20-\x7e]\x00){' + str(min_length).encode() + rb',}'
                utf16_matches = re.findall(utf16_pattern, content)
                utf16_strings = [m.decode('utf-16-le', errors='ignore') for m in utf16_matches]
            except:
                pass
            
            all_strings = [s.decode('ascii', errors='ignore') for s in ascii_strings] + utf16_strings
            
            for s in all_strings:
                s = s.strip()
                
                # Emails
                emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w{2,}', s)
                strings_found['emails'].update(emails)
                
                # URLs
                urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', s)
                strings_found['urls'].update(urls)
                
                # IPs
                ips = re.findall(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', s)
                # Filtrar IPs invalidos
                ips = [ip for ip in ips if not ip.startswith('0.') and ip != '255.255.255.255']
                strings_found['ip_addresses'].update(ips)
                
                # Paths Windows
                paths = re.findall(r'[A-Za-z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*', s)
                strings_found['file_paths'].update(paths)
                
                # Paths Unix
                unix_paths = re.findall(r'/(?:home|Users|var|etc|tmp|usr)/[^\s<>"{}|\\^`\[\]:]+', s)
                strings_found['file_paths'].update(unix_paths)
                
                # Telefones (varios formatos)
                phones = re.findall(r'[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}', s)
                phones = [p for p in phones if len(re.sub(r'\D', '', p)) >= 10]
                strings_found['phone_numbers'].update(phones)
                
                # Strings interessantes (nomes de software, versoes, etc.)
                if any(keyword in s.lower() for keyword in ['adobe', 'photoshop', 'lightroom', 'camera', 
                                                           'iphone', 'samsung', 'canon', 'nikon', 
                                                           'version', 'serial', 'license']):
                    if len(s) < 200:  # Evitar strings muito longas
                        strings_found['interesting_strings'].add(s)
            
            # Converter sets para lists e adicionar ao metadata
            result = {}
            for key, value in strings_found.items():
                if value:
                    items = list(value)[:30]  # Limitar a 30 resultados
                    result[key] = items
                    
                    # Marcar como sensivel
                    if key == 'emails':
                        for email in items[:5]:
                            self.sensitive_data.append(f"[!] Email in binary: {email}")
                    elif key == 'file_paths':
                        for path in items[:3]:
                            self.sensitive_data.append(f"[!] Path in binary: {path}")
                    elif key == 'ip_addresses':
                        for ip in items[:3]:
                            self.sensitive_data.append(f"[!] IP in binary: {ip}")
            
            if result:
                self.metadata['Strings_Analysis'] = result
                
        except Exception as e:
            print_status("error", f"Erro na analise de strings: {str(e)}")
    
    # ==========================================================================
    # HELPERS
    # ==========================================================================
    
    def _bytes_to_human(self, size):
        """Converte bytes para formato legivel"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"
    
    def _print_metadata(self, data, indent=0):
        """Imprime metadados formatados"""
        prefix = "    " * indent
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    print(f"{prefix}{Colors.CYAN}> {key}:{Colors.RESET}")
                    self._print_metadata(value, indent + 1)
                elif isinstance(value, list):
                    print(f"{prefix}{Colors.CYAN}> {key}: {Colors.DIM}[{len(value)} items]{Colors.RESET}")
                    for i, item in enumerate(value[:5]):  # Mostrar apenas 5
                        print(f"{prefix}    {Colors.DIM}* {item}{Colors.RESET}")
                    if len(value) > 5:
                        print(f"{prefix}    {Colors.DIM}... e mais {len(value) - 5} itens{Colors.RESET}")
                else:
                    # Truncar valores longos
                    str_value = str(value)
                    if len(str_value) > 70:
                        str_value = str_value[:67] + "..."
                    print(f"{prefix}{Colors.CYAN}> {key}:{Colors.RESET} {str_value}")
    
    def _count_fields(self, data):
        """Conta total de campos extraidos"""
        count = 0
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, dict):
                    count += self._count_fields(value)
                elif isinstance(value, list):
                    count += len(value)
                else:
                    count += 1
        return count
    
    # ==========================================================================
    # RUN PRINCIPAL
    # ==========================================================================
    
    def run(self):
        """Executa extracao completa de metadados"""
        print_module_header("ADVANCED METADATA EXTRACTOR")
        print(f"\n{Colors.CYAN}[*] Target File: {Colors.WHITE}{self.file_path}{Colors.RESET}\n")
        print_separator()
        
        if not os.path.exists(self.file_path):
            print_status("error", "Arquivo nao encontrado!")
            return {}
        
        # 1. Informacoes basicas do arquivo
        print_status("info", "Extraindo informacoes do arquivo...")
        self.extract_file_info()
        
        # 2. Hashes
        print_status("info", "Calculando hashes...")
        self.calculate_hashes()
        
        # 3. Extracao especifica por tipo
        file_ext = os.path.splitext(self.file_path)[1].lower()
        
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.tif', '.bmp', '.webp', '.heic', '.heif']:
            print_status("info", "Extraindo metadados de imagem (EXIF, XMP, IPTC, GPS)...")
            self.extract_image_metadata()
        
        # 4. Analise de strings (para qualquer arquivo)
        file_size = os.path.getsize(self.file_path)
        if file_size < 50 * 1024 * 1024:  # Menos de 50MB
            print_status("info", "Analisando strings no binario...")
            self.extract_strings()
        
        # ======================================================================
        # EXIBIR RESULTADOS
        # ======================================================================
        
        print_separator()
        print(f"\n{Colors.GREEN}+{'-' * 60}+")
        print(f"|{Colors.WHITE}{Colors.BOLD} {'METADADOS EXTRAIDOS'.center(58)} {Colors.GREEN}|")
        print(f"+{'-' * 60}+{Colors.RESET}\n")
        
        self._print_metadata(self.metadata)
        
        # ======================================================================
        # DADOS SENSÍVEIS
        # ======================================================================
        
        if self.sensitive_data:
            print(f"\n{Colors.RED}+{'-' * 60}+")
            print(f"|{Colors.WHITE}{Colors.BOLD} {'[!] DADOS SENSIVEIS ENCONTRADOS'.center(58)} {Colors.RED}|")
            print(f"+{'-' * 60}+{Colors.RESET}\n")
            
            for i, item in enumerate(self.sensitive_data, 1):
                print(f"    {Colors.YELLOW}{i:2}. {item}{Colors.RESET}")
        
        # ======================================================================
        # WARNINGS
        # ======================================================================
        
        if self.warnings:
            print(f"\n{Colors.YELLOW}+{'-' * 60}+")
            print(f"|{Colors.WHITE}{Colors.BOLD} {'[!] AVISOS'.center(58)} {Colors.YELLOW}|")
            print(f"+{'-' * 60}+{Colors.RESET}\n")
            
            for warning in self.warnings:
                print(f"    {Colors.YELLOW}[!] {warning}{Colors.RESET}")
        
        # Salvar resultados
        self.save_results()
        
        # Estatisticas finais
        total_fields = self._count_fields(self.metadata)
        print(f"\n{Colors.CYAN}[*] Total de campos extraidos: {Colors.WHITE}{total_fields}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Dados sensiveis encontrados: {Colors.RED}{len(self.sensitive_data)}{Colors.RESET}")
        
        return self.metadata
    
    def save_results(self):
        """Salva resultados em arquivo JSON"""
        filename = f"metadata_{os.path.basename(self.file_path)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output = {
            'extraction_info': {
                'tool': 'DAHMER OSINT Framework - Advanced Metadata Extractor',
                'version': '2.0.0',
                'extraction_date': datetime.now().isoformat(),
                'target_file': os.path.abspath(self.file_path),
            },
            'metadata': self.metadata,
            'sensitive_data': self.sensitive_data,
            'warnings': self.warnings,
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False, default=str)
        
        print_status("success", f"Resultados salvos em: {filename}")

# ==============================================================================
# MÓDULO 6: GOOGLE DORKER
# ==============================================================================

class GoogleDorker:
    def __init__(self, target):
        self.target = target
        self.dorks = {}
        self.results = []
        
        # Categorias de dorks
        self.dork_templates = {
            'Arquivos Sensiveis': [
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
            'Diretorios Expostos': [
                f'site:{target} intitle:"index of"',
                f'site:{target} intitle:"index of" "parent directory"',
                f'site:{target} intitle:"index of" password',
                f'site:{target} intitle:"index of" backup',
                f'site:{target} intitle:"index of" .git',
            ],
            'Paineis de Admin': [
                f'site:{target} inurl:admin',
                f'site:{target} inurl:login',
                f'site:{target} inurl:wp-admin',
                f'site:{target} inurl:administrator',
                f'site:{target} inurl:phpmyadmin',
                f'site:{target} inurl:cpanel',
                f'site:{target} inurl:webmail',
                f'site:{target} intitle:"dashboard"',
            ],
            'Informacoes Sensiveis': [
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
            'Git e Repositorios': [
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
        """Executa geracao de dorks"""
        print_module_header("GOOGLE DORKER")
        print(f"\n{Colors.CYAN}[*] Target: {Colors.WHITE}{self.target}{Colors.RESET}\n")
        print_separator()
        
        print(f"\n{Colors.GREEN}[+] Google Dorks gerados para {self.target}:{Colors.RESET}\n")
        
        all_dorks = []
        
        for category, dorks in self.dork_templates.items():
            print(f"\n{Colors.YELLOW}=== {category} ==={Colors.RESET}\n")
            for dork in dorks:
                encoded_dork = quote_plus(dork)
                google_url = f"https://www.google.com/search?q={encoded_dork}"
                print(f"    {Colors.CYAN}->{Colors.RESET} {dork}")
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
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dorks, f, indent=4)
        print_status("success", f"Resultados salvos em {filename}")
        
        # Tambem salva em formato texto para facil uso
        txt_filename = f"dorks_{self.target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(txt_filename, 'w', encoding='utf-8') as f:
            for dork in dorks:
                f.write(f"{dork['dork']}\n")
        print_status("success", f"Lista de dorks salva em {txt_filename}")

# ==============================================================================
# MÓDULO 7: IP GEOLOCATION
# ==============================================================================

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
        """Executa geolocalizacao de IP"""
        print_module_header("IP GEOLOCATION")
        print(f"\n{Colors.CYAN}[*] Target IP: {Colors.WHITE}{self.ip}{Colors.RESET}\n")
        print_separator()
        
        print_status("info", f"Consultando informacoes para {self.ip}...")
        
        # Consulta multiplas fontes
        ipapi_data = self.lookup_ipapi()
        ipinfo_data = self.lookup_ipinfo()
        reverse = self.reverse_dns()
        
        # Consolida informacoes
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
        print(f"\n{Colors.GREEN}[+] Informacoes do IP:{Colors.RESET}\n")
        
        for key, value in self.info.items():
            print(f"    {Colors.CYAN}{key}:{Colors.RESET} {value}")
        
        # Mostra mapa
        if self.info.get('Latitude') != 'N/A' and self.info.get('Longitude') != 'N/A':
            maps_url = f"https://www.google.com/maps?q={self.info['Latitude']},{self.info['Longitude']}"
            print(f"\n    {Colors.YELLOW}[!] Google Maps:{Colors.RESET} {maps_url}")
        
        self.save_results()
        return self.info
    
    def save_results(self):
        """Salva resultados em arquivo"""
        filename = f"ip_{self.ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.info, f, indent=4)
        print_status("success", f"Resultados salvos em {filename}")

# ==============================================================================
# MÓDULO 8: FULL RECON
# ==============================================================================

class FullRecon:
    def __init__(self, target):
        self.target = target
        self.results = {}
    
    def run(self):
        """Executa reconhecimento completo"""
        print_module_header("FULL RECONNAISSANCE")
        print(f"\n{Colors.CYAN}[*] Target: {Colors.WHITE}{self.target}{Colors.RESET}\n")
        print_separator()
        
        print_status("info", "Iniciando reconhecimento completo...")
        print_status("warning", "Este processo pode demorar alguns minutos...\n")
        
        # 1. WHOIS
        print(f"\n{Colors.YELLOW}=== WHOIS ==={Colors.RESET}\n")
        whois_lookup = WhoisLookup(self.target)
        self.results['whois'] = whois_lookup.lookup()
        
        input(f"\n{Colors.CYAN}Pressione ENTER para continuar...{Colors.RESET}")
        
        # 2. Subdomains
        print(f"\n{Colors.YELLOW}=== SUBDOMAINS ==={Colors.RESET}\n")
        subdomain_enum = SubdomainEnumerator(self.target)
        self.results['subdomains'] = list(subdomain_enum.run())
        
        input(f"\n{Colors.CYAN}Pressione ENTER para continuar...{Colors.RESET}")
        
        # 3. Emails
        print(f"\n{Colors.YELLOW}=== EMAILS ==={Colors.RESET}\n")
        email_harvester = EmailHarvester(self.target)
        self.results['emails'] = list(email_harvester.run())
        
        input(f"\n{Colors.CYAN}Pressione ENTER para continuar...{Colors.RESET}")
        
        # 4. Google Dorks
        print(f"\n{Colors.YELLOW}=== GOOGLE DORKS ==={Colors.RESET}\n")
        dorker = GoogleDorker(self.target)
        self.results['dorks'] = dorker.run()
        
        # Resumo final
        print_separator()
        print(f"\n{Colors.GREEN}=== RESUMO DO RECONHECIMENTO ==={Colors.RESET}\n")
        
        print(f"""
    {Colors.CYAN}+------------------------------------------------------------------+
    |{Colors.WHITE}                    RECONNAISSANCE SUMMARY                        {Colors.CYAN}|
    +------------------------------------------------------------------+
    |{Colors.RESET}  Target:              {self.target:<43}{Colors.CYAN}|
    |{Colors.RESET}  Subdomains Found:    {len(self.results.get('subdomains', [])):<43}{Colors.CYAN}|
    |{Colors.RESET}  Emails Found:        {len(self.results.get('emails', [])):<43}{Colors.CYAN}|
    |{Colors.RESET}  Dorks Generated:     {len(self.results.get('dorks', [])):<43}{Colors.CYAN}|
    +------------------------------------------------------------------+{Colors.RESET}
        """)
        
        self.save_results()
        return self.results
    
    def save_results(self):
        """Salva todos os resultados em arquivo"""
        filename = f"full_recon_{self.target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=4, default=str)
        print_status("success", f"Relatorio completo salvo em {filename}")


# ==============================================================================
# FUNÇÕES AUXILIARES
# ==============================================================================

def get_user_input(prompt, allow_empty=False):
    """Obtem input do usuario com validacao"""
    while True:
        user_input = input(f"\n{Colors.CYAN}[?]{Colors.RESET} {prompt}: ").strip()
        if user_input or allow_empty:
            return user_input
        print_status("warning", "Input nao pode ser vazio!")

def pause():
    """Pausa a execucao ate o usuario pressionar ENTER"""
    input(f"\n{Colors.CYAN}Pressione ENTER para voltar ao menu...{Colors.RESET}")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Funcao principal do framework"""
    
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        choice = input(f"{Colors.GREEN}┌──({Colors.CYAN}{AUTHOR}{Colors.GREEN}㉿{Colors.CYAN}dahmer-osint{Colors.GREEN})-[{Colors.WHITE}~{Colors.GREEN}]\n└─{Colors.WHITE}$ {Colors.RESET}").strip()
        
        try:
            if choice == '1':
                # Email Harvester
                domain = get_user_input("Digite o dominio alvo (ex: example.com)")
                harvester = EmailHarvester(domain)
                harvester.run()
                pause()
                
            elif choice == '2':
                # Subdomain Enumerator
                domain = get_user_input("Digite o dominio alvo (ex: example.com)")
                enumerator = SubdomainEnumerator(domain)
                enumerator.run()
                pause()
                
            elif choice == '3':
                # WHOIS Lookup
                target = get_user_input("Digite o dominio ou IP")
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
                # Metadata Extractor (AGORA USANDO O MÓDULO AVANÇADO)
                file_path = get_user_input("Digite o caminho do arquivo")
                extractor = MetadataExtractor(file_path)
                extractor.run()
                pause()
                
            elif choice == '6':
                # Google Dorker
                target = get_user_input("Digite o dominio alvo (ex: example.com)")
                dorker = GoogleDorker(target)
                dorker.run()
                pause()
                
            elif choice == '7':
                # IP Geolocation
                ip = get_user_input("Digite o endereco IP")
                geo = IPGeolocation(ip)
                geo.run()
                pause()
                
            elif choice == '8':
                # Full Recon
                target = get_user_input("Digite o dominio alvo para recon completo")
                recon = FullRecon(target)
                recon.run()
                pause()
                
            elif choice == '0':
                # Exit
                clear_screen()
                print(f"""
{Colors.RED}
    +------------------------------------------------------------------+
    |                                                                  |
    |           ██████╗  ██████╗  ██████╗ ██████╗ ██████╗ ██╗   ██╗███████╗  |
    |          ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝  |
    |          ██║  ███╗██║   ██║██║   ██║██║  ██║██████╔╝ ╚████╔╝ █████╗    |
    |          ██║   ██║██║   ██║██║   ██║██║  ██║██╔══██╗  ╚██╔╝  ██╔══╝    |
    |          ╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   ███████╗  |
    |           ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝  |
    |                                                                  |
    |                Thanks for using DAHMER OSINT Framework!          |
    |                         Stay safe & ethical!                     |
    |                                                                  |
    +------------------------------------------------------------------+
{Colors.RESET}
                """)
                print(f"    {Colors.DIM}Created by {AUTHOR} | Version {VERSION}{Colors.RESET}\n")
                sys.exit(0)
                
            else:
                print_status("error", "Opcao invalida!")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print_status("warning", "\nOperacao cancelada pelo usuario!")
            time.sleep(1)
        except Exception as e:
            print_status("error", f"Erro: {str(e)}")
            pause()


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    # Verifica se esta rodando como root (recomendado para algumas funcoes)
    if os.name != 'nt' and os.geteuid() != 0:
        print(f"{Colors.YELLOW}[!] Algumas funcoes podem requerer privilegios de root.{Colors.RESET}")
    
    # Argumentos de linha de comando para uso direto
    parser = argparse.ArgumentParser(
        description=f'{TOOL_NAME} - Advanced OSINT Framework by {AUTHOR}',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  python osint.py                    # Modo interativo
  python osint.py -e example.com     # Email harvesting
  python osint.py -s example.com     # Subdomain enumeration
  python osint.py -w example.com     # WHOIS lookup
  python osint.py -u johndoe         # Username OSINT
  python osint.py -g example.com     # Google dorks
  python osint.py -i 8.8.8.8         # IP geolocation
  python osint.py -f example.com     # Full recon
        """
    )
    
    parser.add_argument('-e', '--email', metavar='DOMAIN', help='Email harvesting para o dominio')
    parser.add_argument('-s', '--subdomain', metavar='DOMAIN', help='Enumeracao de subdominios')
    parser.add_argument('-w', '--whois', metavar='TARGET', help='WHOIS lookup')
    parser.add_argument('-u', '--username', metavar='USERNAME', help='Username OSINT')
    parser.add_argument('-m', '--metadata', metavar='FILE', help='Extracao de metadados')
    parser.add_argument('-g', '--dorks', metavar='DOMAIN', help='Google dorks generator')
    parser.add_argument('-i', '--ip', metavar='IP', help='IP geolocation')
    parser.add_argument('-f', '--full', metavar='DOMAIN', help='Full reconnaissance')
    parser.add_argument('-v', '--version', action='version', version=f'{TOOL_NAME} v{VERSION}')
    
    args = parser.parse_args()
    
    # Execucao via argumentos
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