import numpy as np
import pygame as py

# size of the screen
w = 1280
h = 720

src = py.display.set_mode((w, h))

class QuadTree:
    def __init__(self, x_min, x_max, y_min, y_max, n=4):
        """
        min max value of particles. This would be used for the bounding box.
        Gets the leftmost, rightmost, topmost, and bottommost particles and their coordinates
        """
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.x_mid = 0
        self.y_mid = 0

        """
        cap/capacity defines how much points are in a quadrant before it subdivides.
        This is arbitrary and could be set to any number.
        """
        self.cap = n

        """
        contains all the points in the screen.
        Note that this must be an array. np.array could be used.
        """
        self.points = []

        """
        contains the children. I still dont know what does this do.
        But must be an array too like self.points
        """
        self.children = []

        # 4 Subsections of the Node
        self.southEast = None
        self.northWest = None
        self.northEast = None
        self.southWest = None

        # checks if the section isn't subdivided yet
        self.divided = False

    def Subdivide(self):
        """
        Subdivides the bounding square into 4 regions.
        ChatGPT said that it should be NE-NW-SE-SW instead but im not sure, so im sticking with this
        """
        x_mid = (self.x_min + self.x_max) / 2
        y_mid = (self.y_min + self.y_max) / 2
        self.northWest = QuadTree(self.x_min, x_mid, y_mid, self.y_max)
        self.northEast = QuadTree(x_mid, self.x_max, y_mid, self.y_max)
        self.southWest = QuadTree(self.x_min, x_mid, self.y_min, y_mid)
        self.southEast = QuadTree(x_mid, self.x_max, self.y_min, y_mid)
        self.divided = True

        self.children = [self.northWest, self.northEast, self.southWest, self.southEast]

    # function to insert points into the tree
    def Insert(self, point):
        """
        If the no. of points are smaller than the capacity,
        append the point to the tree/points array.
        If it is larger, the region will be subdivided but checks first
        if it isn't already divided yet
        """
        if len(self.points) < self.cap:
            self.points.append(point)
        else:
            if not self.divided:
                self.Subdivide()

        for child in self.children:
            if child.x_min <= point[0] < child.x_max and child.y_min <= point[1] < child.y_max:
                child.Insert(point)

    def get_forces(self, point, theta, forces):
        if not self.children:
            d = np.sqrt((self.x_min - point[0])**2 + (self.y_min - point[1])**2) + 1e-9
            f = forces / d
            return f * (self.x_min - point[0]), f * (self.y_min - point[1])
        else:
            x_mid = (self.x_min + self.x_max) / 2
            y_mid = (self.y_min + self.y_max) / 2
            d = np.sqrt((x_mid - point[0])**2 + (y_mid - point[1])**2)
            if d / self.x_max - self.x_min > theta:
                print(d / self.x_max - self.x_min)
                return 0, 0
            else:
                fx, fy = 0, 0
                for child in self.children:
                    if child.x_min <= point[0] < child.x_max and child.y_min <= point[1] < child.y_max:
                        fx_, fy_ = child.get_forces(point, theta, forces)
                        fx += fx_
                        fy += fy_

                    print(fx, fy)
                return fx, fy

    def DrawQuads(self, screen=src):
        # draw the borders of the quad
        py.draw.line(screen, (255, 0, 255), (self.x_min, self.y_min), (self.x_max, self.y_min), 1)
        py.draw.line(screen, (255, 0, 255), (self.x_min, self.y_min), (self.x_min, self.y_max), 1)
        py.draw.line(screen, (255, 0, 255), (self.x_max, self.y_min), (self.x_max, self.y_max), 1)
        py.draw.line(screen, (255, 0, 255), (self.x_min, self.y_max), (self.x_max, self.y_max), 1)
        # if the quad is divided, draw the borders of its quads
        if self.divided:
            self.northWest.DrawQuads(screen)
            self.northEast.DrawQuads(screen)
            self.southWest.DrawQuads(screen)
            self.southEast.DrawQuads(screen)


def barnes_hut_2d(points, theta, max_depth):
    x_min, x_max = np.min(points[:, 0]), np.max(points[:, 0])
    y_min, y_max = np.min(points[:, 1]), np.max(points[:, 1])
    capacity = len(points) // (4 ** max_depth)
    tree = QuadTree(x_min, x_max, y_min, y_max, capacity)

    for point in points:
        tree.Insert(point)
    forces = np.zeros(points.shape)
    for i, point in enumerate(points):
        fx, fy = tree.get_forces(point, theta, 1)
        forces[i] = fx, fy

    return tree, forces


def main():
    py.init()
    screen = src
    clock = py.time.Clock()
    particles = np.random.rand(800, 2) * 720
    theta = 0.5
    max_depth = 2

    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False

        tree, forces = barnes_hut_2d(particles, theta, max_depth)
        # particles += forces
        screen.fill((0, 0, 0))
        tree.DrawQuads()
        # screen.blit(screen, (0, 0))
        for point in particles:
            py.draw.circle(screen, (255, 255, 255), (int(point[0]), int(point[1])), 2)
        # tree.DrawQuads()
        py.display.flip()
        clock.tick(60)

    py.quit()


if __name__ == '__main__':
    main()
