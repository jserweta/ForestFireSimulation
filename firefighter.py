class Firefighter():

    hp = 100
    locX = None
    locY = None
    orderX = None
    orderY = None
    id: int
    state = 'free'

    def __init__(self, id: int):
        self.id = id

    def assign(self, i, j):
        if self.state =='dead':
            return
        else:
           self.locX = i
           self.locY = j
           self.state = 'busy'

    def update(self, fireState):
        if (fireState == 0 or fireState == 7) and self.state != 'dead':
            self.free()
        elif self.orderX or self.orderY:
            self.move()
        else:
            self.hp -= 10
            if self.hp <= 0:
                self.state = 'dead'

    def free(self):
        if self.state == 'dead':
            return
        self.locY = None
        self.locX = None
        self.state = 'free'
        self.hp -= 10

    def move(self):
        if self.state != 'dead':
            if self.orderX:
                distanceX = abs(self.locX - self.orderX)
                if distanceX <= 2:
                    self.locX = self.orderX
                    self.orderX = None
                else:
                    self.locX = self.move2(self.locX, self.orderX)

            if self.orderY:
                distanceY = abs(self.locY - self.orderY)
                if distanceY <= 2:
                    self.locY = self.orderY
                    self.orderY = None
                else:
                    self.locY = self.move2(self.locY, self.orderY)

            if self.orderX or self.orderY:
                self.state = 'moving'
            else :
                self.state = 'busy'

    def move2(self, loc, order):
        if self.state != 'dead':
            if (order < loc):
                return loc - 2
            return loc + 2

    def getGoal(self):
        x = self.orderX
        y = self.orderY
        if not x:
            x = self.locX
        if not y:
            y = self.locY
        return (x, y)