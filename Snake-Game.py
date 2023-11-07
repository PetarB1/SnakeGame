import turtle
import time
import random

window = None
snake = []
head = None
food = None
food_color = None
direction = 'down'
WIDTH = 600
HEIGHT = 600
TURTLE_SIZE = 20
delay_time = 0.1
shapes = {
    0: 'circle',
    1: 'square',
    2: 'triangle'
}
colors = {
    0: 'gold',
    1: 'red',
    2: 'orange',
    3: 'blue',
    4: 'green',
    5: 'pink',
    6: 'yellow'
}
food_color = ''
X_RANGE = (WIDTH - TURTLE_SIZE)/2
Y_RANGE = (HEIGHT - TURTLE_SIZE)/2

pen = None
score = 0
high_score = 0


def set_screen():

    global window

    window = turtle.Screen()
    window.title('Snake')
    window.bgcolor('white smoke')
    window.setup(width=WIDTH,height=HEIGHT)
    window.tracer(0)

def listen_events():
    window.listen()
    window.onkeypress(set_up_direction,'Up')
    window.onkeypress(set_down_direction,'Down')
    window.onkeypress(set_left_direction,'Left')
    window.onkeypress(set_right_direction,'Right ')

def set_up_direction():
    global direction
    if direction != 'down':
        direction = 'up'
def set_down_direction():
    global direction
    if direction != 'up':
        direction = 'down'
def set_left_direction():
    global direction
    if direction != 'right':
        direction = 'left'
def set_right_direction():
    global direction
    if direction != 'left':
        direction = 'right'


def create_head():

    global head,snake

    head = turtle.Turtle()
    head.shape(shapes[1])
    head.speed(0)
    head.penup()

    head.goto(0,0)

    snake.append(head)

def create_score():

    global pen

    pen = turtle.Turtle()
    pen.penup()
    pen.hideturtle()
    pen.goto(0,Y_RANGE - 2*TURTLE_SIZE)
    pen.color('black')

    update_score(0)

def update_score(sc_increment, is_reset=False):
    global score,high_score

    if is_reset:
        score = 0
    else:
        score+=sc_increment

    if score > high_score:
        high_score = score

    pen.clear()

    pen.write("Score: {0}  |  High Score: {1}".format(score,high_score),align='center',font=('Arial',16,'normal'))

def update_screen():
    while window._RUNNING:

        check_border_collisions()
        check_body_collisions()
        move()
        add_food()
        eat_food()
        time.sleep(delay_time)
        window.update()

def check_body_collisions():

    for i, t in enumerate(snake):
        if i > 0:
            if head.distance(t) < TURTLE_SIZE - 1:
                global direction
                direction = 'stop'

                delay(1)
                reset()

def check_border_collisions():

    x = head.xcor()
    y = head.ycor()

    if x <= -X_RANGE:
        head.goto(X_RANGE-1,y)
    if x >= X_RANGE :
        head.goto(-X_RANGE+1,y)
    if y <= -Y_RANGE :
        head.goto(x,Y_RANGE-1)
    if y >= Y_RANGE:
        head.goto(x,-Y_RANGE+1)

def delay(duration):
    time.sleep(duration)

def reset():

    for t in snake:
        t.goto(1000,1000)

    snake.clear()

    create_head()
    update_score(0,is_reset=True)

def add_food():
    if window._RUNNING:
        global food
        if food == None:
            food = turtle.Turtle()

            food.shape(get_shape())
            food.shapesize(0.5,0.5)
            food.speed(0)
            food.penup()
            food.color(get_color())
            move_food(food)


def move_food(food):
    x = random.randint(-X_RANGE,X_RANGE)
    y = random.randint(-Y_RANGE,Y_RANGE - 2 * TURTLE_SIZE)
    food.goto(x,y)

def eat_food():
    if head.distance(food) < TURTLE_SIZE - 1:
        move_food(food)
        food.shape(get_shape())
        create_segment()
        food.color(get_color())
        update_score(10)


def create_segment():

    global snake

    segment = turtle.Turtle()
    segment.shape(shapes[1])
    segment.speed(0)
    segment.color(food_color)
    segment.penup()

    x,y = get_last_segment_position()
    segment.goto(x,y)


    snake.append(segment)
def get_last_segment_position():
    x = snake[-1].xcor()
    y = snake[-1].ycor()

    if direction == 'up':
        y = y - TURTLE_SIZE
    elif direction == 'down':
        y = y + TURTLE_SIZE
    elif direction == 'left':
        x = x + TURTLE_SIZE
    elif direction == 'right':
        x = x - TURTLE_SIZE

    return (x,y)

def get_color():
    global food_color
    index = random.randint(0, len(colors) - 1)
    color = colors[index]
    food_color = color

    return color

def get_shape():
    index = random.randint(0,len(shapes)-1)
    return shapes[index]


def move():
    if window._RUNNING:

        if direction != 'stop':

            move_segments()
            move_head()

def move_head():
    x = head.xcor()
    y = head.ycor()
    if window._RUNNING:
        if direction == 'up':
            head.sety(y + TURTLE_SIZE)
        elif direction == 'down':
            head.sety(y - TURTLE_SIZE)
        elif direction == 'left':
            head.setx(x - TURTLE_SIZE)
        elif direction == 'right':
            head.setx(x + TURTLE_SIZE)

def move_segments():

    for i in range(len(snake)-1,0,-1):
        x = snake[i-1].xcor()
        y = snake[i-1].ycor()
        snake[i].goto(x,y)


set_screen()
listen_events()
create_head()
create_score()
update_screen()
turtle.mainloop()