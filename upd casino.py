import tkinter as tk
from tkinter import ttk, messagebox, font, simpledialog
import random
import math
from PIL import Image, ImageTk
import os
import sys

class CasinoGL:
    def __init__(self, root):
        self.root = root
        self.root.title("Казино GL - Добро пожаловать!")
        self.root.geometry("800x600")
        self.root.configure(bg='#0a1f2d')
        
        # Инициализация данных игрока
        self.balance = 1000  # Начальный баланс
        self.bet_amount = 10  # Стандартная ставка
        self.player_name = "Игрок"
        
        # История операций
        self.transaction_history = []
        
        # Для анимации рулетки
        self.ball_angle = 0
        self.ball_radius = 10
        self.ball_animation_id = None
        self.is_spinning = False
        
        # Для игры в блэкджек
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.game_in_progress = False
        
        # Стилизация
        self.colors = {
            'bg_dark': '#0a1f2d',
            'bg_medium': '#1a3f5d',
            'bg_light': '#2a5f8d',
            'accent_gold': '#ffd700',
            'accent_red': '#ff4747',
            'accent_green': '#47ff7a',
            'text_light': '#ffffff'
        }
        
        # Загрузка изображений (если они существуют)
        self.load_images()
        
        # Создание интерфейса
        self.create_main_menu()
    
    def add_transaction(self, transaction_type, amount, description=""):
        """Добавление записи в историю транзакций"""
        transaction = {
            'type': transaction_type,
            'amount': amount,
            'description': description,
            'balance_after': self.balance
        }
        self.transaction_history.append(transaction)
        
    def load_images(self):
        """Загрузка изображений для интерфейса"""
        try:
            self.card_images = {}
            card_suits = ['hearts', 'diamonds', 'clubs', 'spades']
            card_values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
            
            for suit in card_suits:
                for value in card_values:
                    color = '#ff4747' if suit in ['hearts', 'diamonds'] else '#0a1f2d'
                    img = Image.new('RGB', (80, 120), color='#ffffff')
                    self.card_images[f"{value}_{suit}"] = ImageTk.PhotoImage(img)
        except:
            pass
            
    def create_main_menu(self):
        """Создание главного меню"""
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Заголовок казино
        title_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame, text="GL Казино", 
                               font=('Arial', 36, 'bold'), 
                               fg=self.colors['accent_gold'], 
                               bg=self.colors['bg_dark'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Удачи и крупных выигрышей!", 
                                  font=('Arial', 14), 
                                  fg=self.colors['text_light'], 
                                  bg=self.colors['bg_dark'])
        subtitle_label.pack()
        
        # Информация о балансе с кнопкой пополнения
        balance_frame = tk.Frame(self.root, bg=self.colors['bg_medium'], relief=tk.RAISED, borderwidth=2)
        balance_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Верхняя часть фрейма баланса
        balance_top_frame = tk.Frame(balance_frame, bg=self.colors['bg_medium'])
        balance_top_frame.pack(fill=tk.X, pady=(10, 5))
        
        balance_label = tk.Label(balance_top_frame, text=f"Баланс: {self.balance} ₽", 
                                 font=('Arial', 18, 'bold'), 
                                 fg=self.colors['accent_gold'], 
                                 bg=self.colors['bg_medium'])
        balance_label.pack(side=tk.LEFT, padx=20)
        
        # Кнопка пополнения баланса
        deposit_btn = tk.Button(balance_top_frame, text="Пополнить баланс", 
                                command=self.deposit_balance,
                                font=('Arial', 12, 'bold'),
                                bg=self.colors['accent_green'],
                                fg='black',
                                width=15,
                                height=1)
        deposit_btn.pack(side=tk.RIGHT, padx=20)
        
        # Нижняя часть фрейма баланса
        balance_bottom_frame = tk.Frame(balance_frame, bg=self.colors['bg_medium'])
        balance_bottom_frame.pack(fill=tk.X, pady=(5, 10))
        
        # Кнопка истории операций
        history_btn = tk.Button(balance_bottom_frame, text="История операций", 
                                command=self.show_transaction_history,
                                font=('Arial', 10),
                                bg=self.colors['bg_light'],
                                fg=self.colors['text_light'],
                                width=15)
        history_btn.pack(side=tk.RIGHT, padx=20)
        
        # Кнопка сброса баланса
        reset_btn = tk.Button(balance_bottom_frame, text="Сбросить баланс", 
                              command=self.reset_balance,
                              font=('Arial', 10),
                              bg=self.colors['accent_red'],
                              fg=self.colors['text_light'],
                              width=15)
        reset_btn.pack(side=tk.RIGHT, padx=5)
        
        # Кнопки игр
        games_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        games_frame.pack(pady=30, padx=50, fill=tk.BOTH, expand=True)
        
        # Настройка кнопок
        button_style = {
            'font': ('Arial', 14, 'bold'),
            'width': 20,
            'height': 2,
            'bg': self.colors['bg_light'],
            'fg': self.colors['text_light'],
            'activebackground': self.colors['accent_gold'],
            'activeforeground': self.colors['bg_dark'],
            'relief': tk.RAISED,
            'borderwidth': 3
        }
        
        # Кнопки для разных игр
        roulette_btn = tk.Button(games_frame, text="Рулетка", 
                                 command=self.play_roulette, **button_style)
        roulette_btn.pack(pady=10)
        
        slots_btn = tk.Button(games_frame, text="Слот-машина", 
                              command=self.play_slots, **button_style)
        slots_btn.pack(pady=10)
        
        blackjack_btn = tk.Button(games_frame, text="Блэкджек", 
                                  command=self.play_blackjack, **button_style)
        blackjack_btn.pack(pady=10)
        
        dice_btn = tk.Button(games_frame, text="Кости", 
                             command=self.play_dice, **button_style)
        dice_btn.pack(pady=10)
        
        # Кнопка настроек
        settings_btn = tk.Button(games_frame, text="Настройки и правила", 
                                 command=self.show_settings, **button_style)
        settings_btn.pack(pady=10)
        
        # Кнопка выхода
        exit_btn = tk.Button(games_frame, text="Выход", 
                             command=self.root.quit, **button_style)
        exit_btn.pack(pady=10)
        
        # Информация о разработчике
        footer_label = tk.Label(self.root, text="Казино GL © 2023 | Только для развлекательных целей", 
                                font=('Arial', 10), 
                                fg=self.colors['text_light'], 
                                bg=self.colors['bg_dark'])
        footer_label.pack(side=tk.BOTTOM, pady=10)
    
    def deposit_balance(self):
        """Пополнение баланса"""
        deposit_window = tk.Toplevel(self.root)
        deposit_window.title("Пополнение баланса")
        deposit_window.geometry("400x350")
        deposit_window.configure(bg=self.colors['bg_dark'])
        deposit_window.resizable(False, False)
        
        # Центрирование окна
        deposit_window.transient(self.root)
        deposit_window.grab_set()
        
        # Заголовок
        title_label = tk.Label(deposit_window, text="Пополнение баланса", 
                               font=('Arial', 20, 'bold'), 
                               fg=self.colors['accent_gold'], 
                               bg=self.colors['bg_dark'])
        title_label.pack(pady=20)
        
        # Текущий баланс
        current_balance_label = tk.Label(deposit_window, 
                                         text=f"Текущий баланс: {self.balance} ₽", 
                                         font=('Arial', 14), 
                                         fg=self.colors['text_light'], 
                                         bg=self.colors['bg_dark'])
        current_balance_label.pack(pady=10)
        
        # Варианты пополнения
        amounts_frame = tk.Frame(deposit_window, bg=self.colors['bg_dark'])
        amounts_frame.pack(pady=20)
        
        # Предустановленные суммы
        preset_amounts = [100, 500, 1000, 2000, 5000]
        amount_buttons = []
        
        for i, amount in enumerate(preset_amounts):
            btn = tk.Button(amounts_frame, text=f"{amount} ₽", 
                            command=lambda amt=amount: self.process_deposit(amt, deposit_window),
                            font=('Arial', 12, 'bold'),
                            bg=self.colors['bg_light'],
                            fg=self.colors['text_light'],
                            width=10,
                            height=2)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            amount_buttons.append(btn)
        
        # Кастомная сумма
        custom_frame = tk.Frame(deposit_window, bg=self.colors['bg_dark'])
        custom_frame.pack(pady=20)
        
        custom_label = tk.Label(custom_frame, text="Другая сумма:", 
                                font=('Arial', 12), 
                                fg=self.colors['text_light'], 
                                bg=self.colors['bg_dark'])
        custom_label.grid(row=0, column=0, padx=5)
        
        custom_amount_var = tk.StringVar(value="")
        custom_amount_entry = tk.Entry(custom_frame, 
                                       textvariable=custom_amount_var, 
                                       font=('Arial', 12),
                                       width=15)
        custom_amount_entry.grid(row=0, column=1, padx=5)
        
        rub_label = tk.Label(custom_frame, text="₽", 
                             font=('Arial', 12), 
                             fg=self.colors['text_light'], 
                             bg=self.colors['bg_dark'])
        rub_label.grid(row=0, column=2, padx=5)
        
        custom_deposit_btn = tk.Button(custom_frame, text="Пополнить", 
                                       command=lambda: self.process_custom_deposit(custom_amount_var.get(), deposit_window),
                                       font=('Arial', 10, 'bold'),
                                       bg=self.colors['accent_green'],
                                       fg='black',
                                       width=10)
        custom_deposit_btn.grid(row=0, column=3, padx=10)
        
        # Кнопка отмены
        cancel_btn = tk.Button(deposit_window, text="Отмена", 
                               command=deposit_window.destroy,
                               font=('Arial', 12),
                               bg=self.colors['accent_red'],
                               fg=self.colors['text_light'],
                               width=15)
        cancel_btn.pack(pady=20)
    
    def process_deposit(self, amount, window):
        """Обработка пополнения на предустановленную сумму"""
        if not isinstance(amount, (int, float)) or amount <= 0:
            messagebox.showerror("Ошибка", "Некорректная сумма пополнения!")
            return
        
        self.balance += amount
        self.add_transaction('deposit', amount, f"Пополнение баланса на {amount} ₽")
        
        messagebox.showinfo("Успех", f"Баланс успешно пополнен на {amount} ₽!\nНовый баланс: {self.balance} ₽")
        
        # Обновляем главное меню
        window.destroy()
        self.create_main_menu()
    
    def process_custom_deposit(self, amount_str, window):
        """Обработка пополнения на кастомную сумму"""
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной")
            if amount > 1000000:  # Максимальная сумма
                messagebox.showwarning("Предупреждение", "Слишком большая сумма пополнения!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректную сумму!")
            return
        
        # Подтверждение пополнения
        confirm = messagebox.askyesno("Подтверждение", 
                                      f"Вы уверены, что хотите пополнить баланс на {amount} ₽?\nНовый баланс: {self.balance + amount} ₽")
        
        if confirm:
            self.balance += amount
            self.add_transaction('deposit', amount, f"Пополнение баланса на {amount} ₽")
            
            messagebox.showinfo("Успех", f"Баланс успешно пополнен на {amount} ₽!\nНовый баланс: {self.balance} ₽")
            
            # Обновляем главное меню
            window.destroy()
            self.create_main_menu()
    
    def reset_balance(self):
        """Сброс баланса к начальному значению"""
        confirm = messagebox.askyesno("Сброс баланса", 
                                     f"Вы уверены, что хотите сбросить баланс?\nТекущий баланс: {self.balance} ₽\nНовый баланс: 1000 ₽")
        
        if confirm:
            old_balance = self.balance
            self.balance = 1000
            self.add_transaction('reset', -old_balance + 1000, f"Сброс баланса. Было: {old_balance} ₽, стало: 1000 ₽")
            
            messagebox.showinfo("Успех", f"Баланс сброшен!\nНовый баланс: {self.balance} ₽")
            self.create_main_menu()
    
    def show_transaction_history(self):
        """Показать историю операций"""
        history_window = tk.Toplevel(self.root)
        history_window.title("История операций")
        history_window.geometry("600x400")
        history_window.configure(bg=self.colors['bg_dark'])
        
        # Заголовок
        title_label = tk.Label(history_window, text="История операций", 
                               font=('Arial', 20, 'bold'), 
                               fg=self.colors['accent_gold'], 
                               bg=self.colors['bg_dark'])
        title_label.pack(pady=10)
        
        # Текущий баланс
        current_balance_label = tk.Label(history_window, 
                                         text=f"Текущий баланс: {self.balance} ₽", 
                                         font=('Arial', 14), 
                                         fg=self.colors['text_light'], 
                                         bg=self.colors['bg_dark'])
        current_balance_label.pack(pady=5)
        
        # Создаем текстовое поле с прокруткой для истории
        history_frame = tk.Frame(history_window, bg=self.colors['bg_dark'])
        history_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_text = tk.Text(history_frame, 
                               height=15, 
                               width=70,
                               font=('Arial', 10),
                               bg=self.colors['bg_light'],
                               fg=self.colors['text_light'],
                               yscrollcommand=scrollbar.set)
        history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=history_text.yview)
        
        # Отображаем историю
        if not self.transaction_history:
            history_text.insert(tk.END, "История операций пуста.\n")
        else:
            for i, transaction in enumerate(reversed(self.transaction_history[-20:]), 1):  # Последние 20 операций
                if transaction['type'] == 'deposit':
                    color = 'green'
                    prefix = "+"
                elif transaction['type'] == 'reset':
                    color = 'orange'
                    prefix = ""
                elif transaction['type'] == 'game_loss':
                    color = 'red'
                    prefix = "-"
                elif transaction['type'] == 'game_win':
                    color = 'green'
                    prefix = "+"
                else:
                    color = 'white'
                    prefix = ""
                
                history_text.insert(tk.END, f"{i}. {transaction['description']}\n")
                history_text.insert(tk.END, f"   Сумма: {prefix}{transaction['amount']} ₽ | Баланс после: {transaction['balance_after']} ₽\n")
                history_text.insert(tk.END, "-" * 50 + "\n")
        
        history_text.configure(state='disabled')
        
        # Кнопка закрытия
        close_btn = tk.Button(history_window, text="Закрыть", 
                              command=history_window.destroy,
                              font=('Arial', 12),
                              bg=self.colors['accent_gold'],
                              fg=self.colors['bg_dark'],
                              width=15)
        close_btn.pack(pady=10)
    
    def play_roulette(self):
        """Игра в рулетку"""
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Заголовок
        title_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        title_frame.pack(pady=10)
        
        back_btn = tk.Button(title_frame, text="← Назад", 
                             command=self.create_main_menu,
                             font=('Arial', 10),
                             bg=self.colors['bg_light'],
                             fg=self.colors['text_light'])
        back_btn.pack(side=tk.LEFT, padx=10)
        
        title_label = tk.Label(title_frame, text="Рулетка", 
                               font=('Arial', 28, 'bold'), 
                               fg=self.colors['accent_gold'], 
                               bg=self.colors['bg_dark'])
        title_label.pack()
        
        # Отображение баланса с кнопкой пополнения
        balance_frame = tk.Frame(self.root, bg=self.colors['bg_medium'])
        balance_frame.pack(pady=10)
        
        balance_inner_frame = tk.Frame(balance_frame, bg=self.colors['bg_medium'])
        balance_inner_frame.pack()
        
        self.balance_label = tk.Label(balance_inner_frame, text=f"Баланс: {self.balance} ₽", 
                                      font=('Arial', 16, 'bold'), 
                                      fg=self.colors['accent_gold'], 
                                      bg=self.colors['bg_medium'])
        self.balance_label.grid(row=0, column=0, padx=10)
        
        # Кнопка пополнения баланса в игре
        deposit_btn = tk.Button(balance_inner_frame, text="Пополнить", 
                                command=self.deposit_balance,
                                font=('Arial', 10, 'bold'),
                                bg=self.colors['accent_green'],
                                fg='black')
        deposit_btn.grid(row=0, column=1, padx=10)
        
        # Поле рулетки
        roulette_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        roulette_frame.pack(pady=20)
        
        # Создаем отображение рулетки
        self.roulette_canvas = tk.Canvas(roulette_frame, width=400, height=400, 
                                         bg=self.colors['bg_light'], highlightthickness=0)
        self.roulette_canvas.pack()
        
        # Рисуем простую рулетку
        self.draw_roulette()
        
        # Управление ставками
        bet_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        bet_frame.pack(pady=10)
        
        bet_label = tk.Label(bet_frame, text="Ставка:", 
                             font=('Arial', 14), 
                             fg=self.colors['text_light'], 
                             bg=self.colors['bg_dark'])
        bet_label.grid(row=0, column=0, padx=5)
        
        self.bet_var = tk.IntVar(value=self.bet_amount)
        bet_spinbox = tk.Spinbox(bet_frame, from_=10, to=min(500, self.balance), 
                                 textvariable=self.bet_var, 
                                 font=('Arial', 14), 
                                 width=10)
        bet_spinbox.grid(row=0, column=1, padx=5)
        
        # Кнопки для ставок на цвета
        colors_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        colors_frame.pack(pady=10)
        
        red_btn = tk.Button(colors_frame, text="Красное (x2)", 
                            command=lambda: self.place_roulette_bet("red"),
                            font=('Arial', 12, 'bold'),
                            bg='#ff4747',
                            fg='white',
                            width=15,
                            height=2)
        red_btn.grid(row=0, column=0, padx=10)
        
        black_btn = tk.Button(colors_frame, text="Черное (x2)", 
                              command=lambda: self.place_roulette_bet("black"),
                              font=('Arial', 12, 'bold'),
                              bg='#0a1f2d',
                              fg='white',
                              width=15,
                              height=2)
        black_btn.grid(row=0, column=1, padx=10)
        
        green_btn = tk.Button(colors_frame, text="Зеленое (x14)", 
                              command=lambda: self.place_roulette_bet("green"),
                              font=('Arial', 12, 'bold'),
                              bg='#47ff7a',
                              fg='black',
                            width=15,
                              height=2)
        green_btn.grid(row=0, column=2, padx=10)
        
        # Отображение результата
        self.result_label = tk.Label(self.root, text="Сделайте ставку!", 
                                     font=('Arial', 16), 
                                     fg=self.colors['text_light'], 
                                     bg=self.colors['bg_dark'])
        self.result_label.pack(pady=10)
    
    def draw_roulette(self):
        """Рисуем колесо рулетки на canvas"""
        self.roulette_canvas.delete("all")
        
        # Рисуем внешний круг
        x0, y0 = 50, 50
        x1, y1 = 350, 350
        
        # Разделяем на секторы
        colors = ['#ff4747', '#0a1f2d']  # Красный и черный
        numbers = list(range(1, 37))
        
        # Рисуем секторы
        angle_per_sector = 360 / 36
        
        for i in range(36):
            start_angle = i * angle_per_sector
            end_angle = (i + 1) * angle_per_sector
            
            # Чередуем цвета
            color = colors[i % 2]
            
            # Рисуем сектор
            self.roulette_canvas.create_arc(x0, y0, x1, y1, 
                                             start=start_angle, 
                                             extent=angle_per_sector,
                                             fill=color, 
                                             outline='white')
            
            # Добавляем номер (упрощенно)
            mid_angle = start_angle + angle_per_sector / 2
            rad = math.radians(mid_angle)
            text_x = 200 + 120 * math.cos(rad)
            text_y = 200 + 120 * math.sin(rad)
            
            self.roulette_canvas.create_text(text_x, text_y, 
                                             text=str(numbers[i]), 
                                             fill='white',
                                             font=('Arial', 10, 'bold'))
        
        # Зеленый сектор для 0
        self.roulette_canvas.create_oval(180, 180, 220, 220, fill='#47ff7a', outline='white')
        self.roulette_canvas.create_text(200, 200, text="0", fill='black', font=('Arial', 12, 'bold'))
        
        # Указатель
        self.roulette_canvas.create_polygon(200, 30, 195, 50, 205, 50, fill='gold')
        
        # Инициализация шарика (если анимация не активна)
        if not self.is_spinning:
            self.ball_angle = random.uniform(0, 360)
            self.draw_ball()
    
    def draw_ball(self):
        """Рисуем шарик на рулетке"""
        # Удаляем старый шарик
        self.roulette_canvas.delete("ball")
        
        # Рассчитываем позицию шарика
        rad = math.radians(self.ball_angle)
        ball_x = 200 + 140 * math.cos(rad)
        ball_y = 200 + 140 * math.sin(rad)
        
        # Рисуем шарик
        self.roulette_canvas.create_oval(ball_x - self.ball_radius, ball_y - self.ball_radius,
                                         ball_x + self.ball_radius, ball_y + self.ball_radius,
                                         fill='white', outline='black', width=2, tags="ball")
    
    def animate_ball(self, final_angle, speed=10):
        """Анимация вращения шарика"""
        if self.is_spinning:
            return
            
        self.is_spinning = True
        self.result_label.config(text="Шарик вращается...")
        
        # Начальный угол и скорость
        current_angle = self.ball_angle
        rotations = 5  # Количество полных оборотов
        
        # Рассчитываем конечный угол с несколькими оборотами
        target_angle = final_angle + rotations * 360
        
        # Функция для анимации
        def update_ball():
            nonlocal current_angle
            
            if current_angle < target_angle:
                # Уменьшаем скорость по мере приближения к цели
                progress = (target_angle - current_angle) / (target_angle - self.ball_angle)
                current_speed = max(1, speed * progress)
                
                current_angle += current_speed
                self.ball_angle = current_angle % 360
                self.draw_ball()
                
                # Продолжаем анимацию
                self.ball_animation_id = self.root.after(10, update_ball)
            else:
                # Анимация завершена
                self.ball_angle = final_angle % 360
                self.draw_ball()
                self.is_spinning = False
                
                # Определяем выигрышный номер
                if final_angle == 0:
                    win_number = 0
                else:
                    win_number = int((final_angle / 10) % 36) + 1
                
                # Определяем цвет результата
                if win_number == 0:
                    result_color = "green"
                elif win_number % 2 == 0:
                    result_color = "black"
                else:
                    result_color = "red"
                
                # Определяем выигрыш
                win_multiplier = 0
                if self.current_bet_type == result_color:
                    if self.current_bet_type == "green":
                        win_multiplier = 14
                    else:
                        win_multiplier = 2
                
                # Вычисляем выигрыш
                win_amount = self.current_bet * win_multiplier
                
                if win_amount > 0:
                    self.balance += win_amount
                    self.result_label.config(text=f"Выигрыш! Выпало {win_number} ({result_color}). Вы выиграли {win_amount} ₽!", 
                                             fg=self.colors['accent_green'])
                    self.add_transaction('game_win', win_amount, f"Выигрыш в рулетке: {self.current_bet_type}")
                else:
                    self.result_label.config(text=f"Проигрыш! Выпало {win_number} ({result_color}). Вы проиграли {self.current_bet} ₽.", 
                                             fg=self.colors['accent_red'])
                
                # Обновляем баланс
                self.balance_label.config(text=f"Баланс: {self.balance} ₽")
        
        # Запускаем анимацию
        update_ball()
    
    def place_roulette_bet(self, bet_type):
        """Размещение ставки в рулетке"""
        if self.is_spinning:
            messagebox.showwarning("Ожидание", "Дождитесь завершения предыдущего вращения!")
            return
            
        bet = self.bet_var.get()
        
        if bet > self.balance:
            messagebox.showerror("Ошибка", "Недостаточно средств на балансе!")
            return
        
        # Сохраняем текущую ставку
        self.current_bet = bet
        self.current_bet_type = bet_type
        
        # Вычитаем ставку
        self.balance -= bet
        self.balance_label.config(text=f"Баланс: {self.balance} ₽")
        self.add_transaction('game_loss', bet, f"Ставка в рулетке: {bet_type}")
        
        # Случайный результат (определяем угол для анимации)
        result_number = random.randint(0, 36)
        
        # Рассчитываем угол для этого номера
        if result_number == 0:
            final_angle = random.uniform(0, 10)  # Сектор для 0
        else:
            final_angle = (result_number - 1) * 10 + random.uniform(-2, 2)
        
        # Запускаем анимацию шарика
        self.animate_ball(final_angle)
    
    def play_slots(self):
        """Игра в слот-машину"""
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Заголовок
        title_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        title_frame.pack(pady=10)
        
        back_btn = tk.Button(title_frame, text="← Назад", 
                             command=self.create_main_menu,
                             font=('Arial', 10),
                             bg=self.colors['bg_light'],
                             fg=self.colors['text_light'])
        back_btn.pack(side=tk.LEFT, padx=10)
        
        title_label = tk.Label(title_frame, text="Слот-машина", 
                               font=('Arial', 28, 'bold'), 
                               fg=self.colors['accent_gold'], 
                               bg=self.colors['bg_dark'])
        title_label.pack()
        
        # Отображение баланса с кнопкой пополнения
        balance_frame = tk.Frame(self.root, bg=self.colors['bg_medium'])
        balance_frame.pack(pady=10)
        
        balance_inner_frame = tk.Frame(balance_frame, bg=self.colors['bg_medium'])
        balance_inner_frame.pack()
        
        self.balance_label = tk.Label(balance_inner_frame, text=f"Баланс: {self.balance} ₽", 
                                      font=('Arial', 16, 'bold'), 
                                      fg=self.colors['accent_gold'], 
                                      bg=self.colors['bg_medium'])
        self.balance_label.grid(row=0, column=0, padx=10)
        
        # Кнопка пополнения баланса в игре
        deposit_btn = tk.Button(balance_inner_frame, text="Пополнить", 
                                command=self.deposit_balance,
                                font=('Arial', 10, 'bold'),
                                bg=self.colors['accent_green'],
                                fg='black')
        deposit_btn.grid(row=0, column=1, padx=10)
        
        # Отображение слотов
        slots_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        slots_frame.pack(pady=20)
        
        # Создаем слоты (три ячейки)
        self.slot_labels = []
        for i in range(3):
            slot_label = tk.Label(slots_frame, text="?", 
                                  font=('Arial', 48, 'bold'), 
                                  width=4, 
                                  height=2,
                                  bg='white',
                                  fg=self.colors['bg_dark'],
                                  relief=tk.RIDGE,
                                  borderwidth=5)
            slot_label.grid(row=0, column=i, padx=10)
            self.slot_labels.append(slot_label)
        
        # Управление ставками
        bet_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        bet_frame.pack(pady=10)
        
        bet_label = tk.Label(bet_frame, text="Ставка:", 
                             font=('Arial', 14), 
                             fg=self.colors['text_light'], 
                             bg=self.colors['bg_dark'])
        bet_label.grid(row=0, column=0, padx=5)
        
        self.bet_var = tk.IntVar(value=self.bet_amount)
        bet_spinbox = tk.Spinbox(bet_frame, from_=10, to=min(500, self.balance), 
                                 textvariable=self.bet_var, 
                                 font=('Arial', 14), 
                                 width=10)
        bet_spinbox.grid(row=0, column=1, padx=5)
        
        # Кнопка вращения
        spin_btn = tk.Button(bet_frame, text="Крутить!", 
                             command=self.spin_slots,
                             font=('Arial', 14, 'bold'),
                             bg=self.colors['accent_gold'],
                             fg=self.colors['bg_dark'],
                             width=15,
                             height=2)
        spin_btn.grid(row=0, column=2, padx=20)
        
        # Отображение результата
        self.slots_result_label = tk.Label(self.root, text="Сделайте ставку и нажмите 'Крутить!'", 
                                           font=('Arial', 16), 
                                           fg=self.colors['text_light'], 
                                           bg=self.colors['bg_dark'])
        self.slots_result_label.pack(pady=10)
        
        # Правила игры
        rules_label = tk.Label(self.root, 
                               text="Правила: 3 одинаковых символа = x10 ставки, 2 одинаковых символа = x2 ставки", 
                               font=('Arial', 10), 
                               fg=self.colors['text_light'], 
                               bg=self.colors['bg_dark'])
        rules_label.pack(pady=5)
    
    def spin_slots(self):
        """Вращение слотов"""
        bet = self.bet_var.get()
        
        if bet > self.balance:
            messagebox.showerror("Ошибка", "Недостаточно средств на балансе!")
            return
        
        # Вычитаем ставку
        self.balance -= bet
        self.balance_label.config(text=f"Баланс: {self.balance} ₽")
        self.add_transaction('game_loss', bet, f"Ставка в слотах")
        
        # Символы для слотов
        symbols = ['7', '🍒', '⭐', '🔔', '🍋', '💎']
        
        # Анимация вращения
        for i in range(10):
            for j in range(3):
                self.slot_labels[j].config(text=random.choice(symbols))
            self.root.update()
            self.root.after(100)
        
        # Финальный результат
        results = [random.choice(symbols) for _ in range(3)]
        
        for i in range(3):
            self.slot_labels[i].config(text=results[i])
        
        # Определяем выигрыш
        win_multiplier = 0
        
        # Проверяем комбинации
        if results[0] == results[1] == results[2]:
            win_multiplier = 10  # Три одинаковых символа
        elif results[0] == results[1] or results[1] == results[2] or results[0] == results[2]:
            win_multiplier = 2  # Два одинаковых символа
        
        # Вычисляем выигрыш
        win_amount = bet * win_multiplier
        
        if win_amount > 0:
            self.balance += win_amount
            self.slots_result_label.config(text=f"Выигрыш! Вы выиграли {win_amount} ₽!", 
                                           fg=self.colors['accent_green'])
            self.add_transaction('game_win', win_amount, f"Выигрыш в слотах")
        else:
            self.slots_result_label.config(text=f"Проигрыш! Попробуйте еще раз!", 
                                           fg=self.colors['accent_red'])
        
        # Обновляем баланс
        self.balance_label.config(text=f"Баланс: {self.balance} ₽")
    
    def create_deck(self):
        """Создание колоды карт"""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = []
        
        for suit in suits:
            for value in values:
                deck.append((value, suit))
        
        random.shuffle(deck)
        return deck
    
    def calculate_hand_value(self, hand):
        """Вычисление стоимости руки в блэкджеке"""
        value = 0
        aces = 0
        
        for card in hand:
            card_value = card[0]
            if card_value in ['J', 'Q', 'K']:
                value += 10
            elif card_value == 'A':
                value += 11
                aces += 1
            else:
                value += int(card_value)
        
        # Корректируем стоимость, если есть тузы и перебор
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def play_blackjack(self):
        """Игра в блэкджек"""
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Заголовок
        title_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        title_frame.pack(pady=10)
        
        back_btn = tk.Button(title_frame, text="← Назад", 
                             command=self.create_main_menu,
                             font=('Arial', 10),
                             bg=self.colors['bg_light'],
                             fg=self.colors['text_light'])
        back_btn.pack(side=tk.LEFT, padx=10)
        
        title_label = tk.Label(title_frame, text="Блэкджек", 
                               font=('Arial', 28, 'bold'), 
                               fg=self.colors['accent_gold'], 
                               bg=self.colors['bg_dark'])
        title_label.pack()
        
        # Отображение баланса с кнопкой пополнения
        balance_frame = tk.Frame(self.root, bg=self.colors['bg_medium'])
        balance_frame.pack(pady=10)
        
        balance_inner_frame = tk.Frame(balance_frame, bg=self.colors['bg_medium'])
        balance_inner_frame.pack()
        
        self.balance_label = tk.Label(balance_inner_frame, text=f"Баланс: {self.balance} ₽", 
                                      font=('Arial', 16, 'bold'), 
                                      fg=self.colors['accent_gold'], 
                                      bg=self.colors['bg_medium'])
        self.balance_label.grid(row=0, column=0, padx=10)
        
        # Кнопка пополнения баланса в игре
        deposit_btn = tk.Button(balance_inner_frame, text="Пополнить", 
                                command=self.deposit_balance,
                                font=('Arial', 10, 'bold'),
                                bg=self.colors['accent_green'],
                                fg='black')
        deposit_btn.grid(row=0, column=1, padx=10)
        
        # Фрейм для отображения карт
        cards_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        cards_frame.pack(pady=20)
        
        # Рука дилера
        dealer_frame = tk.Frame(cards_frame, bg=self.colors['bg_dark'])
        dealer_frame.pack(pady=10)
        
        dealer_label = tk.Label(dealer_frame, text="Дилер:", 
                                font=('Arial', 16, 'bold'), 
                                fg=self.colors['text_light'], 
                                bg=self.colors['bg_dark'])
        dealer_label.pack(side=tk.LEFT)
        
        self.dealer_cards_frame = tk.Frame(dealer_frame, bg=self.colors['bg_dark'])
        self.dealer_cards_frame.pack(side=tk.LEFT, padx=10)
        
        self.dealer_value_label = tk.Label(dealer_frame, text="Очков: ?", 
                                           font=('Arial', 14), 
                                           fg=self.colors['text_light'], 
                                           bg=self.colors['bg_dark'])
        self.dealer_value_label.pack(side=tk.LEFT, padx=10)
        
        # Рука игрока
        player_frame = tk.Frame(cards_frame, bg=self.colors['bg_dark'])
        player_frame.pack(pady=10)
        
        player_label = tk.Label(player_frame, text="Ваша рука:", 
                                font=('Arial', 16, 'bold'), 
                                fg=self.colors['text_light'], 
                                bg=self.colors['bg_dark'])
        player_label.pack(side=tk.LEFT)
        
        self.player_cards_frame = tk.Frame(player_frame, bg=self.colors['bg_dark'])
        self.player_cards_frame.pack(side=tk.LEFT, padx=10)
        
        self.player_value_label = tk.Label(player_frame, text="Очков: 0", 
                                           font=('Arial', 14), 
                                           fg=self.colors['text_light'], 
                                           bg=self.colors['bg_dark'])
        self.player_value_label.pack(side=tk.LEFT, padx=10)
        
        # Управление ставками
        bet_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        bet_frame.pack(pady=10)
        
        bet_label = tk.Label(bet_frame, text="Ставка:", 
                             font=('Arial', 14), 
                             fg=self.colors['text_light'], 
                             bg=self.colors['bg_dark'])
        bet_label.grid(row=0, column=0, padx=5)
        
        self.bet_var = tk.IntVar(value=self.bet_amount)
        bet_spinbox = tk.Spinbox(bet_frame, from_=10, to=min(500, self.balance), 
                                 textvariable=self.bet_var, 
                                 font=('Arial', 14), 
                                 width=10)
        bet_spinbox.grid(row=0, column=1, padx=5)
        
        # Кнопки управления игрой
        buttons_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        buttons_frame.pack(pady=10)
        
        self.start_btn = tk.Button(buttons_frame, text="Начать игру", 
                                   command=self.start_blackjack,
                                   font=('Arial', 12, 'bold'),
                                   bg=self.colors['accent_green'],
                                   fg='black',
                                   width=15)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.hit_btn = tk.Button(buttons_frame, text="Взять карту", 
                                 command=self.hit_card,
                                 font=('Arial', 12, 'bold'),
                                 bg=self.colors['bg_light'],
                                 fg=self.colors['text_light'],
                                 width=15,
                                 state=tk.DISABLED)
        self.hit_btn.grid(row=0, column=1, padx=5)
        
        self.stand_btn = tk.Button(buttons_frame, text="Хватит", 
                                   command=self.stand,
                                   font=('Arial', 12, 'bold'),
                                   bg=self.colors['accent_gold'],
                                   fg='black',
                                   width=15,
                                   state=tk.DISABLED)
        self.stand_btn.grid(row=0, column=2, padx=5)
        
        # Отображение результата
        self.blackjack_result_label = tk.Label(self.root, text="Сделайте ставку и начните игру!", 
                                               font=('Arial', 16), 
                                               fg=self.colors['text_light'], 
                                               bg=self.colors['bg_dark'])
        self.blackjack_result_label.pack(pady=10)
        
        # Правила игры
        rules_label = tk.Label(self.root, 
                               text="Правила: цель - набрать 21 очко или ближе к 21, чем дилер. Туз = 1 или 11 очков.", 
                               font=('Arial', 10), 
                               fg=self.colors['text_light'], 
                               bg=self.colors['bg_dark'])
        rules_label.pack(pady=5)
    
    def start_blackjack(self):
        """Начало игры в блэкджек"""
        bet = self.bet_var.get()
        
        if bet > self.balance:
            messagebox.showerror("Ошибка", "Недостаточно средств на балансе!")
            return
        
        # Вычитаем ставку
        self.balance -= bet
        self.current_bet = bet
        self.balance_label.config(text=f"Баланс: {self.balance} ₽")
        self.add_transaction('game_loss', bet, f"Ставка в блэкджеке")
        
        # Создаем колоду и раздаем карты
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        
        # Раздаем по 2 карты
        for _ in range(2):
            self.player_hand.append(self.deck.pop())
            self.dealer_hand.append(self.deck.pop())
        
        # Отображаем карты
        self.display_blackjack_cards()
        
        # Проверяем блэкджек у игрока
        player_value = self.calculate_hand_value(self.player_hand)
        
        if player_value == 21:
            self.blackjack_result_label.config(text="У вас блэкджек!", fg=self.colors['accent_green'])
            self.dealer_turn()
        else:
            self.game_in_progress = True
            self.start_btn.config(state=tk.DISABLED)
            self.hit_btn.config(state=tk.NORMAL)
            self.stand_btn.config(state=tk.NORMAL)
            self.blackjack_result_label.config(text="Ваш ход. Взять карту или хватит?", fg=self.colors['text_light'])
    
    def display_blackjack_cards(self):
        """Отображение карт в блэкджеке"""
        # Очищаем фреймы с картами
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()
        
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        
        # Отображаем карты игрока
        player_value = self.calculate_hand_value(self.player_hand)
        self.player_value_label.config(text=f"Очков: {player_value}")
        
        for card in self.player_hand:
            card_label = tk.Label(self.player_cards_frame, text=card[0], 
                                  font=('Arial', 12), 
                                  width=4,
                                  height=2,
                                  bg='white',
                                  fg='red' if card[1] in ['hearts', 'diamonds'] else 'black',
                                  relief=tk.RAISED,
                                  borderwidth=2)
            card_label.pack(side=tk.LEFT, padx=2)
        
        # Отображаем карты дилера
        if self.game_in_progress:
            # Показываем только одну карту дилера
            dealer_card = self.dealer_hand[0]
            card_label = tk.Label(self.dealer_cards_frame, text=dealer_card[0], 
                                  font=('Arial', 12), 
                                  width=4,
                                  height=2,
                                  bg='white',
                                  fg='red' if dealer_card[1] in ['hearts', 'diamonds'] else 'black',
                                  relief=tk.RAISED,
                                  borderwidth=2)
            card_label.pack(side=tk.LEFT, padx=2)
            
            # Вторая карта скрыта
            hidden_label = tk.Label(self.dealer_cards_frame, text="?", 
                                    font=('Arial', 12), 
                                    width=4,
                                    height=2,
                                    bg=self.colors['bg_light'],
                                    fg=self.colors['text_light'],
                                    relief=tk.RAISED,
                                    borderwidth=2)
            hidden_label.pack(side=tk.LEFT, padx=2)
            
            self.dealer_value_label.config(text="Очков: ?")
        else:
            # Показываем все карты дилера
            dealer_value = self.calculate_hand_value(self.dealer_hand)
            self.dealer_value_label.config(text=f"Очков: {dealer_value}")
            
            for card in self.dealer_hand:
                card_label = tk.Label(self.dealer_cards_frame, text=card[0], 
                                      font=('Arial', 12), 
                                      width=4,
                                      height=2,
                                      bg='white',
                                      fg='red' if card[1] in ['hearts', 'diamonds'] else 'black',
                                      relief=tk.RAISED,
                                      borderwidth=2)
                card_label.pack(side=tk.LEFT, padx=2)
    
    def hit_card(self):
        """Игрок берет карту"""
        if not self.game_in_progress:
            return
        
        self.player_hand.append(self.deck.pop())
        self.display_blackjack_cards()
        
        player_value = self.calculate_hand_value(self.player_hand)
        
        if player_value > 21:
            self.blackjack_result_label.config(text="Перебор! Вы проиграли.", fg=self.colors['accent_red'])
            self.end_blackjack_game(False)
        elif player_value == 21:
            self.blackjack_result_label.config(text="У вас 21 очко!", fg=self.colors['accent_green'])
            self.dealer_turn()
    
    def stand(self):
        """Игрок останавливается"""
        if not self.game_in_progress:
            return
        
        self.blackjack_result_label.config(text="Дилер делает ход...", fg=self.colors['text_light'])
        self.dealer_turn()
    
    def dealer_turn(self):
        """Ход дилера"""
        self.game_in_progress = False
        self.hit_btn.config(state=tk.DISABLED)
        self.stand_btn.config(state=tk.DISABLED)
        
        # Дилер берет карты, пока у него меньше 17 очков
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        
        while dealer_value < 17:
            self.dealer_hand.append(self.deck.pop())
            dealer_value = self.calculate_hand_value(self.dealer_hand)
        
        # Обновляем отображение карт
        self.display_blackjack_cards()
        
        # Определяем результат
        player_value = self.calculate_hand_value(self.player_hand)
        
        if player_value > 21:
            # Игрок уже проиграл (перебор)
            self.end_blackjack_game(False)
        elif dealer_value > 21:
            # Дилер перебрал
            self.blackjack_result_label.config(text="Дилер перебрал! Вы выиграли!", fg=self.colors['accent_green'])
            self.end_blackjack_game(True)
        elif player_value == dealer_value:
            # Ничья
            self.blackjack_result_label.config(text="Ничья! Ставка возвращена.", fg=self.colors['accent_gold'])
            self.end_blackjack_game(None)
        elif player_value > dealer_value:
            # Игрок выиграл
            self.blackjack_result_label.config(text="Вы выиграли!", fg=self.colors['accent_green'])
            self.end_blackjack_game(True)
        else:
            # Дилер выиграл
            self.blackjack_result_label.config(text="Дилер выиграл.", fg=self.colors['accent_red'])
            self.end_blackjack_game(False)
    
    def end_blackjack_game(self, player_won):
        """Завершение игры в блэкджек"""
        if player_won is True:
            win_amount = self.current_bet * 2  # Выигрыш 1:1
            self.balance += win_amount
            self.balance_label.config(text=f"Баланс: {self.balance} ₽")
            self.add_transaction('game_win', win_amount - self.current_bet, f"Выигрыш в блэкджеке")
            self.blackjack_result_label.config(text=f"Вы выиграли {win_amount - self.current_bet} ₽!", fg=self.colors['accent_green'])
        elif player_won is None:
            # Ничья - возвращаем ставку
            self.balance += self.current_bet
            self.balance_label.config(text=f"Баланс: {self.balance} ₽")
            self.blackjack_result_label.config(text="Ничья! Ставка возвращена.", fg=self.colors['accent_gold'])
        else:
            self.blackjack_result_label.config(text=f"Вы проиграли {self.current_bet} ₽.", fg=self.colors['accent_red'])
        
        self.start_btn.config(state=tk.NORMAL)
    
    def play_dice(self):
        """Игра в кости"""
        # Очистка окна
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Заголовок
        title_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        title_frame.pack(pady=10)
        
        back_btn = tk.Button(title_frame, text="← Назад", 
                             command=self.create_main_menu,
                             font=('Arial', 10),
                             bg=self.colors['bg_light'],
                             fg=self.colors['text_light'])
        back_btn.pack(side=tk.LEFT, padx=10)
        
        title_label = tk.Label(title_frame, text="Кости", 
                               font=('Arial', 28, 'bold'), 
                               fg=self.colors['accent_gold'], 
                               bg=self.colors['bg_dark'])
        title_label.pack()
        
        # Отображение баланса с кнопкой пополнения
        balance_frame = tk.Frame(self.root, bg=self.colors['bg_medium'])
        balance_frame.pack(pady=10)
        
        balance_inner_frame = tk.Frame(balance_frame, bg=self.colors['bg_medium'])
        balance_inner_frame.pack()
        
        self.balance_label = tk.Label(balance_inner_frame, text=f"Баланс: {self.balance} ₽", 
                                      font=('Arial', 16, 'bold'), 
                                      fg=self.colors['accent_gold'], 
                                      bg=self.colors['bg_medium'])
        self.balance_label.grid(row=0, column=0, padx=10)
        
        # Кнопка пополнения баланса в игре
        deposit_btn = tk.Button(balance_inner_frame, text="Пополнить", 
                                command=self.deposit_balance,
                                font=('Arial', 10, 'bold'),
                                bg=self.colors['accent_green'],
                                fg='black')
        deposit_btn.grid(row=0, column=1, padx=10)
        
        # Отображение костей
        dice_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        dice_frame.pack(pady=20)
        
        self.dice_labels = []
        for i in range(2):
            dice_label = tk.Label(dice_frame, text="⚀", 
                                  font=('Arial', 48), 
                                  width=4, 
                                  height=2,
                                  bg='white',
                                  fg=self.colors['bg_dark'],
                                  relief=tk.RAISED,
                                  borderwidth=5)
            dice_label.grid(row=0, column=i, padx=20)
            self.dice_labels.append(dice_label)
        
        # Отображение суммы
        self.dice_sum_label = tk.Label(dice_frame, text="Сумма: 0", 
                                       font=('Arial', 20, 'bold'), 
                                       fg=self.colors['accent_gold'], 
                                       bg=self.colors['bg_dark'])
        self.dice_sum_label.grid(row=0, column=2, padx=20)
        
        # Выбор типа ставки
        bet_type_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        bet_type_frame.pack(pady=10)
        
        self.bet_type = tk.StringVar(value="over_7")
        
        tk.Radiobutton(bet_type_frame, text="Больше 7 (x2)", 
                       variable=self.bet_type, value="over_7",
                       font=('Arial', 12),
                       bg=self.colors['bg_dark'],
                       fg=self.colors['text_light'],
                       selectcolor=self.colors['bg_light']).grid(row=0, column=0, padx=10)
        
        tk.Radiobutton(bet_type_frame, text="Меньше 7 (x2)", 
                       variable=self.bet_type, value="under_7",
                       font=('Arial', 12),
                       bg=self.colors['bg_dark'],
                       fg=self.colors['text_light'],
                       selectcolor=self.colors['bg_light']).grid(row=0, column=1, padx=10)
        
        tk.Radiobutton(bet_type_frame, text="Ровно 7 (x4)", 
                       variable=self.bet_type, value="exactly_7",
                       font=('Arial', 12),
                       bg=self.colors['bg_dark'],
                       fg=self.colors['text_light'],
                       selectcolor=self.colors['bg_light']).grid(row=0, column=2, padx=10)
        
        tk.Radiobutton(bet_type_frame, text="Дубль (x6)", 
                       variable=self.bet_type, value="double",
                       font=('Arial', 12),
                       bg=self.colors['bg_dark'],
                       fg=self.colors['text_light'],
                       selectcolor=self.colors['bg_light']).grid(row=0, column=3, padx=10)
        
        # Управление ставками
        bet_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        bet_frame.pack(pady=10)
        
        bet_label = tk.Label(bet_frame, text="Ставка:", 
                             font=('Arial', 14), 
                             fg=self.colors['text_light'], 
                             bg=self.colors['bg_dark'])
        bet_label.grid(row=0, column=0, padx=5)
        
        self.dice_bet_var = tk.IntVar(value=self.bet_amount)
        bet_spinbox = tk.Spinbox(bet_frame, from_=10, to=min(500, self.balance), 
                                 textvariable=self.dice_bet_var, 
                                 font=('Arial', 14), 
                                 width=10)
        bet_spinbox.grid(row=0, column=1, padx=5)
        
        # Кнопка броска
        roll_btn = tk.Button(bet_frame, text="Бросить кости!", 
                             command=self.roll_dice,
                             font=('Arial', 14, 'bold'),
                             bg=self.colors['accent_gold'],
                             fg=self.colors['bg_dark'],
                             width=15,
                             height=2)
        roll_btn.grid(row=0, column=2, padx=20)
        
        # Отображение результата
        self.dice_result_label = tk.Label(self.root, text="Выберите тип ставки и бросьте кости!", 
                                          font=('Arial', 16), 
                                          fg=self.colors['text_light'], 
                                          bg=self.colors['bg_dark'])
        self.dice_result_label.pack(pady=10)
        
        # Правила игры
        rules_label = tk.Label(self.root, 
                               text="Правила: бросаются 2 кости. Выигрыш зависит от типа ставки и суммы очков.", 
                               font=('Arial', 10), 
                               fg=self.colors['text_light'], 
                               bg=self.colors['bg_dark'])
        rules_label.pack(pady=5)
    
    def get_dice_face(self, value):
        """Получение символа грани кости по значению"""
        dice_faces = {
            1: "⚀",
            2: "⚁",
            3: "⚂",
            4: "⚃",
            5: "⚄",
            6: "⚅"
        }
        return dice_faces.get(value, "⚀")
    
    def roll_dice(self):
        """Бросок костей"""
        bet = self.dice_bet_var.get()
        bet_type = self.bet_type.get()
        
        if bet > self.balance:
            messagebox.showerror("Ошибка", "Недостаточно средств на балансе!")
            return
        
        # Вычитаем ставку
        self.balance -= bet
        self.balance_label.config(text=f"Баланс: {self.balance} ₽")
        self.add_transaction('game_loss', bet, f"Ставка в костях: {bet_type}")
        
        # Анимация броска
        for i in range(10):
            for j in range(2):
                self.dice_labels[j].config(text=self.get_dice_face(random.randint(1, 6)))
            self.root.update()
            self.root.after(100)
        
        # Финальный результат
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        
        self.dice_labels[0].config(text=self.get_dice_face(dice1))
        self.dice_labels[1].config(text=self.get_dice_face(dice2))
        
        # Вычисляем сумму и проверяем условия
        total = dice1 + dice2
        is_double = dice1 == dice2
        
        self.dice_sum_label.config(text=f"Сумма: {total}")
        
        # Определяем выигрыш
        win_multiplier = 0
        
        if bet_type == "over_7" and total > 7:
            win_multiplier = 2
        elif bet_type == "under_7" and total < 7:
            win_multiplier = 2
        elif bet_type == "exactly_7" and total == 7:
            win_multiplier = 4
        elif bet_type == "double" and is_double:
            win_multiplier = 6
        
        # Вычисляем выигрыш
        win_amount = bet * win_multiplier
        
        if win_amount > 0:
            self.balance += win_amount
            self.dice_result_label.config(text=f"Выигрыш! Вы выиграли {win_amount} ₽!", 
                                          fg=self.colors['accent_green'])
            self.add_transaction('game_win', win_amount, f"Выигрыш в костях: {bet_type}")
        else:
            self.dice_result_label.config(text=f"Проигрыш! Попробуйте еще раз!", 
                                          fg=self.colors['accent_red'])
        
        # Обновляем баланс
        self.balance_label.config(text=f"Баланс: {self.balance} ₽")
    
    def show_settings(self):
        """Настройки и правила"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Настройки и правила")
        settings_window.geometry("700x550")
        settings_window.configure(bg=self.colors['bg_dark'])
        settings_window.resizable(False, False)
        
        # Заголовок
        title_label = tk.Label(settings_window, text="Настройки и правила казино GL", 
                               font=('Arial', 20, 'bold'), 
                               fg=self.colors['accent_gold'], 
                               bg=self.colors['bg_dark'])
        title_label.pack(pady=20)
        
        # Правила
        rules_frame = tk.Frame(settings_window, bg=self.colors['bg_medium'], relief=tk.RAISED, borderwidth=2)
        rules_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        rules_text = """
        ПРАВИЛА КАЗИНО GL:
        
        1. Рулетка:
           - Красное/Черное: ставка х2
           - Зеленое (0): ставка х14
        
        2. Слот-машина:
           - 3 одинаковых символа: ставка х10
           - 2 одинаковых символа: ставка х2
        
        3. Блэкджек:
           - Цель: набрать 21 очко или ближе к 21, чем дилер
           - Карты: 2-10 = номинал, JQK = 10, A = 1 или 11
           - Выигрыш: ставка х2 (1:1)
        
        4. Кости:
           - Больше 7: ставка х2
           - Меньше 7: ставка х2
           - Ровно 7: ставка х4
           - Дубль: ставка х6
        
        5. Начальный баланс: 1000 ₽
        6. Минимальная ставка: 10 ₽
        7. Максимальная ставка: 500 ₽
        
        8. Пополнение баланса:
           - Можно пополнить на любую сумму до 1,000,000 ₽
           - Доступны предустановленные суммы
           - Можно ввести свою сумму
        
        9. История операций:
           - Все операции сохраняются
           - Можно посмотреть последние 20 операций
        
        Игра предназначена только для развлечения.
        Все выигрыши виртуальные.
        """
        
        rules_label = tk.Label(rules_frame, text=rules_text, 
                               font=('Arial', 11), 
                               fg=self.colors['text_light'], 
                               bg=self.colors['bg_medium'],
                               justify=tk.LEFT)
        rules_label.pack(pady=20, padx=20)
        
        # Кнопка закрытия
        close_btn = tk.Button(settings_window, text="Закрыть", 
                              command=settings_window.destroy,
                              font=('Arial', 14, 'bold'),
                              bg=self.colors['accent_gold'],
                              fg=self.colors['bg_dark'],
                              width=15,
                              height=2)
        close_btn.pack(pady=20)

def main():
    root = tk.Tk()
    app = CasinoGL(root)
    root.mainloop()

if __name__ == "__main__":
    main()