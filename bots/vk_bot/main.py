"""
VK бот для платформы "Семейные корни"
Интеграция с ВКонтакте для привлечения пользователей
"""

import logging
import json
import asyncio
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VK_TOKEN = os.getenv("VK_TOKEN")
VK_GROUP_ID = os.getenv("VK_GROUP_ID", "123456789")

class FamilyRootsVKBot:
    def __init__(self, token: str, group_id: str):
        self.token = token
        self.group_id = group_id
        self.vk = VkApi(token=token)
        self.longpoll = None

    def init_longpoll(self):
        """Инициализировать Long Poll"""
        self.longpoll = VkBotLongPoll(self.vk, self.group_id)

    def send_message(self, user_id: int, message: str):
        """Отправить сообщение пользователю"""
        self.vk.method('messages.send', {
            'peer_id': user_id,
            'message': message,
            'random_id': 0
        })

    def send_keyboard(self, user_id: int, message: str, buttons: list):
        """Отправить сообщение с клавиатурой"""
        keyboard = {
            "one_time": False,
            "buttons": buttons
        }

        self.vk.method('messages.send', {
            'peer_id': user_id,
            'message': message,
            'keyboard': json.dumps(keyboard),
            'random_id': 0
        })

    def handle_message(self, event):
        """Обработать входящее сообщение"""
        user_id = event.obj.message['from_id']
        text = event.obj.message['text'].lower()

        logger.info(f"Сообщение от {user_id}: {text}")

        if text == 'привет' or text == '/start':
            self.welcome_user(user_id)
        elif text.startswith('поиск'):
            self.search_relatives(user_id)
        elif text == 'достижения':
            self.show_achievements(user_id)
        elif text == 'статистика':
            self.show_stats(user_id)
        else:
            self.send_message(user_id,
                "🤔 Я не понимаю эту команду. Напишите 'Привет' для начала.")

    def welcome_user(self, user_id: int):
        """Приветствие нового пользователя"""
        self.send_message(user_id,
            "👋 Привет! Добро пожаловать в Семейные корни!\n\n"
            "Я помогу вам построить генеалогическое дерево и найти дальних родственников. 🌳"
        )

        buttons = [
            [
                {
                    "action": {
                        "type": "text",
                        "label": "👨‍👩‍👧‍👦 Начать"
                    }
                }
            ],
            [
                {
                    "action": {
                        "type": "text",
                        "label": "🔍 Поиск"
                    }
                },
                {
                    "action": {
                        "type": "text",
                        "label": "🏆 Достижения"
                    }
                }
            ],
            [
                {
                    "action": {
                        "type": "open_link",
                        "label": "📱 Открыть приложение",
                        "link": "https://familyroots.ru"
                    }
                }
            ]
        ]

        self.send_keyboard(user_id, "Выберите действие:", buttons)

    def search_relatives(self, user_id: int):
        """Функция поиска родственников"""
        self.send_message(user_id,
            "🔍 Функция поиска родственников в разработке!\n\n"
            "Введите имя родственника или посетите сайт: https://familyroots.ru"
        )

    def show_achievements(self, user_id: int):
        """Показать достижения"""
        self.send_message(user_id,
            "🏆 Ваши достижения:\n\n"
            "🥇 Архивист (100+ персон)\n"
            "🎯 Летописец (5+ веков)\n"
            "🔍 Сыщик (10+ совпадений)\n\n"
            "Продолжайте исследовать! 🚀"
        )

    def show_stats(self, user_id: int):
        """Показать статистику платформы"""
        self.send_message(user_id,
            "📊 Статистика Семейных корней:\n\n"
            "👥 Активных пользователей: 1,234\n"
            "👨‍👩‍👧‍👦 Добавлено персон: 1,500,000\n"
            "🔗 Создано связей: 3,000,000\n"
            "🏆 Достижений: 12,450"
        )

    def run(self):
        """Запустить бота"""
        try:
            self.init_longpoll()
            logger.info("🤖 VK бот запущен!")

            for event in self.longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    self.handle_message(event)
        except Exception as e:
            logger.error(f"Ошибка в боте: {e}")
        finally:
            logger.info("VK бот остановлен")

def main():
    """Main entry point"""
    bot = FamilyRootsVKBot(VK_TOKEN, VK_GROUP_ID)
    bot.run()

if __name__ == "__main__":
    main()
