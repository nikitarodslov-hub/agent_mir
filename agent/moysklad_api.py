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
                params={"search": query, "limit": 20},
                timeout=10,
            )
            if resp.status_code != 200:
                return None

            products = resp.json().get("rows", [])
            if not products:
                return f"Товар «{query}» не найден на складе"

            lines = []
            for product in products[:8]:
                line = self._build_stock_line(product)
                if line:
                    lines.append(line)

            if not lines:
                return f"«{query}» есть в базе, но сейчас нет в наличии (остаток = 0)"
            return "\n".join(lines)
        except Exception as e:
            return f"Ошибка МойСклад: {e}"

    def _build_stock_line(self, product: dict) -> Optional[str]:
        """Fetch stock for one product and return a formatted line, or None if out of stock."""
        try:
            pid = product.get("id", "")
            stock = self._get_product_stock(pid)
            if stock <= 0:
                return None

            name = product.get("name", "Без названия")
            sale_prices = product.get("salePrices", [])
            price_kopecks = sale_prices[0].get("value", 0) if sale_prices else 0
            sale_price = price_kopecks // 100

            category = self._extract_category(name)
            cat_str = f" [{category}]" if category else ""
            price_str = f"{sale_price:,} руб." if sale_price else "цена не указана"
            return f"• {name}{cat_str} — {stock} шт., {price_str}"
        except Exception:
            return None

    def _get_product_stock(self, product_id: str) -> int:
        """Return current stock quantity for a single product via filtered report."""
        try:
            resp = requests.get(
                f"{BASE_URL}/report/stock/all",
                auth=self.auth,
                params={
                    "filter": f"assortment={BASE_URL}/entity/product/{product_id}",
                    "limit": 1,
                },
                timeout=8,
            )
            if resp.status_code != 200:
                return 0
            rows = resp.json().get("rows", [])
            return max(0, int(rows[0].get("stock", 0))) if rows else 0
        except Exception:
            return 0

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
