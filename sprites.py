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
        self.image = pg.surface.Surface((102, 12))
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
        self.rect = pg.rect.Rect(0, 0, 0, 0)
        self.hp_bar = Bar(app, self, hp)
        self.shield = shield
        if shield is not None:
            self.shield_bar = Bar(app, self, shield, 'blue', 55)

    def get_damage(self, damage):
        if self.shield is None:
            self.hp -= damage
            self.hp_bar.update_value(self.hp)
        elif self.shield >= damage:
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

    def get_target(self):
        target = None
        minimum = math.inf
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
    def __init__(self, app, x=150, y=HEIGHT // 2):
        super(MyBase, self).__init__(app, 1000, None, app.all_sprites, app.my_units, app.my_buildings)
        self.app = app
        self.image = pg.surface.Surface((150, 150))
        self.image.fill(MY_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def killed(self):
        self.hp_bar.kill()
        self.kill()
        self.app.lose()


class EnemyBase(SpriteHp):
    def __init__(self, app, x=WIDTH - 150, y=HEIGHT // 2):
        super(EnemyBase, self).__init__(app, 1000, None, app.all_sprites, app.enemy_units, app.enemy_buildings)
        self.app = app
        self.image = pg.surface.Surface((150, 150))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def killed(self):
        self.hp_bar.kill()
        self.kill()
        self.app.win()


class Knight(Unit):
    def __init__(self, app, x, y, side=0):
        if side == 0:
            self.color = MY_COLOR
            self.enemy_units = app.enemy_units
            self.my_group = app.my_units
        elif side == 1:
            self.color = ENEMY_COLOR
            self.enemy_units = app.my_units
            self.my_group = app.enemy_units
        super().__init__(app, 100, None, self.enemy_units, self.my_group)
        self.image = pg.surface.Surface((50, 50))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.attack_distance = 100
        self.speed = 100
        self.shoot_speed = 1
        self.damage = 10

    def update(self):
        target = self.get_target()
        target_x, target_y = target.rect.centerx, target.rect.centery
        angle = math.acos((self.y - target_y) / (math.sqrt((self.y - target_y) ** 2 + (self.x - target_x) ** 2)))
        if target_x < self.x:
            angle = -angle
        target_distance = math.sqrt((self.y - target_y) ** 2 + (self.x - target_x) ** 2)
        if self.attack_distance <= target_distance:
            self.x += math.sin(angle) * self.speed / self.app.fps
            self.y -= math.cos(angle) * self.speed / self.app.fps
            self.rect.x = self.x
            self.rect.y = self.y
        else:
            self.attack(target, self.damage)
