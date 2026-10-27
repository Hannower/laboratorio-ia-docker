# 🚀 Laboratório de IA Generativa com Docker

Ambiente didático completo e integrado para executar projetos de Inteligência Artificial Generativa em contêineres Docker, garantindo paridade de ambiente, versionamento de dependências e orquestração unificada com **Docker Compose**.

---

## 🏗️ Arquitetura do Laboratório

Todos os serviços compartilham a mesma rede Docker interna (`laboratorio-ia-aula`) e a pasta compartilhada de documentos (`./dados/documentos` montada em `/data/documentos`).

```text
               [ Usuário / Navegador / IDE Antigravity ]
                                  │
         ┌────────────────────────┼────────────────────────┐
         │ :3000                  │ :8000                  │ :8001 / stdio
         ▼                        ▼                        ▼
 ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
 │ rag-frontend │ ──────> │ rag-backend  │         │  servidor    │
 │   (Next.js)  │         │   (FastAPI)  │         │  mcp (Fast)  │
 └──────────────┘         └──────┬───────┘         └──────┬───────┘
                                 │                        │
         ┌───────────────────────┼────────────────────────┤
         ▼                       ▼                        ▼
 ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
 │     n8n      │         │   Supabase   │         │  OpenRouter  │
 │  Workflows   │         │  (Postgres/  │         │    (LLMs/    │
 │    :5678     │         │   pgvector)  │         │  Embeddings) │
 └──────┬───────┘         └──────────────┘         └──────────────┘
        │                        ▲
        └───────> /data/documentos ──┘
                {raw, silver, gold}
```

---

## 📦 Projetos Integrados

