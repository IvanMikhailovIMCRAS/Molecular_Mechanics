import numpy as np
import matplotlib.pyplot as plt
import os

def periodic(coord, box):
        if abs(coord) > 0.5 * box: 
            return coord - np.sign(coord) * box
        return coord

class ForceField():
    def __init__(self, r_c, att):
        self.r_c = r_c
        self.att = att
        
    def force(self, r):
        if r < self.r_c:
            return self.att * (1 - r / self.r_c)
        else:
            return 0.0
        
    

class Box():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def periodic_correct(self, xb, yb):
        return periodic(xb, self.x), periodic(yb, self.y)
        
class Bead():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v_x = np.random.uniform(-2.0, 2.0)
        self.v_y = np.random.uniform(-2.0, 2.0)
        self.a_x = 0.0
        self.a_y = 0.0
    def move_bead(self, dt): # ff
        self.v_x += self.a_x * dt 
        self.v_y += self.a_y * dt 
        self.x += self.v_x * dt + 0.5 * self.a_x * dt ** 2
        self.y += self.v_y * dt + 0.5 * self.a_y * dt ** 2

class System():
    def __init__(self, dt, n, box, ff):
        self.dt = dt
        self.n = n
        self.box = box
        self.ff = ff
        self.lst_beads = list()
        self.dbl_list= [(i,j) for i in range(self.n-1) for j in range(i+1,self.n)]
        
    def initial_configuration(self):
        X = np.random.uniform(-self.box.x/2, self.box.x/2, self.n)
        Y = np.random.uniform(-self.box.y/2, self.box.y/2, self.n)
        self.lst_beads=[Bead(x,y) for x,y in zip(X,Y)]
    
    def pair_interaction(self, bead1, bead2):
        dx = bead1.x - bead2.x
        dy = bead1.y - bead2.y
        dx, dy = self.box.periodic_correct(dx, dy)
        r = np.sqrt(dx**2+dy**2)
        bead1.a_x += self.ff.force(r)*dx/r
        bead1.a_y += self.ff.force(r)*dy/r
        bead2.a_x += -self.ff.force(r)*dx/r
        bead2.a_y += -self.ff.force(r)*dy/r
    def step(self):
        for b in self.lst_beads:
            b.a_x = 0
            b.a_y = 0
        for pt in self.dbl_list:
            self.pair_interaction(self.lst_beads[pt[0]], self.lst_beads[pt[1]])
        thermostat(self.lst_beads)
        for b in self.lst_beads:
            b.move_bead(self.dt)  
            b.x, b.y = self.box.periodic_correct(b.x, b.y)  
              
    
def show_beads(sys, namefile='Pic', num_pic=-1):
    plt.figure(figsize=(5,5))
    x = [bead.x for bead in sys.lst_beads]
    y = [bead.y for bead in sys.lst_beads]
    plt.plot(x,y,'o')
    plt.xlim(-sys.box.x/2, sys.box.x/2)
    plt.ylim(-sys.box.y/2, sys.box.y/2)
    if num_pic < 0:
        plt.show()
    else:
        namefile = namefile + '{:04d}'.format(num_pic) + '.jpg'
        plt.savefig(namefile)  

def animation(delay=10, loop=0, namegif='animatedGIF1'):
    #Gifanimationmaker should be installed: sudo apt-get install imagemagick
    os.system(f'convert -delay {delay} -loop {loop} *.jpg {namegif}.gif')
    os.system('rm *.jpg') 

def thermostat(list_beads):
    sum_vx = 0
    sum_vy = 0
    for bead in list_beads:
        sum_vx += bead.v_x**2
        sum_vy += bead.v_y**2
    sum_vx, sum_vy = np.sqrt(sum_vx/len(list_beads)), np.sqrt(sum_vy/len(list_beads))
    if (sum_vx != 0) & (sum_vy != 0):
        for bead in list_beads:
            bead.v_x = bead.v_x / sum_vx
            bead.v_y = bead.v_y / sum_vx
    
           
      
if __name__ == '__main__':
    box = Box(5,5)    
    ff = ForceField(r_c = 1.0, att = 1.0)
    sys = System(dt = 0.02, n = 75, box=box, ff=ff)
    sys.initial_configuration()
    show_beads(sys, num_pic=0)
    for n_step in range(1000):
        sys.step()
        print(sys.lst_beads[0].v_x)
        if n_step % 10 == 0:
            show_beads(sys, num_pic=n_step+1)
    animation()
    
