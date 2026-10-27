import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

# Substitua pela sua string de conexão real do Supabase
DATABASE_URL = os.getenv("DATABASE_URL")
HOST = os.getenv("MCP_HOST", "0.0.0.0")
PORT = int(os.getenv("MCP_PORT", "8001"))

# Inicializa o servidor MCP
mcp = FastMCP("SupabaseRAG", host=HOST, port=PORT)

@mcp.tool()
def listar_chunks_rag(limite: int = 3) -> str:
    """Consulte esta ferramenta para ler os trechos de documentos (chunks) armazenados no banco de dados do Supabase."""
    try:
        if not DATABASE_URL:
            return "Erro: Variável de ambiente DATABASE_URL não está configurada."

        # Estabelece conexão direta com o PostgreSQL do Supabase
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Busca amostras na tabela que foi populada pela ingestão
        cursor.execute("SELECT * FROM rag_chunks LIMIT %s;", (limite,))
        linhas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not linhas:
            return "A tabela rag_chunks está vazia ou não foi encontrada."
            
        resultado = "Dados encontrados no Supabase:\n\n"
        for linha in linhas:
            resultado += f"{str(linha)}\n---\n"
            
        return resultado
        
    except Exception as e:
        return f"Erro de conexão com o banco de dados: {str(e)}"

if __name__ == "__main__":
    # Suporta transporte HTTP (SSE ou streamable-http para Docker) ou stdio para clientes locais (IDE)
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
    if transport in ("sse", "streamable-http"):
        mcp.run(transport=transport)
    else:
        mcp.run_stdio_async()