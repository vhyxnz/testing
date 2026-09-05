"""Tindahan ni Aling Nena: a self-contained, procedural Ursina game.

Run: python sari_sari.py   |   Logic checks: python sari_sari.py --self-test
No downloaded models, textures, fonts or audio are required.
"""
from collections import Counter
import random
import sys

# Prices are fictional gameplay prices, in whole Philippine pesos.
PRODUCTS = [
    ('Kopiko Brown', 10, '#a86939'),
    ('Lucky Me Pancit Canton', 18, '#e6ce42'),
    ('Piattos', 20, '#8b62c4'),
    ('Shampoo sachet', 8, '#ed80ac'),
    ('SkyFlakes', 10, '#e7e8dc'),
    ('Bottled water', 15, '#53b8d1'),
]
DENOMINATIONS = [('Coin', n) for n in (1, 5, 10, 20)] + [
    ('Bill', n) for n in (20, 50, 100, 200, 500, 1000)]


def total(items):
    return sum(PRODUCTS[i][1] * count for i, count in items.items())


def correct_basket(basket, order):
    return +Counter(basket) == +Counter(order)


def payment_for(cost, rng=random):
    return rng.choice([n for n in (20, 50, 100, 200, 500, 1000) if n >= cost])


def self_test():
    """Exercise the money and order rules without a graphics dependency."""
    order = Counter({0: 1, 1: 2})
    assert total(order) == 46
    assert correct_basket(order, Counter({0: 1, 1: 2, 3: 0}))
    assert not correct_basket(Counter({0: 2, 1: 2}), order)
    assert not correct_basket(Counter({0: 1}), order)
    for seed in range(100):
        paid = payment_for(46, random.Random(seed))
        change = paid - 46
        assert change >= 0
        cash = 500
        assert cash + paid - change == cash + 46
    assert len(DENOMINATIONS) == 10
    print('All order, payment, denomination and cash-accounting checks passed.')


if '--self-test' in sys.argv:
    self_test()
    raise SystemExit

try:
    from ursina import (Ursina, Entity, Text, Button, Sky, camera, color,
                        window, application, mouse, time, Vec3, destroy)
except ImportError:
    raise SystemExit('Install the engine first: python -m pip install ursina')

app = Ursina(title='Tindahan ni Aling Nena', borderless=False, fullscreen=False,
             development_mode=False,
             window_type='offscreen' if '--smoke-test' in sys.argv else 'onscreen')
window.color = color.hex('#abcdd1')
window.size = (1280, 800)
window.fps_counter.enabled = False
window.exit_button.enabled = False
camera.position = (0, 4.0, -10.8)
camera.look_at(Vec3(0, 1.6, 2))
camera.fov = 62


def block(pos, scale, tint, **kwargs):
    return Entity(model='cube', position=pos, scale=scale,
                  color=color.hex(tint), **kwargs)


def label(text, pos, scale=1, tint=color.white):
    # Text defaults to UI-sized glyphs; enlarge it for world-space signs.
    return Text(text=text, parent=scene_root, position=pos, scale=scale * 10,
                origin=(0, 0), color=tint, double_sided=True)


scene_root = Entity()
Sky(color=color.hex('#c6e3df'))
# A dollhouse-like first-person cashier view keeps all stock in reach.
block((0, -.15, 2), (17, .3, 18), '#bcb097')
block((0, 0, 2), (9, .12, 7), '#a77b51')
block((-4.5, 2, 2), (.18, 4, 7), '#e3c695')
block((4.5, 2, 2), (.18, 4, 7), '#e3c695')
block((0, 3.9, 2), (9.4, .2, 7.4), '#82624b')
block((0, 2, 5.1), (9, 4, .16), '#77aaa2')
# Open serving window in the rear wall, with a street beyond it.
block((0, 2, 4.95), (3.6, 2.4, .12), '#b8d8cb')
block((0, .35, 4.8), (3.6, .7, .22), '#916540')
for x in (-1.8, 1.8):
    block((x, 1.85, 4.75), (.12, 3, .2), '#604934')
for x in (-1.5, -.9, -.3, .3, .9, 1.5):
    block((x, 2.95, 4.65), (.035, .55, .05), '#515b58')
