import tkinter as tk
import random


# =========================================================
# CỬA SỔ CHÍNH
# =========================================================

root = tk.Tk()
root.title("GAME VƯỢT CHƯỚNG NGẠI VẬT")
root.geometry("900x500")
root.resizable(False, False)


# =========================================================
# MÀN HÌNH GAME
# =========================================================

canvas = tk.Canvas(
    root,
    width=900,
    height=500,
    bg="#87CEEB",
    highlightthickness=0
)

canvas.pack()


# =========================================================
# BIẾN GAME
# =========================================================

player_name = ""

player_x = 100
player_y = 350

player_width = 45
player_height = 60

velocity_y = 0

gravity = 1
jump_power = -17

on_ground = True

obstacles = []

obstacle_speed = 8

spawn_time = 0

score = 0

game_over = False

last_milestone = 0

score_text = None


# =========================================================
# MÀN HÌNH NHẬP TÊN
# =========================================================

def start_screen():

    canvas.delete("all")

    # -----------------------------
    # Bầu trời
    # -----------------------------

    canvas.create_rectangle(
        0,
        0,
        900,
        500,
        fill="#87CEEB",
        outline=""
    )

    # -----------------------------
    # Mặt trời
    # -----------------------------

    canvas.create_oval(
        730,
        40,
        800,
        110,
        fill="yellow",
        outline="orange",
        width=2
    )

    # -----------------------------
    # Mây
    # -----------------------------

    canvas.create_oval(
        100,
        70,
        160,
        110,
        fill="white",
        outline="white"
    )

    canvas.create_oval(
        135,
        50,
        200,
        110,
        fill="white",
        outline="white"
    )

    canvas.create_oval(
        180,
        70,
        240,
        110,
        fill="white",
        outline="white"
    )

    # -----------------------------
    # Tiêu đề
    # -----------------------------

    canvas.create_text(
        450,
        100,
        text="GAME VƯỢT CHƯỚNG NGẠI VẬT",
        font=("Arial", 30, "bold"),
        fill="white"
    )

    # -----------------------------
    # Con gà
    # -----------------------------

    canvas.create_text(
        450,
        185,
        text="🐔",
        font=("Segoe UI Emoji", 70)
    )

    # -----------------------------
    # Hướng dẫn
    # -----------------------------

    canvas.create_text(
        450,
        245,
        text="NHẬP TÊN NHÂN VẬT",
        font=("Arial", 20, "bold"),
        fill="black"
    )

    # -----------------------------
    # Ô nhập tên
    # -----------------------------

    name_entry = tk.Entry(
        root,
        font=("Arial", 18),
        justify="center",
        width=25
    )

    name_entry.place(
        x=300,
        y=275
    )

    name_entry.focus()

    # -----------------------------
    # Hàm bắt đầu
    # -----------------------------

    def start_game():

        global player_name

        name = name_entry.get().strip()

        if name == "":
            name = "Người chơi"

        player_name = name

        name_entry.destroy()
        start_button.destroy()

        run_game()

    # -----------------------------
    # Nút bắt đầu
    # -----------------------------

    start_button = tk.Button(
        root,
        text="BẮT ĐẦU GAME",
        font=("Arial", 16, "bold"),
        bg="#00A651",
        fg="white",
        width=18,
        height=2,
        command=start_game
    )

    start_button.place(
        x=325,
        y=325
    )

    # Nhấn Enter để bắt đầu
    root.bind(
        "<Return>",
        lambda event: start_game()
    )


# =========================================================
# VẼ NHÂN VẬT
# =========================================================

def create_player():

    # -----------------------------
    # Thân
    # -----------------------------

    canvas.create_rectangle(
        player_x,
        player_y,
        player_x + player_width,
        player_y + player_height,
        fill="blue",
        outline="black",
        width=2,
        tags="player"
    )

    # -----------------------------
    # Đầu
    # -----------------------------

    canvas.create_oval(
        player_x + 3,
        player_y - 35,
        player_x + 42,
        player_y + 5,
        fill="yellow",
        outline="black",
        width=2,
        tags="player"
    )

    # -----------------------------
    # Mắt
    # -----------------------------

    canvas.create_oval(
        player_x + 26,
        player_y - 24,
        player_x + 31,
        player_y - 19,
        fill="black",
        tags="player"
    )

    # -----------------------------
    # Chân trái
    # -----------------------------

    canvas.create_line(
        player_x + 10,
        player_y + 60,
        player_x + 5,
        player_y + 76,
        fill="black",
        width=5,
        tags="player"
    )

    # -----------------------------
    # Chân phải
    # -----------------------------

    canvas.create_line(
        player_x + 32,
        player_y + 60,
        player_x + 38,
        player_y + 76,
        fill="black",
        width=5,
        tags="player"
    )


# =========================================================
# TẠO CHƯỚNG NGẠI VẬT
# =========================================================

