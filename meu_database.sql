CREATE TABLE aluno(
    id_aluno SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    email VARCHAR(250) UNIQUE NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    data_ingresso DATE DEFAULT CURRENT_DATE
);

CREATE TABLE curso(
    id_curso SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL,
    carga_horaria INTERGER CHECK (carga_horaria >= 0),
    valor_inscricao DECIMAL(10, 2) NOT NULL,
    status BOOLEAN DEFAULT TRUE
);

CREATE TABLE matricula(
    id_matricula SERIAL PRIMARY KEY,
    aluno_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL, 
    data_matricula DATE DEFAULT CURRENT_DATE,
    status_pagamento VARCHAR(10) DEFAULT "pendente" CHECK (status_pagamento IN ("pago", "pendente")),

    CONSTRAINT fk_aluno FOREIGN KEY (aluno_id) REFERENCES aluno(id_aluno) ON DELETE CASCADE,
    CONSTRAINT fk_curso FOREIGN KEY (curso_id) REFERENCES curso(id_curso) ON DELETE CASCADE
);