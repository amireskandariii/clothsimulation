import numpy as np
class Spring:
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2
		self.rest_length = np.linalg.norm(p1.pos - p2.pos)
		self.k = 0.8		# spring constant
		self.c = 0.02		# damping constant

	def apply_force(self):
		# compute spring force
		direction = self.p2.pos - self.p1.pos
		# print('direction', direction)
		current_length = np.linalg.norm(direction)
		displacement = current_length - self.rest_length
		spring_force = self.k * displacement * direction / current_length

		# compute damping force
		damping_force_p1 = -self.c * self.p1.velocity
		damping_force_p2 = -self.c * self.p2.velocity

		# apply forces to particles
		self.p1.add_force(spring_force + damping_force_p1)
		self.p2.add_force(-spring_force + damping_force_p2)