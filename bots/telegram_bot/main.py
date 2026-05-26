"""
Telegram бот для платформы "Семейные корни"
Привлечение пользователей и уведомления
"""

import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler
)
import os
import httpx

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

# Conversation states
NAME, EMAIL, BIRTHPLACE = range(3)

class FamilyRootsBot:
    def __init__(self, token: str):
        self.token = token
        self.application = None

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler для /start команды"""
        user = update.effective_user
        keyboard = [
            [InlineKeyboardButton("👨‍👩‍👧‍👦 Начать", callback_data="start_tree")],
            [InlineKeyboardButton("🔍 Поиск родственников", callback_data="search")],
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
            [InlineKeyboardButton("🎁 Достижения", callback_data="achievements")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"""Привет, {user.first_name}! 👋

Добро пожаловать в **Семейные корни** - платформу для изучения истории вашей семьи!

🔗 Наша платформа помогает вам:
• Построить генеалогическое дерево
• Найти дальних родственников
• Изучить историю вашей семьи
• Сохранить семейное наследие

Начнем?""",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def start_tree(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начать построение генеалогического дерева"""
        query = update.callback_query
        await query.answer()

        await query.edit_message_text(
            text="Давайте начнем! Сначала расскажите о себе.\n\n"
                 "Как вас зовут?",
            reply_markup=None
        )
        return NAME

    async def get_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получить имя пользователя"""
        user_name = update.message.text
        context.user_data['name'] = user_name

        await update.message.reply_text(
            f"Приятно познакомиться, {user_name}! 😊\n\n"
            "Ваш email для регистрации:"
        )
        return EMAIL

    async def get_email(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получить email пользователя"""
        email = update.message.text
        context.user_data['email'] = email

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{API_URL}/auth/register",
                    json={
                        "email": email,
                        "password": "temp_password",
                        "full_name": context.user_data.get('name', 'User')
                    }
                )
                if response.status_code == 200:
                    await update.message.reply_text(
                        f"✅ Спасибо! Регистрация завершена.\n\n"
                        f"Ссылка на платформу: https://familyroots.ru?ref=telegram"
                    )
                else:
                    await update.message.reply_text(
                        "❌ Ошибка регистрации. Пожалуйста, попробуйте позже."
                    )
            except Exception as e:
                logger.error(f"Registration error: {e}")
                await update.message.reply_text(
                    "❌ Ошибка подключения. Попробуйте позже."
                )

        return ConversationHandler.END

    async def search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Поиск родственников"""
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("По имени", callback_data="search_name")],
            [InlineKeyboardButton("По дате рождения", callback_data="search_birth")],
            [InlineKeyboardButton("Назад", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="Как вы хотите искать?",
            reply_markup=reply_markup
        )

    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать статистику"""
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="""📊 Статистика платформы:

👥 Активных пользователей: 1,234
👨‍👩‍👧‍👦 Добавлено персон: 1,500,000
🔗 Создано связей: 3,000,000
🏆 Достижений разблокировано: 12,450""",
            reply_markup=reply_markup
        )

    async def show_achievements(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать достижения"""
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="""🏆 Ваши достижения:

🥇 Архивист (100+ персон) - 5 уровень
🎯 Летописец (5+ веков) - 3 уровень
🔍 Сыщик (10+ совпадений) - 2 уровень
📚 Историк (50+ документов) - 1 уровень

Продолжайте развиваться! 🚀""",
            reply_markup=reply_markup
        )

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик кнопок"""
        query = update.callback_query
        await query.answer()

        if query.data == "back":
            await self.start(update, context)
        elif query.data == "start_tree":
            await self.start_tree(update, context)
        elif query.data == "search":
            await self.search(update, context)
        elif query.data == "stats":
            await self.show_stats(update, context)
        elif query.data == "achievements":
            await self.show_achievements(update, context)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler для /help команды"""
        help_text = """
🆘 Справка по командам:

/start - Начало работы
/help - Эта справка
/register - Регистрация
/search - Поиск родственников
/stats - Статистика
/achievements - Мои достижения

Для получения помощи посетите: https://familyroots.ru/help
"""
        await update.message.reply_text(help_text)

    async def setup(self):
        """Настройка бота"""
        self.application = Application.builder().token(self.token).build()

        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))

        # Conversation handler
        conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.start_tree, pattern="start_tree")],
            states={
                NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_name)],
                EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_email)],
            },
            fallbacks=[CommandHandler("start", self.start)],
        )
        self.application.add_handler(conv_handler)

        # Button handlers
        self.application.add_handler(CallbackQueryHandler(self.button_handler))

    async def run(self):
        """Запуск бота"""
        await self.setup()
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        logger.info("🤖 Telegram бот запущен!")

async def main():
    """Main entry point"""
    bot = FamilyRootsBot(TOKEN)
    try:
        await bot.run()
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")

if __name__ == "__main__":
    asyncio.run(main())
