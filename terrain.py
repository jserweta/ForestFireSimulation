import math
import random


class TerrainChunk():
    # biome = 'forest'
    fireState = 0
    # road = False
    locX: int
    locY: int
    fire_risk: int
    humidity: int
    temperature: int
    other_danger: int  # np. gazy wydzielane podczas pożaru, zanieczyszczenia, substancje chemiczne

    # fuel = 100000.0

    def __init__(self, x: int, y: int):
        self.locX = x
        self.locY = y
        self.other_danger = random.randint(0, 2)
        self.temperature = random.randint(0,2)
        self.humidity = random.randint(0,2)
        self.fire_risk = self.count_fire_risk()

    def count_fire_risk(self):
        risk_factors = [self.temperature, self.humidity, self.other_danger]
        return int(round(sum(risk_factors) / 3, 0))