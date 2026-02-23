import os
import asyncio
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import memory

load_dotenv()

TELEGRAM_TOKEN     = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL              = os.getenv("OPENROUTER_MODEL")
GROQ_API_KEY       = os.getenv("GROQ_API_KEY")
MAX_HISTORY_TURNS  = 10

SYSTEM_PROMPT = """
Você é o mentor pessoal do usuário. Seu estilo de comunicação é:
- Direto, sincero e sem frescura
- Como um amigo que quer ver o usuário crescer
- Elogia quando merece, cobra quando precisa

SOBRE AS MEMÓRIAS:
Antes de cada resposta você recebe um bloco com memórias de conversas passadas com este usuário.
Você DEVE usar essas memórias para contextualizar sua resposta.
NUNCA pergunte algo que já está respondido nas memórias.
Aja como alguém que conhece bem o usuário e se lembra de tudo que ele já contou.
"""


def _trim_history(history: list) -> list:
    max_msgs = MAX_HISTORY_TURNS * 2
    return history[-max_msgs:] if len(history) > max_msgs else history


async def _ask_ai(user_id: int, user_message: str, history: list) -> str:
    from datetime import datetime
    loop = asyncio.get_running_loop()
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    memories = await loop.run_in_executor(None, memory.get_all, user_id)
    memory_block = (
        "\n\n[Memórias consolidadas do usuário (Mem0)]:\n" + "\n---\n".join(memories)
        if memories else ""
    )

    messages = [
        {"role": "system", "content": f"[Agora: {now}]\n" + SYSTEM_PROMPT + memory_block},
        *history,
        {"role": "user", "content": user_message},
    ]

    response = await loop.run_in_executor(
        None,
        lambda: requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
            json={"model": MODEL, "messages": messages},
            timeout=60,
        ),
    )

    data = response.json()
    if "choices" not in data:
        raise RuntimeError(f"Erro da API: {data}")

    reply = data["choices"][0]["message"]["content"]
    await loop.run_in_executor(None, memory.add, user_id, user_message, reply)
    return reply


async def _send(update: Update, text: str):
    for i in range(0, len(text), 4000):
        await update.message.reply_text(text[i:i + 4000])


async def _process(update: Update, context: ContextTypes.DEFAULT_TYPE, user_message: str):
    user_id = update.effective_user.id
    history = context.user_data.get("history", [])

    try:
        reply = await _ask_ai(user_id, user_message, history)
    except Exception as e:
        await update.message.reply_text(f"Erro: {e}")
        return

    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": reply})
    context.user_data["history"] = _trim_history(history)

    await _send(update, reply)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["history"] = []
    await update.message.reply_text("Olá! Envie uma mensagem e responderei com IA.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _process(update, context, update.message.text)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loop = asyncio.get_running_loop()
    voice = await update.message.voice.get_file()
    file_bytes = await voice.download_as_bytearray()

    try:
        text = await loop.run_in_executor(
            None,
            lambda: requests.post(
                url="https://api.groq.com/openai/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                files={"file": ("audio.ogg", bytes(file_bytes), "audio/ogg")},
                data={"model": "whisper-large-v3"},
                timeout=60,
            ).json()["text"],
        )
    except Exception as e:
        await update.message.reply_text(f"Erro na transcrição: {e}")
        return

    await _process(update, context, text)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    print("Bot rodando...")
    app.run_polling()
