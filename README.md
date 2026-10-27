# 🚀 Laboratório de IA Generativa com Docker

Ambiente didático completo, integrado e modular para executar projetos de **Inteligência Artificial Generativa** em contêineres Docker, garantindo paridade total de ambiente, versionamento de dependências e orquestração unificada com **Docker Compose**.

Desenvolvido para ser clonado e executado diretamente em qualquer computador (sala de aula, laboratório ou ambiente pessoal) que possua apenas o **Docker Desktop** instalado.

---

## 🏗️ Arquitetura do Laboratório

Todos os serviços compartilham a mesma rede interna Docker (`laboratorio-ia-aula`) e a pasta compartilhada de documentos montada em `./dados/documentos` (`/data/documentos` nos contêineres).

```text
               [ Usuário / Navegador / IDE Antigravity ]
                                  │
         ┌────────────────────────┼────────────────────────┐
         │ :3000                  │ :8000                  │ :8001 / stdio
         ▼                        ▼                        ▼
 ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
 │ rag-frontend │ ──────> │ rag-backend  │         │   servidor   │
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

## 📦 Projetos e Serviços Integrados

### 1. 🔍 Projeto RAG (Retrieval-Augmented Generation)
* **Localização:** [`apps/rag/`](apps/rag/)
* **Backend (`FastAPI` - Porta `8000`):**
  * **Extração & OCR:** Leitura estruturada com `pdfplumber` e OCR de segurança via `tesseract-ocr` + `pypdfium2`.
  * **Parser Robusto de Itens:** Extração de produtos e serviços em linha única ou tabelas com descrições multilinhas, homologado para 100% das notas fiscais.
  * **Chunking Semântico:** Divisão contextual (cabeçalho com metadados, agrupamento de itens em lotes e cláusulas adicionais).
  * **Embeddings Neurais:** Vetorização local com `FastEmbed` (`BAAI/bge-small-en-v1.5`, 384 dimensões).
  * **Persistência Híbrida:** Armazenamento vetorial com indexação no **Supabase (pgvector)** com **fallback automático** para banco local espelhado (`apps/rag/data/local_vector_store.json`), permitindo execução offline ou sem Supabase configurado.
  * **LLM & Anti-Alucinação:** Integração com **OpenRouter** com proteção estrita anti-alucinação e tratamento defensivo para tokens de raciocínio (*reasoning*).
* **Frontend (`Next.js` - Porta `3000`):**
  * Dashboard moderno e responsivo com métricas das notas fiscais cadastradas.
  * Chat RAG interativo com streaming, respostas fundamentadas e visualização de citações/chunks.
  * Botão de disparo de ingestão em lote e upload direto de novos arquivos PDF.

### 2. 🔌 Projeto MCP (Model Context Protocol)
* **Localização:** [`apps/mcp/`](apps/mcp/)
* **Servidor FastMCP (Porta `8001` no Docker ou via `stdio`):**
  * Atua como uma ponte padronizada de ferramentas (*tools*) para agentes de IA (Antigravity IDE, Cursor, Claude Desktop).
  * Disponibiliza a ferramenta `listar_chunks_rag` para consulta de chunks e dados fiscais diretamente no PostgreSQL do Supabase via `psycopg2`.
  * **Modo Dual:** Executa como serviço HTTP Streamable (`streamable-http`) na rede Docker e como processo `stdio` para integração nativa com IDEs locais.

### 3. ⚙️ Orquestrador n8n
* **Porta:** `5678`
* **Automação de Ingestão:** Monitora a pasta `/data/documentos/raw` com o nó `Local File Trigger` usando modo *polling* (`usePolling: true`), compatível com Windows WSL 2 e Linux.
* Ao detectar um novo arquivo PDF em `raw`, o n8n chama a API do RAG (`http://rag-backend:8000/api/ingest/default-invoices`), que processa, vetoriza e move a nota para `gold`.
* **Workflow Pronto:** O arquivo de fluxo pronto para importação está disponível em [`workflows/pipeline_ingestao_rag.json`](workflows/pipeline_ingestao_rag.json).

---

## 🛠️ Pré-requisitos para a Sala de Aula

Para rodar este laboratório em qualquer computador, são necessárias **apenas duas ferramentas instaladas na máquina hospedeira**:

