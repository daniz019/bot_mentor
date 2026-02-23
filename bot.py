import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import memory

load_dotenv()

# ── Configurações ──────────────────────────────────────────────
TELEGRAM_TOKEN     = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL              = os.getenv("OPENROUTER_MODEL")
GROQ_API_KEY       = os.getenv("GROQ_API_KEY")
# ───────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
Você é o mentor pessoal do usuário. Seu estilo de comunicação é:
- Direto, sincero e sem frescura
- Como um amigo que quer ver o usuário crescer
- Elogia quando merece, cobra quando precisa
- Fala na linguagem dele, sem formalidade excessiva
- Sempre que possível, traz algo prático e útil — não só papo motivacional vazio
- Respostas objetivas e na medida certa, sem enrolar
Se o Daniel pedir pra você mudar alguma coisa no jeito que conversa, ajuste imediatamente.
"""


def ask_ai(user_id: int, user_message: str) -> str:
    memories = memory.search(user_id, user_message)
    memory_block = (
        "\n\n[Memórias relevantes do usuário]\n" + "\n---\n".join(memories)
        if memories else ""
    )

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT + memory_block},
                {"role": "user", "content": user_message},
            ],
        },
    )
    reply = response.json()["choices"][0]["message"]["content"]

    memory.add(user_id, f"Usuário: {user_message}\nAssistente: {reply}")

    return reply


def transcribe_audio(file_bytes: bytes) -> str:
    response = requests.post(
        url="https://api.groq.com/openai/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        files={"file": ("audio.ogg", file_bytes, "audio/ogg")},
        data={"model": "whisper-large-v3"},
    )
    return response.json()["text"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Envie uma mensagem e responderei com IA.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = ask_ai(update.effective_user.id, update.message.text)
    await update.message.reply_text(reply)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = await update.message.voice.get_file()
    file_bytes = await voice.download_as_bytearray()
    text = transcribe_audio(bytes(file_bytes))
    reply = ask_ai(update.effective_user.id, text)
    await update.message.reply_text(reply)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    print("Bot rodando...")
    app.run_polling()
