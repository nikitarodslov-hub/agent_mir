import anthropic
from .knowledge_base import COMPANY_KNOWLEDGE, QUESTION_TYPE_NAMES

SOURCE_AVITO = "авито"

SYSTEM_PROMPT_TEMPLATE = """Ты — помощник менеджера по продажам магазина Miraphone (I-Mart), магазин БУ техники Apple.

{knowledge}

---

ТВОЯ ЗАДАЧА:
Написать ГОТОВЫЙ ответ клиенту от имени менеджера магазина.
- Не объясняй свои действия, не пиши ничего лишнего — только текст ответа клиенту
- Обращайся к клиенту по имени: {client_name}
- Источник сообщения: {source}
- Тип вопроса клиента: {question_type}
{avito_note}
- Пиши живым языком, дружелюбно, коротко
- ОБЯЗАТЕЛЬНО заканчивай вопросом или призывом к действию
"""

AVITO_NOTE = """
!!! ИСТОЧНИК — АВИТО. Обязательные правила:
- Описывай состояние ТОЛЬКО через категорию: Категория А / Категория Б / Категория С
- Никаких слов "отличный", "хороший", "прекрасный"
- Не указывай контактные данные
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
        avito_note = AVITO_NOTE if SOURCE_AVITO in source.lower() else ""
        q_type_name = QUESTION_TYPE_NAMES.get(question_type, question_type)

        system = SYSTEM_PROMPT_TEMPLATE.format(
            knowledge=COMPANY_KNOWLEDGE,
            client_name=client_name,
            source=source,
            question_type=q_type_name,
            avito_note=avito_note,
        )

        conversation_text = "\n".join(
            f"[{i+1}] {msg}" for i, msg in enumerate(messages)
        )
        user_content = f"Сообщение(я) от клиента:\n{conversation_text}"

        if inventory_info:
            user_content += f"\n\nДанные склада (МойСклад):\n{inventory_info}"

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            system=system,
            messages=[{"role": "user", "content": user_content}],
        )

        return response.content[0].text.strip()
