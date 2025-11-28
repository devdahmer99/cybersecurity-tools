# DAHMER OSINT Framework - Windows ExifTool Installer
# PowerShell script para instalação automática do ExifTool no Windows
# Created by devdahmer99

param(
    [switch]$Force,
    [switch]$Chocolatey,
    [switch]$Manual,
    [string]$InstallPath = "C:\exiftool"
)

# Função para escrever mensagens coloridas
function Write-StatusMessage {
    param(
        [string]$Message,
        [string]$Type = "Info"
    )
    
    switch ($Type) {
        "Success" { Write-Host "[SUCCESS] $Message" -ForegroundColor Green }
        "Error"   { Write-Host "[ERROR] $Message" -ForegroundColor Red }
        "Warning" { Write-Host "[WARNING] $Message" -ForegroundColor Yellow }
        "Info"    { Write-Host "[INFO] $Message" -ForegroundColor Cyan }
    }
}

# Função para verificar se é administrador
function Test-Administrator {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Função para verificar se ExifTool já está instalado
function Test-ExifToolInstalled {
    try {
        $result = & exiftool -ver 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "ExifTool v$result já está instalado!" "Success"
            return $true
        }
    } catch {
        # ExifTool não encontrado
    }
    return $false
}

# Função para instalar via Chocolatey
function Install-ViaChocolatey {
    try {
        # Verificar se Chocolatey está instalado
        $chocoVersion = & choco --version 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-StatusMessage "Chocolatey não encontrado. Instalando Chocolatey primeiro..." "Info"
            
            # Instalar Chocolatey
            Set-ExecutionPolicy Bypass -Scope Process -Force
            [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
            Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
            
            if ($LASTEXITCODE -ne 0) {
                throw "Falha na instalação do Chocolatey"
            }
            
            # Recarregar PATH
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        }
        
        Write-StatusMessage "Instalando ExifTool via Chocolatey..." "Info"
        & choco install exiftool -y
        
        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "ExifTool instalado com sucesso via Chocolatey!" "Success"
            return $true
        } else {
            throw "Falha na instalação via Chocolatey"
        }
    } catch {
        Write-StatusMessage "Erro na instalação via Chocolatey: $_" "Error"
        return $false
    }
}

# Função para instalação manual
function Install-Manually {
    param([string]$Path = "C:\exiftool")
    
    try {
        Write-StatusMessage "Iniciando instalação manual em $Path..." "Info"
        
        # Criar diretório
        if (!(Test-Path $Path)) {
            New-Item -ItemType Directory -Path $Path -Force | Out-Null
        }
        
        # URL do ExifTool
        $downloadUrl = "https://exiftool.org/exiftool-12.70.zip"
        $zipPath = Join-Path $Path "exiftool.zip"
        
        Write-StatusMessage "Baixando ExifTool..." "Info"
        
        # Baixar arquivo
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($downloadUrl, $zipPath)
        
        Write-StatusMessage "Extraindo arquivos..." "Info"
        
        # Extrair ZIP
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        [System.IO.Compression.ZipFile]::ExtractToDirectory($zipPath, $Path)
        
        # Encontrar e renomear exiftool(-k).exe
        $exiftoolExe = Get-ChildItem -Path $Path -Name "*exiftool*.exe" -Recurse | Select-Object -First 1
        if ($exiftoolExe) {
            $sourcePath = Join-Path $Path $exiftoolExe
            $targetPath = Join-Path $Path "exiftool.exe"
            
            if ($exiftoolExe -like "*(-k)*") {
                Move-Item $sourcePath $targetPath -Force
            }
        }
        
        # Limpar arquivo ZIP
        Remove-Item $zipPath -Force
        
        # Adicionar ao PATH
        $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
        if ($currentPath -notlike "*$Path*") {
            Write-StatusMessage "Adicionando $Path ao PATH do sistema..." "Info"
            [Environment]::SetEnvironmentVariable("Path", "$currentPath;$Path", "Machine")
        }
        
        Write-StatusMessage "ExifTool instalado com sucesso em $Path!" "Success"
        Write-StatusMessage "IMPORTANTE: Reinicie o PowerShell para que o PATH seja atualizado." "Warning"
        
        return $true
        
    } catch {
        Write-StatusMessage "Erro na instalação manual: $_" "Error"
        return $false
    }
}

