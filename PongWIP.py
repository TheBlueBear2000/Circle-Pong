import turtle
import math
import random
from time import sleep

RADIUS = 230                    # Default: 230
PADDLE_SIZE = 90                # Default: 90
PADDLE_SPEED = 2                # Default: 1
BALL_SPEED = 1.6                # Default: 0.8
SCREEN_SIZE = (600,600)         # Default: (600,600)
PADDLE_WIDTH = 30               # Default: 30
BALL_SIZE = 10                  # Default: 10
BACKGROUND_COLOR = 'blue'       # Default: 'blue'
OBJECT_COLOR = 'white'          # Default: 'white'
TPS = 60                        # Default: 60

# POWERUPS

MIN_POWERUP_SIZE = 5
MAX_POWERUP_SIZE = 20
PADDLE_SIZE_MULTIPLIER = 1.2





turtle.mode("logo")
window = turtle.Screen()
window.title("Circle Pong")
window.bgcolor(BACKGROUND_COLOR)
window.setup(width=SCREEN_SIZE[0],height=SCREEN_SIZE[1],startx=0,starty=0)
window.tracer(0,0)

bounces = 0
highscore = 0

class ball(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.sizeOfPen = BALL_SIZE
        self.pensize(self.sizeOfPen)
        self.color(OBJECT_COLOR)
        self.penup()
        self.speed(0)
        self.hideturtle()
        self.ballSpeed = BALL_SPEED
        self.canBounce = True

    def getDistance(self):
        return math.sqrt((self.xcor()**2) + (self.ycor()**2))
    
    def moveBall(self):
        if self.getDistance() < RADIUS-10:
            self.forward(self.ballSpeed)
        else:
            self.forward(RADIUS+1-self.getDistance())
        if (self.getDistance() < RADIUS - 3) and (self.canBounce == False):
            self.canBounce = True
            print("Can bounce")
        self.dot()

    def bounce(self,paddleRotation,paddle):
        movementAngle = 0
        if paddle.moveLeft:
            movementAngle -= 40
        if paddle.moveRight:
            movementAngle += 40

        self.left(180-(2*(paddleRotation - self.heading())) + (random.randint(-5,5)) + movementAngle)
        self.forward(max(BALL_SPEED,1))
        global bounces
        bounces += 1
        print("Score: " + str(bounces))
        self.ballSpeed *= 1.1
        self.canBounce = False
        print("Can't bounce")


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
        self.pencolor(OBJECT_COLOR)
        self.goto(0,0)
        self.setheading(0)
        self.speed(0)
        self.hideturtle()
        self.paddle_size = PADDLE_SIZE
        self.isLarge = False
        self.moveLeft = False
        self.moveRight = False

    def drawPaddle(self):
        angle = self.heading()
        self.forward(RADIUS)
        self.left(90)
        self.pendown()
        self.forward(self.paddle_size/2)
        self.left(180)
        self.forward(self.paddle_size)
        self.penup()
        self.goto(0,0)
        self.setheading(angle)
    
    def turn(self,left,right):
        if left:
            self.left(PADDLE_SPEED)
        if right:
            self.right(PADDLE_SPEED)
    
    def calculateBounceAngle(self):
        angle = self.heading()
        self.forward(RADIUS)
        self.right(90)
        self.forward(self.paddle_size/2)
        self.bounceAngle = theBall.towards(myPaddle) * 2
        self.goto(0,0)
        self.setheading(angle)


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

key_a = WatchedKey('a')
key_d = WatchedKey('d')
key_left = WatchedKey('Right') # Swapped because of starting angle
key_right = WatchedKey('Left')
key_space = WatchedKey('space')
window.listen()


class Powerup(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.size = random.randint(MIN_POWERUP_SIZE,MAX_POWERUP_SIZE)
        self.pensize(1)
        self.penup()
        self.pencolor(OBJECT_COLOR)
        self.goto(0,0)
        self.setheading(random.randint(0,360))
        self.forward(random.randint(20, RADIUS - 20))
        self.speed(0)
        self.hideturtle()
        self.fillcolor(OBJECT_COLOR)

    def draw(self):
        self.forward(self.size/2)
        self.left(90)
        self.begin_fill()
        self.pendown()
        self.forward(self.size/2)
        self.left(90)
        for i in range(3):
            self.forward(self.size)
            self.left(90)
        self.forward(self.size/2)
        self.penup()
        self.end_fill()
        self.right(90)
        self.forward(0-(self.size/2))

class SizePowerup(Powerup):
    def __init__(self):
        Powerup.__init__(self)

    def doPowerup(self,paddle,ball):
        if paddle.isLarge == False:
            paddle.paddle_size *= PADDLE_SIZE_MULTIPLIER







def checkView(paddle,ball):
    ballStartAngle = paddle.heading()

    ballAngle = paddle.towards(ball.pos())
    paddleAngle = paddle.heading()

    if ballAngle < paddle.bounceAngle/2  and  paddleAngle > 360 - (paddle.bounceAngle/2):
        ballAngle += 360
    if paddleAngle < paddle.bounceAngle/2  and  ballAngle > 360 - (paddle.bounceAngle/2):
        paddleAngle += 360

    both = (ballAngle,paddleAngle)

    if max(both) - min(both) <= paddle.bounceAngle:
        return True
    return False


move_left = False
move_right = False

wipeScreen = turtle.Turtle()
wipeScreen.pencolor(BACKGROUND_COLOR)
wipeScreen.pensize(max(SCREEN_SIZE))
wipeScreen.speed(0)
wipeScreen.goto(0,0)
wipeScreen.hideturtle()

def clearScreen(wipeScreen):
    wipeScreen.pencolor(BACKGROUND_COLOR)
    wipeScreen.pensize(max(SCREEN_SIZE))
    wipeScreen.dot()

    wipeScreen.pencolor(OBJECT_COLOR)
    wipeScreen.pensize(RADIUS+2)
    wipeScreen.dot()

    wipeScreen.pencolor(BACKGROUND_COLOR)
    wipeScreen.pensize(RADIUS-2)
    wipeScreen.dot()




pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.goto(0,-30)
pen.pencolor(OBJECT_COLOR)
pen.penup()



def moveLeft():
    global myPaddle
    global playerStarted
    myPaddle.left(PADDLE_SPEED)
    playerStarted = True
def moveRight():
    global myPaddle
    global playerStarted
    myPaddle.right(PADDLE_SPEED)
    playerStarted = True

def moveOtherLeft():
    global myOtherPaddle
    global playerStarted
    myOtherPaddle.left(PADDLE_SPEED)
    playerStarted = True
def moveOtherRight():
    global myOtherPaddle
    global playerStarted
    myOtherPaddle.right(PADDLE_SPEED)
    playerStarted = True

arial = ("Arial Black Regular",60,"normal")

myPaddle = paddle()
myOtherPaddle = paddle()
theBall = ball()

# Calclate Bounce Angle


while True:

    clearScreen(wipeScreen)
    
    bounces = 0
    playerStarted = False

    pen.goto(0,-30)

    myPaddle.setheading(0)
    myPaddle.calculateBounceAngle()
    myOtherPaddle.setheading(180)
    myOtherPaddle.calculateBounceAngle()

    theBall.goto(0,0)
    theBall.setheading(random.randint(0,360))

    print("ball's speed = " + str(theBall.ballSpeed))

    runningGame = True

    #powerup = Powerup()
    #powerup.draw()

    while runningGame:

        sleep(1/TPS)

        theBall.clear()
        myPaddle.clear()
        myOtherPaddle.clear()
        pen.clear()


        
        myPaddle.moveLeft, myPaddle.moveRight, myOtherPaddle.moveLeft, myOtherPaddle.moveRight = False, False, False, False

        if key_a.down:
            moveLeft()
            myPaddle.moveLeft = True
        if key_d.down:
            moveRight()
            myPaddle.moveRight = True
        if key_left.down:
            moveOtherLeft()
            myOtherPaddle.moveLeft = True
        if key_right.down:
            moveOtherRight()
            myOtherPaddle.moveRight = True


        myPaddle.drawPaddle()
        myOtherPaddle.drawPaddle()

        if playerStarted:
            theBall.moveBall()
            pen.write(str(bounces),align="center",font=arial)
        else:
            theBall.drawArrow()

        

        if theBall.getDistance() >= RADIUS:
        
            if checkView(myPaddle,theBall):
                theBall.bounce(myPaddle.heading(),myPaddle)
            elif checkView(myOtherPaddle,theBall):
                theBall.bounce(myOtherPaddle.heading(),myOtherPaddle)
            else:
                print("gameover")
                if bounces > highscore:
                    highscore = bounces
                wipeScreen.clear()
                pen.undo()
                pen.penup()
                pen.color(OBJECT_COLOR)
                pen.goto(0,50)
                pen.write("Gameover!",align="center",font=("Arial Black Regular",100,"normal"))
                pen.goto(0,-30)
                pen.write("Score: {}".format(bounces),align="center",font=arial)
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
                    


        
