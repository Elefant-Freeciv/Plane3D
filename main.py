import pygame
from MainScene import MainScene
from Objects import Cube, Tank
import cProfile




class Renderer:

    def __init__(self):
        self.screen_width = 1050/2
        self.screen_height = 700/2
        self.main_screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.running = True
        self.clock = pygame.time.Clock()
        self.current_scene = MainScene(self)
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 15)
        pygame.display.set_caption("Plane3D")
        self.main_screen.fill((255, 255, 255))

    def run(self):
        while self.running == True:
            #self.main_screen.fill((0, 0, 0))
            dt = self.clock.tick(60)/1000.0
            # update current scene
            self.current_scene.update(dt)
            # render current scene
            self.current_scene.render(self.main_screen)

            fps = self.font.render(str(int(self.clock.get_fps())), 1, (0, 0, 0))
            objs = self.font.render(str(len(MainScene.vertices)), 1, (0, 0, 0))
            self.main_screen.blit(fps, (0, 0))
            self.main_screen.blit(objs, (0, 20))

            pygame.display.flip()
            pressed_keys = pygame.key.get_pressed()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        Cube.make()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:
                        Tank.make()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        Global.viewpos[2] += 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 5:
                        Global.viewpos[2] -= 1
                if pressed_keys[pygame.K_m]:
                    Move.movepos()
            self.current_scene.handle_input(events, pressed_keys)


if __name__ == '__main__':
#     import cProfile, pstats
    renderer=Renderer()
#     profiler = cProfile.Profile()
#     profiler.enable()
    renderer.run()
#     profiler.disable()
#     stats = pstats.Stats(profiler).sort_stats("tottime")
#     stats.print_stats()
#     renderer = Renderer()
#     cProfile.run("renderer.run()")

