# Bot Mentor

Bot pessoal de IA no Telegram com **memória inteligente persistente por usuário**. A cada mensagem, o bot recupera automaticamente as interações mais relevantes do histórico usando a API do [Mem0](https://mem0.ai) e as injeta no contexto da IA — sem limite de tempo, sem perder detalhes importantes.

## Funcionalidades

- IA conversacional via [OpenRouter](https://openrouter.ai) (suporta qualquer modelo LLM)
- Transcrição de mensagens de voz via [Groq Whisper](https://console.groq.com)
- Memória inteligente persistente na nuvem gerenciada pelo Mem0
- Busca semântica avançada: recupera o contexto necessário do histórico a cada interação
- Atualização dinâmica de memórias (o Mem0 condensa o conhecimento e apaga informações irrelevantes)

## Como funciona

```
Mensagem do usuário
    → Recuperação de memórias relevantes do usuário via API do Mem0
    → Injeta as memórias recuperadas no system prompt
    → Chama o LLM via OpenRouter para gerar a resposta
    → Salva/Atualiza as informações da interação na memória do Mem0
    → Responde ao usuário
```

## Estrutura do Projeto

```
.
├── bot.py            # Bot do Telegram e handlers de mensagem
├── memory.py         # Módulo de inicialização e gerenciamento do Mem0
├── requirements.txt  # Dependências do projeto (incluindo mem0ai)
├── .env              # Chaves de API (não versionado)
└── .gitignore
```

## Requisitos

- Python 3.10+
- Token do Bot do Telegram (via [BotFather](https://t.me/botfather))
- Chave de API da OpenRouter
- Chave de API da Groq (para transcrição de mensagens de voz)
- Chave de API do Mem0

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

3. Crie um arquivo `.env` na raiz do projeto com suas chaves:

```env
TELEGRAM_TOKEN=seu_token_telegram
OPENROUTER_API_KEY=sua_chave_openrouter
OPENROUTER_MODEL=anthropic/claude-3.5-haiku
GROQ_API_KEY=sua_chave_groq
MEM0_API_KEY=sua_chave_mem0
```

4. Rode o bot:

```bash
python bot.py
```
