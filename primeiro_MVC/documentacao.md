vou construir a tela de cadastro e login no formato mvc(model-view-controller) e alvando os dados em banco de dados.

-------------------------------------------------------
1.1  criando o banco de dados. (banco_primeiro_mvc.sql)
-------------------------------------------------------
o banco de dados deve ter para o cadastro: nome, email e senha.

CREATE DATABASE IF NOT EXISTS primeiro_mvc;
USE primeir_mvc;

CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(20) NOT NULL
);

----------------------------------------------------------
1.2 configurar a conexão com o banco de dados (config.php)
----------------------------------------------------------
definir constantes globais com as credenciais de acesso ao bano de dados mysql.

<?php
    define('DB_HOST', 'localhost');
    define('DB_USER', 'root');
    define('DB_PASS', '');
    define('DB_NAME', 'primeiro_mvc');


?>

o define cria uma constante em php cujo valor não pode ser alterado durante a execução do script, tornando ideal para confgurações fixas.

----------------------------------------------
1.3 criando o model ( Model/UsuarioModel.php)
----------------------------------------------
primeiro crio a pasta Model e dentro da pasta o arquivo UsuarioModel.php

<?php

    class UsuarioModel{
        public $id;
        public $nome;
        public $email;
        public $senha;

    }



?>

--------------------------------------
1.4 criando a DAO (data access object)
--------------------------------------

primeiro cria a psta DAO depois dentro da pasta crie o arquivo UsuarioDAO.php
a DAO é responsavel exclusivamete por conversar com o banco de dados. conectando ao banco e executa os comandos SQL para inserir, consultar, editar ou apagar cadastro ou informações.

<?php

    class UsuarioDAO{
        private $conexao;

        public function __construct(){
            //inicializa a coexão com o banco usando PDO
            $this->conexao = new PDO("mysql:host = " . DB_HOST . ";dbname=" . DB_NAME, DB_USER, DB_PASS);
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

-------------------------
1.5 criando o controller
-------------------------




