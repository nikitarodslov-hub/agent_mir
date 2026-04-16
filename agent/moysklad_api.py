import re
import requests
from typing import Optional


BASE_URL = "https://api.moysklad.ru/api/remap/1.2"

# Категории в названии товара (паттерн: "Категория А/Б/С/S")
CATEGORY_RE = re.compile(r"категори[яи]?\s*([абсsАБСS])", re.IGNORECASE)

# Паттерны для извлечения модели устройства из текста клиента
DEVICE_PATTERNS = [
    # iPhone 13 Pro Max 256GB
    re.compile(
        r"iphone?\s*(\d{1,2})\s*(pro)?\s*(max)?\s*(\d+\s*(?:gb|гб))?",
        re.IGNORECASE,
    ),
    # айфон 13 про 256
    re.compile(
        r"айфон\s*(\d{1,2})\s*(про)?\s*(макс)?\s*(\d+\s*(?:гб|gb))?",
        re.IGNORECASE,
    ),
    # Samsung Galaxy S23 / A54
    re.compile(
        r"samsung\s+galaxy\s+([sa]\d+)(?:\s+ultra|\s+plus|\s+\+)?",
        re.IGNORECASE,
    ),
    re.compile(r"galaxy\s+([sa]\d+)", re.IGNORECASE),
    # MacBook Pro/Air M1/M2/M3 14"
    re.compile(r"macbook\s+(pro|air)?\s*(m\d)?", re.IGNORECASE),
    # iPad Pro/Air/mini
    re.compile(r"ipad\s*(pro|air|mini)?\s*(\d+)?", re.IGNORECASE),
]


class MoySkladAPI:
    def __init__(self, login: str, password: str):
        self.auth = (login, password)
        self._enabled = bool(login and password)

    def is_enabled(self) -> bool:
        return self._enabled

    def search_inventory(self, query: str) -> Optional[str]:
        """Search products by query, return formatted availability string."""
        if not self._enabled:
            return None
        try:
            resp = requests.get(
                f"{BASE_URL}/entity/product",
                auth=self.auth,
                params={"search": query, "limit": 50},
                timeout=10,
            )
            if resp.status_code != 200:
                return None

            products = resp.json().get("rows", [])
            if not products:
                return f"Товар '{query}' не найден на складе"

            product_ids = [p["id"] for p in products[:10]]
            lines = self._get_stock_lines(products[:10], product_ids)

            if not lines:
                return f"'{query}' есть в базе, но наличие = 0"
            return "\n".join(lines)
        except Exception as e:
            return f"Ошибка МойСклад: {e}"

    def _get_stock_lines(self, products: list, product_ids: list) -> list[str]:
        lines = []
        try:
            stock_resp = requests.get(
                f"{BASE_URL}/report/stock/all",
                auth=self.auth,
                params={"limit": 100},
                timeout=10,
            )
            if stock_resp.status_code != 200:
                return lines

            stock_rows = {
                row["meta"]["href"].split("/")[-1]: row
                for row in stock_resp.json().get("rows", [])
                if "meta" in row
            }

            for product in products:
                pid = product["id"]
                row = stock_rows.get(pid)
                if not row:
                    continue
                qty = int(row.get("stock", 0))
                if qty <= 0:
                    continue

                name = product.get("name", "Без названия")
                # price in kopecks → rubles
                sale_price = product.get("salePrices", [{}])[0].get("value", 0) // 100
                category = self._extract_category(name)
                cat_str = f" [{category}]" if category else ""
                price_str = f"{sale_price:,} руб." if sale_price else "цена не указана"
                lines.append(f"• {name}{cat_str} — {qty} шт., {price_str}")
        except Exception:
            pass
        return lines

    def _extract_category(self, name: str) -> str:
        m = CATEGORY_RE.search(name)
        if m:
            c = m.group(1).upper()
            mapping = {"А": "A", "Б": "Б", "С": "C", "S": "S", "A": "A", "B": "Б"}
            return mapping.get(c, c)
        return ""

    def parse_device_from_message(self, text: str) -> Optional[str]:
        """Extract device model mention from client message."""
        for pattern in DEVICE_PATTERNS:
            m = pattern.search(text)
            if m:
                return m.group(0).strip()
        # Fallback: look for "iphone" or "айфон" word
        simple = re.search(r"(iphone|айфон|samsung|macbook|ipad)\s*\S*", text, re.IGNORECASE)
        if simple:
            return simple.group(0).strip()
        return None
