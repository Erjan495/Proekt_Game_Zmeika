import random
import tkinter as tk

# Настройки игры
WIDTH = 600
HEIGHT = 400
SEG_SIZE = 20  # Размер одного сегмента змейки и еды
SPEED = 120  # Скорость игры (меньше значение — быстрее змейка)

# Создаем главное окно приложения
root = tk.Tk()
root.title("Игра")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)
root.configure(bg="white")

# Создаем холст для отрисовки игры с чисто белым фоном
canvas = tk.Canvas(
    root, width=WIDTH, height=HEIGHT, bg="white", highlightthickness=0
)
canvas.pack()

# Начальные переменные игры
snake = [(100, 100), (80, 100), (60, 100)]
direction = "Right"
next_direction = "Right"
score = 0
food = None
game_over = False

# Отображение счета
score_text = canvas.create_text(
    50, 20, text=f"Счет: {score}", fill="black", font=("Arial", 14, "bold")
)


def spawn_food():
    """Создает еду в случайном месте на сетке."""
    global food
    while True:
        x = random.randint(0, (WIDTH - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
        y = random.randint(0, (HEIGHT - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
        if (x, y) not in snake:
            food = (x, y)
            break


def change_direction(event):
    """Меняет направление движения по нажатию клавиш."""
    global next_direction
    key = event.keysym
    opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
    if key in opposites and opposites[key] != direction:
        next_direction = key


def draw():
    """Отрисовывает змейку и еду."""
    canvas.delete("game_obj")

    # Рисуем еду (красный квадрат)
    if food:
        fx, fy = food
        canvas.create_rectangle(
            fx,
            fy,
            fx + SEG_SIZE,
            fy + SEG_SIZE,
            fill="#e74c3c",
            outline="",
            tags="game_obj",
        )

    # Рисуем змейку (зеленые квадраты, голова темнее)
    for i, (x, y) in enumerate(snake):
        color = "#1e8449" if i == 0 else "#2ecc71"
        canvas.create_rectangle(
            x,
            y,
            x + SEG_SIZE,
            y + SEG_SIZE,
            fill=color,
            outline="white",
            tags="game_obj",
        )


def move_snake():
    """Основной игровой цикл: движение, проверка столкновений и поедания."""
    global direction, score, game_over

    if game_over:
        return

    direction = next_direction
    head_x, head_y = snake[0]

    if direction == "Up":
        head_y -= SEG_SIZE
    elif direction == "Down":
        head_y += SEG_SIZE
    elif direction == "Left":
        head_x -= SEG_SIZE
    elif direction == "Right":
        head_x += SEG_SIZE

    new_head = (head_x, head_y)

    # Проверка столкновения со стенами или с самой собой
    if (
        head_x < 0
        or head_x >= WIDTH
        or head_y < 0
        or head_y >= HEIGHT
        or new_head in snake
    ):
        end_game()
        return

    snake.insert(0, new_head)

    # Проверка, съела ли змейка еду
    if new_head == food:
        score += 1
        canvas.itemconfig(score_text, text=f"Счет: {score}")
        spawn_food()
    else:
        snake.pop()

    draw()
    root.after(SPEED, move_snake)


def end_game():
    """Экран окончания игры."""
    global game_over
    game_over = True
    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 - 20,
        text="Игра окончена!",
        fill="black",
        font=("Arial", 24, "bold"),
        tags="game_obj",
    )
    canvas.create_text(
        WIDTH // 2,
        HEIGHT // 2 + 20,
        text="Нажмите Пробел, чтобы начать заново",
        fill="gray",
        font=("Arial", 14),
        tags="game_obj",
    )


def restart_game(event):
    """Перезапуск игры."""
    global snake, direction, next_direction, score, game_over
    if game_over:
        snake = [(100, 100), (80, 100), (60, 100)]
        direction = "Right"
        next_direction = "Right"
        score = 0
        game_over = False
        canvas.itemconfig(score_text, text=f"Счет: {score}")
        spawn_food()
        move_snake()


# Привязка клавиш управления
root.bind("<KeyPress>", change_direction)
root.bind("<space>", restart_game)

# Запуск игры
spawn_food()
move_snake()

# Запускаем главный цикл приложения, чтобы окно не закрывалось
root.mainloop()



