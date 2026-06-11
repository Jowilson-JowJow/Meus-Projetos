import fitz  # PyMuPDF
import json


def extrair_texto_pdf(caminho_pdf):
    doc = fitz.open(caminho_pdf)
    
    for numero_pagina in range(len(doc)):
        pagina = doc[numero_pagina]
        print(f"--- Lendo a Página {numero_pagina + 1} ---")
        
        # Extrai o texto formatado em blocos
        blocos = pagina.get_text("blocks")
        
        for bloco in blocos:
            # bloco[4] contém o texto do bloco atual
            texto_do_bloco = bloco[4].strip()
            
            if texto_do_bloco:
                print(texto_do_bloco)
                print("-" * 20)

# Exemplo de uso:
# extrair_texto_pdf("questoes_fisica.pdf")

def extrair_graficos_como_svg(caminho_pdf):
    doc = fitz.open(caminho_pdf)
    
    for numero_pagina in range(len(doc)):
        pagina = doc[numero_pagina]
        
        # Converte os elementos vetoriais da página inteira em um único código SVG
        codigo_svg = pagina.get_svg_image(text_as_path=False)
        
        # Salva o arquivo SVG temporariamente para testar
        nome_arquivo = f"pagina_{numero_pagina + 1}.svg"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(codigo_svg)
            
        print(f"Gráficos da página {numero_pagina + 1} exportados como SVG com sucesso!")

# Exemplo de uso:
# extrair_graficos_como_svg("questoes_fisica.pdf")

def converter_pagina_para_json(caminho_pdf, numero_da_pagina):
    doc = fitz.open(caminho_pdf)
    pagina = doc[numero_da_pagina]
    
    # 1. Extrai o texto bruto para processar depois (via Regex)
    texto_completo = pagina.get_text("text")
    
    # 2. Extrai a parte gráfica como SVG
    codigo_svg = pagina.get_svg_image(text_as_path=False)
    
    # 3. Monta a estrutura de dados (Exemplo manual básico)
    questao_estruturada = {
        "materia": "Física",
        "enunciado_bruto": texto_completo, # Aqui você aplicará Regex para separar enunciado de alternativas
        "codigo_svg": codigo_svg
    }
    
    # Converte o dicionário Python para uma string JSON legível
    json_resultado = json.dumps(questao_estruturada, ensure_ascii=False, indent=4)
    return json_resultado

# Uso:
# dados_json = converter_pagina_para_json("questoes_fisica.pdf", 0)
# print(dados_json)

import fitz  # PyMuPDF
import re
import json

def processar_questao_pdf(caminho_pdf, numero_pagina):
    # 1. Abre o PDF e seleciona a página
    doc = fitz.open(caminho_pdf)
    pagina = doc[numero_pagina]
    
    # Extrai o texto limpo da página
    texto_completo = pagina.get_text("text").strip()
    
    # Extrai o gráfico/tabela da página inteira como SVG
    codigo_svg = pagina.get_svg_image(text_as_path=False)
    
    # 2. Expressão Regular para capturar as alternativas
    # Explicação do padrão: 
    # ^([A-Ea-e])         -> Procura por letras de A a E (maísculas ou minúsculas) no início da linha
    # [\s]*[\.\)]        -> Seguidas por um ponto '.' ou parênteses ')'
    # (.*)$              -> Captura todo o resto do texto daquela linha como o conteúdo da alternativa
    padrao_alternativas = re.compile(r'^([A-Ea-e])[\s]*[\.\)]+(.*)$', re.MULTILINE)
    
    # Encontra todas as ocorrências de alternativas no texto
    matches = list(padrao_alternativas.finditer(texto_completo))
    
    alternativas = {}
    enunciado = texto_completo
    
    if matches:
        # O enunciado será tudo o que está ANTES da primeira alternativa encontrada
        primeira_match_pos = matches[0].start()
        enunciado = texto_completo[:primeira_match_pos].strip()
        
        # Extrai o texto de cada alternativa
        for i, match in enumerate(matches):
            letra = match.group(1).upper() # Garante que fica em maiúsculo (A, B, C...)
            
            # O texto da alternativa vai até o início da próxima alternativa (ou até o fim do texto)
            inicio_texto = match.start(2)
            fim_texto = matches[i+1].start() if i + 1 < len(matches) else len(texto_completo)
            
            texto_alternativa = texto_completo[inicio_texto:fim_texto].strip()
            # Limpa possíveis resíduos de outras letras que vieram junto
            texto_alternativa = re.sub(r'^[A-Ea-e][\.\)]\s*', '', texto_alternativa)
            
            alternativas[letra] = texto_alternativa

    # 3. Estrutura o dicionário final (Pronto para virar JSON)
    questao_formatada = {
        "id_pagina": numero_pagina + 1,
        "enunciado": enunciado,
        "alternativas": alternativas,
        "codigo_svg": codigo_svg
    }
    
    doc.close()
    return questao_formatada

# --- TESTANDO O SCRIPT ---
# Substitua pelo nome do seu arquivo PDF real e a página desejada (0 é a primeira página)
# resultado = processar_questao_pdf("suas_questoes.pdf", 0)
# print(json.dumps(resultado, ensure_ascii=False, indent=2))


