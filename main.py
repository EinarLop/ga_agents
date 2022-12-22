import pyglet
from pyglet import shapes
import random
from ball import *
import matplotlib.pyplot as plt


window = pyglet.window.Window(400, 400)
speed = 0.1

balls = []
frame = 0
fitness_history = []
currentGenNum = 0




numGenLabel = pyglet.text.Label("Generation: " + str(currentGenNum),
                                font_size=10,
                                color=(255, 255, 255, 255),
                                x=150,
                                y=380)

for _ in range(generation_size):
    currentBall = Ball()
    currentBall.create_gens()
    balls.append(currentBall)


def init_gen(parentOne, parentTwo):
    global balls
    global frame
    balls = []
    for _ in range(generation_size):
        currentBall = Ball()
        currentBall.create_gens(parentOne, parentTwo)

        currentBall.mutate()
        balls.append(currentBall)
    frame = 0
    pyglet.clock.schedule_interval(life, speed)


def select_parents():
    for ball in balls:
        ball.calculate_fitness()
    balls.sort(key=lambda x: x.fitness, reverse=False)
    return balls[0], balls[1]


def life(dt):
    global frame
    global currentGenNum
    global numGenLabel
    parentOne, parentTwo = None, None

    for ball in balls:
        ball.agent.x += ball.movements[frame][0]
        ball.agent.y += ball.movements[frame][1]
        ball.star_collision()

    # if currentGenNum > number_generations:
    #     pyglet.clock.unschedule(life)
    if frame >= gens_size-1:
        pyglet.clock.unschedule(life)
        if currentGenNum < number_generations:
            parentOne, parentTwo = select_parents()
            currentFitness = (parentOne.fitness + parentTwo.fitness) / 2
            fitness_history.append(currentFitness)
            init_gen(parentOne.movements, parentTwo.movements)
            numGenLabel.text = "Generation: " + str(currentGenNum)
            currentGenNum += 1
        else:
            print(balls[0].movements)
    frame += 1

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

@window.event
def on_draw():
    window.clear()
    batch.draw()
    numGenLabel.draw()



pyglet.clock.schedule_interval(life, speed)

pyglet.app.run()
plt.plot(fitness_history)
plt.show()
