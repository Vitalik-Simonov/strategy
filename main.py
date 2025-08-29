from config import *
import asyncio


class App:
    def __init__(self):
        self.FPS = FPS
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        pg.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT], pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.all_sprites = pg.sprite.Group()

    def draw(self):
        self.screen.fill(pg.Color((252, 219, 109)))
        self.all_sprites.draw(self.screen)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

    def update(self):
        self.check_events()
        self.all_sprites.update()

        pg.display.set_caption(str(self.clock.get_fps()))
        pg.display.flip()
        self.clock.tick(self.FPS)

    async def run(self):
        while True:
            self.update()
            self.draw()
            await asyncio.sleep(0)


if __name__ == '__main__':
    app = App()
    asyncio.run(app.run())
