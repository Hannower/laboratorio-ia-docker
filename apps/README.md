# Apps da formação

Cada projeto desenvolvido em aula fica em uma pasta própria dentro de `apps/`, por exemplo `apps/rag`, `apps/mcp`, `apps/agente-a` e `apps/agente-b`.

Cada app declara suas dependências e pode ter seu próprio Dockerfile. Python e Node.js usam imagens separadas; `compose.yaml` define como se comunicam na rede comum `aula`. Serviços de banco continuam remotos (Supabase), portanto não há contêiner de banco nesta composição.

Não coloque ambientes `venv`, `node_modules`, `.env`, tokens ou documentos de alunos dentro do Git. Os arquivos de dados de aula ficam em `dados/documentos` e são montados nos serviços que precisam deles.

## Dependências Python previstas

O RAG instala FastAPI/Uvicorn, FastEmbed, PDFPlumber/PyPDF, tiktoken e python-dotenv. MCP instala o SDK `mcp` e python-dotenv. Agentes poderão instalar LangChain e seus conectores somente quando essa etapa for adicionada. A lista final deve acompanhar as dependências reais de cada app, sem exigir bibliotecas que não usa.
