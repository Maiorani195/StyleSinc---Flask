# 🚀 StyleSinc Flask API

O **StyleSinc** é uma API RESTful robusta desenvolvida em Python e Flask, focada na gestão inteligente de inventário e vendas para o setor de moda e e-commerce. O sistema utiliza uma arquitetura moderna com MongoDB para flexibilidade de dados e Pydantic para validação rigorosa.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.12+
- **Framework Web:** [Flask](https://flask.palletsprojects.com/) (Arquitetura baseada em Blueprints)
- **Banco de Dados:** [MongoDB](https://www.mongodb.com/) (NoSQL)
- **Modelagem e Validação:** [Pydantic V2](https://docs.pydantic.dev/)
- **Segurança:** [PyJWT](https://pyjwt.readthedocs.io/) (JSON Web Tokens)
- **Processamento de Arquivos:** CSV & IO Streams
- **Ambiente:** `python-dotenv` para gestão de variáveis de ambiente

## 🏗️ Arquitetura do Projeto

O projeto segue uma estrutura modular para facilitar a escalabilidade e manutenção:

```text
StyleSinc Flask/
├── app/
│   ├── models/          # Definições de esquemas de dados (Pydantic)
│   ├── routes/          # Definição dos endpoints (Blueprints)
│   ├── decorators.py    # Middlewares (ex: @token_required)
│   ├── utils.py         # Funções utilitárias
│   └── __init__.py      # Inicialização do app e DB
├── testes/              # Suíte de testes automatizados
├── .env                 # Configurações sensíveis (não commitado)
├── config.py            # Carregamento de configurações
├── run.py               # Ponto de entrada da aplicação
└── requirements.txt     # Dependências do projeto
```

## 🔒 Segurança

A API utiliza autenticação baseada em tokens **JWT**. 
- As rotas sensíveis exigem o header: `Authorization: Bearer <seu_token>`.
- O acesso é gerenciado pelo decorator `@token_required`, que valida a assinatura e a expiração do token em tempo real.

## 🚀 Principais Funcionalidades

### 📦 Gestão de Produtos (CRUD)
- **GET** `/products`: Lista todos os produtos no catálogo.
- **POST** `/products`: Cria um novo produto (Requer Auth).
- **PUT** `/products/<id>`: Atualiza dados de um produto existente (Requer Auth).
- **DELETE** `/products/<id>`: Remove um produto do sistema (Requer Auth).
- **GET** `/products/<id>`: Busca detalhes de um produto específico.

### 💰 Gestão de Vendas
- **POST** `/sales/upload`: Importação em lote de vendas através de arquivo CSV.
  - O sistema processa o arquivo em stream (memória), valida cada linha individualmente e retorna um relatório de sucessos e erros.

### 🔑 Autenticação
- **POST** `/login`: Gera um token JWT válido por 30 minutos a partir de credenciais administrativas.

## ⚙️ Como Executar o Projeto

### 1. Clonar e Configurar Ambiente
```bash
# Navegue até a pasta
cd "StyleSinc Flask"

# Crie e ative o ambiente virtual
python -m venv venv
# Windows:
.\venv\Scripts\activate
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes chaves:
```env
MONGO_URI=sua_uri_do_mongodb
SECRET_KEY=sua_chave_secreta_para_jwt
```

### 4. Rodar a Aplicação
```bash
python run.py
```
A API estará disponível em `http://localhost:5000`.

## ✅ Tratamento de Erros
A API retorna códigos HTTP padronizados:
- `200/201`: Sucesso.
- `400`: Dados mal formados ou falha de validação (Pydantic).
- `401`: Token inválido, expirado ou ausente.
- `404`: Recurso não encontrado.
- `500`: Erro interno no servidor.

---
Desenvolvido com foco em **Integridade de Dados** e **Segurança**. 🚀
