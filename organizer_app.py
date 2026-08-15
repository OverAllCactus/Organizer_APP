import tkinter as tk
import asyncio

from modules import CalculatorWidget, CurrencyConverterWidget, UnitsConverterWidget

class OrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Органайзер (Production-ready)")
        self.root.geometry("900x640")
        self.root.configure(bg="#F5F7FA")

        self.loop = asyncio.new_event_loop()

        header = tk.Label(
            root, text="Органайзер",
            font=("Segoe UI", 20, "bold"),
            bg="#F5F7FA", fg="#2C3E50"
        )
        header.pack(pady=(25, 10))

        container = tk.Frame(root, bg="#F5F7FA")
        container.pack(fill="x", padx=20, pady=10)

        # --- Калькулятор ---
        self.calc = CalculatorWidget(
            parent=container, loop=self.loop, padx=10, pady=10, bg="#ffffff"
        )
        self.calc.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Frame(container, width=1, bg="#E0E6ED").pack(side="left", fill="y", padx=5)

        # --- Конвертер валют ---
        self.currency = CurrencyConverterWidget(
            parent=container, loop=self.loop, padx=10, pady=10, bg="#ffffff"
        )
        self.currency.pack(side="left", fill="both", expand=True, padx=(10, 10))

        tk.Frame(container, width=1, bg="#E0E6ED").pack(side="left", fill="y", padx=5)

        # --- Конвертер единиц ---
        self.units = UnitsConverterWidget(
            parent=container, loop=self.loop, padx=10, pady=10, bg="#ffffff"
        )
        self.units.pack(side="left", fill="both", expand=True, padx=(10, 0))


        self._start_polling()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _start_polling(self):
        try:
            self.loop.run_until_complete(asyncio.sleep(0))
        except Exception:
            pass
        self.root.after(16, self._start_polling)

    def on_close(self):
        # Останавливаем задачи внутри виджетов
        self.calc.stop()
        self.currency.stop()
        self.units.stop()

        try:
            self.loop.close()
        except Exception:
            pass

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = OrganizerApp(root)
    root.mainloop()
