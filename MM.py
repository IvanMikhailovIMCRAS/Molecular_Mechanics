import numpy as np
import matplotlib.pyplot as plt

def periodic(coord, box):
        if abs(coord) > 0.5 * box: 
            return coord - np.sign(coord) * box
        return coord

class Box():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def periodic_correct(self, xb, yb):
        return periodic(xb, self.x), periodic(yb, self.y)
        
class Bead():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.v_x = 0.0
        self.v_y = 0.0
        self.a_x = 0.0
        self.a_y = 0.0
    def move_bead(self,dt): # ff
        self.x += self.v_x * dt + 0.5 * self.a_x * dt ** 2
        self.y += self.v_y * dt + 0.5 * self.a_y * dt ** 2

class System():
    def __init__(self, dt, n, box, r_c,att):
        self.dt = dt
        self.n = n
        self.box = box
        self.r_c = r_c
        self.att = att
        self.lst_beads = list()
        self.dbl_list= [(i,j) for i in range(self.n-1) for j in range(i+1,self.n)]
        
    def initial_configuration(self):
        X = np.random.uniform(-self.box.x/2, self.box.x/2, self.n)
        Y = np.random.uniform(-self.box.y/2, self.box.y/2, self.n)
        self.lst_beads=[Bead(x,y) for x,y in zip(X,Y)]
    def force(self,r):
        if r<self.r_c:
            return self.att * (1 - r / self.r_c)
        else:
            return 0.0
    def pair_interaction(self,bead1,bead2):
        dx = bead1.x - bead2.x
        dy = bead1.y - bead2.y
        dx, dy = self.box.periodic_correct(dx, dy)
        r = np.sqrt(dx**2+dy**2)
        bead1.a_x += self.force(r)*dx/r
        bead1.a_y += self.force(r)*dy/r
        bead2.a_x += -self.force(r)*dx/r
        bead2.a_y += -self.force(r)*dy/r
    def step(self):
        for b in self.lst_beads:
            b.a_x = 0
            b.a_y = 0
        for pt in self.dbl_list:
            self.pair_interaction(self.lst_beads[pt[0]],self.lst_beads[pt[1]])
        for b in self.lst_beads:
            b.move_bead(self.dt)  
            b.x, b.y = self.box.periodic_correct(b.x, b.y)  
              
def show_beads(sys):
    plt.figure(figsize=(5,5))
    x = [bead.x for bead in sys.lst_beads]
    y = [bead.y for bead in sys.lst_beads]
    plt.plot(x,y,'o')
    plt.xlim(-sys.box.x/2, sys.box.x/2)
    plt.ylim(-sys.box.y/2, sys.box.y/2)
    plt.show()
      
if __name__ == '__main__':
    box = Box(5,5)    
    sys = System(dt = 0.1, n = 75, box=box, r_c = 1.0, att = 1.0)
    sys.initial_configuration()
    show_beads(sys)
    for _ in range(100):
        sys.step()
    show_beads(sys)
