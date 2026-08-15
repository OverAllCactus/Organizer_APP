import asyncio
import tkinter as tk

from .services import calculate_expression


class CalculatorWidget(tk.Frame):
    def __init__(self, parent, loop, **kwargs):
        super().__init__(parent, **kwargs)
        self.loop = loop
        self.result_var = tk.StringVar(value="0")
        self.task = None

        self.bg_color = "#ffffff"
        self.btn_bg = "#f5f5f5"
        self.btn_active = "#e0e0e0"
        self.op_bg = "#ff9800"
        self.op_active = "#e68900"

        self.configure(bg=self.bg_color)

        header = tk.Label(
            self,
            text="Калькулятор",
            font=("Segoe UI", 16, "bold"),
            bg=self.bg_color,
            fg="#333333",
        )
        header.pack(pady=(15, 5))

        self.lbl_result = tk.Label(
            self,
            textvariable=self.result_var,
            font=("Consolas", 24, "bold"),
            bg="#ffffff",
            relief="flat",
            anchor="e",
            padx=15,
            pady=10,
        )
        self.lbl_result.pack(fill="x", padx=10)

        btn_frame = tk.Frame(self, bg=self.bg_color)
        btn_frame.pack(padx=10, pady=5)

        self.current = ""
        self.prev = ""
        self.op = None

        buttons = [
            ("7", lambda: self.append_digit("7")),
            ("8", lambda: self.append_digit("8")),
            ("9", lambda: self.append_digit("9")),
            ("/", lambda: self.set_op("/")),
            ("4", lambda: self.append_digit("4")),
            ("5", lambda: self.append_digit("5")),
            ("6", lambda: self.append_digit("6")),
            ("*", lambda: self.set_op("*")),
            ("1", lambda: self.append_digit("1")),
            ("2", lambda: self.append_digit("2")),
            ("3", lambda: self.append_digit("3")),
            ("-", lambda: self.set_op("-")),
            ("0", lambda: self.append_digit("0")),
            (".", lambda: self.append_digit(".")),
            ("=", self.on_calculate),
            ("+", lambda: self.set_op("+")),
            ("C", self.clear),
        ]

        for i, (text, cmd) in enumerate(buttons):
            row = i // 4
            col = i % 4

            is_op = text in "+-*/"
            bg = self.op_bg if is_op else self.btn_bg
            active_bg = self.op_active if is_op else self.btn_active

            btn = tk.Button(
                btn_frame,
                text=text,
                width=4,
                height=2,
                command=cmd,
                bg=bg,
                fg="#000000",
                activebackground=active_bg,
                relief="flat",
            )
            btn.grid(row=row, column=col, padx=4, pady=4)

    def append_digit(self, digit: str) -> None:
        if digit == "." and "." in self.current:
            return
        if self.current == "0" and digit != ".":
            self.current = digit
        else:
            self.current += digit
        self.result_var.set(self.current or "0")

    def set_op(self, op: str) -> None:
        if not self.current and not self.prev:
            return
        if self.prev and self.current:
            self._compute_sync()
        self.prev = self.current
        self.op = op
        self.current = ""

    def _compute_sync(self) -> None:
        try:
            if not self.prev or not self.current or not self.op:
                return
            expr = f"{self.prev}{self.op}{self.current}"
            res = calculate_expression(expr)
            self.prev = str(res)
            self.current = ""
            self.op = None
            self.result_var.set(str(res))
        except Exception:
            self.result_var.set("Ошибка")

    def on_calculate(self) -> None:
        if not self.prev or not self.current or not self.op:
            return
        self.task = self.loop.create_task(self._do_calculation())

    async def _do_calculation(self) -> None:
        try:
            await asyncio.sleep(2)
            self._compute_sync()
        except asyncio.CancelledError:
            pass

    def clear(self) -> None:
        self.current = ""
        self.prev = ""
        self.op = None
        self.result_var.set("0")

    def stop(self) -> None:
        if getattr(self, "task", None):
            self.task.cancel()
            try:
                self.loop.run_until_complete(self.task)
            except asyncio.CancelledError:
                pass
