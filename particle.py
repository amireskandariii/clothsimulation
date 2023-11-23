import numpy as np
dt = 0.33

class Particle:
	def __init__(self, x, y):
		self.pos = np.array([x, y])
		self.mass = 1
		self.force = np.array([0, 0])
		self.velocity = 0
		self.acc = 0

	def update(self):
		self.acc = self.force / self.mass
		self.velocity = self.velocity + self.acc * dt
		self.pos = self.pos + self.velocity * dt
		if self.pos[1] > 1.15:   # so that there's a floor somehow
			self.pos[1] = 1.15

	def add_force(self, f):
		self.force = self.force + f
		