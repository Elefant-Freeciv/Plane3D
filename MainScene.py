from Scene import Scene
import pygame
import Math3D
import math
from Math3D import *
import Math2D
import Texturing as TEX
from PIL import Image, ImageDraw
from numpy import asarray
with Image.open("alphazero.bmp") as renderimgbak:
    renderimgbak=renderimgbak.copy()
print("initialized MainScene")


class MainScene(Scene):
    def __init__(self, renderer):
        xr=0
        yr=0
        zr=0
        self.__renderer = renderer
        MainScene.vertices = [[(20.0, 0.0, 0.0, 000, 000, 000, 0.0, 0.0, 0.0, 0, 0, xr, yr, zr),  #x axis
            (-20.0, 0.0, 0.0, 000, 000, 000, 0.0, 0.0, 0.0, 0, 0, xr, yr, zr), #x axis
            (20.0, 0.0, 0.0, 000, 000, 000, 0.0, 0.0, 0.0, 0, 0, xr, yr, zr),  #x axis
            (0.0, 20.0, 0.0, 000, 000, 000, 0.0, 0.0, 0.0, 0, 0, xr, yr, zr),  #y axis
            (0.0, 20.0, 0.0, 000, 000, 000, 0.0, 0.0, 0.0, 0, 0, xr, yr, zr),  #y axis
            (0.0, -20.0, 0.0, 000, 000, 000, 0.0, 0.0, 0.0, 0, 0, xr, yr, zr),  #y axis
            (0.0, 0.0, 20.0, 000, 000, 000, 0.0, 0.0, 0.0, 0, 0, xr, yr, zr),  #z axis
            (0.0, 0.0, 20.0, 000, 000, 000, 0.0, 0.0, 0.0, 0, 0, xr, yr, zr),  #z axis
            (0.0, 0.0, -20.0, 000, 000, 000, 0.0, 0.0, 0.0, 0, 0, xr, yr, zr)]]
        self.viewpos = [0.0, 0.0, -10.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.delta = 0.0
        self.last_frame_verts = []
        self.clicking = False
        self.start_click = []
        self.render_surface = pygame.Surface((self.__renderer.screen_width, self.__renderer.screen_height))

    def update(self, delta):
        self.delta = delta
        if self.clicking:
            rel_pos = [pygame.mouse.get_pos()[1] - self.start_click[1], pygame.mouse.get_pos()[0] - self.start_click[0]]
            self.rotation[0] = -rel_pos[0] / self.__renderer.screen_width
            self.rotation[1] = -rel_pos[1] / self.__renderer.screen_height

    def render(self, screen):
        renderimg=renderimgbak.copy()
        model = Mat4()
        Math3D.translate(model, Vec3(1.0, 1.0, 1.0))
        Math3D.rotate(model, 10.0 * self.rotation[0], Vec3(1.0, 0.0, 0.0))
        Math3D.rotate(model, 10.0 * self.rotation[1], Vec3(0.0, 1.0, 0.0))

        view = Mat4()
        Math3D.translate(view, Vec3(-self.viewpos[0], -self.viewpos[1], self.viewpos[2]))

        right = 12.0
        top = 8.0
        far = 100.0
        near = 0.1
        orth_proj = Mat4()
        orth_proj.matrix[0][0] = 1 / right
        orth_proj.matrix[1][1] = 1 / top
        orth_proj.matrix[2][2] = -2 / (far - near)
        orth_proj.matrix[2][3] = -((far + near) / (far - near))

        world_space_tris = []
        for obj in MainScene.vertices:
            for i in range(0, len(obj), 3):
                tri = []
                rgb = None
                for (x, y, z, r, g, b,X,Y,Z, tex, o, xr, yr, zr) in obj[i:i+3]:
                    point=Math2D.rotate3d(x,y,z,xr,yr,zr)
                    x=point[0]
                    y=point[1]
                    z=point[2]
                    vec = model * Vec4(x+X, y+Y, z+Z, 1.0)
                    tri.append(vec)
                    rgb = (r, g, b)
                    tex = [tex,o]
                world_space_tris.append([tri, rgb, tex])

        # sort the triangles so they get drawn in the right order. Sorted by mean depth of vertices in triangle
        world_space_tris.sort(
            key=lambda k: sum([vec.z for vec in k[0]]) / 3, reverse=True)

        transformed_vertices_tris = []
        for tri, col, tex in world_space_tris:
            new_tri = []
            for v in tri:
                vec = orth_proj * view * v
                vec.w = -vec.z
                vec = Vec3(vec.x / vec.w, vec.y / vec.w, vec.z / vec.w)
                new_tri.append(vec)
            transformed_vertices_tris.append([new_tri, col, tex])

        self.render_surface.fill((255, 255, 255))
        for tri, col, tex in transformed_vertices_tris:
            point1x = math.ceil(((tri[0].x + 1.0) / 2.0) * self.__renderer.screen_width)
            point1y = math.ceil(((-tri[0].y + 1.0) / 2.0) * self.__renderer.screen_height)
            point2x = math.ceil(((tri[1].x + 1.0) / 2.0) * self.__renderer.screen_width)
            point2y = math.ceil(((-tri[1].y + 1.0) / 2.0) * self.__renderer.screen_height)
            point3x = math.ceil(((tri[2].x + 1.0) / 2.0) * self.__renderer.screen_width)
            point3y = math.ceil(((-tri[2].y + 1.0) / 2.0) * self.__renderer.screen_height)
            #pygame.draw.polygon(self.render_surface, (col[0], col[1], col[2]), [[point1x, point1y], [point2x, point2y], [point3x, point3y]])
#             pygame.draw.line(self.render_surface, (0, 0, 0), (point1x, point1y), (point2x, point2y))
#             pygame.draw.line(self.render_surface, (0, 0, 0), (point2x, point2y), (point3x, point3y))
#             pygame.draw.line(self.render_surface, (0, 0, 0), (point3x, point3y), (point1x, point1y))
#             pygame.draw.circle(self.render_surface, (0, 0, 0), (point1x, point1y), 3)
#             pygame.draw.circle(self.render_surface, (0, 0, 0), (point2x, point2y), 3)
#             pygame.draw.circle(self.render_surface, (0, 0, 0), (point3x, point3y), 3)
            if tex != [0,0]:
                renderimg=TEX.texture((point1x,point1y),(point2x,point2y),(point3x,point3y),tex[0],tex[1], renderimg)
        img = TEX.pilImageToSurface(renderimg)
        self.render_surface.blit(img, img.get_rect())
        screen.blit(self.render_surface, (0, 0))




    def handle_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.clicking == False:
                    self.start_click = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
                    self.clicking = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.clicking = False
                self.start_click = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
        if pressed_keys[pygame.K_UP]:
            self.viewpos[1] += 0.1
        if pressed_keys[pygame.K_DOWN]:
            self.viewpos[1] -= 0.1
        if pressed_keys[pygame.K_LEFT]:
            self.viewpos[0] -= 0.1
        if pressed_keys[pygame.K_RIGHT]:
            self.viewpos[0] += 0.1
        if pressed_keys[pygame.K_PAGEUP]:
            self.viewpos[2] -= 0.1
        if pressed_keys[pygame.K_PAGEDOWN]:
            self.viewpos[2] += 0.1
        if pressed_keys[pygame.K_e]:
            self.rotation[1] += 0.01
        if pressed_keys[pygame.K_q]:
            self.rotation[1] -= 0.01
        if pressed_keys[pygame.K_w]:
            self.rotation[0] += 0.01
        if pressed_keys[pygame.K_s]:
            self.rotation[0] -= 0.01