1. **Docker Desktop** (com suporte a WSL 2 no Windows ou Docker Engine no Linux/macOS) em execução.
2. **Git** para clonar o repositório.
3. **Chave de API do OpenRouter**:
   * Obtenha em [openrouter.ai](https://openrouter.ai/keys) (necessária para as respostas da LLM no Chat RAG).
4. *(Opcional)* **Supabase**: URL e chaves caso queira usar persistência em nuvem pgvector. Se não preencher, o sistema funciona normalmente usando o banco vetorial local embutido.

> ℹ️ **Nota:** Não é necessário instalar Python, Node.js, Tesseract ou bibliotecas no computador local — todas as dependências rodam isoladas nos contêineres Docker.

---

## 🚀 Passo a Passo Completo para Novo Computador

Siga esta sequência exata quando for utilizar o projeto em outro computador no curso:

### Passo 1: Clonar o Repositório
Abra o terminal (PowerShell no Windows, ou Bash no Linux/macOS) e clone o repositório:
```bash
git clone https://github.com/Hannower/laboratorio-ia-docker.git
cd laboratorio-ia-docker
```

---

### Passo 2: Configurar as Variáveis de Ambiente (`.env`)

1. **Criar os arquivos a partir dos modelos de exemplo:**
   * **No Windows (PowerShell):**
     ```powershell
     Copy-Item apps/rag/.env.example apps/rag/.env
     Copy-Item apps/mcp/.env.example apps/mcp/.env
     ```
   * **No Linux / macOS (Bash):**
     ```bash
     cp apps/rag/.env.example apps/rag/.env
     cp apps/mcp/.env.example apps/mcp/.env
     ```

2. **Editar `apps/rag/.env`:**
   Abra o arquivo `apps/rag/.env` no seu editor (VS Code, Bloco de Notas ou Antigravity) e configure:
   ```env
   # Obrigatório para as respostas do Chat RAG:
   OPENROUTER_API_KEY=sk-or-v1-sua-chave-aqui

   # Opcional (se não tiver, o RAG usa automaticamente o banco vetorial local):
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_PUBLISHABLE_KEY=sua_chave_anonima
   SUPABASE_SECRET_KEY=sua_chave_service_role
   ```

3. **Editar `apps/mcp/.env` (Opcional):**
   Caso vá utilizar o servidor MCP conectado ao banco Supabase:
   ```env
   DATABASE_URL=postgresql://postgres.seu-projeto:sua-senha@seu-host:5432/postgres
   ```

---

### Passo 3: Iniciar o Ambiente com Docker Compose
Na raiz do projeto (`laboratorio-ia-docker`), execute o comando para construir as imagens e subir todos os 4 contêineres:
```bash
docker compose up --build -d
```

Aguarde o download e a compilação inicial. Ao finalizar, verifique se todos os serviços estão saudáveis:
```bash
docker compose ps
```
Você verá 4 serviços em execução:
* `laboratorio-rag-frontend` (Porta 3000)
* `laboratorio-rag-backend` (Porta 8000)
* `laboratorio-n8n` (Porta 5678)
* `laboratorio-mcp` (Porta 8001)

---

### Passo 4: Gerar as Notas Fiscais Fictícias de Aula
Em uma máquina nova com clone limpo, as pastas de documentos iniciam vazias.

Gere todas as **13 notas fiscais didáticas completas** com um único comando executado **diretamente dentro do contêiner Docker** (sem precisar de Python ou bibliotecas instaladas na sua máquina):
```bash
docker compose exec rag-backend python generate_invoices.py
```
Esse comando criará automaticamente as notas fiscais `NF-001001` até `NF-001013` dentro da pasta `./dados/documentos/raw`.

> 💡 **Dica:** Você também pode simplesmente arrastar qualquer arquivo PDF de nota fiscal para a pasta local `./dados/documentos/raw`.

---

### Passo 5: Configurar e Ativar o n8n

Como o volume de dados do n8n inicia limpo no novo computador, configure o workflow de ingestão seguindo estes passos rápidos:

1. Acesse no navegador: [http://localhost:5678](http://localhost:5678)
2. No primeiro acesso, crie seu usuário e senha de administrador local no n8n.
3. No menu lateral esquerdo, vá em **Workflows**.
4. No canto superior direito, clique no menu de três pontinhos `...` e escolha **Import from File**.
5. Selecione o arquivo [`workflows/pipeline_ingestao_rag.json`](workflows/pipeline_ingestao_rag.json) da pasta do projeto.
6. **Ativar o Gatilho Automático:**
   * No canto superior direito da tela do fluxo aberto, localize a chave de status (ao lado do botão *Test step*).
   * Altere a chave de **Inactive** para **Active**.
   * Clique em **Save** (ou `Ctrl+S`).
7. **Pronto!** O n8n agora monitora a pasta `/data/documentos/raw`. Assim que novos PDFs chegarem, ele aciona automaticamente a API de ingestão e move os arquivos processados para `gold`.

---

### Passo 6: Ingerir os Documentos no Banco Vetorial

Você pode processar os documentos gerados de 3 formas:

* **Opção 1 (Automática via n8n):** Com o workflow em **Active**, o n8n processa as notas automaticamente em lote.
* **Opção 2 (Pela Interface Web do RAG):** Acesse [http://localhost:3000](http://localhost:3000) e clique no botão **"Ingerir Notas Fiscais"**.
* **Opção 3 (Via API direta):** Execute no terminal:
  ```bash
  curl -X POST http://localhost:8000/api/ingest/default-invoices?base_id=default
  ```

Após o processamento, as notas processadas sairão de `dados/documentos/raw` e estarão salvas em `dados/documentos/gold`.

---

### Passo 7: Testar Perguntas no Chat RAG

Abra o frontend no navegador: **[http://localhost:3000](http://localhost:3000)**

Faça perguntas no chat para testar a recuperação e raciocínio da LLM:

* *"Quais produtos constam na nota fiscal NF-001001 e qual o valor total?"*
* *"Liste os itens adquiridos na nota fiscal NF-001010 de banco de dados vetorial."*
* *"Quais notas fiscais tratam de segurança da informação, auditoria ou firewall?"*
* *"Qual o valor total somado de todas as notas fiscais emitidas para a Escola Teophilo?"*

---

## 🌐 Tabela de Portas e Endpoints

| Serviço | URL de Acesso | Finalidade |
| :--- | :--- | :--- |
| **Frontend RAG** | [http://localhost:3000](http://localhost:3000) | Interface gráfica com Chat RAG e Dashboard |
| **Backend Swagger (API Docs)** | [http://localhost:8000/docs](http://localhost:8000/docs) | Documentação interativa de todas as rotas da API |
| **Backend Health Check** | [http://localhost:8000/api/health](http://localhost:8000/api/health) | Diagnóstico do RAG, modelo de embedding e Supabase |
| **Orquestrador n8n** | [http://localhost:5678](http://localhost:5678) | Painel visual de automação e fluxos de dados |
| **Servidor MCP (Streamable HTTP)** | [http://localhost:8001/mcp](http://localhost:8001/mcp) | Endpoint HTTP para agentes e ferramentas |

---

## 📂 Estrutura das Pastas de Documentos

O diretório local [`dados/documentos/`](dados/documentos) é compartilhado com os contêineres via volume Docker (`/data/documentos`):

```text
dados/documentos/
├── raw/     # Entrada: Coloque aqui os PDFs brutos que serão processados
├── silver/  # Intermediário: Validação e OCR estruturado
└── gold/    # Concluído: Documentos indexados com sucesso no banco vetorial
```

---

## 🔌 Conectando o Servidor MCP na sua IDE (Antigravity ou Cursor)

Para utilizar o servidor FastMCP diretamente conectado via `stdio` na sua IDE local:

Edite o arquivo de configuração de servidores MCP da IDE (ou `.agents/mcp_config.json`):
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

## 🛠️ Comandos Úteis do Docker para Sala de Aula

* **Verificar o status dos contêineres:**
  ```bash
  docker compose ps
  ```
* **Visualizar logs em tempo real (todos os serviços):**
  ```bash
  docker compose logs -f
  ```
* **Visualizar logs apenas do Backend RAG:**
  ```bash
  docker compose logs -f rag-backend
  ```
* **Visualizar logs apenas do n8n:**
  ```bash
  docker compose logs -f n8n
  ```
* **Reiniciar um serviço específico:**
  ```bash
  docker compose restart rag-backend
  ```
* **Parar o laboratório preservando os dados:**
  ```bash
  docker compose down
  ```
* **Reconstruir as imagens após atualizações de código:**
  ```bash
  docker compose up --build -d
  ```

---

## ❓ Resolução de Problemas Comuns (Troubleshooting)

### 1. Coloquei o PDF na pasta `raw`, mas o n8n não processou
* Verifique se o workflow do n8n está com o switch marcado como **Active** no canto superior direito da tela do fluxo.
* Se estiver inativo, mude para **Active** e salve.
* Caso prefira testar manualmente, clique no nó `Local File Trigger` e selecione **Test step** ou clique no botão **"Ingerir Notas Fiscais"** em [http://localhost:3000](http://localhost:3000).

### 2. A LLM respondeu "Sem dados disponiveis na base"
* O sistema possui uma diretriz estrita anti-alucinação. Isso significa que os chunks daquela nota fiscal específica não foram encontrados no banco vetorial.
* Verifique se o arquivo PDF foi ingerido e movido para a pasta `dados/documentos/gold/`.
* Acesse [http://localhost:8000/api/documents](http://localhost:8000/api/documents) no navegador para conferir se a nota aparece listada e se o campo `itens` possui produtos cadastrados.

### 3. Erro de porta já em uso (`bind: address already in use`)
* Se você já tiver outro serviço rodando nas portas `3000`, `8000`, `5678` ou `8001`, pare a aplicação anterior ou execute:
  ```bash
  docker compose down
  ```
