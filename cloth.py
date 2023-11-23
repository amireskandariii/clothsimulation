import math
import numpy as np
import particle as P
import spring as S

class Cloth:
	def __init__(self):
		x_offset = 0.05
		y_offset = 0.05
		x_spacing = 0.05
		y_spacing = 0.05
		self.num_iterations = 2
		self.points = []
		self.springs = []

		num_x_points = self.num_x_points = 20
		num_y_points = self.num_y_points = 12

		y = y_offset
		for i in range(0, num_y_points):
			self.points.append([])
			x = x_offset
			for j in range(0, num_x_points):
				point = P.Particle(x, y)
				print('x', x, 'y', y)
				self.points[i].append(point)
				if i > 0:
					spring = S.Spring(self.points[i - 1][j], self.points[i][j])
					self.springs.append(spring)
				if j > 0:
					spring = S.Spring(self.points[i][j - 1], self.points[i][j])
					self.springs.append(spring)
				x = x + x_spacing
			y = y + y_spacing


		# pin the top right, top middle, and top left.
		self.points[0][0].mass = float('inf')
		self.points[0][math.floor(num_x_points / 2)].mass = float('inf')
		self.points[0][num_x_points - 1].mass = float('inf')
		self.num_constraints = len(self.springs)

	def update(self):
		num_x = self.num_x_points
		num_y = self.num_y_points
		num_c = self.num_constraints
		num_i = self.num_iterations

		for i in range(0, num_y):
			for j in range(0, num_x):
				self.points[i][j].force = np.array([0, 0.005])

		for i in range(0, num_i):
			for j in range(0, num_c):
				self.springs[j].apply_force()


		for i in range(0, num_y):
			for j in range(0, num_x):
				self.points[i][j].update()

	def getClosestPoint(self, pos):
		min_dist = 1
		min_point = None
		num_x = self.num_x_points
		num_y = self.num_y_points
		for i in range(0, num_y):
			for j in range(0, num_x):
				dist = np.linalg.norm(pos - self.points[i][j].pos)
				if dist < min_dist:
					min_dist = dist
					min_point = self.points[i][j]
		return min_point