# ES-PI1-2026-T2-G03 — Sistema de Votação Digital

Projeto desenvolvido para a disciplina **Projeto Integrador I – Engenharia de Software** da PUC Campinas.

> ⚠️ Este projeto tem finalidade exclusivamente didática e não possui relação com sistemas eleitorais reais.

---

## 📋 Descrição do nosso Projeto

- Gerenciamento de eleitores e candidatos
- Processo de votação com autenticação por mesário
- Criptografia de dados sensíveis (Cifra de Hill)
- Logs de auditoria e relatórios de resultado

---

## 👥 Integrantes

| Nome | RA |
|------|----|
| (Arthur Lopes Santos Silva) | (26010221) |
| (Gabriel Augusto Jorge) | (26010868) |
| (Kauã Vargas Martins) | (26011086) |
| (Kauan Martinelli Corrêa) | (26004903) |
| (Leonardo Antunes de Souza) | (26004615) |
---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.14.3
- **Banco de Dados:** MySQL
- **Bibliotecas:** `mysql.connector`, `datetime`, `random`, `os`
- **Repositório:** Git + GitHub
- **Gerenciamento:** GitHub Projects

---

## ▶️ Como Executar

### Pré-requisitos

- Python 3.14.3 instalado
- MySQL instalado e rodando
- Biblioteca `mysql-connector-python` instalada:

```bash
pip install mysql-connector-python
```

### Passo a passo

**1. Clone o repositório:**
```bash
git clone https://github.com/zusflee/ES-PI1-2026-T2-G03.git
cd ES-PI1-2026-T2-G03
```

**2. Crie o banco de dados:**

Abra o MySQL e execute o script:
```bash
mysql -u root -p < database/script_database.sql
```

**3. Configure a conexão:**

Edite o arquivo `database/conexao_SQL.py` e ajuste seu usuário e senha do MySQL:
```python
user="root",      # seu usuário
password="",      # sua senha
```


**4. Execute o sistema:**
```bash
python main/main.py
```