# Função para testar a instalação
function Test-Installation {
    Write-StatusMessage "Testando instalação..." "Info"
    
    # Recarregar PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    try {
        $version = & exiftool -ver 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "? ExifTool v$version está funcionando corretamente!" "Success"
            
            # Testar com arquivo de exemplo
            $testResult = & exiftool -j -ver 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-StatusMessage "? Modo JSON funcionando corretamente!" "Success"
            }
            
            return $true
        }
    } catch {
        Write-StatusMessage "? ExifTool não está funcionando corretamente" "Error"
        Write-StatusMessage "Tente reiniciar o PowerShell ou adicionar manualmente ao PATH" "Warning"
    }
    
    return $false
}

# Função principal
function Main {
    Write-Host @"

????????????????????????????????????????????????????????????????????
?              DAHMER OSINT - ExifTool Windows Installer          ?
?                     PowerShell Auto-Installer                   ?
????????????????????????????????????????????????????????????????????

"@ -ForegroundColor Cyan

    # Verificar se já está instalado
    if ((Test-ExifToolInstalled) -and !$Force) {
        Write-StatusMessage "ExifTool já está instalado. Use -Force para reinstalar." "Warning"
        return
    }
    
    # Verificar privilégios de administrador
    if (!(Test-Administrator)) {
        Write-StatusMessage "Executando sem privilégios de administrador." "Warning"
        Write-StatusMessage "Algumas funcionalidades podem não funcionar corretamente." "Warning"
    }
    
    $installSuccess = $false
    
    # Escolher método de instalação
    if ($Chocolatey -or (!$Manual -and !$Chocolatey)) {
        Write-StatusMessage "Tentando instalação via Chocolatey..." "Info"
        $installSuccess = Install-ViaChocolatey
    }
    
    if (!$installSuccess -and ($Manual -or !$Chocolatey)) {
        Write-StatusMessage "Tentando instalação manual..." "Info"
        $installSuccess = Install-Manually -Path $InstallPath
    }
    
    if ($installSuccess) {
        # Testar instalação
        Start-Sleep -Seconds 2
        if (Test-Installation) {
            Write-Host @"

????????????????????????????????????????????????????????????????????
?                    INSTALAÇÃO CONCLUÍDA!                        ?
????????????????????????????????????????????????????????????????????

ExifTool foi instalado com sucesso!

Para usar com DAHMER OSINT Framework:
1. Reinicie o PowerShell
2. Execute: python osint.py
3. Selecione opção 5 (Metadata Extractor)
4. Selecione opção 11 (ExifTool Status)

"@ -ForegroundColor Green
        } else {
            Write-StatusMessage "Instalação pode estar incompleta. Reinicie o PowerShell e teste novamente." "Warning"
        }
    } else {
        Write-Host @"

????????????????????????????????????????????????????????????????????
?                    INSTALAÇÃO FALHADA!                          ?
????????????????????????????????????????????????????????????????????

Para instalação manual:
1. Baixe de: https://exiftool.org/
2. Extraia para C:\exiftool\
3. Renomeie exiftool(-k).exe para exiftool.exe
4. Adicione C:\exiftool ao PATH do Windows

"@ -ForegroundColor Red
    }
}

# Executar instalação
try {
    Main
} catch {
    Write-StatusMessage "Erro inesperado: $_" "Error"
    Write-StatusMessage "Tente executar como Administrador ou instalar manualmente." "Warning"
} finally {
    Write-Host "`nPressione qualquer tecla para continuar..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}