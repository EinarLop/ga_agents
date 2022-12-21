import pyglet
from pyglet import shapes
import random
from ball import *

generation_size = 20
gens_size = 500

window = pyglet.window.Window(400,400)
target = shapes.Rectangle(340, 50, 20, 20, color=(255, 22, 20), batch=batch)

balls = []
frame = 0
fitness_history = []

label = pyglet.text.Label("",
                          font_name='Times New Roman',multiline=True, width =150, height=400,
                          font_size=10,color=(255, 255,255,255),
                          x=0, y=390)  
star = shapes.Star(350, 350, 5, 10, num_spikes=5, color=(255, 255, 0), batch=batch)

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
        if random.random() > 0.85:
            currentBall.mutate()
        balls.append(currentBall)
    frame = 0

    
    pyglet.clock.schedule_interval(life, 0.001)


def select_parents():
    for ball in balls:
        ball.calculate_fitness()
    balls.sort(key=lambda x: x.fitness, reverse=False)
    return balls[0] ,balls[1]
    

def life(dt):
    
    global frame
    

    for ball in balls:
        ball.agent.x += ball.movements[frame][0]
        ball.agent.y += ball.movements[frame][1]
        ball.star_collision()
   
    if frame >= gens_size-1:
        pyglet.clock.unschedule(life)
        parentOne, parentTwo = select_parents()
        init_gen(parentOne.movements,parentTwo.movements)
        fitness_history.append((parentOne.fitness+parentTwo.fitness)/2)
    global label

    label.text = "Best parent fitness history: " + ' '.join(str(v) for v in fitness_history) 
    

   
    frame += 1






@window.event
def on_draw():
    window.clear()
    batch.draw()
    label.draw()

pyglet.clock.schedule_interval(life, 0.001)

pyglet.app.run()
