import numpy as np
import matplotlib.pyplot as plt

class Box():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
class Bead():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.v_x = 0.0
        self.v_y = 0.0
        self.a_x = 0.0
        self.a_y = 0.0
    def Move_Bead(self,dt): # ff
        self.x += self.v_x * dt + 0.5 * self.a_x * dt ** 2
        self.y += self.v_y * dt + 0.5 * self.a_y * dt ** 2

class System():
    def __init__(self,dt,n,r_c,att):
        self.dt = dt
        self.n = n
        self.lst_beads = list()
        self.dbl_list= [(i,j) for i in range(self.n-1) for j in range(i+1,self.n)]
        self.r_c = r_c
        self.att = att
        
    def initial_configuration(self,box):
        X = np.random.uniform(-box.x/2,box.x/2, self.n)
        Y = np.random.uniform(-box.y/2,box.y/2, self.n)
        # print(X)
        self.lst_beads=[Bead(x,y) for x,y in zip(X,Y)]
    def force(self,r):
        if r<self.r_c:
            return self.att * (1 - r / self.r_c)
        else:
            return 0.0
    def pair_interaction(self,bead1,bead2): #ff
        dx = bead1.x - bead2.x
        dy = bead1.y - bead2.y
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
            b.Move_Bead(self.dt)    
              
def show_beads(sys,box):
    
    x = [bead.x for bead in sys.lst_beads]
    y = [bead.y for bead in sys.lst_beads]
    plt.plot(x,y,'o')
    plt.xlim(-box.x/2,box.x/2)
    plt.ylim(-box.y/2,box.y/2)
    plt.show()
      
if __name__ == '__main__':
    box = Box(10,10)    
    sys = System(dt = 0.1, n = 40, r_c = 2, att = 2)
    sys.initial_configuration(box)
    show_beads(sys,box)
    for _ in range(1000):
        sys.step()
        #print(sys.lst_beads[0].x)
    show_beads(sys,box)
    # print(sys.dbl_list)
    

                    
        
        
       
