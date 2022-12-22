import pyglet
from pyglet import shapes
import random
from ball import *
import matplotlib.pyplot as plt


window = pyglet.window.Window(400, 600)


balls = []
frame = 0
fitness_history = []
currentGenNum = 0


graph = pyglet.graphics.Batch()
points = []

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
    pyglet.clock.schedule_interval(life, 0.01)


def select_parents():
    for ball in balls:
        ball.calculate_fitness()
    balls.sort(key=lambda x: x.fitness, reverse=False)
    return balls[0], balls[1]


def life(dt):
    global frame
    global currentGenNum
    global numGenLabel

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
            points.append(shapes.Circle(5+currentGenNum, 400+ currentFitness, 1, color=(255, 0, 0), batch=graph))
            print("Current fitness", parentOne.movements)
            fitness_history.append(currentFitness)
            init_gen(parentOne.movements, parentTwo.movements)
            numGenLabel.text = "Generation: " + str(currentGenNum)
            currentGenNum += 1
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
    graph.draw()


pyglet.clock.schedule_interval(life, 0.01)

pyglet.app.run()
plt.plot(fitness_history)
plt.show()
