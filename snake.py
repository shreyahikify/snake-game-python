import turtle
import time
import random

# --- CONFIGURATION ---
DELAY = 0.1
HIGH_SCORE_FILE = "data.txt"

# Create high score file if it doesn't exist
try:
    with open(HIGH_SCORE_FILE, "r") as f:
        high_score = int(f.read())
except (FileNotFoundError, ValueError):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write("0")
    high_score = 0

# --- SETUP SCREEN ---
screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)

# --- SCOREBOARD ---
score = 0
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)

def update_scoreboard():
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

update_scoreboard()

# --- SNAKE HEAD ---
head = turtle.Turtle()
head.shape("square")
head.color("green")
head.penup()
head.direction = "stop"

# --- FOOD ---
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# --- FUNCTIONS ---
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)

def reset_game():
    global score, high_score
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    if score > high_score:
        high_score = score
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(high_score))
    score = 0
    update_scoreboard()

# --- INPUTS ---
screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

# --- MAIN LOOP ---
running = True
def stop(): global running; running = False
root = screen.getcanvas().winfo_toplevel()
root.protocol("WM_DELETE_WINDOW", stop)

while running:
    try:
        screen.update()

        # Border Collision
        if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
            reset_game()

        # Food Collision
        if head.distance(food) < 20:
            food.goto(random.randint(-270, 270), random.randint(-270, 270))
            new_seg = turtle.Turtle("square")
            new_seg.color("lightgreen")
            new_seg.penup()
            segments.append(new_seg)
            score += 10
            update_scoreboard()

        # Move Segments
        for i in range(len(segments)-1, 0, -1):
            segments[i].goto(segments[i-1].pos())
        if segments:
            segments[0].goto(head.pos())

        move()

        # Tail Collision
        for seg in segments:
            if seg.distance(head) < 20:
                reset_game()

        time.sleep(DELAY)
    except:
        break