import requests

def enviar_para_o_servidor(dados_da_questao):
    # O endereço onde o seu arquivo PHP estará rodando
    url_do_servidor = "http://localhost/seu_projeto/salvar_questao.php"
    
    # Cabeçalho informando que estamos enviando um arquivo JSON legítimo
    headers = {'Content-Type': 'application/json'}
    
    try:
        # Envia os dados via POST
        resposta = requests.post(url_do_servidor, json=dados_da_questao, headers=headers)
        
        if resposta.status_code == 200:
            print("🚀 Sucesso! Questão enviada e processada pelo PHP.")
            print("Resposta do Servidor:", resposta.text)
        else:
            print(f"❌ Erro no servidor: Status {resposta.status_code}")
            print(resposta.text)
            
    except Exception as e:
        print("❌ Falha ao conectar com o servidor PHP:", e)

# --- COMO EXECUTAR NO SEU LOOP ---
# q = processar_questao_pdf("suas_questoes.pdf", 0)
# enviar_para_o_servidor(q)

# <?php
# // salvar_questao.php

# // 1. Configurações de conexão com o banco de dados
# $host = 'localhost';
# $dbname = 'sistema_fisica';
# $usuario = 'root';
# $senha = '';

# try {
#     $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $usuario, $senha);
#     $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
#     // 2. Captura o JSON bruto que o Python enviou pelo corpo da requisição (POST)
#     $json_recebido = file_get_contents('php://input');
#     $dados = json_decode($json_recebido, true);

#     if (!$dados) {
#         throw new Exception("Dados JSON inválidos ou vazios.");
#     }

#     // Atribui os dados às variáveis de forma organizada
#     $enunciado = $dados['enunciado'];
#     $codigo_svg = $dados['codigo_svg']; // O texto do SVG entra como LONGTEXT no banco
#     $alternativas = $dados['alternativas']; // É um array/dicionário com A, B, C, D, E

#     // 3. Inicia uma transação (se algo der errado nas alternativas, ele desfaz tudo)
#     $pdo->beginTransaction();

#     // Passo A: Insere a questão principal e o SVG do gráfico
#     $stmtQuestao = $pdo->prepare("INSERT INTO questoes (enunciado, codigo_svg) VALUES (:enunciado, :codigo_svg)");
#     $stmtQuestao->execute([
#         ':enunciado'  => $enunciado,
#         ':codigo_svg' => $codigo_svg
#     ]);
    
#     // Pega o ID gerado para essa questão específica
#     $questao_id = $pdo->lastInsertId();

#     // Passo B: Varre as alternativas (A, B, C...) e insere vinculando ao ID da questão
#     $stmtAlternativa = $pdo->prepare("INSERT INTO alternativas (questao_id, letra, texto_alternativa) VALUES (:questao_id, :letra, :texto)");
    
#     foreach ($alternativas as $letra => $texto_alternativa) {
#         $stmtAlternativa->execute([
#             ':questao_id' => $questao_id,
#             ':letra'      => $letra,
#             ':texto'      => $texto_alternativa
#         ]);
#     }

#     // Se tudo deu certo, confirma as gravações no banco
#     $pdo->commit();

#     echo json_encode(["status" => "sucesso", "mensagem" => "Questão $questao_id salva com sucesso!"]);

# } catch (Exception $e) {
#     // Se houve erro, desfaz qualquer inserção parcial para não sujar o banco
#     if (isset($pdo) && $pdo->inTransaction()) {
#         $pdo->rollBack();
#     }
    
#     http_response_code(500);
#     echo json_encode(["status" => "erro", "mensagem" => $e->getMessage()]);
# }
# ?>


# -- 1. Cria o banco de dados se ele não existir
# CREATE DATABASE IF NOT EXISTS sistema_fisica
# CHARACTER SET utf8mb4
# COLLATE utf8mb4_unicode_ci;

# USE sistema_fisica;

# -- ====================================================
# -- 2. Tabela Principal: Questões
# -- ====================================================
# CREATE TABLE IF NOT EXISTS questoes (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     enunciado TEXT NOT NULL,
#     codigo_svg LONGTEXT DEFAULT NULL, -- Guarda o código XML do gráfico/figura/tabela
#     criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

# -- ====================================================
# -- 3. Tabela Relacionada: Alternativas
# -- ====================================================
# CREATE TABLE IF NOT EXISTS alternativas (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     questao_id INT NOT NULL,           -- Vincula com a tabela de questões
#     letra CHAR(1) NOT NULL,            -- Guarda 'A', 'B', 'C', 'D' ou 'E'
#     texto_alternativa TEXT NOT NULL,
    
#     -- Cria a chave estrangeira (FK)
#     -- ON DELETE CASCADE garante que se você apagar uma questão, 
#     -- todas as alternativas dela são apagadas automaticamente.
#     CONSTRAINT fk_questao_alternativa 
#         FOREIGN KEY (questao_id) 
#         REFERENCES questoes(id) 
#         ON DELETE CASCADE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;