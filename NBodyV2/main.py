import time
import random
import pygame as py
import numpy as np
import pickle as pk
import tkinter as tk
from tkinter import filedialog
from pygame.locals import *

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (30, 30, 30)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Window:
    def __init__(self):
        # Initialize pygame
        py.init()

        # Initialize tkinter for File Explorer dialog
        root = tk.Tk()
        root.withdraw()

        self.resolution = [(1920, 1080), (1280, 1024), (1600, 900), (1280, 720)]
        self.surface = py.display.set_mode((1280, 720), HWSURFACE | DOUBLEBUF)
        py.display.set_caption("Resizable")

        # this was here for readability, used in LineGrid()
        self.colNb = None
        self.rowNb = None
        self.cellSize = 50

        # this was here for readability, used mainly in Camera Pan and Zoom
        self.x_offset = -self.surface.get_width() / 2  # x and y offsets the virtual space 0, 0 from
        self.y_offset = -self.surface.get_height() / 2  # originally top left to center of the screen
        self.startPanX = 0
        self.startPanY = 0
        self.x_pan = 0
        self.y_pan = 0
        self.startPan = False
        self.zoomScaleX = 1.0
        self.zoomScaleY = 1.0
        self.previous_zoom = 1
        self.zoom_level = 1

        # used in SpawnBody() and EulerAlgo()
        self.bodies = np.array([])  # stores body positions
        self.velocity = np.array([])  # stores body velocities
        self.mass = np.array([])  # stores body masses
        self.startLaunch = False  # True if user left-clicks, initiates body launch
        self.startLaunch_pos = np.array([0, 0])  # stores the launch start position
        self.launchVector = np.array([0, 0])  # stores the launch direction
        self.setMass = 10  # stores the selected mass
        self.enableGalaxySpawn = False  # True if user activates spawn galaxy key
        self.num_body = 0

        # this was here for readability, used in ParticleEffect()
        self.surfaceW = None
        self.surfaceY = None
        self.ParticleEffects()

        # used in SpawnGalaxy()
        self.center_mass = 1000000
        self.galaxy_size = 400
        self.galaxy_radius = 1500
        self.body_masses = 100
        self.body_velocity = 500
        self.side_angle = 180
        self.side_angle_speed = 100

        self.pause = False

    def EventHandle(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                exit()
            """
            if event.type == VIDEORESIZE:
                surface = py.display.set_mode((event.w, event.h), HWSURFACE | DOUBLEBUF | RESIZABLE)
            """
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    exit()
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
                if event.key == py.K_g:
                    self.enableGalaxySpawn = not self.enableGalaxySpawn
                if event.key == py.K_p:
                    self.pause = not self.pause
                if event.key == py.K_r:
                    self.num_body = 0
                    self.bodies = np.array([])
                    self.velocity = np.array([])
                    self.mass = np.array([])
                    print("reset")
                if (event.mod & py.KMOD_CTRL) and event.key == K_s:
                    self.SaveState()
                    py.key.set_mods(0)
                if (event.mod & py.KMOD_CTRL) and event.key == K_l:
                    self.LoadState()
                    py.key.set_mods(0)

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
                    self.CameraZoom(1.1, 1.1)
                    self.UpdateGridZoom(1.1)
                if event.button == 5:
                    self.GetMousePos()
                    self.CameraZoom(0.9, 0.9)
                    self.UpdateGridZoom(0.9)
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
                        print("method: ", self.bodies[-1])
                    # print("Vel", self.velocity)
                if event.button == 3:
                    self.startPan = False

        if self.startLaunch:
            dv = self.startLaunch_pos - py.mouse.get_pos()
            self.launchVector = dv
            # print(self.launchVector)

    def ParticleEffects(self):
        r = 64
        sz = int(max(min(abs(4 * self.zoom_level), 1), 1))

        self.surfaceY = py.Surface((r, r))
        py.draw.circle(self.surfaceY, (1, 1, 1), (32, 32), 32, 32)  # Soft Glow Color
        py.draw.circle(self.surfaceY, (255, 235, 0), (32, 32), sz, sz)  # Yellow Color

        self.surfaceW = py.Surface((r, r))
        py.draw.circle(self.surfaceW, (3, 3, 3), (32, 32), 32, 32)  # Bright Glow Color
        py.draw.circle(self.surfaceW, (255, 255, 255), (32, 32), sz, sz)  # White Color

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

        AfterZoomX, AfterZoomY = self.ScreenToSpace(self.x_pan, self.y_pan)

        self.x_offset += (BeforeZoomX - AfterZoomX)
        self.y_offset += (BeforeZoomY - AfterZoomY)

    def UpdateGridZoom(self, new_zoom):
        if new_zoom == 1.1:
            self.zoom_level += 0.1
        else:
            self.zoom_level -= 0.1

        zoom_diff = round(self.zoom_level - self.previous_zoom, 3)
        if zoom_diff == 1:
            self.previous_zoom = self.zoom_level
            self.cellSize *= 0.5
        if zoom_diff == -1:
            self.previous_zoom = self.zoom_level
            self.cellSize *= 4

        # self.zoom_level += new_zoom

        print("P: ", self.previous_zoom, "C: ", self.zoom_level, "D: ", zoom_diff)

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

        center_body = mouse_pos.tolist()
        self.center_mass = 1000000
        self.galaxy_size = 400
        self.galaxy_radius = 2500
        self.body_masses = 10
        self.body_velocity = 500
        self.side_angle = 20
        self.side_angle_speed = 50

        if body_list:
            body_list[-1] = np.array(mouse_pos)
            vel_list[-1] = np.array(vel)
            mass_list[-1] = self.center_mass
        else:
            body_list.append(np.array(center_body))
            vel_list.append(np.array(center_body))
            mass_list.append(np.array(self.center_mass))

        for i in range(self.galaxy_size // 2):
            angle = np.random.randint(-self.side_angle, self.side_angle)
            rad = np.deg2rad(angle)
            vel_rad = np.deg2rad(angle + self.side_angle_speed)
            radius = np.random.randint(100, self.galaxy_radius)
            p = np.array([np.cos(rad) * radius, radius * np.sin(rad)]) + mouse_pos
            vel_direction = np.array([np.cos(vel_rad), np.sin(vel_rad)]) * self.body_velocity + vel
            body_list.append(p)
            vel_list.append(vel_direction)
            mass_list.append(self.body_masses)

        for i in range(self.galaxy_size // 2):
            angle = np.random.randint(180 - self.side_angle, 180 + self.side_angle)
            rad = np.deg2rad(angle)
            vel_rad = np.deg2rad(angle + self.side_angle_speed)
            radius = np.random.randint(100, self.galaxy_radius)
            p = np.array([np.cos(rad) * radius, radius * np.sin(rad)]) + mouse_pos
            vel_direction = np.array([np.cos(vel_rad), np.sin(vel_rad)]) * self.body_velocity + vel
            body_list.append(p)
            vel_list.append(vel_direction)
            mass_list.append(self.body_masses)

        self.num_body += self.galaxy_size

        self.bodies = np.array(body_list)  # convert back into numpy array
        self.velocity = np.array(vel_list)
        self.mass = np.array(mass_list)

    def EulerAlgo(self):
        # Body Properties
        pos = self.bodies
        vel = self.velocity
        mass = self.mass

        # Gravity Constant
        G = 0.66743  # N m^2 / kg^2

        # Timestep
        dt = 0.1

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
        vel += sum_acc * dt
        pos += vel * dt

    def DrawBody(self):
        self.surface.blit(self.surface, (0, 0))

        # iterate the bodies, with the length of the array as the range
        for i in range(len(self.bodies)):
            # get positions @ index 'i'
            bodies = self.bodies[i]

            # convert the virtual space positions into screen positions while ignoring some returns
            x, _ = self.SpaceToScreen(bodies[0], self.surface.get_width())
            _, y = self.SpaceToScreen(self.surface.get_height(), bodies[1])

            # setting r=64 in draw surfaces makes only (32, 32) the value that will make the circle whole
            # thus, offsetting the spawn by 32px
            x -= 32
            y -= 32

            # randomly flips to 0 or 1
            flip = random.randint(0, 1)

            if flip == 1:
                self.surface.blit(self.surfaceY, [x, y], special_flags=py.BLEND_RGB_ADD)
            else:
                self.surface.blit(self.surfaceW, [x, y], special_flags=py.BLEND_RGB_ADD)

            # Draw the line indicating the launch vector
            if self.startLaunch and i == len(self.bodies) - 1:
                end_point = [x + 32, y + 32] + self.launchVector
                # print(self.launchVector)
                py.draw.line(self.surface, RED, [x + 32, y + 32], end_point, 1)

    def SaveState(self):
        try:
            filePath = filedialog.asksaveasfilename(defaultextension=".pkl",
                                                    filetypes=[("Pickle files", "*.pkl"),
                                                               ("All files", "*.*")])
            states = {"pos": self.bodies, "vel": self.velocity, "mass": self.mass}
            with open(filePath, 'wb') as f:
                pk.dump(states, f)
            print("Current State Saved!")
        except FileNotFoundError:
            pass

    def LoadState(self):
        try:
            filePath = filedialog.askopenfile(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
            filePath = filePath.name
            with open(filePath, 'rb') as f:
                states = pk.load(f)
                self.bodies = states["pos"]
                self.velocity = states["vel"]
                self.mass = states["mass"]
            print("Saved State Loaded")
        except AttributeError:
            pass

    def Run(self):
        running = True
        while running:
            in_t = time.time()
            self.EventHandle()
            self.surface.fill((0, 0, 0))
            self.surface.blit(self.surface, (0, 0))
            self.Gridlines()
            self.DrawBody()
            if not self.pause and not self.startLaunch:
                self.EulerAlgo()
            py.display.flip()
            # print(time.time() - in_t)

        # quit py after closing window
        py.quit()


if __name__ == "__main__":
    print("started")
    w = Window()
    w.Run()
