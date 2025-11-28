# ?? Como Testar sua Ferramenta OSINT com Imagens Reais

## ?? Método 1: Menu Interativo (Mais Fácil)

```bash
python osint.py
```

**Então:**
- **Opção 5**: Metadata Extractor (análise completa)
- **Opção 6**: Geolocation Analyzer (só GPS/localização)

Digite o caminho para sua imagem quando solicitado.

## ??? Método 2: Linha de Comando (Mais Rápido)

```bash
# Análise completa de metadados
python osint.py -m "C:\caminho\para\sua_foto.jpg"

# Análise só de GPS/localização  
python osint.py -l "C:\caminho\para\sua_foto.jpg"
```

## ?? Onde Encontrar Imagens para Testar

### ? **Imagens Seguras para Teste:**

1. **Fotos suas antigas**: 
   - Fotos do smartphone com GPS ativo
   - Screenshots salvos como imagem
   - Fotos de câmera digital

2. **Criar imagem de teste**:
   ```bash
   # Execute este comando para criar uma imagem de teste
   python -c "from PIL import Image; img=Image.new('RGB',(400,300),'blue'); img.save('teste.jpg'); print('Imagem teste.jpg criada!')"
   
   # Depois teste com:
   python osint.py -m teste.jpg
   ```

3. **Download de imagens públicas**:
   - Imagens de exemplo da internet (sem direitos autorais)
   - Imagens de bancos de imagens gratuitos
   - Screenshots de mapas

### ?? **CUIDADO - NÃO use:**
- Fotos de outras pessoas sem permissão
- Imagens corporativas confidenciais  
- Arquivos de investigações ativas

## ?? Exemplo Prático Passo a Passo

### **1. Criar arquivo de teste:**
```bash
# Abra o PowerShell na pasta da ferramenta
cd "C:\Users\ecorrea\cybersecurity-tools\dahmer_osint_framework"

# Execute a ferramenta no modo interativo
python osint.py
```

### **2. No menu, escolha:**
```
???(devdahmer99?dahmer-osint)-[~]
??$ 5

Digite o caminho do arquivo: teste.jpg
```

### **3. Resultado esperado:**
```
[INFO] Extraindo informações do arquivo...
[INFO] Calculando hashes...
[INFO] Analisando dados de geolocalização...

+----------------------------------------------------------+
|                    METADADOS EXTRAÍDOS                  |
+----------------------------------------------------------+

> File_Information:
    > File_Name: teste.jpg
    > File_Size_Human: 2.34 KB
    > Created_Time: 2024-11-25 15:30:45

> Hashes:
    > MD5: d41d8cd98f00b204e9800998ecf8427e
    > SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

?? GEOLOCALIZAÇÃO DETECTADA (se houver GPS)
   GPS: 40.758000, -73.985500
   ?? Endereço: Times Square, Manhattan, New York
   ?? Google Maps: https://www.google.com/maps?q=40.758,-73.9855

?? DADOS SENSÍVEIS ENCONTRADOS
   [!] GPS LOCATION FOUND: 40.758000, -73.985500
   [!] Google Maps: https://www.google.com/maps?q=40.758,-73.9855

? Resultados salvos em: metadata_teste.jpg_20241125_153045.json
```

## ?? Tipos de Arquivos Testáveis

### ? **Formatos Suportados:**

| Tipo | Formatos | GPS | Metadados |
|------|----------|-----|-----------|
| **Imagens** | JPG, PNG, TIFF, GIF, BMP, WEBP, HEIC | ? | ? |
| **Documentos** | PDF, DOCX, XLSX, PPTX | ? | ? |
| **Mídia** | MP4, MP3, AVI, MOV | ?* | ?* |

*Requer ExifTool instalado

## ?? O Que a Ferramenta Pode Encontrar

### ?? **Dados de Localização:**
- Coordenadas GPS exatas (latitude/longitude)
- Altitude onde a foto foi tirada
- Timestamp GPS (data/hora)
- Endereço completo (via geocodificação reversa)
- Links diretos para Google Maps, Waze, Apple Maps

### ?? **Informações do Dispositivo:**
- Marca e modelo da câmera/smartphone
- Números de série do dispositivo
- Configurações da câmera (ISO, velocidade, abertura)
- Orientação da foto

### ?? **Software e Edição:**
- Programas usados para editar (Photoshop, Lightroom)
- Versões de software
- Histórico de modificações
- Perfis de cor ICC

### ?? **Dados do Autor:**
- Nome do fotógrafo/criador
- Informações de copyright
- Dados de contato
- Organização

## ? Comandos Rápidos para Teste

```bash
# Teste básico com qualquer imagem
python osint.py -m "SuaFoto.jpg"

# Só GPS (mais rápido)  
python osint.py -l "SuaFoto.jpg"

# Verificar se ExifTool está funcionando
python osint.py
# ? Opção 12: ExifTool Status

# Instalar ExifTool (se necessário)
python install_exiftool.py
```

## ?? Cenários de Teste Recomendados

### **1. Teste com Foto do Smartphone**
```bash
# Use uma foto sua tirada com GPS ativo
python osint.py -l "IMG_20241125_123456.jpg"
# Resultado: Deve mostrar localização exata onde tirou a foto
```

### **2. Teste com Screenshot**
```bash
# Screenshot de alguma coisa salvou como imagem
python osint.py -m "Screenshot.png"  
# Resultado: Metadados básicos, sem GPS
```

### **3. Teste com Imagem Editada**
```bash
# Foto editada no Photoshop/Lightroom
python osint.py -m "FotoEditada.jpg"
# Resultado: Histórico de edição, software usado
```

### **4. Teste com Documento PDF**
```bash
# Qualquer PDF
python osint.py -m "documento.pdf"
# Resultado: Autor, software, datas de criação
```

## ?? Solução de Problemas

### **Arquivo não encontrado:**
```bash
# Use caminho absoluto
python osint.py -m "C:\Users\SeuUsuario\Desktop\foto.jpg"

# Ou navegue até a pasta
cd "C:\Users\SeuUsuario\Desktop"
python "C:\Users\ecorrea\cybersecurity-tools\dahmer_osint_framework\osint.py" -m foto.jpg
```

### **Nenhum metadado encontrado:**
- Arquivo pode ter metadados removidos
- Formato pode não suportar metadados  
- Instale ExifTool para melhor suporte: `python install_exiftool.py`

### **GPS não detectado:**
- GPS pode ter estado desabilitado
- Metadados GPS podem ter sido removidos
- Nem todas as imagens têm GPS

## ? Verificação Final

**Para confirmar que está funcionando:**

1. Execute: `python osint.py`
2. Escolha opção **12** (ExifTool Status)
3. Deve mostrar se ExifTool está instalado
4. Teste com qualquer imagem usando opção **5** ou **6**

**Sua ferramenta está pronta para análise profissional de metadados! ??**