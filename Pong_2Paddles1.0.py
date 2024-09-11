import turtle
import math
import random

RADIUS = 230                    # Default: 230
PADDLE_SIZE = 90                # Default: 90
PADDLE_SPEED = 14               # Default: 14
BALL_SPEED = 0.8                # Default: 1.0 
SCREEN_SIZE = (600,600)         # Default: (600,600)
PADDLE_WIDTH = 30               # Default: 30
BALL_SIZE = 10                  # Default: 10
BACKGROUND_COLOR = 'blue'       # Default: 'blue'
OBJECT_COLOR = 'white'          # Default: 'white'






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

    def getDistance(self):
        return(math.sqrt((self.xcor()**2) + (self.ycor()**2)))
    
    def moveBall(self):
        if self.getDistance() < RADIUS-10:
            self.forward(self.ballSpeed)
        else:
            self.forward(RADIUS+1-self.getDistance())
        self.dot()

    def bounce(self,paddleRotation):
        self.left(180-(2*(paddleRotation - self.heading())) + (random.randint(-5,5)))
        self.forward(max(BALL_SPEED,1))
        global bounces
        bounces += 1
        print("Score: " + str(bounces))
        self.ballSpeed *= 1.1


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



def checkView(paddle,ball):
    ballStartAngle = paddle.heading()

    ballAngle = paddle.towards(ball.pos())
    paddleAngle = paddle.heading()

    if ballAngle < BOUNCE_ANGLE/2  and  paddleAngle > 360 - (BOUNCE_ANGLE/2):
        ballAngle += 360
    if paddleAngle < BOUNCE_ANGLE/2  and  ballAngle > 360 - (BOUNCE_ANGLE/2):
        paddleAngle += 360

    both = (ballAngle,paddleAngle)
    #print(max(both) - min(both))

    #if paddleAngle + 5 <= 360 and paddleAngle - 5 >= 0:
    #    if (paddleAngle - 5 < ballAngle < paddleAngle + 5):
    #        print()
    #if paddleAngle + 5 > 360:


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




pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.goto(0,-30)
pen.pencolor("white")
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
myPaddle.forward(RADIUS)
myPaddle.right(90)
myPaddle.forward(PADDLE_SIZE/2)
BOUNCE_ANGLE = theBall.towards(myPaddle) * 2
myPaddle.goto(0,0)
myPaddle.setheading(0)



runningGame = True
playerStarted = False

def main():

    clearScreen(wipeScreen)
    
    global bounces
    bounces = 0

    global playerStarted
    playerStarted = False

    pen.goto(0,-30)

    myPaddle.setheading(0)
    myOtherPaddle.setheading(180)

    theBall.goto(0,0)
    theBall.setheading(random.randint(0,360))

    print("ball's speed = " + str(theBall.ballSpeed))

    while runningGame:

        theBall.clear()
        myPaddle.clear()
        myOtherPaddle.clear()
        pen.clear()

        window.onkeypress(moveLeft,"Left")
        window.onkeypress(moveRight,"Right")

        window.onkeypress(moveOtherLeft,"d")
        window.onkeypress(moveOtherRight,"a")

        window.listen()


        myPaddle.drawPaddle()
        myOtherPaddle.drawPaddle()

        if theBall.getDistance() >= RADIUS:
            if checkView(myPaddle,theBall):
                theBall.bounce(myPaddle.heading())
            elif checkView(myOtherPaddle,theBall):
                theBall.bounce(myOtherPaddle.heading())
            else:
                print("gameover")
                global highscore
                if bounces > highscore:
                    highscore = bounces
                wipeScreen.clear()

                while True:
                    pen.undo()
                    pen.penup()
                    pen.color("white")
                    pen.goto(0,50)
                    pen.write("Gameover!",align="center",font=("Arial Black Regular",100,"normal"))
                    pen.goto(0,-30)
                    pen.write("Score: {}".format(bounces),align="center",font=arial)
                    pen.goto(0,-110)
                    pen.write("Highscore: {}".format(highscore),align="center",font=arial)
                    pen.goto(0,-180)
                    pen.write("(Press space to continue)",align="center",font=("Arial Black Regular",30,"normal"))
                    pen.goto(0,-30)

                    window.onkeypress(main,"space")
                    window.listen()
                    theBall.ballSpeed = BALL_SPEED
                    theBall.ballSpeed *= 2
        
        if playerStarted:
            theBall.moveBall()
            pen.write(str(bounces),align="center",font=arial)
        else:
            theBall.drawArrow()

        window.update()

main()

        
