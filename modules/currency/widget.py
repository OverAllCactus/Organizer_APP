import asyncio
import tkinter as tk
from tkinter import ttk

from .services import convert

class CurrencyConverterWidget(tk.Frame):
    def __init__(self, parent, loop, **kwargs):
        super().__init__(parent, **kwargs)
        self.loop = loop

        self.bg_color = "#ffffff"
        self.configure(bg=self.bg_color)

        header = tk.Label(
            self,
            text="Конвертер валют (API + кэш)",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_color,
            fg="#333333",
        )
        header.pack(pady=(15, 5))

        frm = tk.Frame(self, bg=self.bg_color)
        frm.pack(padx=20, pady=10, fill="x")

        tk.Label(frm, text="Сумма:", bg=self.bg_color).grid(
            row=0, column=0, sticky="e"
        )
        self.entry_val = tk.Entry(frm, font=("Segoe UI", 12))
        self.entry_val.insert(0, "100")
        self.entry_val.grid(row=0, column=1, padx=8, sticky="ew")

        tk.Label(frm, text="Из:", bg=self.bg_color).grid(
            row=1, column=0, sticky="e", pady=(8, 0)
        )
        self.combo_from = ttk.Combobox(
            frm, values=["RUB", "USD", "EUR"], state="readonly", width=10
        )
        self.combo_from.current(0)
        self.combo_from.grid(row=1, column=1, sticky="w", pady=(8, 0))

        tk.Label(frm, text="В:", bg=self.bg_color).grid(
            row=2, column=0, sticky="e", pady=(8, 0)
        )
        self.combo_to = ttk.Combobox(
            frm, values=["RUB", "USD", "EUR"], state="readonly", width=10
        )
        self.combo_to.current(0)
        self.combo_to.grid(row=2, column=1, sticky="w", pady=(8, 0))

        frm.columnconfigure(1, weight=1)

        self.lbl_status = tk.Label(
            self,
            text="Статус: готов",
            fg="#555555",
            font=("Segoe UI", 10),
            bg=self.bg_color,
        )
        self.lbl_status.pack(pady=(5, 10))

        self.lbl_result = tk.Label(
            self,
            text="Результат: ?",
            font=("Consolas", 18, "bold"),
            fg="#2E7D32",
            bg=self.bg_color,
        )
        self.lbl_result.pack(pady=5)

        btn = tk.Button(
            self,
            text="Конвертировать",
            command=self.on_convert,
            bg="#2196F3",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            font=("Segoe UI", 11, "bold"),
        )
        btn.pack(pady=15)

        self.task = None

    def on_convert(self) -> None:
        try:
            value = float(self.entry_val.get())
        except ValueError:
            self.lbl_status.config(text="Ошибка: введите число", fg="red")
            return

        from_cur = self.combo_from.get()
        to_cur = self.combo_to.get()

        self.lbl_status.config(
            text=f"Статус: загрузка курса ({from_cur} → {to_cur})...",
            fg="#FF9800",
        )
        self.lbl_result.config(text="...")

        self.task = self.loop.create_task(
            self._run_convert(value, from_cur, to_cur)
        )

    async def _run_convert(
        self, value: float, from_cur: str, to_cur: str
    ) -> None:
        try:
            result = await convert(value, from_cur, to_cur)
            self.lbl_result.config(text=f"{result:,.2f} {to_cur}")
            self.lbl_status.config(text="Статус: готово", fg="#2E7D32")
        except Exception as e:
            self.lbl_status.config(text=f"Ошибка: {e}", fg="red")

    def stop(self) -> None:
        if getattr(self, "task", None):
            self.task.cancel()
            try:
                self.loop.run_until_complete(self.task)
            except asyncio.CancelledError:
                pass