### 1. 🔍 Projeto RAG (Retrieval-Augmented Generation)
* **Localização:** [`apps/rag/`](file:///c:/ARQUIVOS/Projetos/laboratorio-ia-docker/apps/rag)
* **Backend (`FastAPI` - Porta `8000`):**
  * Extração e OCR de documentos fiscais em PDF (`tesseract-ocr`, `pdfplumber`, `pypdfium2`).
  * Chunking semântico estruturado com metadados fiscais (número da nota, CNPJ, fornecedor, itens e valores).
  * Geração de vetores locais com `FastEmbed` (`BAAI/bge-small-en-v1.5`, 384 dimensões).
  * Persistência vetorial no **Supabase (pgvector)** com fallback automático para vetor local JSON (`local_vector_store.json`).
  * Chat e respostas inteligentes contextualizadas com LLMs via **OpenRouter**.
  * **Ingestão integrada:** Monitora e processa notas fiscais em [`./dados/documentos/raw`](file:///c:/ARQUIVOS/Projetos/laboratorio-ia-docker/dados/documentos/raw) e as promove para [`./dados/documentos/gold`](file:///c:/ARQUIVOS/Projetos/laboratorio-ia-docker/dados/documentos/gold).
* **Frontend (`Next.js` - Porta `3000`):**
  * Dashboard moderno e responsivo para visualização das faturas cadastradas.
  * Chat RAG interativo com respostas fundamentadas e visualização de citações/chunks.
  * Botão de disparo para ingestão em lote e upload de novos PDFs.

### 2. 🔌 Projeto MCP (Model Context Protocol)
* **Localização:** [`apps/mcp/`](file:///c:/ARQUIVOS/Projetos/laboratorio-ia-docker/apps/mcp)
* **Servidor FastMCP (Porta `8001` no Docker ou via `stdio`):**
  * Atua como uma ponte padronizada de ferramentas (tools) para agentes de IA (como Antigravity IDE, Cursor e Claude Desktop).
  * Disponibiliza a ferramenta `listar_chunks_rag` para que o agente consulte chunks e dados fiscais diretamente no PostgreSQL do Supabase via `psycopg2`.
  * **Modo Dual:** Executa como serviço HTTP Streamable (`streamable-http`) na rede Docker e como processo `stdio` para integração nativa com IDEs locais.

### 3. ⚙️ Orquestrador n8n
* **Porta:** `5678`
* Automação de fluxos com nós de monitoramento de arquivos (`Local File Trigger`) mapeados em `/data/documentos/raw` para acionar a API do RAG (`http://rag-backend:8000`).

---

## 🛠️ Pré-requisitos

1. **Docker Desktop** instalado com suporte a WSL 2 e em execução.
2. **Git** para clonar o repositório.
3. Chaves de API das plataformas externas:
   * **Supabase:** URL do projeto e Service Role / Anon Key, além da string de conexão PostgreSQL.
   * **OpenRouter:** Chave de API para inferência de LLM.

---

## 🚀 Passo a Passo para Execução

### Passo 1: Clonar o Repositório
Abra o terminal (PowerShell ou Bash) e clone o repositório:
```bash
git clone https://github.com/Hannower/laboratorio-ia-docker.git
cd laboratorio-ia-docker
```

### Passo 2: Configurar as Variáveis de Ambiente

1. **Configurar o RAG:**
   Crie o arquivo `.env` dentro de `apps/rag/` a partir do modelo de exemplo:
   ```powershell
   Copy-Item apps/rag/.env.example apps/rag/.env
   ```
   Edite `apps/rag/.env` com as suas credenciais:
   ```env
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_PUBLISHABLE_KEY=sua_chave_anonima
   SUPABASE_SECRET_KEY=sua_chave_service_role
   OPENROUTER_API_KEY=sua_chave_openrouter
   ```

2. **Configurar o MCP:**
   Crie o arquivo `.env` dentro de `apps/mcp/`:
   ```powershell
   Copy-Item apps/mcp/.env.example apps/mcp/.env
   ```
   Edite `apps/mcp/.env` adicionando a string de conexão do PostgreSQL do Supabase:
   ```env
   DATABASE_URL=postgresql://postgres.seu-projeto:sua-senha@seu-host:5432/postgres
   ```

### Passo 3: Iniciar o Ambiente com Docker Compose
Na raiz do repositório, execute o comando para construir as imagens e iniciar todos os contêineres em segundo plano:
```powershell
docker compose up --build -d
```

### Passo 4: Acompanhar os Serviços
Para verificar o status dos contêineres:
```powershell
docker compose ps
```
Para visualizar os logs em tempo real:
```powershell
docker compose logs -f
```

---

## 🌐 Endpoints e Portas

| Serviço | URL de Acesso | Descrição |
| :--- | :--- | :--- |
| **Frontend RAG** | [http://localhost:3000](http://localhost:3000) | Interface do usuário e chat RAG |
| **Backend RAG (API Docs)** | [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger interativo da API FastAPI |
| **Backend RAG (Health)** | [http://localhost:8000/api/health](http://localhost:8000/api/health) | Status do RAG, vetores e documentos |
| **Servidor MCP** | [http://localhost:8001/mcp](http://localhost:8001/mcp) | Endpoint HTTP Streamable do servidor MCP |
| **Orquestrador n8n** | [http://localhost:5678](http://localhost:5678) | Painel de workflows do n8n |

---

## 📂 Pastas Compartilhadas de Dados

O diretório local [`dados/documentos/`](file:///c:/ARQUIVOS/Projetos/laboratorio-ia-docker/dados/documentos) é compartilhado com os contêineres via volume Docker (`/data/documentos`):

* **`dados/documentos/raw`**: Coloque aqui os arquivos PDF brutos para ingestão.
* **`dados/documentos/silver`**: Destinado aos dados pós-limpeza e validação (ETL intermediário).
* **`dados/documentos/gold`**: Destino final dos documentos cujos chunks e metadados foram ingeridos com sucesso no banco de dados.

> 💡 **Gerar faturas fictícias para teste:**  
> Caso queira gerar novos PDFs de teste, execute na pasta do RAG:
> ```powershell
> python apps/rag/generate_invoices.py
> ```
> O script colocará automaticamente as novas faturas em `./dados/documentos/raw`.

---

## 🔌 Conectando o MCP ao Antigravity IDE ou Cursor

Caso prefira utilizar o servidor MCP localmente diretamente conectado à IDE (transporte `stdio`):

No arquivo de configuração de servidores MCP da IDE (ou em `.agents/mcp_config.json`):
```json
{
  "mcpServers": {
    "mcp-supabase": {
      "command": "python",
      "args": [
        "c:/ARQUIVOS/Projetos/laboratorio-ia-docker/apps/mcp/server.py"
      ],
      "env": {
        "DATABASE_URL": "postgresql://postgres.seu-projeto:sua-senha@seu-host:5432/postgres"
      }
    }
  }
}
```

---

## 🛑 Comandos Úteis do Docker

* **Parar todos os serviços:**
  ```powershell
  docker compose down
  ```
  *(Os dados persistidos do n8n e os arquivos em `dados/documentos` são preservados).*
* **Reiniciar apenas um serviço:**
  ```powershell
  docker compose restart rag-backend
  ```
* **Ver logs de um serviço específico:**
  ```powershell
  docker compose logs -f rag-backend
  ```
* **Reconstruir imagens após alterações de código:**
  ```powershell
  docker compose up --build -d
  ```
