#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DAHMER OSINT Framework - ExifTool Auto Installer
Instalador automático do ExifTool para Windows e Linux
Created by devdahmer99
"""

import os
import sys
import platform
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path

def print_status(status, message):
    """Função para imprimir status colorido"""
    colors = {
        'info': '\033[94m[INFO]\033[0m',
        'success': '\033[92m[SUCCESS]\033[0m', 
        'warning': '\033[93m[WARNING]\033[0m',
        'error': '\033[91m[ERROR]\033[0m'
    }
    print(f"{colors.get(status, '')} {message}")

def check_admin():
    """Verifica se o script está sendo executado como administrador"""
    try:
        if platform.system() == 'Windows':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except:
        return False

def install_windows():
    """Instala ExifTool no Windows"""
    print_status('info', 'Instalando ExifTool no Windows...')
    
    try:
        # Verificar se Chocolatey está disponível
        result = subprocess.run(['choco', '--version'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print_status('info', 'Chocolatey encontrado! Instalando via Chocolatey...')
            subprocess.run(['choco', 'install', 'exiftool', '-y'], check=True)
            print_status('success', 'ExifTool instalado via Chocolatey!')
            return True
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_status('warning', 'Chocolatey não encontrado. Fazendo instalação manual...')
    
    # Instalação manual
    try:
        install_dir = Path('C:/exiftool')
        install_dir.mkdir(exist_ok=True)
        
        print_status('info', 'Baixando ExifTool...')
        url = 'https://exiftool.org/exiftool-12.70.zip'
        zip_path = install_dir / 'exiftool.zip'
        
        urllib.request.urlretrieve(url, zip_path)
        
        print_status('info', 'Extraindo arquivos...')
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(install_dir)
        
        # Renomear exiftool(-k).exe para exiftool.exe
        for file in install_dir.glob('**/exiftool*.exe'):
            if 'exiftool(-k)' in file.name:
                file.rename(install_dir / 'exiftool.exe')
                break
        
        # Limpar arquivo zip
        zip_path.unlink()
        
        print_status('success', f'ExifTool instalado em {install_dir}')
        print_status('warning', f'Adicione {install_dir} ao PATH do Windows para usar globalmente')
        
        return True
        
    except Exception as e:
        print_status('error', f'Erro na instalação manual: {str(e)}')
        return False

def install_linux():
    """Instala ExifTool no Linux"""
    print_status('info', 'Instalando ExifTool no Linux...')
    
    # Detectar distribuição
    try:
        with open('/etc/os-release', 'r') as f:
            os_info = f.read().lower()
            
        if 'ubuntu' in os_info or 'debian' in os_info:
            print_status('info', 'Sistema Ubuntu/Debian detectado...')
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'libimage-exiftool-perl'], check=True)
            
        elif 'centos' in os_info or 'rhel' in os_info or 'fedora' in os_info:
            print_status('info', 'Sistema CentOS/RHEL/Fedora detectado...')
            try:
                subprocess.run(['sudo', 'dnf', 'install', '-y', 'perl-Image-ExifTool'], check=True)
            except:
                subprocess.run(['sudo', 'yum', 'install', '-y', 'perl-Image-ExifTool'], check=True)
                
        elif 'arch' in os_info:
            print_status('info', 'Sistema Arch Linux detectado...')
            subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'perl-image-exiftool'], check=True)
            
        else:
            print_status('warning', 'Distribuição não reconhecida. Tentando instalação genérica...')
            # Instalação manual via CPAN
            subprocess.run(['sudo', 'cpan', 'Image::ExifTool'], check=True)
            
        print_status('success', 'ExifTool instalado com sucesso!')
        return True
        
    except subprocess.CalledProcessError as e:
        print_status('error', f'Erro durante a instalação: {str(e)}')
        return False
    except Exception as e:
        print_status('error', f'Erro inesperado: {str(e)}')
        return False

def verify_installation():
    """Verifica se ExifTool foi instalado corretamente"""
    try:
        if platform.system() == 'Windows':
            result = subprocess.run(['where', 'exiftool'], 
                                  capture_output=True, text=True, timeout=5)
        else:
            result = subprocess.run(['which', 'exiftool'], 
                                  capture_output=True, text=True, timeout=5)
            
        if result.returncode == 0:
            # Testar versão
            version_result = subprocess.run(['exiftool', '-ver'], 
                                          capture_output=True, text=True, timeout=5)
            if version_result.returncode == 0:
                version = version_result.stdout.strip()
                print_status('success', f'ExifTool {version} está funcionando corretamente!')
                return True
                
    except Exception as e:
        print_status('error', f'Erro ao verificar instalação: {str(e)}')
    
    return False

def main():
    """Função principal"""
    print("""
????????????????????????????????????????????????????????????????????
?                    DAHMER OSINT - ExifTool Installer             ?
?                         Auto-installer for ExifTool             ?
????????????????????????????????????????????????????????????????????
""")
    
    system = platform.system()
    print_status('info', f'Sistema detectado: {system}')
    
    if system == 'Windows':
        if not install_windows():
            print_status('error', 'Falha na instalação do Windows')
            return False
    elif system == 'Linux':
        if not install_linux():
            print_status('error', 'Falha na instalação do Linux')
            return False
    else:
        print_status('error', f'Sistema {system} não suportado pelo instalador automático')
        print('Por favor, instale ExifTool manualmente: https://exiftool.org/install.html')
        return False
    
    # Verificar instalação
    print_status('info', 'Verificando instalação...')
    if verify_installation():
        print_status('success', 'Instalação concluída com sucesso!')
        print('\nAgora você pode usar o DAHMER OSINT Framework com suporte completo ao ExifTool!')
        return True
    else:
        print_status('error', 'ExifTool não foi encontrado após a instalação')
        print('Você pode precisar reiniciar o terminal ou adicionar ExifTool ao PATH')
        return False

if __name__ == '__main__':
    try:
        if not main():
            sys.exit(1)
    except KeyboardInterrupt:
        print_status('warning', 'Instalação cancelada pelo usuário')
        sys.exit(1)
    except Exception as e:
        print_status('error', f'Erro inesperado: {str(e)}')
        sys.exit(1)