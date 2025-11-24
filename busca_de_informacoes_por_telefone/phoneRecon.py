import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests
import sys
import webbrowser
import time

# --- CONFIGURAÇÃO GLOBAL ---
# Cadastre-se em numverify.com (Plano Free) para obter sua chave.
# Se deixar vazio "", o script pulará a etapa de API.
API_KEY = "ed4f47d485b04d6f8b331df7cfeb0181" 

# --- CORES DO TERMINAL ---
R = "\033[1;31m"  # Red
G = "\033[0;32m"  # Green
Y = "\033[1;33m"  # Yellow
C = "\033[1;36m"  # Cyan
W = "\033[0;0m"   # Reset (White)

def banner():
    print(f"{C}")
    print("="*65)
    print(f"   PHONE HUNTER v5.0 - ADVANCED OSINT & RECON TOOL")
    print(f"   Blackbox Edition | HLR Check | Dorking Automation")
    print("="*65 + f"{W}")

def limpar_numero(raw_input):
    """Remove caracteres não numéricos"""
    return "".join(filter(str.isdigit, raw_input))

def gerar_dorks(numero, codigo_pais="55"):
    """Gera links de inteligência para busca manual"""
    print(f"\n{Y}[*] Gerando Vetores de Busca (OSINT)...{W}")
    
    # Prepara variações para busca
    num_full = f"{codigo_pais}{numero}"
    
    dorks = {
        "WhatsApp Direto (API)": f"https://api.whatsapp.com/send?phone={num_full}",
        "Telegram Direto": f"https://t.me/+{num_full}",
        "Google (Busca Estrita)": f"https://www.google.com/search?q=%22{num_full}%22",
        "Google (Busca Hifenizada)": f"https://www.google.com/search?q=%22{numero}%22+OR+%22{num_full}%22",
        "Facebook (Perfil/Post)": f"https://www.google.com/search?q=site:facebook.com+%22{numero}%22",
        "Instagram (Bio)": f"https://www.google.com/search?q=site:instagram.com+%22{numero}%22",
        "Twitter/X (Leaks)": f"https://www.google.com/search?q=site:twitter.com+%22{numero}%22",
        "Linkedin (Profissional)": f"https://www.google.com/search?q=site:linkedin.com+%22{numero}%22",
        "Pastebin (Vazamentos)": f"https://www.google.com/search?q=site:pastebin.com+%22{num_full}%22",
        "Busca em PDF (Docs)": f"https://www.google.com/search?q=filetype:pdf+%22{numero}%22",
        "TrueCaller (Web)": f"https://www.truecaller.com/search/br/{numero}",
        "Sync.me (Sync)": f"https://sync.me/search/?number={num_full}"
    }

    print(f"{C}--- CLIQUE PARA INVESTIGAR ---{W}")
    for nome, link in dorks.items():
        print(f"[{G}+{W}] {nome}:\n    {link}")

def consulta_numverify(numero_formatado):
    """Consulta API HLR real"""
    if not API_KEY:
        print(f"\n{R}[!] API Key do NumVerify não configurada. Pulando HLR Real.{W}")
        return

    print(f"\n{Y}[*] Consultando API NumVerify (HLR Lookup)...{W}")
    url = f"http://apilayer.net/api/validate?access_key={API_KEY}&number={numero_formatado}&country_code=&format=1"
    
    try:
        req = requests.get(url)
        data = req.json()

        if data.get("valid") is True:
            print(f"{G}[SUCCESS] Dados Obtidos:{W}")
            print(f"   > Operadora Atual:  {G}{data.get('carrier')}{W}")
            print(f"   > Localização:      {data.get('location')}")
            print(f"   > Tipo de Linha:    {data.get('line_type')}")
        else:
            erro = data.get('error', {}).get('type', 'Desconhecido')
            print(f"{R}[ERROR] Falha na API: {erro}{W}")

    except Exception as e:
        print(f"{R}[!] Erro de conexão: {e}{W}")

def analisar_variacoes(numero_limpo):
    """Tenta lidar com a confusão do 9º dígito no Brasil"""
    
    # Remove o 55 se o usuário colocou, para padronizar
    if numero_limpo.startswith("55") and len(numero_limpo) > 11:
        numero_limpo = numero_limpo[2:]
        
    candidatos = []
    
    # 1. O número exatamente como digitado
    candidatos.append(numero_limpo)
    
    # 2. Lógica Brasileira (DDD + 8 ou 9 dígitos)
    # Se tem 10 dígitos (Ex: 51 9999 9999), pode ser um fixo ou celular antigo
    if len(numero_limpo) == 10:
        # Cria versão com 9 dígitos (celular moderno)
        versao_9 = f"{numero_limpo[:2]}9{numero_limpo[2:]}"
        candidatos.append(versao_9)
    
    # Se tem 11 dígitos, pode ser que o usuário já digitou certo, 
    # mas vamos garantir que a versão "sem o 9" também seja verificada para WhatsApp antigo
    elif len(numero_limpo) == 11:
        versao_8 = f"{numero_limpo[:2]}{numero_limpo[3:]}" # Remove o 3º digito (o 9)
        candidatos.append(versao_8)

    print(f"\n{Y}[*] Analisando Variações Possíveis...{W}")
    
    encontrou_valido = False
    
    for num in candidatos:
        try:
            # Tenta parsear como BR
            parsed = phonenumbers.parse(num, "BR")
            
            # Formatações
            fmt_intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            fmt_e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            
            # Validação
            is_valid = phonenumbers.is_valid_number(parsed)
            
            marcador = f"{G}VÁLIDO{W}" if is_valid else f"{R}INVÁLIDO/LEGACY{W}"
            
            print(f"\n--- Análise: {fmt_intl} [{marcador}] ---")
            
            if is_valid:
                encontrou_valido = True
                print(f"   > Local (Estático): {geocoder.description_for_number(parsed, 'pt-br')}")
                print(f"   > Operadora (Orig): {carrier.name_for_number(parsed, 'pt-br')}")
                print(f"   > Formato E.164:    {fmt_e164}")
                
                # Chama API apenas para o número válido
                if API_KEY:
                    consulta_numverify(fmt_e164.replace("+", ""))
            else:
                print(f"   > Nota: Pode ser um número antigo (WhatsApp) ou inexistente.")

            # Gera Dorks para TODAS as versões (o alvo pode usar número antigo no Face/Whats)
            gerar_dorks(num)
            
        except Exception as e:
            print(f"{R}Erro ao processar variação {num}: {e}{W}")

    if not encontrou_valido:
        print(f"\n{R}[!] Aviso: Nenhuma das variações parece ser um número de celular ATIVO na rede atual.{W}")
        print(f"{R}    Verifique se o DDD está correto. O script gerou os links mesmo assim.{W}")

def main():
    banner()
    raw = input(f"\n{C}Digite o Alvo (Ex: 51999998888): {W}")
    
    limpo = limpar_numero(raw)
    
    if len(limpo) < 8:
        print(f"{R}[!] Erro: Número muito curto.{W}")
        sys.exit()
        
    analisar_variacoes(limpo)
    print(f"\n{C}[*] Reconhecimento Finalizado.{W}")

if __name__ == "__main__":
    main()
