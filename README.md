# Bot Mentor

Assistente pessoal de IA construído com Python e Telegram, com memória vetorial persistente por usuário. O bot mantém contexto entre sessões armazenando e recuperando o histórico de conversas por busca semântica, imitando o comportamento de agentes com memória de longo prazo.

## Funcionalidades

- IA conversacional via [OpenRouter](https://openrouter.ai) (suporta qualquer modelo LLM)
- Transcrição de mensagens de voz via [Groq Whisper](https://console.groq.com)
- Memória persistente por usuário usando banco de vetores local (ChromaDB)
- Recuperação semântica: a cada interação, as memórias mais relevantes são injetadas no prompt automaticamente
- A memória sobrevive a reinicializações do bot — armazenada em disco, não em RAM

## Arquitetura

```
Mensagem do usuário
    → Busca semântica na memória do usuário (ChromaDB)
    → Injeta memórias relevantes no system prompt
    → Chama o LLM via OpenRouter
    → Salva a interação no banco de vetores
    → Responde ao usuário
```

## Estrutura do Projeto

```
.
├── bot.py        # Bot do Telegram e handlers de mensagem
├── memory.py     # Módulo de memória vetorial (ChromaDB + sentence-transformers)
├── .env          # Chaves de API (não versionado)
├── .gitignore
└── chroma_db/    # Banco de vetores persistente (não versionado)
```

## Requisitos

- Python 3.10+
- Token do Bot do Telegram (via [BotFather](https://t.me/botfather))
- Chave de API da OpenRouter
- Chave de API da Groq

## Configuração

1. Clone o repositório:

```bash
git clone https://github.com/daniz019/bot_mentor.git
cd bot_mentor
```

2. Instale as dependências:

```bash
pip install python-telegram-bot requests chromadb sentence-transformers python-dotenv
```

3. Crie um arquivo `.env` na raiz do projeto:

```env
TELEGRAM_TOKEN=seu_token_telegram
OPENROUTER_API_KEY=sua_chave_openrouter
OPENROUTER_MODEL=anthropic/claude-3.5-haiku
GROQ_API_KEY=sua_chave_groq
```

4. Rode o bot:

```bash
python bot.py
```

## Comportamento da Memória

Cada usuário do Telegram possui uma coleção de memória isolada. Cada turno de conversa (pergunta + resposta) é transformado em vetor e armazenado. Nas mensagens seguintes, o sistema recupera as 5 memórias semanticamente mais próximas e as inclui no contexto enviado ao LLM.

Isso permite que o bot lembre de fatos, preferências e interações passadas indefinidamente, sem nenhum gerenciamento manual de sessão ou sumarização.

