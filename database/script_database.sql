-- 1) Criar o banco de dados

CREATE DATABASE sistema_eleitoral;
USE sistema_eleitoral;

-- 2) Criar tabela eleitores - guarda todos os cadastrados

CREATE TABLE eleitores (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(100)    NOT NULL,
    titulo          VARCHAR(12)     NOT NULL UNIQUE, -- (char ou varchar de 12 ?) Dúvida !!!!!!
    cpf             VARCHAR(100)    NOT NULL UNIQUE,   -- armazenado criptografado, usar varchar(100) ou usar char(11) Dúvida !!!!!!!!
    chave_acesso    VARCHAR(100)    NOT NULL,           -- armazenado criptografado, tamanho original ~~~~ 7 caracteres
    is_mesario      TINYINT      NOT NULL DEFAULT 0, -- 0 = eleitor comum, 1 = mesário, usar tinyint para economizar espaço em colunas com pequenos intervalos
    status_voto     VARCHAR(20)     NOT NULL DEFAULT 'Não Votou' -- 'Não Votou' ou 'Já Votou'
);

-- 3) Criar tabela candidatos (opcional) os que podem ser votados

CREATE TABLE IF NOT EXISTS candidatos (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(100)    NOT NULL,
    numero      INT             NOT NULL UNIQUE,
    partido     VARCHAR(100)    NOT NULL,
    total_votos INT             NOT NULL DEFAULT 0
);

-- 4) Criar tabela votos para registrar cada voto confirmado

CREATE TABLE IF NOT EXISTS votos (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    id_candidato    INT             NULL,               -- NULL = voto nulo
    data_hora       DATETIME        NOT NULL,
    protocolo       VARCHAR(255)    NOT NULL UNIQUE,    -- armazenado criptografado, tamanho original ~~~ 12 caracteres
    FOREIGN KEY (id_candidato) REFERENCES candidatos(id) ON DELETE SET NULL -- chave estrangeira usada para estabelecer um relacionamento entre duas tabelas em um banco de dados
);

