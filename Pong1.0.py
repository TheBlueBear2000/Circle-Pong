import turtle
import math
import random

RADIUS = 300
PADDLE_WIDTH = 30



window = turtle.Screen()
window.title("Circle Pong")
window.bgcolor('blue')
window.setup(width=600,height=600)
window.tracer()


class ball(turtle.Turtle):
    def __init__(self):
        self = turtle.Turtle()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0,0)
        self.degrees(random.randint(0,360))

    def getDistance(self):
        return(math.sqrt((self.pos[0]**2) + (self.pos[1]**2)))
    
    def moveBall(self):
        self.forward(3)



class paddle(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.pencolor("white")
        self.goto(0,0)
        self.degrees(0)

    def drawPaddle(self):
        angle = self.degrees
        self.forward(RADIUS)
        self.degrees += 90
        self.pendown()
        self.forward(PADDLE_WIDTH/2)
        self.degrees += 180
        self.forward(PADDLE_WIDTH)
        self.goto(0,0)
        self.degrees=(angle)

myPaddle = paddle()

runningGame = True
while runningGame:
    turtle.clear()

    
