import aiohttp
from typing import Optional, Dict


API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

async def fetch_rates_from_api(base: str = "USD") -> Optional[Dict[str, float]]:
    async with aiohttp.ClientSession() as session:
        """
        Делает запрос к API и возвращает курсы.
        Возвращает None при ошибке сети или если ответ не соответствует ожиданиям.
        Не сохраняет кэш и не валидирует наличие конкретных валют (это делает caller).
        """
        try:
            async with session.get(API_URL, params={"base": base}, timeout=5) as resp:
                data = await resp.json()
                rates = data.get("rates")
                if not isinstance(rates, dict):
                    return None
                return rates
        except Exception as e:
            return None
        