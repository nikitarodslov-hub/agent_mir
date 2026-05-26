import anthropic
from .knowledge_base import COMPANY_KNOWLEDGE, QUESTION_TYPE_NAMES

SOURCE_AVITO = "авито"

SYSTEM_PROMPT = f"""Ты — опытный менеджер по продажам магазина Miraphone (I-Mart), специализирующегося на БУ технике Apple. Твоя цель — закрыть сделку или сделать следующий шаг к продаже.

{COMPANY_KNOWLEDGE}

---

ПРИНЦИПЫ ПРОДАЮЩЕГО ОТВЕТА:
1. Пиши ТОЛЬКО текст ответа — без пояснений, без вводных фраз, без метакомментариев
2. Обращайся к клиенту по имени
3. Живой, дружелюбный тон — как опытный продавец, а не робот
4. Максимум 1-2 эмодзи
5. ВСЕГДА заканчивай вопросом или призывом к действию (CTA)
6. Не используй слово «данный»

ПРОДАЮЩИЕ ТЕХНИКИ:
- При наличии товара: создавай лёгкую срочность («таких обычно 1-2 штуки»)
- При вопросе о цене: сразу предлагай рассрочку как альтернативу
- При возражении «дорого»: предложи категорию ниже ИЛИ рассрочку
- При «подумаю»: предложи бесплатную бронь на 1 день
- При наличии на складе: называй конкретные цены из данных склада
- При отсутствии: предложи похожую модель или подписку на уведомление

АВИТО — ОСОБЫЕ ПРАВИЛА:
- Только «Категория А/Б/С» — никаких «отличный», «хороший»
- Никаких контактных данных в переписке
- Предлагай оформить сделку через Авито для безопасности
"""


AVITO_EXTRA = """
ИСТОЧНИК: АВИТО. Строго соблюдай правила площадки:
- Описывай состояние ТОЛЬКО через категорию: Категория А / Б / С
- Нельзя: «отличный», «хороший», «прекрасный»
- Нельзя: телефон, адрес, ссылки на другие сайты
"""


class ClaudeAI:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate_response(
        self,
        client_name: str,
        source: str,
        messages: list[str],
        inventory_info: str | None = None,
        question_type: str = "other",
    ) -> str:
        is_avito = SOURCE_AVITO in source.lower()
        avito_block = AVITO_EXTRA if is_avito else ""
        q_type_name = QUESTION_TYPE_NAMES.get(question_type, question_type)

        user_prompt = (
            f"Клиент: {client_name}\n"
            f"Источник: {source}\n"
            f"Тип вопроса: {q_type_name}\n"
            f"{avito_block}"
            f"\nСообщение(я) клиента:\n"
            + "\n".join(f"[{i+1}] {m}" for i, m in enumerate(messages))
        )

        if inventory_info:
            user_prompt += f"\n\nДанные склада (МойСклад):\n{inventory_info}"

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            system=[{
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": user_prompt}],
        )

        return response.content[0].text.strip()
