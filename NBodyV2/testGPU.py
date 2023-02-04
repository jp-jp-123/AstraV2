import math
import time
import pygame as py
import numpy as np
import numba
import platform
import torch
# import matplotlib.pyplot as plt
from pygame.locals import *

py.init()

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
time_limit = 5000
py.time.set_timer(py.USEREVENT, time_limit)


class Window:
    def __init__(self):
        py.init()
        self.surface = py.display.set_mode((1280, 720), HWSURFACE | DOUBLEBUF | RESIZABLE)
        py.display.set_caption("Resizable")

        self.isRunning = True

        # this was here for readability, used in LineGrid()
        self.colNb = None
        self.rowNb = None
        self.cellSize = 50

        # this was here for readability, used mainly in Camera Pan and Zoom
        self.x_offset = -self.surface.get_width() / 2
        self.y_offset = -self.surface.get_height() / 2
        self.startPanX = 0
        self.startPanY = 0
        self.x_pan = 0
        self.y_pan = 0
        self.startPan = False
        self.zoomScaleX = 1.0
        self.zoomScaleY = 1.0
        self.previous_zoom = 1
        self.zoom_level = 1

        # used in various methods
        self.bodies = np.array([], dtype=np.float64)  # stores body positions
        self.velocity = np.array([], dtype=np.float64)  # stores body velocities
        self.mass = np.array([], dtype=np.float64)  # stores body masses
        self.startLaunch = False  # True if user left-clicks, initiates body launch
        self.startLaunch_pos = np.array([0, 0])  # stores the launch start position
        self.launchVector = np.array([0, 0])  # stores the launch direction
        self.setMass = 10  # stores the selected mass
        self.enableGalaxySpawn = False  # True if user activates spawn galaxy key
        self.num_body = 0

    def EventHandle(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                exit()
            elif event.type == py.USEREVENT:
                self.isRunning = False

            if event.type == VIDEORESIZE:
                surface = py.display.set_mode((event.w, event.h), HWSURFACE | DOUBLEBUF | RESIZABLE)

            if event.type == py.KEYDOWN:
                if event.key == py.K_1:
                    self.setMass = 100
                if event.key == py.K_2:
                    self.setMass = 200
                if event.key == py.K_3:
                    self.setMass = 300
                if event.key == py.K_4:
                    self.setMass = 400
                if event.key == py.K_5:
                    self.setMass = 500
                if event.key == py.K_6:
                    self.setMass = 600
                if event.key == py.K_7:
                    self.setMass = 700
                if event.key == py.K_8:
                    self.setMass = 800
                if event.key == py.K_9:
                    self.setMass = 900
                if event.key == py.K_0:
                    self.setMass = 10
                if event.key == py.K_BACKSLASH:
                    self.setMass = 10000
                    print("Mass = 10000")
                if event.key == py.K_g:
                    self.enableGalaxySpawn = not self.enableGalaxySpawn
                    print("Galaxy Spawn: Enabled")
                if event.key == py.K_r:
                    self.num_body = 0
                    self.bodies = np.array([])
                    self.velocity = np.array([])
                    self.mass = np.array([])

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.SpawnBody(event.pos, [0, 0], self.setMass)
                    self.startLaunch = True
                    self.startLaunch_pos = np.array(py.mouse.get_pos())
                if event.button == 3:
                    self.startPan = True
                    self.startPanX, self.startPanY = py.mouse.get_pos()
                if event.button == 4:
                    self.GetMousePos()
                    zp = self.CameraZoom(1.1, 1.1)
                    self.UpdateGridZoom(zp)
                if event.button == 5:
                    self.GetMousePos()
                    zm = self.CameraZoom(0.9, 0.9)
                    self.UpdateGridZoom(zm)
            elif event.type == MOUSEMOTION:
                if self.startPan:
                    self.GetMousePos()
                    self.CameraPan(self.x_pan, self.y_pan)

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.startLaunch = False
                    x, y = self.launchVector
                    self.velocity[-1] = np.array([x, y]) / (self.zoom_level ** 2)
                    if self.enableGalaxySpawn:
                        self.SpawnGalaxy(self.bodies[-1], self.velocity[-1])
                    # print("Vel", self.velocity)
                if event.button == 3:
                    self.startPan = False

        if self.startLaunch:
            dv = self.startLaunch_pos - py.mouse.get_pos()
            self.launchVector = dv
            # print(self.launchVector)

    def SpaceToScreen(self, space_x, space_y):
        screen_x = int((space_x - self.x_offset) * self.zoomScaleX)
        screen_y = int((space_y - self.y_offset) * self.zoomScaleY)

        return screen_x, screen_y

    def ScreenToSpace(self, screen_x, screen_y):
        space_x = (float(screen_x) / self.zoomScaleX) + self.x_offset
        space_y = (float(screen_y) / self.zoomScaleY) + self.y_offset

        return space_x, space_y

    def GetMousePos(self):
        self.x_pan, self.y_pan = py.mouse.get_pos()

    def CameraPan(self, mouse_x, mouse_y):
        if self.startPan:
            self.x_offset -= (mouse_x - self.startPanX) / self.zoomScaleX
            self.y_offset -= (mouse_y - self.startPanY) / self.zoomScaleY
            self.startPanX = mouse_x
            self.startPanY = mouse_y

        return self.x_offset, self.y_offset

    def CameraZoom(self, scale_x, scale_y):
        BeforeZoomX, BeforeZoomY = self.ScreenToSpace(self.x_pan, self.y_pan)

        self.zoomScaleX *= scale_x
        self.zoomScaleY *= scale_y
        zoom_level = (self.zoomScaleX + self.zoomScaleY) / 2

        AfterZoomX, AfterZoomY = self.ScreenToSpace(self.x_pan, self.y_pan)

        self.x_offset += (BeforeZoomX - AfterZoomX)
        self.y_offset += (BeforeZoomY - AfterZoomY)

        return zoom_level

    def UpdateGridZoom(self, new_zoom):
        zoom_diff = self.zoom_level - self.previous_zoom
        if math.ceil(zoom_diff) == 4:
            self.previous_zoom = new_zoom
            self.cellSize /= 3
        if math.ceil(zoom_diff) == -4:
            self.previous_zoom = new_zoom
            self.cellSize *= 9

        self.zoom_level = new_zoom

        # print("P: ", self.previous_zoom, "C: ", new_zoom, "D: ", math.ceil(zoom_diff))

    def Gridlines(self):
        self.colNb = self.surface.get_width()
        self.rowNb = self.surface.get_height()
        # left, top = self.ScreenToSpace(0, 0)
        # right, bottom = self.ScreenToSpace(self.colNb, self.rowNb)
        # Draw Horizontal Lines
        for row in range(-self.rowNb, self.rowNb):
            # if top <= row <= bottom:
            rowCoord = row * self.cellSize
            x, y = self.SpaceToScreen(self.rowNb, rowCoord)
            py.draw.line(self.surface, GRAY, (0, y), (self.colNb, y))
        # Draw Vertical Lines
        for col in range(-self.colNb, self.colNb):
            # if left <= col <= right:
            colCoord = col * self.cellSize
            x, y = self.SpaceToScreen(colCoord, self.colNb)
            py.draw.line(self.surface, GRAY, (x, 0), (x, self.rowNb))

    def SpawnBody(self, mouse_pos, vel, mass):
        body_list = self.bodies.tolist()  # converts array into list
        vel_list = self.velocity.tolist()
        mass_list = self.mass.tolist()

        mouse_pos = self.ScreenToSpace(mouse_pos[0],
                                       mouse_pos[1])  # converts mouse position into virtual space position

        body_list.append(mouse_pos)  # append the mouse position to the list
        vel_list.append(vel)
        mass_list.append(mass)

        self.bodies = np.array(body_list, dtype=float)  # convert back into numpy array
        self.velocity = np.array(vel_list, dtype=float)
        self.mass = np.array(mass_list, dtype=float)

        # print("MPos: ", self.bodies, "Mass", self.mass)

    def SpawnGalaxy(self, mouse_pos, vel):
        body_list = self.bodies.tolist()  # converts array into list
        vel_list = self.velocity.tolist()
        mass_list = self.mass.tolist()

        print(mouse_pos)

        center_body = mouse_pos.tolist()
        center_mass = 100000000
        galaxy_size = 200
        galaxy_radius = 2000
        body_mass = 100
        body_velocity = 250
        side_angle = 10
        side_angle_speed = 50

        if not body_list:
            body_list[-1] = np.array(mouse_pos)
            vel_list[-1] = np.array(vel)
            mass_list[-1] = center_mass
        else:
            body_list.append(np.array(center_body))
            vel_list.append(np.array(center_body))
            mass_list.append(np.array(center_mass))

        for i in range(galaxy_size // 2):
            angle = np.random.randint(-side_angle, side_angle)
            rad = np.deg2rad(angle)
            vel_rad = np.deg2rad(angle + side_angle_speed)
            radius = np.random.randint(0, galaxy_radius)
            p = np.array([np.cos(rad) * rad, radius * np.sin(rad)]) + mouse_pos
            vel_direction = np.array([np.cos(vel_rad), np.sin(vel_rad)]) * body_velocity + vel
            body_list.append(p)
            vel_list.append(vel_direction)
            mass_list.append(body_mass)

        for i in range(galaxy_size // 2):
            angle = np.random.randint(180 - side_angle, 180 + side_angle)
            rad = np.deg2rad(angle)
            vel_rad = np.deg2rad(angle + side_angle_speed)
            radius = np.random.randint(0, galaxy_radius)
            p = np.array([np.cos(rad) * rad, radius * np.sin(rad)]) + mouse_pos
            vel_direction = np.array([np.cos(vel_rad), np.sin(vel_rad)]) * body_velocity + vel
            body_list.append(p)
            vel_list.append(vel_direction)
            mass_list.append(body_mass)

        self.num_body += galaxy_size

        print(self.num_body)

        self.bodies = np.array(body_list)  # convert back into numpy array
        self.velocity = np.array(vel_list)
        self.mass = np.array(mass_list)

    def EulerAlgo(self):
        # Body Properties
        pos = self.bodies
        vel = self.velocity
        mass = self.mass

        # Gravity Constant
        G = 0.1  # N m^2 / kg^2

        # Timestep
        dt = 0.01

        # artificial distancing to avoid divide by 0
        eps = 1e-9

        # Compute the distance matrix
        distance = np.sqrt(((pos[:, np.newaxis] - pos[np.newaxis, :]) ** 2).sum(-1))

        # Compute the acceleration matrix
        acc = -G * mass[:, np.newaxis] * (pos[:, np.newaxis] - pos[np.newaxis, :]) / (
                (distance[..., np.newaxis] + eps) ** 2)

        # Sum the acceleration on each axis
        sum_acc = acc.sum(axis=1)

        # Update the positions and velocities
        pos += vel * dt
        vel += sum_acc * dt

    def DrawBody(self):
        self.surface.blit(self.surface, (0, 0))

        # iterate the bodies, with the length of the array as the range
        for i in range(len(self.bodies)):
            # get positions @ index 'i'
            bodies = self.bodies[i]

            # convert the virtual space positions into screen positions while ignoring some returns
            x, _ = self.SpaceToScreen(bodies[0], self.surface.get_width())
            _, y = self.SpaceToScreen(self.surface.get_height(), bodies[1])

            # draw the body, multiply the radius by zoom scaling (y or x zoom will do)
            py.draw.circle(self.surface, WHITE, (x, y), 2 * self.zoomScaleX)

            # Draw the line indicating the launch vector
            if self.startLaunch and i == len(self.bodies) - 1:
                end_point = [x, y] + self.launchVector
                # print(self.launchVector)
                py.draw.line(self.surface, RED, [x, y], end_point, 1)

    def TestRun(self):
        body = 1000
        self.bodies = np.random.uniform(-720, 720, (body, 2))
        self.velocity = np.random.uniform(0, 1, (body, 2))
        self.mass = np.random.randint(100, 200, (body, ))

    def run(self):
        times = []
        while self.isRunning:
            s_time = time.time()
            self.EventHandle()
            self.surface.fill((0, 0, 0))
            self.surface.blit(self.surface, (0, 0))
            self.Gridlines()
            self.TestRun()
            self.DrawBody()
            self.EulerAlgo()
            py.display.flip()
            e_time = time.time()
            times.append(e_time - s_time)

        # quit py after closing window
        py.quit()

        return times


if __name__ == '__main__':
    w = Window()
    # a_time = w.run()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type == 'cuda':
        print("Using GPU")
        device = torch.device("cuda")
        print("Using GPU:", torch.cuda.get_device_name(0))
    else:
        print("Using CPU")
        device = torch.device("cpu")
        print("Using CPU:", platform.processor())
    result = w.run()
    sim = [torch.tensor(x).to(device) for x in result]
    a_time = sum(result)/len(result)
    print(f"Average time: {a_time}")

    # Plot the results using Matplotlib
    '''plt.bar([0], [a_time], label='Average Time')
    plt.xlabel('Function')
    plt.ylabel('Time (s)')
    plt.title('Function Average Time')
    plt.legend()
    plt.show()'''
