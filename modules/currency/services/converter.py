from datetime import date
from typing import Optional, Dict

from .api_client import fetch_rates_from_api
from .cache import load_cache, save_cache

SUPPORTED_CURRENCIES = {"USD", "EUR", "RUB"}

def _has_all_required_currencies(rates: Optional[Dict]) -> bool:
    if not rates:
        return False
    return all(c in rates for c in SUPPORTED_CURRENCIES)

async def get_rates() -> Dict[str, float]:
    cache = load_cache()
    today = date.today().isoformat()

    # 1. Если есть кэш и его дата совпадает с текущей — используем кэш
    if "date" in cache and cache["date"] == today:
        cached_rates = cache.get("rates", {})
        if _has_all_required_currencies(cached_rates):
            return cached_rates

    # 2. Пытаемся получить свежие курсы через API
    fresh_rates = await fetch_rates_from_api()
    if fresh_rates is not None and _has_all_required_currencies(fresh_rates):
        # Сохраняем кэш с текущей датой
        save_cache(fresh_rates)
        return fresh_rates

    # 3. Если API не помог, пробуем использовать старый кэш 
    if "rates" in cache and _has_all_required_currencies(cache["rates"]):
        return cache["rates"]

    raise RuntimeError("Не удалось получить корректные курсы валют. Проверьте кэш и подключение к интернету.")

async def convert(amount: float, from_currency: str, to_currency: str) -> float:
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency not in SUPPORTED_CURRENCIES or to_currency not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Неподдерживаемая валюта. Допустимы: {', '.join(SUPPORTED_CURRENCIES)}")

    rates = await get_rates()

    if from_currency not in rates:
        raise RuntimeError(f"Курс для валюты {from_currency} отсутствует в текущих данных")
    if to_currency not in rates:
        raise RuntimeError(f"Курс для валюты {to_currency} отсутствует в текущих данных")

    rate_from = rates[from_currency]
    rate_to = rates[to_currency]

    result = amount * (rate_to / rate_from)

    return result
