import numpy as np
from numpy.random import rand
from math import ceil, sin, cos, sqrt
from nn import Network

# constant for force calculations
SIN_75_SQRT_2 = np.sin(75 / 180 * 2 * np.pi) / np.sqrt(2)


class Drone:
    def __init__(self, nn=None, size=40):
        self.size = size
        self.position = np.array([0.5, 0.5])
        self.velocity = np.array([0.0, 0.0])
        self.forces = np.array([0.0, 0.0])
        self.alive = True

        self.torque = 0
        self.angle = 0
        self.angular_momentum = 0.0

        # initialize thrusters
        self.br_thr = 0.5
        self.bl_thr = 0.5
        self.tr_thr = 0.5
        self.tl_thr = 0.5

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

        self.velocity += dt * (self.forces + np.array([0.0, 1]))  # forces + gravity
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
        bottom_thruster_orientation = np.array([sin(self.angle), -cos(self.angle)])

        bl_thrust = self.bl_thr * bottom_thruster_orientation
        br_thrust = self.br_thr * bottom_thruster_orientation

        tr_thruster_orientation = np.array(
            [sin(self.angle - np.pi / 6), -cos(self.angle - np.pi / 6)]
        )
        tl_thruster_orientation = np.array(
            [sin(self.angle + np.pi / 6), -cos(self.angle + np.pi / 6)]
        )

        tr_thrust = 0.5 * self.tr_thr * tr_thruster_orientation
        tl_thrust = 0.5 * self.tl_thr * tl_thruster_orientation

        self.forces = bl_thrust + br_thrust + tr_thrust + tl_thrust

        # compute torque
        # bottom thrusters : r x F = r*F*sin(theta) =  +- size* sqrt(2) * sqrt(2) / 2 * thrust
        bl_torque = self.bl_thr * self.size
        br_torque = -self.br_thr * self.size

        # top thrusters : r x F = r*F*sin(theta) = +- size* sin(75)/sqrt(2) * thrust
        tl_torque = 0.5 * self.tl_thr * self.size * SIN_75_SQRT_2
        tr_torque = -0.5 * self.tr_thr * self.size * SIN_75_SQRT_2

        self.torque = bl_torque + br_torque + tl_torque + tr_torque

    def update_thrusters(self):

        self.br_thr, self.bl_thr, self.tr_thr, self.tl_thr = self.nn.forward_pass(
            np.array(
                [
                    self.velocity[0],
                    self.velocity[1],
                    self.target[0] - self.position[0],
                    self.target[1] - self.position[1],
                    np.sin(self.angle),
                    np.cos(self.angle),
                    self.angular_momentum,
                ]
            )
        )
        # print(
        #     f"thrusters updated to {self.br_thr, self.bl_thr, self.tr_thr, self.tl_thr}"
        # )
