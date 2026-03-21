# 🤖 Chatbot — RAG + Django + Gemini + React

Sistema de chatbot organizado em **monorepo**, com frontend em React, backend em Django REST Framework, autenticação JWT, banco de dados **PostgreSQL com pgvector** e suporte a **RAG (Retrieval-Augmented Generation)** com a **Gemini API**.

---

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Padrões de Projeto](#padrões-de-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Requisitos](#requisitos)
- [Como rodar o projeto](#como-rodar-o-projeto)
- [Configuração do PostgreSQL + Docker](#configuração-do-postgresql--docker)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Configuração do Django](#configuração-do-django)
- [Rotas da API](#rotas-da-api)
- [Autenticação JWT](#autenticação-jwt)
- [Testando com Postman](#testando-com-postman)
- [Arquitetura RAG](#arquitetura-rag)
- [Erros Comuns](#erros-comuns)
- [Próximos Passos](#próximos-passos)

---

## Visão Geral

Este projeto é organizado como um **monorepo**: frontend e backend ficam no mesmo repositório, mas separados por responsabilidade.

| Parte | Tecnologia | Localização |
|---|---|---|
| Interface web | React + JavaScript | `frontend/` |
| API e chatbot | Python + Django REST Framework | `Backend/` |
| Configuração Django | Django | `config/` |
| Banco de dados | PostgreSQL 16 + pgvector | Docker |
| Ponto de entrada | Django CLI | `manage.py` |

---

## Estrutura do Projeto

```
Chatbot/
├── frontend/                         # Interface web em React
│   └── src/
│       ├── pages/
│       ├── components/
│       ├── services/
│       └── routes/
│
├── Backend/
│   └── app/
│       ├── api/                      # Camada HTTP
│       │   ├── views/
│       │   │   ├── auth.py           # Login do admin
│       │   │   ├── chat.py           # Endpoint do chatbot
│       │   │   ├── documents.py      # CRUD de documentos
│       │   │   ├── categories.py
│       │   │   └── users.py
│       │   ├── factories.py          # Factory Method
│       │   ├── permissions.py
│       │   └── urls.py
│       ├── application/              # Casos de uso
│       │   ├── login_admin.py
│       │   ├── delete_document.py
│       │   ├── answer_question.py
│       │   ├── create_document.py
│       │   ├── list_documents.py
│       │   ├── update_document.py
│       │   ├── embedding_provider.py
│       │   ├── index_document.py
│       │   └── vector_store.py
│       ├── domain/                   # Contratos e entidades
│       │   └── repositories/
│       │       └── document_repository.py  # Interface abstrata
│       ├── infrastructure/           # Implementações concretas
│       │   ├── embeddings/
│       │   ├── llm/
│       │   ├── repositories/
│       │   │   ├── in_memory/
│       │   │   └── sql/
│       │   │       └── postgres_document_repository.py
│       │   └── vectorstore/
│       └── documents/                # Models e indexação de PDFs
│           ├── models.py
│           ├── apps.py
│           └── management/commands/
│               └── indexar_documentos.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── Documentos/                       # PDFs indexados no banco
│   ├── portarias/                    # 20 PDFs
│   ├── resolucoes/                   # 20 PDFs
│   └── rod/                          # 2 PDFs
│
├── migrations/
│   └── criar_indice_vetorial.sql
│
├── docker-compose.yml
├── Dockerfile
├── init.sql
├── .env.example
├── manage.py
└── requirements.txt
```

---

## Padrões de Projeto

O projeto aplica padrões do livro **"Padrões de Projeto" (Gang of Four)** para garantir flexibilidade, testabilidade e manutenção do código.

### 1. Factory Method (GoF p.112) — Criação

**Onde:** `Backend/app/api/factories.py`

As views nunca instanciam casos de uso diretamente. A Factory centraliza a criação e injeta as dependências corretas.

```
LoginView → AuthFactory.make_login() → LoginAdmin
DocumentDeleteView → DocumentFactory.make_delete() → DeleteDocument(PostgresDocumentRepository)
```

### 2. Strategy (GoF p.292) — Comportamental

**Onde:** `Backend/app/infrastructure/llm/` *(a implementar)*

Permite trocar o provedor de LLM (Gemini, OpenAI, etc.) sem alterar os casos de uso. O `AnswerQuestion` delega para um `LLMProvider` abstrato.

### 3. Repository (GoF — separação domínio/infraestrutura)

**Onde:** `Backend/app/domain/repositories/` e `infrastructure/repositories/`

A camada de aplicação depende apenas da interface abstrata `DocumentRepository`. As implementações concretas (`PostgresDocumentRepository`, `SQLiteDocumentRepository`, `InMemoryDocumentRepository`) são intercambiáveis.

---

## Tecnologias Utilizadas

### Frontend
- React, JavaScript, Axios, React Router

### Backend
- Python 3.10+, Django 5.1, Django REST Framework
- Simple JWT, django-cors-headers

### Banco de Dados
- PostgreSQL 16 + pgvector (via Docker)
- psycopg2-binary (driver Python)

### IA / RAG
- Gemini API, Embeddings, Vector Store (pgvector)

---

## Requisitos

- Python 3.10+
- Node.js 18+
- Docker Desktop
- Chave de API do Gemini

---

## Como rodar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/LES-Chatbot-KTP/Chatbot.git
cd Chatbot
```

### 2. Criar e ativar o ambiente virtual

**Windows PowerShell**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers google-genai psycopg2-binary pypdf python-dotenv
```

### 4. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env e preencha GEMINI_API_KEY, POSTGRES_PASSWORD e SECRET_KEY
```

### 5. Subir o banco de dados

> O Docker Desktop precisa estar aberto antes desse passo.

```bash
docker-compose up -d db
```

### 6. Aplicar migrações

```bash
python manage.py makemigrations documents
python manage.py migrate
```

### 7. Criar o índice vetorial no PostgreSQL

**Windows PowerShell:**
```powershell
Get-Content migrations/criar_indice_vetorial.sql | docker exec -i chatbot_db psql -U chatbot_user -d chatbot
```

**Linux / macOS:**
```bash
docker exec -i chatbot_db psql -U chatbot_user -d chatbot < migrations/criar_indice_vetorial.sql
```

### 8. Indexar os documentos PDF

```bash
python manage.py indexar_documentos
```

Resultado esperado:
```
✅ Indexação concluída: 42 documento(s), 650 chunk(s)
```

### 9. Criar superusuário e iniciar o servidor

```bash
python manage.py createsuperuser
python manage.py runserver
```

O backend ficará disponível em **http://127.0.0.1:8000/**

### 10. Rodar o frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

O frontend ficará disponível em **http://localhost:5173/**

---

## Configuração do PostgreSQL + Docker

O projeto usa **PostgreSQL 16 com a extensão pgvector** para armazenar documentos e embeddings vetoriais.

### Estrutura do banco

| Tabela | Descrição |
|---|---|
| `documents_documento` | 42 PDFs indexados (portarias, resoluções, RODs) |
| `documents_chunkdocumento` | 650 chunks de texto com embeddings vetoriais |

### Verificar se o banco está rodando

```bash
docker-compose ps
# chatbot_db   Up (healthy)   0.0.0.0:5432->5432/tcp
```

### Consultar dados no banco

```bash
docker exec -it chatbot_db psql -U chatbot_user -d chatbot
```

```sql
SELECT tipo, COUNT(*) FROM documents_documento GROUP BY tipo;
SELECT COUNT(*) FROM documents_chunkdocumento;
SELECT id, nome, tipo FROM documents_documento LIMIT 10;
```

---

## Variáveis de Ambiente

| Variável | Descrição |
|---|---|
| `GEMINI_API_KEY` | Chave de acesso à API do Gemini |
| `CHAT_MODEL` | Modelo para gerar respostas (ex: gemini-1.5-flash) |
| `EMBEDDING_MODEL` | Modelo para embeddings (ex: models/text-embedding-004) |
| `TOP_K` | Quantidade de chunks recuperados na busca vetorial |
| `POSTGRES_DB` | Nome do banco de dados |
| `POSTGRES_USER` | Usuário do banco |
| `POSTGRES_PASSWORD` | Senha do banco |
| `DB_HOST` | Host do banco (localhost em dev, db no Docker) |
| `SECRET_KEY` | Chave secreta do Django |
| `DEBUG` | True em desenvolvimento, False em produção |

> ⚠️ Nunca suba o `.env` para o GitHub. Apenas o `.env.example`.

---

## Configuração do Django

Em `config/settings.py`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "Backend.app",
    "Backend.app.documents",
]

ROOT_URLCONF = "config.urls"
STATIC_URL = "/static/"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
]
```

---

## Rotas da API

### `POST /api/auth/login/`
Autentica o administrador e retorna tokens JWT.

```json
// Request
{ "username": "seu_usuario", "password": "sua_senha" }

// Response 200
{
  "access": "eyJ...",
  "refresh": "eyJ...",
  "username": "seu_usuario",
  "email": "email@exemplo.com"
}
```

Erros: `400` campos em branco, `401` credenciais inválidas ou usuário sem `is_staff`.

---

### `POST /api/auth/refresh/`
Renova o token de acesso.

```json
{ "refresh": "seu_refresh_token" }
```

---

### `POST /api/chat/`
Recebe uma pergunta e retorna a resposta do chatbot.

```json
// Request
{ "question": "O que é RAG?" }

// Response
{ "answer": "RAG é uma abordagem que recupera contexto antes de gerar a resposta." }
```

---

### `DELETE /api/documents/<id>/`
Exclui um documento e todos os seus chunks. Requer autenticação JWT de administrador.

```http
DELETE http://127.0.0.1:8000/api/documents/1/
Authorization: Bearer SEU_ACCESS_TOKEN
```

```json
// Response 200
{
  "message": "Documento 'PORTARIA Nº 1 - 2025...' excluído com sucesso.",
  "id": 1
}
```

Erros: `401` sem token, `404` ID não encontrado.

---

## Autenticação JWT

1. Fazer login via `POST /api/auth/login/`
2. Copiar o token `access` da resposta
3. Enviar no header de todas as rotas protegidas:

```http
Authorization: Bearer SEU_ACCESS_TOKEN
```

---

## Testando com Postman

### Login
```
POST http://127.0.0.1:8000/api/auth/login/
Body (raw JSON): { "username": "Thaylan", "password": "sua_senha" }
```

### Chat
```
POST http://127.0.0.1:8000/api/chat/
Body (raw JSON): { "question": "oi" }
```

### Excluir documento
```
DELETE http://127.0.0.1:8000/api/documents/1/
Headers: Authorization: Bearer SEU_TOKEN
```

---

## Arquitetura RAG

```
