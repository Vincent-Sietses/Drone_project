import numpy as np
import tkinter as tk
from math import ceil, sin, cos, sqrt
from time import sleep, time
from random import random


HEIGHT = 800
WIDTH = 1200

## ALL COORDINATES ARE IN [0,1]x[0,1]


class Drone:
    def __init__(self, size=30):
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

    def update(self, dt):
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


def construct_window() -> tk.Tk:
    window = tk.Tk()
    window.maxsize(WIDTH, HEIGHT)
    window.minsize(WIDTH, HEIGHT)
    window.configure(bg="black")
    return window


def draw_drone(dr) -> None:
    global canvas
    pos_x, pos_y = WIDTH * dr.position[0], HEIGHT * dr.position[1]

    size = dr.size
    angle = dr.angle
    canvas.create_polygon(  # draw drone body
        [
            pos_x - size,
            pos_y - size,
            pos_x - size,
            pos_y + size,
            pos_x + size,
            pos_y + size,
            pos_x + size,
            pos_y - size,
        ],
        outline="white",
        fill="lime",
        width=5,
        tags="drone",
    )
    canvas.create_polygon(
        [
            pos_x + 0.5 * size,
            pos_y + 0.5 * size,
            pos_x - 0.5 * size,
            pos_y + 0.5 * size,
            pos_x - 0.5 * size,
            pos_y - 0.5 * size,
            pos_x + 0.5 * size,
            pos_y - 0.5 * size,
        ],
        outline="blue",
        fill="grey",
        width=7,
        smooth=1,
        tags="drone",
    )
    canvas.create_polygon(
        [
            pos_x + 0.4 * size,
            pos_y + 0.2 * size,
            pos_x - 0.4 * size,
            pos_y + 0.2 * size,
            pos_x - 0.4 * size,
            pos_y - 0.2 * size,
            pos_x + 0.4 * size,
            pos_y - 0.2 * size,
        ],
        outline="black",
        fill="white",
        width=ceil(0.1 * size),
        smooth=1,
        tags="drone",
    )
    canvas.create_polygon(  # bottom left thruster
        [
            pos_x - (0.9 * size),
            pos_y + (0.95 * size),
            pos_x - (0.3 * size),
            pos_y + (0.95 * size),
            pos_x - (0.2 * size),
            pos_y + (1.3 * size),
            pos_x - (1 * size),
            pos_y + (1.3 * size),
        ],
        outline="black",
        fill="grey",
        width=2,
        tags="drone",
    )
    canvas.create_polygon(  # bottom right thruster
        [
            pos_x + 0.3 * size,
            pos_y + 0.95 * size,
            pos_x + 0.9 * size,
            pos_y + 0.95 * size,
            pos_x + 1 * size,
            pos_y + 1.3 * size,
            pos_x + 0.2 * size,
            pos_y + 1.3 * size,
        ],
        outline="black",
        fill="grey",
        width=2,
        tags="drone",
    )


def update_drone(drone):
    global canvas, delta

    ## Auxiliary function to allow circle drawing on the canvas
    def _create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    tk.Canvas.create_circle = _create_circle
    # delete previous thruster effects
    for tag in canvas.find_all():
        canvas.delete(tag)

    # draw thruster flames

    pos_x, pos_y = WIDTH * dr.position[0], HEIGHT * dr.position[1]
    size = dr.size
    if drone.br_thr:
        canvas.create_polygon(  # bottom right thruster
            [
                pos_x + 0.6 * size,
                pos_y + 1.1 * size,
                pos_x + (0.6 - 0.2 * drone.br_thr) * size,
                pos_y + (1.3 + 0.4 * drone.br_thr) * size,
                pos_x + (0.6 + 0.2 * drone.br_thr) * size,
                pos_y + (1.3 + 0.4 * drone.br_thr) * size,
            ],
            outline="red",
            fill="yellow",
            width=3,
            tags="flame",
        )
        for _ in range(ceil(5 * drone.br_thr)):
            canvas.create_circle(
                pos_x + (0.8 - 0.4 * random()) * size,
                pos_y + (1.3 + 0.6 * random() * drone.br_thr) * size,
                2,
                tag="flame",
                fill="red",
                outline="orange",
                width=1,
            )
    if drone.bl_thr:
        canvas.create_polygon(  # bottom left thruster
            [
                pos_x - 0.6 * size,
                pos_y + 1.1 * size,
                pos_x - (0.6 - 0.2 * drone.bl_thr) * size,
                pos_y + (1.3 + 0.4 * drone.bl_thr) * size,
                pos_x - (0.6 + 0.2 * drone.br_thr) * size,
                pos_y + (1.3 + 0.4 * drone.br_thr) * size,
            ],
            outline="red",
            fill="yellow",
            width=3,
            tags="flame",
        )
        for _ in range(ceil(5 * drone.bl_thr)):
            canvas.create_circle(
                pos_x - (0.4 + 0.4 * random()) * size,
                pos_y + (1.3 + 0.6 * random() * drone.bl_thr) * size,
                2,
                tag="flame",
                fill="red",
                outline="orange",
                width=1,
            )

    draw_drone(dr)

    # if the angle is non-zero, rotate all the points around the center of the drone
    a = drone.angle
    if a:
        R = np.array(
            [[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]
        )  # rotation matrix
        o = np.atleast_2d([pos_x, pos_y])  # drone center

        for tag in canvas.find_all():  # loop over all polygons
            newxy = []
            point_list = canvas.coords(tag)  # get polygon points
            for i in range(
                0, len(point_list), 2
            ):  # for every pair, apply the rotation matrix

                p = np.atleast_2d(point_list[i : i + 2])
                # move point to origin, apply the rotation, move it back and append it to the new coordinate list
                newxy += [c for c in np.squeeze((R @ (p.T - o.T) + o.T).T)]
            canvas.coords(tag, newxy)

    canvas.pack()


def game_loop(dr):
    global window, canvas, delta
    sleep(delta - 0.001)
    print(dr.position)
    print(dr.velocity)
    dr.update(delta)

    update_drone(dr)
    # window.update()
    # canvas.update()
    canvas.pack()
    if dr.position[1] < 1:
        window.after(1, game_loop, dr)


if __name__ == "__main__":

    window = construct_window()
    canvas = tk.Canvas(window, bg="black", height=HEIGHT, width=WIDTH)
    dr = Drone()
    delta = 0.01
    draw_drone(dr)

    window.after(0, game_loop, dr)

    window.mainloop()

