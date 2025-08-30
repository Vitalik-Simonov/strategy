from config import *
import asyncio
from sprites import MyBase, EnemyBase, Knight


class App:
    def __init__(self):
        self.FPS = FPS
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        if sys.platform == "win32":
            try:
                import ctypes
                # Попытка для Windows 8.1+
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except:
                try:
                    # Для Windows Vista+
                    ctypes.windll.user32.SetProcessDPIAware()
                except:
                    pass
            os.environ['SDL_VIDEODRIVER'] = 'windib'

        elif sys.platform.startswith('linux'):
            # Для Linux: настройки для Wayland/X11
            os.environ['SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR'] = '0'
            os.environ['SDL_VIDEO_X11_VIDEOVISUAL'] = '1'
        pg.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])#, pg.FULLSCREEN)
        self.init()

    def init(self):
        self.clock = pg.time.Clock()
        self.fps = FPS
        self.all_sprites = pg.sprite.Group()
        self.UI_sprites = pg.sprite.Group()
        self.my_units = pg.sprite.Group()
        self.my_buildings = pg.sprite.Group()
        self.enemy_units = pg.sprite.Group()
        self.enemy_buildings = pg.sprite.Group()

        self.my_base = MyBase(self)
        self.enemy_base = EnemyBase(self)
        Knight(self, 1500, 500, 1)

    def draw(self):
        self.screen.fill(pg.Color((252, 219, 109)))
        pg.draw.line(self.screen, (100, 100, 100), (WIDTH // 3, 0), (WIDTH // 3, HEIGHT))
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
        self.fps = self.clock.get_fps() + 0.00001

    async def run(self):
        while True:
            self.update()
            self.draw()
            await asyncio.sleep(0)

    def win(self):
        print('win')

    def lose(self):
        print('lose')


if __name__ == '__main__':
    app = App()
    asyncio.run(app.run())
