CREATE DATABASE IF NOT EXISTS sistema;

USE sistema;

CREATE TABLE IF NOT EXISTS usuarios (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    nome  VARCHAR(100),
    email VARCHAR(100),
    senha VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS clientes (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    nome     VARCHAR(100),
    telefone VARCHAR(20),
    email    VARCHAR(100),
    endereco VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS bicicletas (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id  INT,
    marca       VARCHAR(100),
    modelo      VARCHAR(100),
    cor         VARCHAR(50),
    numero_serie VARCHAR(100),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS servicos (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    bicicleta_id INT,
    descricao    VARCHAR(255),
    valor        DECIMAL(10,2),
    status       VARCHAR(50),
    data_entrada DATE,
    data_saida   DATE,
    FOREIGN KEY (bicicleta_id) REFERENCES bicicletas(id)
);

-- Usuario padrão para primeiro acesso (senha: 1234)
INSERT INTO usuarios (nome, email, senha) VALUES ('Administrador', 'admin@oficina.com', '1234');
