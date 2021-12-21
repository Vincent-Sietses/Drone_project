import tkinter as tk
import numpy as np
from math import ceil, sin, cos, sqrt
from time import sleep, time
from random import random
from drone import Drone


HEIGHT = 800
WIDTH = 1200

## ALL COORDINATES ARE IN [0,1]x[0,1]


def construct_window() -> tk.Tk:
    window = tk.Tk()
    window.maxsize(WIDTH, HEIGHT)
    window.minsize(WIDTH, HEIGHT)
    window.configure(bg="black")
    return window


def draw_drone(drone, canvas) -> None:
    pos_x, pos_y = WIDTH * drone.position[0], HEIGHT * drone.position[1]

    size = drone.size
    angle = drone.angle
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


def update_drone(drone: Drone, canvas: tk.Canvas, delta: float):

    ## Auxiliary function to allow circle drawing on the canvas
    def _create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    tk.Canvas.create_circle = _create_circle
    # delete previous thruster effects
    for tag in canvas.find_all():
        canvas.delete(tag)

    # draw thruster flames

    pos_x, pos_y = WIDTH * drone.position[0], HEIGHT * drone.position[1]
    size = drone.size
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

    draw_drone(drone, canvas)

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


def window_loop(drone, window, canvas, delta):

    sleep(delta - 0.001)

    drone.update(delta)

    update_drone(drone, canvas, delta)

    canvas.pack()
    if drone.position[1] < 1:
        window.after(1, window_loop, drone, window, canvas, delta)


def run_window(drone=None):

    window = construct_window()
    canvas = tk.Canvas(window, bg="black", height=HEIGHT, width=WIDTH)
    if not drone:
        drone = Drone()
    delta = 0.006

    window.after(0, window_loop, drone, window, canvas, delta)

    window.mainloop()

