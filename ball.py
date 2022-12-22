import random
import math
import pyglet
from pyglet import shapes
import numpy as np

generation_size = 100
gens_size = 100
number_generations = 10000

batch = pyglet.graphics.Batch()

stars = [ shapes.Star(100, 350, 5, 10, num_spikes=5, color=(255, 255, 0), batch=batch), shapes.Star(50, 100, 5, 10, num_spikes=5, color=(255, 255, 0), batch=batch), shapes.Star(380, 350, 5, 10, num_spikes=5, color=(255, 255, 0), batch=batch)]
target = shapes.Rectangle(375, 190, 20, 20, color=(255, 22, 20), batch=batch)



class Ball:
    def __init__(self):
        self.movements = []
        self.agent = shapes.Circle(-5, 200, 5,
                                   color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                   batch=batch)
        self.fitness = 0
        self.rewards = [False,False,False, False]
        self.target = False

    def create_gens(self, parentOne=[], parentTwo=[]):
        if len(parentOne) == 0:
            self.movements = [[0,0] for _ in range(gens_size)]
            # self.movements = [[-11, 19], [20, 20], [20, 15], [18, 20], [17, 17], [17, 18], [13, 20], [5, 16], [-4, 20], [17, -14], [18, -8], [15, -18], [3, -17], [16, -18], [13, -4], [16, -17], [15, -9], [9, -18], [17, 12], [-12, 13], [8, -3], [2, -10], [-18, -19], [9, 19], [20, 19], [9, -5], [8, 13], [18, 18], [-11, 3], [-4, 13], [0, -19], [-15, 11], [2, -2], [12, 20], [-12, -3], [11, -12], [19, -8], [11, -9], [-6, -1], [17, 19], [-15, 18], [14, 8], [20, 19], [18, 9], [17, -17], [10, 16], [-19, -20], [-20, -14], [-19, -18], [-20, -10], [-19, -17], [-20, -20], [-17, -18], [-20, -19], [-20, -9], [-17, -17], [-20, -17], [-20, -17], [-19, 2], [-20, -16], [-19, -6], [-4, -16], [-6, 7], [-15, -18], [5, -9], [-6, 0], [17, -1], [-14, -2], [12, 16], [16, 13], [7, -10], [14, 13], [18, -6], [20, 16], [10, 15], [11, -17], [-1, 4], [13, 18], [5, -9], [14, 0], [16, 20], [11, -17], [15, 17], [-5, 3], [16, -5], [13, 19], [9, 18], [13, 0], [16, -5], [15, 8], [13, 15], [-6, -2], [15, 6], [11, 16], [13, -3], [19, -20], [-3, 7], [-7, -13], [-3, -12], [15, -11]]
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
                self.fitness += agentStarDistance*0.025
            if not self.target:
                self.fitness += agenetTargetDistance*0.1