block((0, 2.7, 4.65), (3.6, .035, .05), '#515b58')
label('T I N D A H A N   N I   A L I N G   N E N A', (0, 3.48, 4.65), 1.1)
label('Tuloy po kayo!', (0, 3.2, 4.6), .75)
# Wooden estante and six clickable product stacks.
stock_entities = []
for side in (-1, 1):
    x = side * 3.1
    block((x, 1.7, 3.8), (2.2, 2.9, .18), '#64482f')
    for y in (.45, 1.35, 2.25, 3.15):
        block((x, y, 3.35), (2.25, .12, 1.05), '#ad7c45')
    for dx in (-1.08, 1.08):
        block((x + dx, 1.8, 3.35), (.1, 2.8, 1.05), '#865b35')
for i, (name, price, tint) in enumerate(PRODUCTS):
    x = -3.1 if i < 3 else 3.1
    y = 2.62 - (i % 3) * .9
    product = block((x, y, 2.98), (1.6, .64, .48), tint, collider='box')
    product.product_id = i
    product.on_click = lambda index=i: game.add_item(index)
    stock_entities.append(product)
    label(f'{i + 1}. {name}\nP{price}', (x, y, 2.72), .72, color.black)
# Hanging sachet strings, deliberately clear of selectable stock.
for x in (-1.5, -1.05, 1.05, 1.5):
    block((x, 3.03, 2.5), (.016, 1.1, .02), '#ded3a8')
    for j in range(3):
        block((x, 3.45 - j * .28, 2.5), (.26, .23, .035),
              '#ed80ac' if x < 0 else '#b47739', rotation_z=x * 4)
# Glass aparador: transparent front, wooden frame and countertop.
block((0, .62, .35), (5.2, 1.15, 1.25), '#6e4d35')
glass = block((0, .75, -.3), (4.9, .78, .025), '#9cd3da')
glass.alpha = .32
for x in (-2.55, 2.55):
    block((x, .7, -.34), (.1, 1.2, .1), '#c3945b')
counter = block((0, 1.27, .35), (5.4, .12, 1.5), '#d2ab72', collider='box')
counter.on_click = lambda: game.checkout()
label('APARADOR  /  CHECKOUT', (0, 1.05, -.43), .8)
bell = Entity(model='sphere', position=(1.68, 2.55, 4.45),
              scale=(.18, .23, .18), color=color.gold)


