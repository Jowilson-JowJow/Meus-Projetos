import fitz  # PyMuPDF
import re
import json
import requests

def processar_e_enviar_pdf(caminho_pdf, url_servidor):
    # 1. Abre o arquivo PDF
    doc = fitz.open(caminho_pdf)
    print(f"📚 PDF aberto com sucesso. Total de páginas: {len(doc)}")
    
    # Expressão regular para identificar o início das alternativas (ex: A), b., C -)
    padrao_alternativas = re.compile(r'^([A-Ea-e])[\s]*[\.\)]+(.*)$', re.MULTILINE)
    
    # Loop por todas as páginas do PDF
    for numero_pagina in range(len(doc)):
        pagina = doc[numero_pagina]
        print(f"\n🔄 Processando página {numero_pagina + 1}...")
        
        # Extrai o texto limpo da página
        texto_completo = pagina.get_text("text").strip()
        
        # Extrai os elementos gráficos (tabelas/gráficos) da página inteira como SVG
        codigo_svg = pagina.get_svg_image(text_as_path=False)
        
        # Encontra onde estão as alternativas no texto
        matches = list(padrao_alternativas.finditer(texto_completo))
        
        alternativas = {}
        enunciado = texto_completo
        
        if matches:
            # O enunciado é tudo o que antecede a primeira alternativa detectada
            primeira_match_pos = matches[0].start()
            enunciado = texto_completo[:primeira_match_pos].strip()
            
            # Varre e separa cada alternativa
            for i, match in enumerate(matches):
                letra = match.group(1).upper()
                
                inicio_texto = match.start(2)
                fim_texto = matches[i+1].start() if i + 1 < len(matches) else len(texto_completo)
                
                texto_alternativa = texto_completo[inicio_texto:fim_texto].strip()
                texto_alternativa = re.sub(r'^[A-Ea-e][\.\)]\s*', '', texto_alternativa)
                
                alternativas[letra] = texto_alternativa
        else:
            print(f"⚠️ Nenhuma alternativa padrão encontrada na página {numero_pagina + 1}. Enviando tudo como enunciado.")

        # Monta o pacote de dados (Dicionário Python)
        dados_questao = {
            "enunciado": enunciado,
            "alternativas": alternativas,
            "codigo_svg": codigo_svg
        }
        
        # 2. Envia os dados estruturados para o arquivo PHP
        headers = {'Content-Type': 'application/json'}
        try:
            resposta = requests.post(url_servidor, json=dados_questao, headers=headers)
            if resposta.status_code == 200:
                print(f"✅ Página {numero_pagina + 1} salva com sucesso no MySQL!")
            else:
                print(f"❌ Erro na página {numero_pagina + 1}: Código {resposta.status_code}")
                print(resposta.text)
        except Exception as e:
            print(f"❌ Falha de conexão ao enviar a página {numero_pagina + 1}: {e}")
            break # Para o loop se o servidor estiver caído

    doc.close()
    print("\n🏁 Processo de extração e envio finalizado.")

# --- EXECUÇÃO DO SCRIPT ---
if __name__ == "__main__":
    # Ajuste o nome do seu arquivo PDF e a URL do seu servidor local
    ARQUIVO_PDF = "questoes_fisica.pdf" 
    URL_API = "http://localhost/app-fisica/salvar_questao.php"
    
    processar_e_enviar_pdf(ARQUIVO_PDF, URL_API)