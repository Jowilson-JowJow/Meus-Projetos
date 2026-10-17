<?php

    class UsuarioDAO{
        private $conexao;

        public function __construct(){
            //inicializa a coexão com o banco usando PDO
            $this->conexao = new PDO("mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4", DB_USER, DB_PASS, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
        }

        public function inserir(UsuarioModel $usuario){
            $sql = "INSERT INTO usuario (nome, email, senha) VALUES (:nome, :email, :senha)";
            $stmt = $this->conexao->prepare($sql);

            $stmt->bindValue(':nome', $usuario->nome);
            $stmt->bindValue(':email', $usuario->email);
            //criptogrfa a senha antes de salvar por segurança
            $stmt->bindValue(':senha', password_hash($usuario->senha, PASSWORD_DEFAULT));

            return $stmt->execute();

        }
    }


?>