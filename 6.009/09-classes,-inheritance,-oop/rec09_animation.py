import pygame, sys, time
from pygame.locals import  *
from rec09_solution import *
# Change the above to just "rec09" instead of "rec09_solution" to work with our starting point!

class pgObject():
    def __init__(self, base, size, col, name):
        self.base = base
        self.size = size
        self.color = col
        self.name = name
        self.next = (0, 0)
        self.obj = None

    def pgRect(self, frac=0.0):
        if self.next[0] > 0 or self.next[1] > 0:
            return pygame.Rect(self.base[0]*(1.0 - frac) + self.next[0]*frac,
                               self.base[1]*(1.0 - frac) + self.next[1]*frac, self.size[0], self.size[1])
        else:
            return pygame.Rect(self.base[0], self.base[1], self.size[0], self.size[1])

    def pgColor(self):
        return self.color

    def pgDraw(self, win, font, color, frac=0.0):
        cord = (self.base[0]*(1.0 - frac) + self.next[0]*frac,
                self.base[1]*(1.0 - frac) + self.next[1]*frac)
        pygame.draw.rect(win, self.pgColor(), self.pgRect(frac))
        text = font.render(self.name, True, color, self.pgColor())
        textRect = text.get_rect()
        textRect.topleft = (cord[0] + 2, cord[1] + 2)
        win.blit(text, textRect)



class pgQueue(pgObject):
    def __init__(self, x, y,  queue):
        super().__init__((x, y+25), (200 if queue.name != "Finished Goods" else 350, 50), (0,200,200), queue.name)
        self.obj = queue

class pgMachine(pgObject):
    def __init__(self, x, y,  machine):
        super().__init__((x, y), (200, 100), (200,100,100), machine.__class__.__name__)
        self.obj = machine
        self.status = "foo"

    def pgMacDraw(self, win, font, color):
        text = font.render(self.status, True, color, self.pgColor())
        textRect = text.get_rect()
        textRect.topleft = (self.base[0] + 2, self.base[1] + 80)
        win.blit(text, textRect)


class pgPart(pgObject):
    def __init__(self, part):
        super().__init__((0, 0), (40, 20), (250, 250, 250), f"{part.__class__.__name__}({part.id})")
        self.obj = part

class pgFactory():
    WINDOWWIDTH = 1800
    WINDOWHEIGHT = 800

    MOVESPEED = 4
    EPOCH = 100

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)

    def __init__(self):
        pygame.init()
        self.windowSurface = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT), 0, 32)
        pygame.display.set_caption('Factory Floor')
        pygame.font.init()
        self.font1 = pygame.font.Font('freesansbold.ttf', 12)
        self.font2 = pygame.font.SysFont("sans", 9)
        self.objs = []
        self.parts = []


    def setup(self, stuff):
        nl = len(stuff)
        nh = 0
        for s in stuff:
            if isinstance(s, list):
                nh = max(nh, len(s))

        xoff = self.WINDOWWIDTH/(nl+1)
        yoff = self.WINDOWHEIGHT/(nh+2)

        x = xoff
        for s in stuff:
            if isinstance(s, list):
                y = self.WINDOWHEIGHT/2 - yoff/len(s)
                for obj in s:
                    self.addobj(obj, x, y)
                    y += yoff
            else:
                self.addobj(s, x, self.WINDOWHEIGHT/2)
            x += xoff

    def addobj(self, obj, x, y):
        if isinstance(obj, ConveyorBelt):
            q = pgQueue(x, y, obj)
            self.objs.append(q)
        if isinstance(obj, Machine):
            m = pgMachine(x, y, obj)
            self.objs.append(m)


    def run_epoch(self):
        # reset start
        for p in self.parts:
            p.base = p.next

        # add update the locations of all parts
        newparts = []
        for obj in self.objs:
            x = obj.base[0] + 45*len(obj.obj.parts) - 40
            y = obj.base[1] + 25
            for p in obj.obj.parts:
                self.update_part(p, (x, y), newparts)
                x -= 45
            if isinstance(obj, pgMachine):
                obj.status = f"remaining {obj.obj.time_remaining} of {obj.obj.tat}"
        self.parts = newparts

        # now run animation
        for i in range(self.EPOCH):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.windowSurface.fill(self.BLACK)

            for q in self.objs:
                q.pgDraw(self.windowSurface, self.font1, self.BLACK)
                if isinstance(q, pgMachine):
                    q.pgMacDraw(self.windowSurface, self.font2, self.BLACK)

            for p in self.parts:
                p.pgDraw(self.windowSurface, self.font2,self.BLACK, float(i)/float(self.EPOCH))

            pygame.display.update()
            time.sleep(0.01)



    def get_part(self, part):
        for p in self.parts:
            if p.obj == part.obj:
                return p
        return None

    def update_part(self, part, cord, newparts):
        pgp = self.get_part(pgPart(part))
        if pgp == None:
            inclpgp = None
            if isinstance(part, Assembly):
                incl = part.sub[0]
                inclpgp = self.get_part(pgPart(incl))
            pgp = pgPart(part)
            if inclpgp:
                pgp.base = inclpgp.base
            else:
                pgp.base = (-30, self.WINDOWHEIGHT/2)
        newparts.append(pgp)
        pgp.next = cord



class pgAnime(Anime):
    def __init__(self):
        self.pg = pgFactory()

    def run_epoh(self):
        self.pg.run_epoch()

    def setup(self, mylist):
        self.pg.setup(mylist)

def animateTinyFactory():
    runTinyFactory(pgAnime())

def animateToyFactory():
    runToyFactory(pgAnime())
