import requests
import sys
import argparse
from colorama import init, Fore, Style
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

def banner():
    print(Fore.CYAN + """
    ##############################################
    #    HTTP VERB ENUMERATOR - Eduardo Dahmer   #
    #    Identify Allowed Methods (OPTIONS + Fuzz) #
    ##############################################
    """ + Style.RESET_ALL)

def check_options_header(url):
    """
    Tenta obter os métodos permitidos via cabeçalho 'Allow' (RFC Standard)
    """
    print(f"\n{Fore.YELLOW}[*] Verificando via método OPTIONS (Standard)...{Style.RESET_ALL}")
    try:
        response = requests.options(url, verify=False, timeout=10)
        allow_header = response.headers.get('Allow')
        
        if allow_header:
            print(f"{Fore.GREEN}[+] Cabeçalho 'Allow' encontrado: {allow_header}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] O servidor respondeu ao OPTIONS, mas não enviou o cabeçalho 'Allow'.{Style.RESET_ALL}")
            print(f"    Status Code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[!] Erro ao conectar: {e}{Style.RESET_ALL}")

def active_fuzzing(url):
    """
    Testa cada método individualmente e analisa o status code.
    Útil quando o OPTIONS é bloqueado ou mentiroso.
    """
    print(f"\n{Fore.YELLOW}[*] Iniciando Fuzzing Ativo de Métodos...{Style.RESET_ALL}")
    
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'HEAD', 'CONNECT', 'PATCH']
    
    for method in methods:
        try:
            res = requests.request(method, url, verify=False, timeout=5)
            
            if res.status_code == 405:
                print(f"{Fore.RED}[x] {method}: 405 - Not Allowed{Style.RESET_ALL}")
            elif res.status_code == 501:
                print(f"{Fore.RED}[x] {method}: 501 - Not Implemented{Style.RESET_ALL}")
            elif res.status_code in [200, 201, 202]:
                print(f"{Fore.GREEN}[+] {method}: {res.status_code} - ACEITO (Investigar!){Style.RESET_ALL}")
            elif res.status_code in [401, 403]:
                print(f"{Fore.YELLOW}[!] {method}: {res.status_code} - Existe (Requer Auth/Proibido){Style.RESET_ALL}")
            else:
                print(f"{Fore.BLUE}[?] {method}: {res.status_code} - Resposta Incomum{Style.RESET_ALL}")
                
        except requests.exceptions.RequestException:
            print(f"{Fore.RED}[Error] Falha ao testar {method}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="Enumerador de Métodos HTTP")
    parser.add_argument("url", help="URL alvo (ex: http://localhost:8000/adminDashboard.php)")
    args = parser.parse_args()

    target = args.url
    
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target

    banner()
    print(f"Alvo: {target}")
    
    check_options_header(target)
    
    active_fuzzing(target)

if __name__ == "__main__":
    main()
