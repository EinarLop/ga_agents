import random
import math
import pyglet
from pyglet import shapes
import numpy as np

generation_size = 100
gens_size = 100
number_generations = 10000

batch = pyglet.graphics.Batch()

stars = [shapes.Star(100, 50, 5, 10, num_spikes=5, color=(255, 255, 0), batch=batch), shapes.Star(250, 300, 5, 10, num_spikes=5, color=(255, 255, 0), batch=batch)]
target = shapes.Rectangle(375, 190, 20, 20, color=(255, 22, 20), batch=batch)



class Ball:
    def __init__(self):
        self.movements = []
        self.agent = shapes.Circle(-5, 200, 5,
                                   color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                   batch=batch)
        self.fitness = 0
        self.rewards = [False, False]
        self.target = False

    def create_gens(self, parentOne=[], parentTwo=[]):
        if len(parentOne) == 0:
            self.movements = [[0,0] for _ in range(gens_size)]
            # print("first gen", self.movements)

        else:
            crossPoint = random.randint(0, gens_size)
            self.movements = parentOne[0:crossPoint] + parentTwo[crossPoint:]
            # print("new gens", self.movements)

    def move(self, frame):
        self.agent.x += self.movements[frame][0]
        self.agent.y += self.movements[frame][1]

    def calculate_fitness(self):
        # self.fitness += (-10 * math.dist([self.agent.x, self.agent.y], [target.x, target.y])) + (100*len(np.where(self.rewards == False)))
        self.fitness += math.dist([self.agent.x, self.agent.y], [target.x, target.y])
        pass

    def mutate(self):
        self.movements[random.randint(0, gens_size) - 1] = [random.randint(-20, 20), random.randint(-20, 20)]

    def star_collision(self):
        for i, star in enumerate(stars):
            agenetTargetDistance = math.dist([self.agent.x, self.agent.y], [star.x, star.y])
            starTargetDistance = math.dist([star.x, star.y], [target.x, target.y])
            agentStarDistance = math.dist([star.x, star.y], [self.agent.x, self.agent.y])
            if agentStarDistance <= 10 and not self.rewards[i]:
                self.fitness -= 250
                self.rewards[i] = True
            if agenetTargetDistance <= 10 and not self.target:
                self.fitness -= 500
                self.target = True
            if not self.rewards[i]:
                self.fitness += agentStarDistance*0.05
            if not self.target:
                self.fitness += agenetTargetDistance*0.1


