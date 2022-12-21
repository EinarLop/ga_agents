import random
import math
import pyglet
from pyglet import shapes

generation_size = 20
gens_size = 500


batch = pyglet.graphics.Batch()


class Ball:
    def __init__(self):
        self.movements = []
        self.agent = shapes.Circle(200, 200, 5, color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)), batch=batch)
        self.fitness = 0
        self.reward = False
    
    def create_gens(self, parentOne = [], parentTwo = []):
        if len(parentOne) == 0:
            self.movements = [[random.randint(-1,1), random.randint(-1,1)] for _ in range(gens_size)]
            # print("first gen", self.movements)

        else:
            crossPoint = random.randint(0, gens_size)
            self.movements = parentOne[0:crossPoint] + parentTwo[crossPoint:]
            # print("new gens", self.movements)


    def move(self, frame):
        self.agent.x += self.movements[frame][0]
        self.agent.y += self.movements[frame][1]
    
    def calculate_fitness(self):
        self.fitness += math.dist([self.agent.x,self.agent.y], [340,50]) * 150

    def mutate(self):
        for _ in range(random.randint(0, 10)):
            self.movements[random.randint(0, gens_size)-1] = [random.randint(-5,5), random.randint(-5,5)] 

    def star_collision(self):
        distance = math.dist([self.agent.x,self.agent.y], [350,350])
        if distance <= 10 and not self.reward:

            self.fitness -= 100
            self.reward = True
        elif distance>10 and not self.reward:
    
            self.fitness = self.fitness - (900 - distance)
            
            
        