# Bot Mentor

Bot pessoal de IA no Telegram integrado com OpenRouter (LLM) e Groq Whisper (transcrição de voz). Responde mensagens de texto e áudios com uma IA configurável via variáveis de ambiente.

## Funcionalidades

- IA conversacional via [OpenRouter](https://openrouter.ai) (suporta qualquer modelo LLM)
- Transcrição de mensagens de voz via [Groq Whisper](https://console.groq.com)
- Configuração por variáveis de ambiente

## Estrutura do Projeto

```
.
├── bot.py            # Bot do Telegram e handlers de mensagem
├── requirements.txt  # Dependências do projeto
├── .env              # Chaves de API (não versionado)
└── .gitignore
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
pip install -r requirements.txt
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
