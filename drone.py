import numpy as np
from numpy.random import rand
from math import ceil, sin, cos, sqrt
from nn import Network


class Drone:
    def __init__(self, size=40):
        self.size = size
        self.position = np.array([0.5, 0.5])
        self.velocity = np.array([0.0, 0.0])
        self.forces = np.array([0.0, 0.0])

        self.torque = 0
        self.angle = 0
        self.angular_momentum = 0.0

        # initialize thrusters
        self.br_thr = 0.4
        self.bl_thr = 0.4
        # print(
        #    rand(4, 10), rand(10,), rand(10, 10), rand(10,), rand(10, 2), rand(2,),
        # )
        self.nn = Network(
            2 * rand(6, 10) - 1,
            2 * rand(10,) - 1,
            2 * rand(10, 10) - 1,
            2 * rand(10,) - 1,
            2 * rand(10, 2) - 1,
            2 * rand(2,) - 1,
        )

    def update(self, dt):
        self.update_thrusters()
        self.compute_forces()

        self.br_thr += dt * 0.11
        self.bl_thr += dt * 0.1

        self.velocity += dt * (self.forces + np.array([0.0, 1]))  # forces + gravity
        self.position += self.velocity * dt

        self.angular_momentum += self.torque * dt
        self.angle += self.angular_momentum * dt

    def compute_forces(self):
        # compute linear force
        thruster_orientation = np.array([sin(self.angle), -cos(self.angle)])

        bl_thrust = self.bl_thr * thruster_orientation
        br_thrust = self.br_thr * thruster_orientation

        self.forces = bl_thrust + br_thrust

        # compute torque r x F = r*F*sin(theta) =  +- size* sqrt(2) * sqrt(2) / 2 * thrust
        bl_torque = self.bl_thr * self.size
        br_torque = -self.br_thr * self.size

        self.torque = bl_torque + br_torque

    def update_thrusters(self):
        self.br_thr, self.bl_thr = self.nn.forward_pass(
            np.array(
                [
                    self.position[0],
                    self.position[1],
                    self.velocity[0],
                    self.velocity[1],
                    self.angle,
                    self.angular_momentum,
                ]
            )
        )
