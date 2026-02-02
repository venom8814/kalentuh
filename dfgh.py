import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import os

try:
    from transformers import pipeline
    translator = pipeline("translation_en_to_ru", model="Helsinki-NLP/opus-mt-en-ru")
    MODEL_LOADED = True
except Exception as e:
    MODEL_LOADED = False
    ERROR_MSG = str(e)

def translate_text():
    if not MODEL_LOADED:
        messagebox.showerror("Ошибка", f"Модель не загружена:\n{ERROR_MSG}")
        return

    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Внимание", "Введите текст для перевода!")
        return

    translate_btn.config(state=tk.DISABLED)
    status_label.config(text="Переводим... ⏳", fg="blue")

    def run_translation():
        try:
            result = translator(text, max_length=512)
            translated = result[0]['translation_text']
            root.after(0, lambda: update_output(translated))
        except Exception as e:
            root.after(0, lambda: show_error(str(e)))
        finally:
            root.after(0, lambda: translate_btn.config(state=tk.NORMAL))

    threading.Thread(target=run_translation, daemon=True).start()

def update_output(text):
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, text)
    output_text.config(state=tk.DISABLED)
    status_label.config(text="Перевод завершён ✅", fg="green")

def show_error(msg):
    messagebox.showerror("Ошибка перевода", msg)
    status_label.config(text="Готово", fg="black")
    translate_btn.config(state=tk.NORMAL)

root = tk.Tk()
root.title("Переводчик с Английского на Русский")
root.geometry("700x500")
root.resizable(True, True)

title = tk.Label(root, text="Переводчик", font=("Arial", 16, "bold"))
title.pack(pady=10)

tk.Label(root, text="Английский текст:", font=("Arial", 10)).pack(anchor="w", padx=20)
input_text = scrolledtext.ScrolledText(root, height=6, width=80, wrap=tk.WORD, font=("Arial", 10))
input_text.pack(padx=20, pady=5)

translate_btn = tk.Button(
    root, text="Перевести на русский", command=translate_text,
    bg="#2196F3", fg="white", font=("Arial", 11), padx=10, pady=5
)
translate_btn.pack(pady=10)

tk.Label(root, text="Русский перевод:", font=("Arial", 10)).pack(anchor="w", padx=20)
output_text = scrolledtext.ScrolledText(
    root, height=6, width=80, wrap=tk.WORD, font=("Arial", 10),
    state=tk.DISABLED, bg="#f9f9f9"
)
output_text.pack(padx=20, pady=5)

status_label = tk.Label(
    root,
    text="Первый запуск: требуется интернет для загрузки модели (~200 МБ). Далее — оффлайн.",
    font=("Arial", 9), fg="gray"
)
status_label.pack(side=tk.BOTTOM, pady=8)

info = tk.Label(
    root,
    text="Используется модель Helsinki-NLP/opus-mt-en-ru (нейросеть, работает локально)",
    font=("Arial", 8), fg="darkgray"
)
info.pack(side=tk.BOTTOM)

root.mainloop()