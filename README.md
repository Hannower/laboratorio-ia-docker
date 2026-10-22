# Laboratório de IA Generativa com Docker

Ambiente didático para reaproveitar projetos da formação em computadores diferentes. O objetivo é manter versões e dependências em contêineres e iniciar os serviços com Docker Compose.

## Estado inicial

Esta primeira versão prepara o n8n e a estrutura compartilhada de documentos. Os serviços RAG, Next.js, MCP e agentes serão adicionados quando o código de cada projeto estiver integrado a este repositório.

```text
aluno/navegador
      │
      ├── Next.js (futuro)
      ├── Backend Python / RAG (futuro) ── Supabase remoto / OpenRouter
      ├── MCP Streamable HTTP (futuro)
      └── n8n ── rede Docker compartilhada
                 └── /data/documentos/{raw,silver,gold}
```

## Requisitos no Windows 11

- Docker Desktop atualizado e iniciado, usando o backend WSL 2.
- Git para clonar o repositório.
- Conexão à internet no primeiro início para baixar a imagem do n8n.
- Recomendado para trabalhar com IDE, navegador e serviços simultâneos: 16 GB de RAM.

Node.js, Python, npm e uv não precisam estar instalados no Windows para os serviços que forem executados em contêineres. O desenvolvimento local fora do Docker pode continuar exigindo essas ferramentas.

## Iniciar

No PowerShell, na pasta clonada:

```powershell
Copy-Item .env.example .env
docker compose up -d
```

Abra http://localhost:5678 e conclua a criação da conta local do n8n. Para acompanhar:

```powershell
docker compose ps
docker compose logs -f n8n
```

Para parar sem remover os dados persistidos:

```powershell
docker compose down
```

Não use `docker compose down -v` se quiser preservar os workflows, credenciais e dados locais do n8n.

## Pastas de dados da turma

Os diretórios `dados/documentos/raw`, `silver` e `gold` são compartilhados com o contêiner n8n em `/data/documentos`. Os alunos podem trazer os arquivos de exercício em pendrive ou copiá-los do Drive para `raw`.

- **raw**: arquivos de origem ainda não tratados.
- **silver**: resultados da transformação básica, quando a etapa ETL for introduzida.
- **gold**: dados preparados para consumo no laboratório.

Criar essas pastas é uma preparação de organização. A movimentação de um arquivo, por si só, não executa limpeza, validação ou ETL. Não coloque dados pessoais, documentos confidenciais nem credenciais reais nos exemplos do repositório público.

## Organização prevista

- `frontend/`: interface Next.js, adicionada quando o frontend for integrado.
- `backend/`: API Python e aplicação RAG.
- `mcp/`: servidor MCP, inicialmente com transporte HTTP na rede Docker.
- `workflows/`: exportações de workflows n8n sem segredos.
- `dados/documentos/raw|silver|gold/`: dados de exercício locais, ignorados pelo Git.
- `compose.yaml`: serviços, rede e volumes.

## Persistência e troca de computador

Git guarda código e configurações versionadas. O volume Docker `n8n_data` guarda workflows, credenciais e estado do n8n na máquina local; ele não acompanha um clone do Git.

Para continuar em outro computador:

1. Clone este repositório.
2. Copie os arquivos de exercício do pendrive ou do Drive para `dados/documentos`.
3. Recrie o arquivo `.env` usando `.env.example`.
4. Inicie com `docker compose up -d`.
5. Importe os workflows versionados em `workflows/` e configure as credenciais próprias daquele computador.

Se for necessário recuperar o estado completo do n8n, faça backup do volume `n8n_data` e da chave de criptografia da instância. Não publique esse backup nem a chave. As credenciais podem ser criptografadas e não são portáveis sem a chave correspondente.

## Rede dos contêineres

Os serviços conectam-se pelo nome do serviço dentro da rede Compose, por exemplo `http://backend:8000` e `http://mcp:8001/mcp`. O navegador no Windows usa as portas publicadas em `localhost`. Não use `localhost` dentro de um contêiner para acessar outro serviço: ali, localhost aponta para o próprio contêiner.

## Integração RAG + n8n planejada

1. O gatilho de arquivo observa `/data/documentos/raw`.
2. Um evento de arquivo inicia o fluxo.
3. O nó HTTP Request chama a API RAG pelo nome do serviço Compose.
4. O fluxo confirma que a ingestão terminou com sucesso.
5. A aplicação RAG continua responsável por persistir os registros e mover o original para `gold`.

Apenas um componente deve mover o arquivo para `gold`. O fluxo deve tratar arquivo ainda em cópia, eventos repetidos, nomes duplicados e falhas parciais. O Local File Trigger é um recurso de n8n auto-hospedado e precisa de configuração deliberada.

## Etapas seguintes da formação

- **Data Lake**: apresentar a estrutura raw/gold e as regras de armazenamento.
- **ETL/ELT**: acrescentar silver e transformações verificáveis.
- **Agentes**: incorporar LangChain e memória como serviços opcionais, com credenciais separadas.
- **Integração final**: conectar frontend, API RAG, MCP, n8n e agentes pela rede Compose, ativando apenas os serviços da aula.

Consulte `docs/PLANO.md` para o desenho incremental.

## Segurança didática

- `.env`, documentos de exercício, credenciais n8n e estado local ficam fora do Git.
- Use chaves com menor privilégio possível e nunca compartilhe chaves secretas em sala, prints, workflows exportados ou commits.
- Restrinja o n8n à máquina local durante o laboratório; não habilite acesso público sem configurar autenticação e revisar a segurança.
- O nó Local File Trigger acessa o sistema de arquivos montado. Monte apenas a pasta de dados necessária.
- Não habilite nós de execução arbitrária de comandos para este exercício.

## Documentação oficial

- [Docker Desktop no Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Docker Compose](https://docs.docker.com/compose/)
- [n8n com Docker Compose](https://docs.n8n.io/hosting/installation/docker/)
- [Local File Trigger](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.localfiletrigger/)
- [n8n Community Edition](https://docs.n8n.io/hosting/community-edition-features/)
