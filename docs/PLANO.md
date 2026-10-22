# Plano de evolução do laboratório

A composição atual inicia somente o n8n. As próximas aplicações entram à medida que seus códigos forem incorporados, com versões fixadas e configurações próprias.

## Fase A — n8n e arquivos (Módulo 3, U1)

- n8n em contêiner.
- `documentos/raw`, `silver` e `gold` montados em `/data/documentos`.
- Local File Trigger observa somente `raw`.
- HTTP Request chama a API RAG pelo nome do serviço na rede Compose.
- RAG confirma persistência; apenas um componente move o original para `gold`.
- Verificar cópias em andamento, eventos repetidos, arquivo repetido e falha parcial.

## Fase B — Data Lake (Módulo 3, U3)

- `raw`: origem bruta; `silver`: transformação validada; `gold`: dados preparados para consumo.
- Git guarda código, schemas, documentação e workflows sem dados confidenciais.
- Dados de aula entram por pendrive ou Drive e ficam em volumes locais ignorados pelo Git.
- Acrescentar manifesto de dados sintéticos e orientação de retenção.

## Fase C — ETL/ELT (Módulo 3, U4)

- Etapa explícita de extração, limpeza, validação e gravação em `silver`.
- Promover para `gold` somente após critérios verificáveis.
- Registrar erros e permitir reprocessamento idempotente.
- Separar workflow n8n das transformações Python existentes.

## Fase D — Agentes e memória (Módulo 4)

- Acrescentar LangChain quando o projeto exigir.
- Manter agente, memória e RAG com responsabilidades claras.
- Chaves do modelo ficam em credenciais locais.
- Definir limites de ferramentas e aprovação humana antes de permitir escrita.

## Arquitetura alvo

- `frontend`: Next.js.
- `backend`: API Python, RAG e integração com OpenRouter/Supabase.
- `mcp`: servidor MCP, inicialmente Streamable HTTP.
- `n8n`: workflows e gatilhos de arquivos.
- `agent`: opcional, somente quando necessário à unidade.
- Todos os serviços usam a rede Compose `aula` e acessam outros serviços por seus nomes.

## Validação antes da turma

1. Iniciar o clone em computador limpo.
2. Confirmar que `raw/silver/gold` ficam visíveis ao n8n.
3. Testar arquivo sintético: chamada da API, persistência e promoção de estágio.
4. Repetir evento e induzir falha para verificar duplicação e recuperação.
5. Testar backup e restauração do volume n8n em outra máquina sob controle do professor.
