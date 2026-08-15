import asyncio
import tkinter as tk
from tkinter import ttk

from .services import convert


class UnitsConverterWidget(tk.Frame):
    def __init__(self, parent, loop, **kwargs):
        super().__init__(parent, **kwargs)
        self.loop = loop
        self.bg_color = "#ffffff"
        self.configure(bg=self.bg_color)

        header = tk.Label(
            self,
            text="Конвертер единиц",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_color,
            fg="#333333",
        )
        header.pack(pady=(15, 5))

        frm = tk.Frame(self, bg=self.bg_color)
        frm.pack(padx=20, pady=10, fill="x")

        tk.Label(frm, text="Тип:", bg=self.bg_color).grid(
            row=0, column=0, sticky="e", pady=(0, 6)
        )
        self.type_combo = ttk.Combobox(
            frm,
            values=["Длина", "Вес"],
            state="readonly",
            width=12,
        )
        self.type_combo.current(0)
        self.type_combo.grid(row=0, column=1, sticky="w", pady=(0, 6))
        self.type_combo.bind("<<ComboboxSelected>>", self.on_type_change)

        tk.Label(frm, text="Из:", bg=self.bg_color).grid(
            row=1, column=0, sticky="e", pady=(0, 6)
        )
        self.from_combo = ttk.Combobox(frm, state="readonly", width=12)
        self.from_combo.grid(row=1, column=1, sticky="w", pady=(0, 6))

        tk.Label(frm, text="В:", bg=self.bg_color).grid(
            row=2, column=0, sticky="e", pady=(0, 6)
        )
        self.to_combo = ttk.Combobox(frm, state="readonly", width=12)
        self.to_combo.grid(row=2, column=1, sticky="w", pady=(0, 6))

        tk.Label(frm, text="Значение:", bg=self.bg_color).grid(
            row=3, column=0, sticky="e", pady=(0, 8)
        )
        self.entry_val = tk.Entry(frm, font=("Segoe UI", 12), width=14)
        self.entry_val.insert(0, "1")
        self.entry_val.grid(row=3, column=1, sticky="w", pady=(0, 8))

        self.lbl_result = tk.Label(
            self,
            text="Результат: ?",
            font=("Consolas", 16, "bold"),
            fg="#2E7D32",
            bg=self.bg_color,
        )
        self.lbl_result.pack(pady=8)

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

        self._populate_units()
        self.task = None

    def _populate_units(self) -> None:
        t = self.type_combo.get()
        key_map = {"Длина": "length", "Вес": "weight"}
        key = key_map.get(t)

        units = list(UNITS_CONFIG := {
            "length": ["m", "cm", "mm", "km", "ft", "in"],
            "weight": ["kg", "g"],
        }.get(key, []))
        self.from_combo["values"] = units
        self.to_combo["values"] = units
        if len(units) >= 2:
            self.from_combo.current(0)
            self.to_combo.current(1)
        self.to_combo.configure(state="readonly")

    def on_type_change(self, event=None) -> None:
        self._populate_units()

    def on_convert(self) -> None:
        try:
            value = float(self.entry_val.get())
        except ValueError:
            self.lbl_result.config(text="Ошибка: число")
            return

        t = self.type_combo.get()
        from_u = self.from_combo.get()
        to_u = self.to_combo.get()
        if not from_u or not to_u:
            self.lbl_result.config(text="Ошибка: выберите единицы")
            return
        self.task = self.loop.create_task(
            self._run_convert(value, from_u, to_u, t)
        )

    async def _run_convert(
        self, value: float, from_u: str, to_u: str, category_name: str
    ) -> None:
        await asyncio.sleep(5)  # имитация небольшой задержки
        category_map = {"Длина": "length", "Вес": "weight"}
        category = category_map.get(category_name)
        if not category:
            self.lbl_result.config(text="Ошибка: категория")
            return
        try:
            result = convert(value, from_u, to_u, category)
            self.lbl_result.config(text=f"{result:.4f}")
        except Exception as e:
            self.lbl_result.config(text=f"Ошибка: {e}")

    def stop(self) -> None:
        if getattr(self, "task", None):
            self.task.cancel()
            try:
                self.loop.run_until_complete(self.task)
            except asyncio.CancelledError:
                pass