def create_obstacle():

    height = random.randint(40, 80)

    width = random.randint(30, 50)

    x = 900

    y = 425 - height

    # -----------------------------
    # Thân chướng ngại vật
    # -----------------------------

    body = canvas.create_rectangle(
        x,
        y,
        x + width,
        425,
        fill="red",
        outline="black",
        width=2
    )

    # -----------------------------
    # Gai
    # -----------------------------

    spike = canvas.create_polygon(
        x,
        y,
        x + width / 2,
        y - 20,
        x + width,
        y,
        fill="black",
        outline="black"
    )

    obstacles.append({
        "body": body,
        "spike": spike
    })


# =========================================================
# NHÂN VẬT NHẢY
# =========================================================

def jump(event=None):

    global velocity_y
    global on_ground

    # Nếu Game Over thì SPACE để chơi lại
    if game_over:

        restart_game()

        return

    # Nếu đang đứng trên mặt đất thì nhảy
    if on_ground:

        velocity_y = jump_power

        on_ground = False


# =========================================================
# DI CHUYỂN NHÂN VẬT
# =========================================================

def move_player():

    global player_y
    global velocity_y
    global on_ground

    # Trọng lực
    velocity_y += gravity

    # Di chuyển
    player_y += velocity_y

    # Chạm đất
    if player_y >= 350:

        player_y = 350

        velocity_y = 0

        on_ground = True

    # Xóa nhân vật cũ
    canvas.delete("player")

    # Vẽ nhân vật mới
    create_player()


# =========================================================
# DI CHUYỂN CHƯỚNG NGẠI VẬT
# =========================================================

def move_obstacles():

    for obstacle in obstacles:

        canvas.move(
            obstacle["body"],
            -obstacle_speed,
            0
        )

        canvas.move(
            obstacle["spike"],
            -obstacle_speed,
            0
        )


# =========================================================
# KIỂM TRA VA CHẠM
# =========================================================

def check_collision():

    global game_over

    # Tọa độ nhân vật
    player_left = player_x
    player_right = player_x + player_width

    player_top = player_y - 35
    player_bottom = player_y + player_height

    # Kiểm tra từng chướng ngại vật
    for obstacle in obstacles:

        body = canvas.coords(
            obstacle["body"]
        )

        if len(body) != 4:
            continue

        obstacle_left = body[0]
        obstacle_top = body[1]
        obstacle_right = body[2]
        obstacle_bottom = body[3]

        # Va chạm
        if (
            player_right > obstacle_left
            and
            player_left < obstacle_right
            and
            player_bottom > obstacle_top
            and
            player_top < obstacle_bottom
        ):

            game_over = True

            show_game_over()

            return


# =========================================================
# XÓA CHƯỚNG NGẠI VẬT CŨ
# =========================================================

def delete_old_obstacles():

    global obstacles

    new_obstacles = []

    for obstacle in obstacles:

        body = canvas.coords(
            obstacle["body"]
        )

        if len(body) != 4:
            continue

        # Nếu vẫn còn trên màn hình
        if body[2] > 0:

            new_obstacles.append(
                obstacle
            )

        else:

            canvas.delete(
                obstacle["body"]
            )

            canvas.delete(
                obstacle["spike"]
            )

    obstacles = new_obstacles


# =========================================================
# GÀ KHEN KHI ĐẠT MỐC
# =========================================================

def chicken_praise(points):

    # Xóa lời khen cũ
    canvas.delete("praise")

    # Khung
    canvas.create_rectangle(
        230,
        105,
        670,
        325,
        fill="white",
        outline="green",
        width=5,
        tags="praise"
    )

    # Gà
    canvas.create_text(
        450,
        160,
        text="🐔",
        font=("Segoe UI Emoji", 60),
        tags="praise"
    )

    # Lời khen
    canvas.create_text(
        450,
        225,
        text="GIỎI LẮM! 👏",
        font=("Arial", 30, "bold"),
        fill="green",
        tags="praise"
    )

    # Tên + điểm
    canvas.create_text(
        450,
        270,
        text=f"{player_name} đạt {points} điểm!",
        font=("Arial", 19, "bold"),
        fill="blue",
        tags="praise"
    )

    # Sau 2 giây biến mất
    root.after(
        2000,
        lambda: canvas.delete("praise")
    )


# =========================================================
# GAME OVER
# =========================================================

def show_game_over():

    # Xóa lời khen nếu đang hiện
    canvas.delete("praise")

    # Khung Game Over
    canvas.create_rectangle(
        190,
        80,
        710,
        395,
        fill="black",
        outline="red",
        width=5,
        tags="gameover"
    )

    # Gà
    canvas.create_text(
        450,
        145,
        text="🐔",
        font=("Segoe UI Emoji", 65),
        tags="gameover"
    )

    # Gà chê
    canvas.create_text(
        450,
        215,
        text="SAO NGU THẾ? 😂",
        font=("Arial", 34, "bold"),
        fill="yellow",
        tags="gameover"
    )

    # Tên
    canvas.create_text(
        450,
        260,
        text=f"Người chơi: {player_name}",
        font=("Arial", 19, "bold"),
        fill="white",
        tags="gameover"
    )

    # Điểm
    canvas.create_text(
        450,
        295,
        text=f"Điểm: {score // 10}",
        font=("Arial", 22, "bold"),
        fill="white",
        tags="gameover"
    )

    # Chơi lại
    canvas.create_text(
        450,
        345,
        text="Nhấn SPACE để chơi lại",
        font=("Arial", 20, "bold"),
        fill="lime",
        tags="gameover"
    )


