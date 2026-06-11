<?php
// salvar_questao.php
header("Content-Type: application/json; charset=UTF-8");

// Configurações do Banco de Dados
$host = 'localhost';
$dbname = 'sistema_fisica';
$usuario = 'root'; // Ajuste se o seu usuário do banco for diferente
$senha = '';       // Ajuste se o seu banco tiver senha

try {
    // Conexão PDO com suporte a caracteres especiais
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $usuario, $senha);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Captura o JSON bruto enviado pelo Python
    $json_recebido = file_get_contents('php://input');
    $dados = json_decode($json_recebido, true);

    if (empty($dados['enunciado'])) {
        throw new Exception("Dados insuficientes: Enunciado vazio.");
    }

    $enunciado = $dados['enunciado'];
    $codigo_svg = $dados['codigo_svg'] ?? null;
    $alternativas = $dados['alternativas'] ?? [];

    // Inicia transação para garantir consistência (Tudo ou nada)
    $pdo->beginTransaction();

    // 1. Insere a questão e o SVG correspondente
    $stmtQuestao = $pdo->prepare("INSERT INTO questoes (enunciado, codigo_svg) VALUES (:enunciado, :codigo_svg)");
    $stmtQuestao->execute([
        ':enunciado'  => $enunciado,
        ':codigo_svg' => $codigo_svg
    ]);
    
    // Recupera o ID gerado para esta questão
    $questao_id = $pdo->lastInsertId();

    // 2. Insere as alternativas vinculadas à questão
    $stmtAlternativa = $pdo->prepare("INSERT INTO alternativas (questao_id, letra, texto_alternativa) VALUES (:questao_id, :letra, :texto)");
    
    foreach ($alternativas as $letra => $texto_alternativa) {
        $stmtAlternativa->execute([
            ':questao_id' => $questao_id,
            ':letra'      => $letra,
            ':texto'      => $texto_alternativa
        ]);
    }

    // Confirma as inserções no banco
    $pdo->commit();

    echo json_encode(["status" => "sucesso", "id_questao" => $questao_id]);

} catch (Exception $e) {
    // Desfaz alterações caso ocorra algum erro no processo
    if (isset($pdo) && $pdo->inTransaction()) {
        $pdo->rollBack();
    }
    
    http_response_code(500);
    echo json_encode(["status" => "erro", "mensagem" => $e->getMessage()]);
}
?>