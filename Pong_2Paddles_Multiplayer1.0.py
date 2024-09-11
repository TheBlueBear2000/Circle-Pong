import turtle
import math
import random

RADIUS = 230                    # Default: 230
PADDLE_SIZE = 90                # Default: 90
PADDLE_SPEED = 1                # Default: 1
BALL_SPEED = 0.8                # Default: 0.8
SCREEN_SIZE = (600,600)         # Default: (600,600)
PADDLE_WIDTH = 30               # Default: 30
BALL_SIZE = 10                  # Default: 10
BACKGROUND_COLOR = 'blue'       # Default: 'blue'
OBJECT_COLOR = 'white'          # Default: 'white'
BARRIER_ROTATION = 0            # Default: 0







turtle.mode("logo")
window = turtle.Screen()
window.title("Circle Pong")
window.bgcolor('blue')
window.setup(width=SCREEN_SIZE[0],height=SCREEN_SIZE[1],startx=0,starty=0)
window.tracer(0,0)

bounces = 0
highscore = 0

class ball(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.sizeOfPen = BALL_SIZE
        self.pensize(self.sizeOfPen)
        self.color("white")
        self.penup()
        self.speed(0)
        self.hideturtle()
        self.ballSpeed = BALL_SPEED
        self.lastBounce = 0

    def getDistance(self):
        return(math.sqrt((self.xcor()**2) + (self.ycor()**2)))
    
    def moveBall(self):
        if self.getDistance() < RADIUS-10:
            self.forward(self.ballSpeed)
        else:
            self.forward(RADIUS+1-self.getDistance())
        self.dot()

    def bounce(self,paddleRotation,clockwise):
        if self.lastBounce >= 10:
            self.left(180-(2*(paddleRotation - self.heading())) + (random.randint(-5,5)))
            if clockwise == True:
                self.left(10)
            elif clockwise == False:
                self.right(10)
            self.forward(max(BALL_SPEED,1))
            global bounces
            bounces += 1
            print("Score: " + str(bounces))
            self.ballSpeed *= 1.1
        else:
            self.setheading(self.towards(0, 0))
            self.left(random.randint(-50, 50))
            self.forward(max(BALL_SPEED,1))
            


    def drawArrow(self):
        angle = self.heading()
        self.pensize(self.sizeOfPen/2)
        self.pendown()
        self.forward(RADIUS/3)
        self.left(135)
        self.forward(RADIUS/15)
        self.left(180)
        self.forward(RADIUS/15)
        self.left(270)
        self.forward(RADIUS/15)
        self.penup()
        self.goto(0,0)
        self.setheading(angle)
        self.pensize(self.sizeOfPen)
        self.dot()


class paddle(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.pensize(PADDLE_WIDTH)
        self.penup()
        self.pencolor("white")
        self.goto(0,0)
        self.setheading(0)
        self.speed(0)
        self.hideturtle()
        self.clockwise = None

    def drawPaddle(self):
        angle = self.heading()
        self.forward(RADIUS)
        self.left(90)
        self.pendown()
        self.forward(PADDLE_SIZE/2)
        self.left(180)
        self.forward(PADDLE_SIZE)
        self.penup()
        self.goto(0,0)
        self.setheading(angle)
    
    def turn(self,left,right):
        if left:
            self.left(PADDLE_SPEED)
        if right:
            self.right(PADDLE_SPEED)


class WatchedKey:
    def __init__(self, key):
        self.key = key
        self.down = False
        window.onkeypress(self.press, key)
        window.onkeyrelease(self.release, key)

    def press(self):
        self.down = True

    def release(self):
        self.down = False

key_w = WatchedKey('w')
key_s = WatchedKey('s')
key_up = WatchedKey('Up') # Swapped because of starting angle
key_down = WatchedKey('Down')
key_space = WatchedKey('space')
window.listen()



def checkView(paddle,ball):
    ballStartAngle = paddle.heading()

    ballAngle = paddle.towards(ball.pos())
    paddleAngle = paddle.heading()

    if ballAngle < BOUNCE_ANGLE/2  and  paddleAngle > 360 - (BOUNCE_ANGLE/2):
        ballAngle += 360
    if paddleAngle < BOUNCE_ANGLE/2  and  ballAngle > 360 - (BOUNCE_ANGLE/2):
        paddleAngle += 360

    both = (ballAngle,paddleAngle)

    if max(both) - min(both) <= BOUNCE_ANGLE:
        return True
    return False


move_left = False
move_right = False

wipeScreen = turtle.Turtle()
wipeScreen.pencolor("blue")
wipeScreen.pensize(max(SCREEN_SIZE))
wipeScreen.speed(0)
wipeScreen.goto(0,0)
wipeScreen.hideturtle()

def clearScreen(wipeScreen):
    wipeScreen.pencolor("blue")
    wipeScreen.pensize(max(SCREEN_SIZE))
    wipeScreen.dot()

    wipeScreen.pencolor("white")
    wipeScreen.pensize(RADIUS+2)
    wipeScreen.dot()

    wipeScreen.pencolor("blue")
    wipeScreen.pensize(RADIUS-2)
    wipeScreen.dot()
    
    wipeScreen.penup()
    wipeScreen.pencolor("white")
    wipeScreen.pensize(5)
    wipeScreen.right(BARRIER_ROTATION)
    wipeScreen.forward(RADIUS)
    wipeScreen.pendown()
    wipeScreen.backward(RADIUS*2)
    wipeScreen.goto(0,0)
    wipeScreen.left(BARRIER_ROTATION)
    
    wipeScreen.pencolor("blue")
    wipeScreen.pensize(40)
    wipeScreen.dot()




pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.goto(0,-30)
pen.pencolor("white")
pen.penup()



def moveLeft():
    global myPaddle
    global playerStarted
    if myPaddle.heading() - PADDLE_SPEED < 360 and myPaddle.heading() - PADDLE_SPEED >= 180:
        myPaddle.left(PADDLE_SPEED)
    playerStarted = True
def moveRight():
    global myPaddle
    global playerStarted
    if myPaddle.heading() + PADDLE_SPEED < 360 and myPaddle.heading() + PADDLE_SPEED >= 180:
        myPaddle.right(PADDLE_SPEED)
    playerStarted = True

def moveOtherLeft():
    global myOtherPaddle
    global playerStarted
    if myOtherPaddle.heading() - PADDLE_SPEED >= 0 and myOtherPaddle.heading() - PADDLE_SPEED < 180:
        myOtherPaddle.left(PADDLE_SPEED)
    playerStarted = True
def moveOtherRight():
    global myOtherPaddle
    global playerStarted
    if myOtherPaddle.heading() + PADDLE_SPEED >= 0 and myOtherPaddle.heading() + PADDLE_SPEED < 180:
        myOtherPaddle.right(PADDLE_SPEED)
    playerStarted = True

arial = ("Arial Black Regular",60,"normal")

myPaddle = paddle()
myOtherPaddle = paddle()
theBall = ball()

# Calclate Bounce Angle
myPaddle.forward(RADIUS)
myPaddle.right(90)
myPaddle.forward(PADDLE_SIZE/2)
BOUNCE_ANGLE = theBall.towards(myPaddle) * 2
myPaddle.goto(0,0)
myPaddle.setheading(0)

while True:

    clearScreen(wipeScreen)
    
    bounces = 0
    playerStarted = False

    pen.goto(0,-30)

    myPaddle.setheading(270)
    myOtherPaddle.setheading(90)

    theBall.goto(0,0)
    theBall.setheading(random.randint(0,360))
    theBall.lastBounce = 0

    print("ball's speed = " + str(theBall.ballSpeed))

    runningGame = True

    while runningGame:
        
        if theBall.lastBounce < 10:
            theBall.lastBounce += 1

        theBall.clear()
        myPaddle.clear()
        myOtherPaddle.clear()
        pen.clear()

        myPaddle.clockwise = None
        myOtherPaddle.clockwise = None

        if key_s.down:
            moveLeft()
            myPaddle.clockwise = False
        if key_w.down:
            moveRight()
            myPaddle.clockwise = True
        if key_up.down:
            moveOtherLeft()
            myOtherPaddle.clockwise = True
        if key_down.down:
            moveOtherRight()
            myOtherPaddle.clockwise = False


        myPaddle.drawPaddle()
        myOtherPaddle.drawPaddle()

        if playerStarted:
            theBall.moveBall()
            pen.write(str(bounces),align="center",font=arial)
        else:
            theBall.drawArrow()

        

        if theBall.getDistance() >= RADIUS:
            if checkView(myPaddle,theBall):
                theBall.bounce(myPaddle.heading(), myPaddle.clockwise)
            elif checkView(myOtherPaddle,theBall):
                theBall.bounce(myOtherPaddle.heading(), myOtherPaddle.clockwise)
            else:
                print("gameover")
                if bounces > highscore:
                    highscore = bounces
                if theBall.xcor() <= 0:
                    winner = "Right"
                else:
                    winner = "Left"
                wipeScreen.clear()
                pen.undo()
                pen.penup()
                pen.color("white")
                pen.goto(0,50)
                pen.write(f"{winner} won!",align="center",font=("Arial Black Regular",100,"normal"))
                pen.goto(0,-30)
                pen.write("Bounces: {}".format(bounces),align="center",font=arial)
                pen.goto(0,-110)
                pen.write("Highscore: {}".format(highscore),align="center",font=arial)
                pen.goto(0,-180)
                pen.write("(Press space to continue)",align="center",font=("Arial Black Regular",30,"normal"))
                pen.goto(0,-30)

                # figure break method
                theBall.ballSpeed = BALL_SPEED
                
                while key_space.down == False: 
                    window.listen()
                    window.update()
                    
                runningGame = False
                break
        window.update()
                    


        
