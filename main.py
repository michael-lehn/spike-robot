from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import wait

hub = PrimeHub()

m_left = Motor(Port.A, positive_direction=Direction.CLOCKWISE)
m_right = Motor(Port.E, positive_direction=Direction.COUNTERCLOCKWISE)

sensors = [
    ColorSensor(Port.C),   # Sensor 0 = Front
    ColorSensor(Port.D),   # Sensor 1 = Middle
    ColorSensor(Port.F),   # Sensor 2 = Back
]

color = [None, None, None] # "white" or "black"
reflect = [0, 0, 0]
BLACK_THRESHOLD = 45

def calibrate_color(n=10, delay_ms=50):
    global BLACK_THRESHOLD

    hub.display.text("C")
    # Weiß messen
    w = [0, 0, 0]
    for _ in range(n):
        for i, s in enumerate(sensors):
            w[i] += s.reflection()
        wait(delay_ms)
    w = [v // n for v in w]
    w_mean = sum(w) // 3

    hub.display.text("BLACK")
    wait(500)  # kurzer Hinweis

    # Schwarz messen
    b = [0, 0, 0]
    for _ in range(n):
        for i, s in enumerate(sensors):
            b[i] += s.reflection()
        wait(delay_ms)
    b = [v // n for v in b]
    b_mean = sum(b) // 3

    BLACK_THRESHOLD = (w_mean + b_mean) // 2
    hub.display.number(BLACK_THRESHOLD)
    wait(500)

def read_colors():
    global color, reflect
    for i, s in enumerate(sensors):
        r = s.reflection()
        reflect[i] = r
        color[i] = "white" if r >= BLACK_THRESHOLD else "black"
    
    s = 0;
    if color[0] == "black":
        s += 1;
    if color[1] == "black":
        s += 2;
    if color[2] == "black":
        s += 4;
    hub.display.text(str(s))

def step_finish():
    while not (m_left.done() and m_right.done()):
        wait(1)
    while not (m_left.done() and m_right.done()):
        wait(1)

def step_forward(speed=500, angle=360):
    m_left.run_angle(speed, angle, wait=False)
    m_right.run_angle(speed, angle, wait=False)
    step_finish()

def step_rotation(speed=500, angle=10):
    m_left.run_angle(speed, angle, wait=False)
    m_right.run_angle(speed, -angle, wait=False)
    step_finish()

def forward(speed):
    m_left.run(speed)
    m_right.run(speed)

def stop():
    m_left.stop()
    m_right.stop()

# calibrate_color()

best_val = reflect[0]
best_degree = 0

def align_search(n, degree):
    global best_val, best_degree

    read_colors()
    for d in range(1, n+1):
        step_rotation(50, degree)
        read_colors()
        print(f"d = {d}, degree={degree}, reflect = {reflect}")
        if reflect[0] > 80:
            continue
        if reflect[0] < best_val:
            best_val = reflect[0]
            best_degree = d * degree
        if reflect[0] > 50:
            continue
        if reflect[0] <= reflect[1]:
            return True
    step_rotation(50, n * -degree)
    return False

align_last = 1
def align():
    global align_last, best_val, best_degree
    read_colors()
    print(f"align: {reflect} align_last = {align_last}")
    best_val = reflect[0]
    best_degree = 0

    n = 15;
    degree = 20
    if align_last > 0:
        print(f"case1: align_last = {align_last}")
        if align_search(n, degree):
            align_last = 1
            print(f"now: align_last = {align_last}")
            return
        elif align_search(n, -degree):
            align_last = -1
            print(f"now: align_last = {align_last}")
            return
    elif align_last < 0:
        print(f"case2: align_last = {align_last}")
        if align_search(n, -degree):
            align_last = -1
            print(f"now: align_last = {align_last}")
            return
        elif align_search(n, degree):
            align_last = 1
            print(f"now: align_last = {align_last}")
            return
    else:
        align_last = 0
        print("didn't work last time. But I like you never give up")

    print(f"using best guess {best_degree}")
    if best_degree > 0:
        align_last = 1
    elif best_degree < 0:
        align_last = -1
    step_rotation(50, best_degree)


forward(50);
while True:
    read_colors()
    print(f"reflect = {reflect}")
    if reflect[0] > reflect[1]:
        stop()
        align()
        forward(50);
    wait(10)


# while True:
#     read_colors()
#     print(reflect)
#     wait(10)
#     step_rotation(50, 10)


#    if color[1] == "black":
#        if color[0] == "black":
#            stop()
#            step_rotation(50, 90)
#        elif color[2] == "black":
#            stop()
#            step_rotation(50, -90)
#        else:
#            forward(50)
#    elif color[1] == "white":
#        if color[0] == "black":
#            stop()
#            step_rotation(50, 90)
#        elif color[2] == "black":
#            stop()
#            step_rotation(50, -90)
#        else:
#            forward(10);
#
hub.display.text("OUT")

