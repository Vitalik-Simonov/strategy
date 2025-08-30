from config import *


class Bar(pg.sprite.Sprite):
    def __init__(self, app, target, max_value=100, color='green', shift=10):
        super(Bar, self).__init__(app.all_sprites)
        self.app = app
        self.target = target
        self.max_value = max_value
        self.value = max_value
        self.color = color
        self.shift = shift
        self.image = pg.surface.Surface((102, 22))
        self.image.fill('black')
        pg.draw.rect(self.image, self.color, (1, 1, 100, 10))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.target.rect.centerx
        self.rect.bottom = self.target.rect.y - self.shift

    def update(self):
        self.rect.centerx = self.target.rect.centerx
        self.rect.bottom = self.target.rect.y - self.shift

    def update_value(self, value):
        if value == self.value:
            return
        self.value = value
        self.image.fill('black')
        pg.draw.rect(self.image, self.color, (1, 1, self.value * 100 // self.max_value, 10))


class SpriteHp(pg.sprite.Sprite):
    def __init__(self, app, hp=100, shield=None, *groups):
        super(SpriteHp, self).__init__(*groups)
        self.app = app
        self.hp = hp
        self.hp_bar = Bar(app, self, hp)
        if shield is not None:
            self.shield = shield
            self.shield_bar = Bar(app, self, shield, 'blue', 55)
        else:
            self.shield = 0

    def get_damage(self, damage):
        if self.shield is None:
            self.hp -= damage
            self.hp_bar.update_value(self.hp)
        if self.shield >= damage:
            self.shield -= damage
            self.shield_bar.update_value(self.shield)
        else:
            damage -= self.shield
            self.shield = None
            self.hp -= damage
            self.shield_bar.kill()
            self.hp_bar.update_value(self.hp)

        if self.hp <= 0:
            self.killed()

    def killed(self):
        self.hp_bar.kill()
        self.kill()


class Unit(SpriteHp):
    def __init__(self, app, hp, shield, enemy_units, my_group):
        super().__init__(app, hp, shield, app.all_sprites, my_group)
        self.app = app
        self.enemy_units = enemy_units
        self.timer = 0

    def get_target(self, distance=100):
        target = None
        minimum = distance
        for sprite in self.enemy_units:
            dist = math.dist((self.rect.centerx, self.rect.centery), (sprite.rect.centerx, sprite.rect.centery))
            if minimum >= dist:
                target = sprite
                minimum = dist
        return target

    def attack(self, target, damage=1):
        if hasattr(target, 'get_damage'):
            if time.time() - self.timer >= self.shoot_speed:
                self.timer = time.time()
                target.get_damage(damage)


class MyBase(SpriteHp):
    def __init__(self, app, x=100, y=HEIGHT // 2):
        super(MyBase, self).__init__(app, 1000, None, app.all_sprites, app.my_units, app.my_buildings)
        self.app = app
        self.image = pg.surface.Surface((100, 100))
        self.image.fill('blue')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def killed(self):
        self.hp_bar.kill()
        self.kill()
        self.app.lose()


class EnemyBase(SpriteHp):
    def __init__(self, app, x=WIDTH - 100, y=HEIGHT // 2):
        super(EnemyBase, self).__init__(app, 1000, None, app.all_sprites, app.enemy_units, app.enemy_buildings)
        self.app = app
        self.image = pg.surface.Surface((100, 100))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def killed(self):
        self.hp_bar.kill()
        self.kill()
        self.app.win()


class Knight(Unit):
    def __init__(self, app, x, y, enemy_units, my_group):
        super().__init__(app, 100, None, enemy_units, my_group)
        self.enemy_units = enemy_units
        self.image = pg.surface.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.distance = 500
        self.speed = 100
        self.shoot_speed = 1

    def update(self):
        target = self.get_target()
        target_x, target_y = target.rect.centerx, target.rect.centery
        angle = math.acos((self.y - target_y) / (math.sqrt((self.y - target_y) ** 2 + (self.x - target_x) ** 2)))
        if target_x < self.x:
            angle = -angle
        if math.sqrt((self.y - target_y) ** 2 + (self.x - target_x) ** 2) >= self.distance:
            speed = self.speed
        else:
            speed = 0
        self.x += math.sin(angle) * speed / self.app.clock.get_fps()
        self.y -= math.cos(angle) * speed / self.app.clock.get_fps()
        self.rect.x = self.x
        self.rect.y = self.y