# =========================================================
# CHƠI LẠI
# =========================================================

def restart_game():

    global game_over
    global score
    global player_y
    global velocity_y
    global on_ground
    global obstacles
    global spawn_time
    global obstacle_speed
    global last_milestone

    # Xóa thông báo
    canvas.delete("gameover")

    canvas.delete("praise")

    # Xóa chướng ngại vật
    for obstacle in obstacles:

        canvas.delete(
            obstacle["body"]
        )

        canvas.delete(
            obstacle["spike"]
        )

    obstacles = []

    # Đặt lại nhân vật
    player_y = 350

    velocity_y = 0

    on_ground = True

    # Đặt lại điểm
    score = 0

    # Đặt lại thời gian tạo vật
    spawn_time = 0

    # Đặt lại tốc độ
    obstacle_speed = 8

    # Đặt lại mốc khen
    last_milestone = 0

    # Chơi lại
    game_over = False

    # Vẽ lại nhân vật
    canvas.delete("player")

    create_player()


# =========================================================
# VÒNG LẶP GAME
# =========================================================

def game_loop():

    global score
    global spawn_time
    global obstacle_speed
    global last_milestone

    # Chỉ chạy khi chưa Game Over
    if not game_over:

        # -----------------------------
        # Di chuyển nhân vật
        # -----------------------------

        move_player()

        # -----------------------------
        # Tạo chướng ngại vật
        # -----------------------------

        spawn_time += 1

        if spawn_time >= random.randint(60, 100):

            create_obstacle()

            spawn_time = 0

        # -----------------------------
        # Di chuyển vật cản
        # -----------------------------

        move_obstacles()

        # -----------------------------
        # Kiểm tra va chạm
        # -----------------------------

        check_collision()

        # -----------------------------
        # Xóa vật cũ
        # -----------------------------

        delete_old_obstacles()

        # -----------------------------
        # Tăng điểm
        # -----------------------------

        score += 1

        current_points = score // 10

        # -----------------------------
        # Hiển thị điểm
        # -----------------------------

        canvas.itemconfig(
            score_text,
            text=f"Điểm: {current_points}"
        )

        # -----------------------------
        # GÀ KHEN 100, 200, 300...
        # -----------------------------

        if current_points >= 100:

            milestone = (
                current_points // 100
            ) * 100

            if milestone > last_milestone:

                last_milestone = milestone

                chicken_praise(
                    milestone
                )

        # -----------------------------
        # Tăng tốc độ
        # -----------------------------

        if score % 500 == 0:

            obstacle_speed += 1

    # Gọi lại sau 20 mili giây
    root.after(
        20,
        game_loop
    )


# =========================================================
# VÀO GAME
# =========================================================

def run_game():

    global score_text

    canvas.delete("all")

    # -----------------------------
    # Bầu trời
    # -----------------------------

    canvas.create_rectangle(
        0,
        0,
        900,
        425,
        fill="#87CEEB",
        outline=""
    )

    # -----------------------------
    # Mặt trời
    # -----------------------------

    canvas.create_oval(
        730,
        40,
        800,
        110,
        fill="yellow",
        outline="orange",
        width=2
    )

    # -----------------------------
    # Mây
    # -----------------------------

    canvas.create_oval(
        100,
        70,
        160,
        110,
        fill="white",
        outline="white"
    )

    canvas.create_oval(
        135,
        50,
        200,
        110,
        fill="white",
        outline="white"
    )

    canvas.create_oval(
        180,
        70,
        240,
        110,
        fill="white",
        outline="white"
    )

    # -----------------------------
    # Mặt đất
    # -----------------------------

    canvas.create_rectangle(
        0,
        425,
        900,
        500,
        fill="green",
        outline="green"
    )

    # -----------------------------
    # Tên người chơi
    # -----------------------------

    canvas.create_text(
        20,
        20,
        anchor="nw",
        text=f"👤 {player_name}",
        font=("Arial", 22, "bold"),
        fill="black"
    )

    # -----------------------------
    # Điểm
    # -----------------------------

    score_text = canvas.create_text(
        20,
        55,
        anchor="nw",
        text="Điểm: 0",
        font=("Arial", 22, "bold"),
        fill="black"
    )

    # -----------------------------
    # Hướng dẫn
    # -----------------------------

    canvas.create_text(
        20,
        90,
        anchor="nw",
        text="SPACE = NHẢY",
        font=("Arial", 15, "bold"),
        fill="black"
    )

    # -----------------------------
    # Nhân vật
    # -----------------------------

    create_player()


# =========================================================
# PHÍM SPACE
# =========================================================

root.bind(
    "<space>",
    jump
)


# =========================================================
# BẮT ĐẦU
# =========================================================

start_screen()

game_loop()

root.mainloop()