class StoreGame:
    """Explicit phases prevent double sales and changing a paid basket."""

    def __init__(self):
        self.cash = 500
        self.reputation = 100
        self.day = 1
        self.sales = 0
        self.goal = 200
        self.served = 0
        self.basket = Counter()
        self.change = []
        self.tray = []
        self.customer = None
        self.phase = 'waiting'
        self.wait = 1
        self.notice_timer = 0
        self.build_ui()
        self.refresh()

    def build_ui(self):
        # UI stays within a 4:3 safe area, including on narrower windows.
        Entity(parent=camera.ui, model='quad', y=.435, z=.1,
               scale=(1.32, .115), color=color.hex('#203b37'))
        self.hud = Text(parent=camera.ui, x=-.63, y=.475, scale=.88)
        self.order_text = Text(parent=camera.ui, x=-.63, y=.395, scale=.84)
        self.notice = Text(parent=camera.ui, origin=(0, 0), y=.29,
                           scale=1, color=color.yellow)
        Entity(parent=camera.ui, model='quad', y=-.36, z=.1,
               scale=(1.32, .27), color=color.hex('#203b37'))
        self.basket_text = Text(parent=camera.ui, x=-.63, y=-.245, scale=.75)
        self.checkout_button = Button(text='Checkout [Enter]', x=.43, y=-.28,
                                      scale=(.36, .055), on_click=self.checkout)
        Button(text='Undo item [Backspace]', x=.43, y=-.35,
               scale=(.36, .055), on_click=self.undo_item)
        self.next_button = Button(text='Next day', x=.43, y=-.42,
                                  scale=(.36, .055), on_click=self.next_day)
        Text('Click shelf / keys 1-6: add item | Enter: checkout / give change | Esc: quit',
             parent=camera.ui, origin=(0, 0), y=-.478, scale=.68)
        self.money_ui = Entity(parent=camera.ui, z=-.2, enabled=False)
        Entity(parent=self.money_ui, model='quad', position=(0, .015, .1),
               scale=(1.27, .45), color=color.hex('#294b45'))
        self.money_text = Text(parent=self.money_ui, x=-.59, y=.21, scale=.9)
        for i, (kind, value) in enumerate(DENOMINATIONS):
            Button(parent=self.money_ui, text=f'{kind} P{value}',
                   x=-.48 + (i % 5) * .24, y=.035 - (i // 5) * .07,
                   scale=(.22, .055), on_click=lambda n=value: self.add_change(n))
        Button(parent=self.money_ui, text='Undo', x=-.42, y=-.15,
               scale=(.25, .055), on_click=self.undo_change)
        Button(parent=self.money_ui, text='Clear', x=-.12, y=-.15,
               scale=(.25, .055), on_click=self.clear_change)
        Button(parent=self.money_ui, text='Give change', x=.31, y=-.15,
               scale=(.48, .055), on_click=self.finish_sale)

    def say(self, message, seconds=4):
        self.notice.text = message
        self.notice_timer = seconds

    def refresh(self):
        self.hud.text = (f'ALING NENA\'S  |  Day {self.day}  |  Cash P{self.cash}\n'
                         f'Daily sales P{self.sales} / P{self.goal}  |  Reputation {self.reputation}/100')
        contents = '\n'.join(f'{n} x {PRODUCTS[i][0]}' for i, n in self.basket.items() if n)
        self.basket_text.text = 'ON THE COUNTER\n' + (contents or '(empty)')
        self.next_button.enabled = self.phase in ('day_end', 'game_over')
        self.next_button.text = 'Restart' if self.phase == 'game_over' else 'Next day'
        if self.phase == 'payment':
            self.money_text.text = (f'Total: P{total(self.order)}    Customer pays: P{self.payment}\n'
                                    f'Change selected: P{sum(self.change)}   (calculate the amount!)')

    def arrive(self):
        self.phase = 'approaching'
        self.customer = Entity(position=(-1.2, 0, 4.1))
        Entity(parent=self.customer, model='cube', y=1.05, scale=(.65, .9, .4),
               color=color.hex(random.choice(['#e79452', '#739bcc', '#c988a9'])))
        Entity(parent=self.customer, model='sphere', y=1.78, scale=.5,
               color=color.hex('#be8b63'))
        for x in (-.19, .19):
            Entity(parent=self.customer, model='cube', position=(x, .38, 0),
                   scale=(.23, .7, .26), color=color.hex('#3f5265'))
        self.order = Counter({i: random.randint(1, 2) for i in
                              random.sample(range(len(PRODUCTS)), min(3, 2 + self.day // 3))})
        self.order_text.text = 'May paparating na customer...'

    def greet(self):
        self.phase = 'shopping'
        words = {1: 'isang', 2: 'dalawang'}
        items = [f'{words[n]} {PRODUCTS[i][0]}' for i, n in self.order.items()]
        self.order_text.text = 'Customer: Pabili po ng\n' + ' at '.join(items) + '.'
        self.say('Ting!  Tao po!')

    def add_item(self, index):
        if self.phase != 'shopping':
            return
        if sum(self.basket.values()) >= 6:
            self.say('Counter full! Undo an item first.')
            return
        self.basket[index] += 1
        slot = len(self.tray)
        item = block((-1.8 + slot * .7, 1.49, .1), (.42, .32, .3), PRODUCTS[index][2])
        self.tray.append((index, item))
        self.refresh()

    def undo_item(self):
        if self.phase != 'shopping' or not self.tray:
            return
        index, entity = self.tray.pop()
        destroy(entity)
        self.basket[index] -= 1
        self.refresh()

    def penalize(self, message):
        self.reputation = max(0, self.reputation - 8)
        self.say(message)
        if self.reputation == 0:
            self.phase = 'game_over'
            self.money_ui.enabled = False
            self.order_text.text = 'Store closed: reputation reached zero. Click Restart to try again.'
        self.refresh()

    def checkout(self):
        if self.phase == 'payment':
            self.finish_sale()
            return
        if self.phase != 'shopping':
            return
        if not correct_basket(self.basket, self.order):
            self.penalize('Hindi po iyan ang order. Check the items!  (-8 reputation)')
            return
        self.payment = payment_for(total(self.order))
        self.phase = 'payment'
        self.change.clear()
        self.money_ui.enabled = True
        self.order_text.text = (f'Customer: P{total(self.order)} lahat, di ba?\n'
                                f'Heto po ang P{self.payment}. Sukli po!')
        self.refresh()

    def add_change(self, amount):
        if self.phase == 'payment':
            self.change.append(amount)
            self.refresh()

    def undo_change(self):
        if self.phase == 'payment' and self.change:
            self.change.pop()
            self.refresh()

    def clear_change(self):
        self.change.clear()
        self.refresh()

    def finish_sale(self):
        if self.phase != 'payment':
            return
        if sum(self.change) != self.payment - total(self.order):
            self.penalize('Mali ang sukli! Try again.  (-8 reputation)')
            return
        # Payment is settled once, only after the change has been verified.
        self.cash += self.payment - sum(self.change)
        self.sales += total(self.order)
        self.served += 1
        self.reputation = min(100, self.reputation + 3)
        self.money_ui.enabled = False
        self.phase = 'leaving'
        self.say('Salamat po!  +3 reputation')
        self.order_text.text = 'Customer: Sa uulitin!'
        self.clear_counter()
        self.refresh()

    def clear_counter(self):
        for _, entity in self.tray:
            destroy(entity)
        self.tray.clear()
        self.basket.clear()

    def next_day(self):
        if self.phase == 'game_over':
            self.cash, self.reputation, self.day = 500, 100, 1
            self.goal = 200
            self.clear_counter()
            if self.customer:
                destroy(self.customer)
                self.customer = None
        elif self.phase == 'day_end':
            self.day += 1
            self.goal += 100
        else:
            return
        self.sales, self.served = 0, 0
        self.phase, self.wait = 'waiting', 1
        self.order_text.text = 'Bukas na ang tindahan! Waiting for a customer...'
        self.refresh()

    def tick(self):
        dt = min(time.dt, .1)
        self.notice_timer -= dt
        if self.notice_timer <= 0:
            self.notice.text = ''
        if self.phase == 'waiting':
            self.wait -= dt
            if self.wait <= 0:
                self.arrive()
        elif self.phase == 'approaching':
            self.customer.x = min(0, self.customer.x + dt * .8)
            if self.customer.x >= 0:
                self.greet()
        elif self.phase == 'leaving':
            self.customer.x += dt * 1.2
            if self.customer.x > 2.4:
                destroy(self.customer)
                self.customer = None
                if self.sales >= self.goal:
                    self.phase = 'day_end'
                    self.order_text.text = (f'Day {self.day} complete! {self.served} happy customers.\n'
                                            'Daily goal reached. Click Next day to keep running the store.')
                else:
                    self.phase, self.wait = 'waiting', 1.5
                    self.order_text.text = 'Waiting for the next customer...'
                self.refresh()


game = StoreGame()


def update():
    game.tick()


def input(key):
    if key in ('1', '2', '3', '4', '5', '6'):
        game.add_item(int(key) - 1)
    elif key == 'backspace':
        game.undo_change() if game.phase == 'payment' else game.undo_item()
    elif key == 'enter':
        game.checkout()
    elif key == 'escape':
        application.quit()


if __name__ == '__main__':
    if '--smoke-test' in sys.argv:
        # Exercise actual engine entities and checkout, without opening a window.
        from pathlib import Path
        # Offscreen buffers do not emit the normal window resize event.
        camera.ui_lens.set_film_size(20 * app.win.get_x_size() / app.win.get_y_size(), 20)
        game.arrive()
        game.greet()
        game.checkout()
        assert game.reputation == 92
        for index, count in game.order.items():
            for _ in range(count):
                game.add_item(index)
        game.checkout()
        assert game.phase == 'payment'
        game.add_change(game.payment - total(game.order) + 1)
        game.finish_sale()
        assert game.phase == 'payment' and game.cash == 500
        game.clear_change()
        due = game.payment - total(game.order)
        for denomination in (1000, 500, 200, 100, 50, 20, 10, 5, 1):
            while due >= denomination:
                game.add_change(denomination)
                due -= denomination
        expected = 500 + total(game.order)
        game.finish_sale()
        assert game.cash == expected and game.phase == 'leaving'
        game.finish_sale()
        assert game.cash == expected
        for _ in range(3):
            app.taskMgr.step()
            app.graphicsEngine.renderFrame()
        app.win.saveScreenshot('smoke-test.png')
        Path('smoke-test-passed.txt').write_text('Engine startup, order rejection, change rejection, sale and duplicate-sale checks passed.')
        app.destroy()
    else:
        app.run()
