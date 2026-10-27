# 🔌 MCP Supabase Server (RAG Bridge)

> Servidor baseado no **Model Context Protocol (MCP)** para permitir que Agentes de IA consultem dados relacionais e vetoriais de documentos fiscais armazenados no **Supabase**.

---

## 🎯 Objetivo

Este projeto atua como uma ponte padronizada de comunicação (via protocolo MCP e transporte `stdio`) entre assistentes de inteligência artificial (como Antigravity, Claude Desktop ou Cursor) e a base de dados PostgreSQL/pgvector gerenciada pelo pipeline RAG.

Com este conector, o Agente de IA ganha a ferramenta (tool) necessária para inspecionar, auditar e recuperar trechos de notas fiscais diretamente da tabela `rag_chunks`.

---

## 🏗️ Arquitetura

```
[ Agente de IA (Antigravity) ]
            │
            │ (stdio / MCP Protocol)
            ▼
[ Servidor MCP Local (server.py) ]
            │
            │ (Conexão Direta / psycopg2)
            ▼
[ Banco Supabase PostgreSQL ]
            └── Tabela: rag_chunks (Documentos RAG)
```

---

## 📂 Estrutura de Arquivos

```text
mcp-supabase-server/
├── .venv/               # Ambiente virtual Python isolado
├── .env                 # Credenciais de conexão (ignorado pelo git)
├── .env.example         # Exemplo de configuração das variáveis
├── .gitignore           # Filtro de arquivos sensíveis e temporários
├── server.py            # Servidor FastMCP com a ferramenta de consulta
└── README.md            # Documentação do projeto
```

---

## ⚙️ Pré-requisitos

1. **Python 3.10+** instalado.
2. Projeto RAG configurado com tabelas criadas no **Supabase**.
3. String de conexão PostgreSQL do Supabase (`postgresql://...`).

---

## 🚀 Instalação e Configuração

### 1. Criar e Ativar o Ambiente Virtual

No diretório do projeto:

**No Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**No Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar Dependências

Com a `.venv` ativada, execute:

```bash
pip install mcp psycopg2-binary python-dotenv
```

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://postgres.SEU_PROJETO:SUA_SENHA@SEU_HOST:PORT/postgres
```

> ⚠️ **Atenção:** Caso sua string de conexão do Supabase inclua o parâmetro `?pgbouncer=true`, certifique-se de removê-lo se o driver `psycopg2` apresentar problemas de conexão direta.

---

## 🛠️ Ferramentas Disponíveis no MCP

| Ferramenta | Descrição | Parâmetros |
| :--- | :--- | :--- |
| `listar_chunks_rag` | Consulta trechos de notas fiscais armazenados no Supabase | `limite` (int, padrão: 3) |

---

## 🔌 Conexão com o Antigravity / Clientes MCP

Para registrar este servidor no seu cliente (ex.: no arquivo `settings.json` do VS Code para o Antigravity):

```json
{
  "antigravity.mcpServers": {
    "mcp-supabase": {
      "command": "C:\\CAMINHO\\COMPLETO\\mcp-supabase-server\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\CAMINHO\\COMPLETO\\mcp-supabase-server\\server.py"
      ]
    }
  }
}
```

> **Dica:** No Windows, lembre-se de usar barras duplas (`\\`) nos caminhos do arquivo JSON.

---

## 💬 Exemplo de Uso com o Agente

Após recarregar o cliente com o servidor registrado, você pode solicitar ao Agente:

> *"Use a ferramenta `listar_chunks_rag` para verificar quais notas fiscais e itens estão registrados no banco do Supabase."*