import numpy as np
from numpy.random import rand
from math import ceil, sin, cos, sqrt
from nn import Network


class Drone:
    def __init__(self, nn, size=40):
        self.size = size
        self.position = np.array([0.5, 0.5])
        self.velocity = np.array([0.0, 0.0])
        self.forces = np.array([0.0, 0.0])
        self.alive = True

        self.torque = 0
        self.angle = 0
        self.angular_momentum = 0.0

        # initialize thrusters
        self.br_thr = 0.4
        self.bl_thr = 0.4

        # give neural network
        self.nn = nn

        self.target = None

    def set_target(self, tar):
        self.target = tar

    def update(self, dt):
        # print(self.velocity)
        # print(self.position)
        self.update_thrusters()
        self.compute_forces()

        self.br_thr += dt * 0.1
        self.bl_thr += dt * 0.1

        self.velocity += dt * (self.forces + np.array([0.0, 0.9]))  # forces + gravity
        self.position += self.velocity * dt

        self.angular_momentum += self.torque * dt
        self.angle += self.angular_momentum * dt

        self.check_if_alive()

    def check_if_alive(self):
        if min(self.position) < 0 or max(self.position) > 1:
            self.alive = False
            # print(f"DEBUG : drone {self} died")

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
                    self.target[0] - self.position[0],
                    self.target[1] - self.position[1],
                    self.angle,
                    self.angular_momentum,
                ]
            )
        )
        # print(f"thrusters updated to {self.br_thr, self.bl_thr}")
