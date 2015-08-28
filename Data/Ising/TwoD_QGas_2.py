
# coding: utf-8

# In[2]:

import numpy as np
import scipy
import scipy.signal
import random
import numpy.fft
import matplotlib.pyplot as plt
exp=np.exp
arange=np.arange

class Particle(object):
    
    def __init__(self,index,state,position,pairing=None,bell_state=None,bell_state_time=None):
        self.index=index
        self.pairing=pairing
        self.state=state
        self.bell_state=bell_state
        self.position=position
        self.bell_state_time=bell_state_time


# In[4]:

class Gas(list):
    def __init__(self, y_length, x_length, Temperature):
        pars = [[Particle(i,random.choice([-1,1]),[i,j]) for i in range(x_length)] for j in range(y_length)]
        k=0
        for i in range(len(pars)):
            for j in range(len(pars[0])):
                pars[i][j]=Particle(k,random.choice([-1,1]),[i,j])
                k=k+1
        super(Gas,self).__init__(pars)
        self.Temperature=Temperature
    
    def x_length(self):
        return len(self[0])
    
    def y_length(self):
        return len(self)
    
    def shape(self):
        return [self.y_length(), self.x_length()]
    
    def size(self):
        return self.y_length()*self.x_length()
    
    def indexes(self):
        return np.array([[self[i][j].index for j in range(len(self[0]))] for i in range(len(self))])
    
    def pairings(self):
        return np.array([[self[i][j].pairing for j in range(len(self[0]))] for i in range(len(self))])
    
    def states(self):
        return np.array([[self[i][j].state for j in range(len(self[0]))] for i in range(len(self))])
    
    def positions(self):
        return np.array([[self[i][j].position for j in range(len(self[0]))] for i in range(len(self))])
    
    def bell_states(self):
        return np.array([[self[i][j].bell_state for j in range(len(self[0]))] for i in range(len(self))])
    
    def bell_state_times(self):
        return np.array([[self[i][j].bell_state_time for j in range(len(self[0]))] for i in range(len(self))])
    
    def move(self, max_vel_temp):
        new=Gas(self.y_length(), self.x_length(), self.Temperature)
        for i in range(self.y_length()):
            for j in range(self.x_length()):
                new[i][j]=Particle('empty','none','none')
        
        vmax_x=self.x_length()
        vmax_y=self.y_length()
        for i in range(self.y_length()):
            for j in range(self.x_length()):
                moved='no'
                num = random.gauss(len(self)*(1.-exp(-self.Temperature/max_vel_temp)),(len(self)*(1.-exp(-self.Temperature/max_vel_temp)))/2.)
                velocity = int(abs(num))
                direction = random.random()
                #print(direction)
                
                if velocity==0:
                    #print(velocity)
                    if new[i][j].index=='empty':
                        new[i][j]=self[i][j]
                    else:
                        for k in range(self.y_length()):
                            for p in range(self.x_length()):
                                if new[k][p].index=='empty':
                                    new[k][p]=self[i][j]
                                    moved='yes'
                                    break
                            if moved=='yes':
                                break
            
                elif direction<=0.5:
                    if velocity > vmax_x:
                        velocity = vmax_x
                    #print(velocity)
                    
                    if direction > 0.25 and direction <= 0.5:
                        if velocity > (self.x_length()-j-1):
                            for m in range(velocity-(self.x_length()-j),-1,-1):
                                if new[i][m].index=='empty':
                                    new[i][m]=self[i][j]
                                    moved='yes'
                                    break
                            if moved=='no':
                                for m in range(self.x_length()-1,j-1,-1):
                                    if new[i][m].index=='empty':
                                        new[i][m]=self[i][j]
                                        moved='yes'
                                        break
                                if moved=='no':
                                    for k in range(self.y_length()):
                                        for p in range(self.x_length()):
                                            if new[k][p].index=='empty':
                                                new[k][p]=self[i][j]
                                                moved='yes'
                                                break
                                        if moved=='yes':
                                            break
                                
                        else:
                            for m in range(j+velocity,j-1,-1):
                                if new[i][m].index=='empty':
                                    new[i][m]=self[i][j]
                                    moved='yes'
                                    break
                    
                            if moved=='no':
                                for k in range(self.y_length()):
                                    for p in range(self.x_length()):
                                        if new[k][p].index=='empty':
                                            new[k][p]=self[i][j]
                                            moved='yes'
                                            break
                                    if moved=='yes':
                                        break
                                        
                    elif direction <= 0.25:
                        if velocity > j:
                            for m in range(self.x_length()-(velocity-j),self.x_length()):
                                if new[i][m].index=='empty':
                                    new[i][m]=self[i][j]
                                    moved='yes'
                                    break
                            if moved=='no':
                                for m in range(0,j+1):
                                    if new[i][m].index=='empty':
                                        new[i][m]=self[i][j]
                                        moved='yes'
                                        break
                                if moved=='no':
                                    for k in range(self.y_length()):
                                        for p in range(self.x_length()):
                                            if new[k][p].index=='empty':
                                                new[k][p]=self[i][j]
                                                moved='yes'
                                                break
                                        if moved=='yes':
                                            break
                                
                        else:
                            for m in range(j-velocity,j+1):
                                if new[i][m].index=='empty':
                                    new[i][m]=self[i][j]
                                    moved='yes'
                                    break
                            if moved=='no':
                                for k in range(self.y_length()):
                                    for p in range(self.x_length()):
                                        if new[k][p].index=='empty':
                                            new[k][p]=self[i][j]
                                            moved='yes'
                                            break
                                    if moved=='yes':
                                        break
                                            
                elif direction > 0.5:
                    if velocity > vmax_y:
                        velocity = vmax_y
                    #print(velocity)
                    
                    if direction > 0.75:
                        if velocity > (self.y_length()-i-1):
                            for m in range(velocity-(self.y_length()-i),-1,-1):
                                if new[m][j].index=='empty':
                                    new[m][j]=self[i][j]
                                    moved='yes'
                                    break
                            if moved=='no':
                                for m in range(self.y_length()-1,i-1,-1):
                                    if new[m][j].index=='empty':
                                        new[m][j]=self[i][j]
                                        moved='yes'
                                        break
                                if moved=='no':
                                    for k in range(self.y_length()):
                                        for p in range(self.x_length()):
                                            if new[k][p].index=='empty':
                                                new[k][p]=self[i][j]
                                                moved='yes'
                                                break
                                        if moved=='yes':
                                            break
                                
                        else:
                            for m in range(i+velocity,i,-1):
                                if new[m][j].index=='empty':
                                    new[m][j]=self[i][j]
                                    moved='yes'
                                    break
                    
                            if moved=='no':
                                for k in range(self.y_length()):
                                    for p in range(self.x_length()):
                                        if new[k][p].index=='empty':
                                            new[k][p]=self[i][j]
                                            moved='yes'
                                            break
                                    if moved=='yes':
                                        break
                                            
                    elif direction > 0.5 and direction <=0.75:
                        if velocity > i:
                            for m in range(self.y_length()-(velocity-i),self.y_length()+1):
                                if new[m][j].index=='empty':
                                    new[m][j]=self[i][j]
                                    moved='yes'
                                    break
                            if moved=='no':
                                for m in range(0,i+1):
                                    if new[m][j].index=='empty':
                                        new[m][j]=self[i][j]
                                        moved='yes'
                                        break
                                if moved=='no':
                                    for k in range(self.y_length()):
                                        for p in range(self.x_length()):
                                            if new[k][p].index=='empty':
                                                new[k][p]=self[i][j]
                                                moved='yes'
                                                break
                                        if moved=='yes':
                                            break
                                
                        else:
                            for m in range(i-velocity,i+1):
                                if new[m][j].index=='empty':
                                    new[m][j]=self[i][j]
                                    moved='yes'
                                    break
                            if moved=='no':
                                for k in range(self.y_length()):
                                    for p in range(self.x_length()):
                                        if new[k][p].index=='empty':
                                            new[k][p]=self[i][j]
                                            moved='yes'
                                            break
                                    if moved=='yes':
                                        break
                                        
                #print(self.indexes())
                #print(new.indexes())
        for i in range(self.y_length()):
            for j in range(self.x_length()):
                self[i][j]=new[i][j]
                self[i][j].position=[i,j]

                
                
                
    def Ising_Energy(self):
        E=0
        for i in range(self.y_length()):
            for j in range(self.x_length()):
                if i==0 and j!=(self.x_length()-1):
                    E=E+(self[i][j].state*self[self.y_length()-1][j].state)+(self[i][j].state*self[i][j+1].state)
                elif i==0 and j==(self.x_length()-1):
                    E=E+(self[i][j].state*self[self.y_length()-1][j].state)+(self[i][j].state*self[i][0].state)
                elif i!=0 and j!=(self.x_length()-1):
                    E=E+(self[i][j].state*self[i-1][j].state)+(self[i][j].state*self[i][j+1].state)
                elif i!=0 and j==(self.x_length()-1):
                     E=E+(self[i][j].state*self[i-1][j].state)+(self[i][j].state*self[i][0].state)
        return (-1)*E
    
    def Ising_DE(self,i,j):
        if i==0:
            top=self[self.y_length()-1][j].state
        else:
            top=self[i-1][j].state
        if i==(self.y_length()-1):
            bottom=self[0][j].state
        else:
            bottom=self[i+1][j].state
        if j==0:
            left=self[i][self.x_length()-1].state
        else:
            left=self[i][j-1].state
        if j==(self.x_length()-1):
            right=self[i][0].state
        else:
            right=self[i][j+1].state
            
        E_i=(-1*self[i][j].state)*(top+bottom+left+right)
        E_f=self[i][j].state*(top+bottom+left+right)
        return float(E_f-E_i)
    
    def Ising_Energy2(self):
        E=0
        for i in range(self.y_length()):
            for j in range(self.x_length()):
                    if i==0:
                        top=self[self.y_length()-1][j].state
                    else:
                        top=self[i-1][j].state
                    if i==(self.y_length()-1):
                        bottom=self[0][j].state
                    else:
                        bottom=self[i+1][j].state
                    if j==0:
                        left=self[i][self.x_length()-1].state
                    else:
                        left=self[i][j-1].state
                    if j==(self.x_length()-1):
                        right=self[i][0].state
                    else:
                        right=self[i][j+1].state
            
                    E=E+(-1*self[i][j].state)*(top+bottom+left+right)
        return E
    
    
    def Ising_interaction(self):
        T=float(self.Temperature)
        i=random.randint(0,self.y_length()-1)
        j=random.randint(0,self.x_length()-1)
        DE=self.Ising_DE(i,j)
        prob=random.random()
        if DE<=0:
            self[i][j].state=self[i][j].state*(-1)
        elif prob<exp((-1*DE)/T):
            self[i][j].state=self[i][j].state*(-1)
            
    def Magnitization(self):
        net_moment=0
        for i in range(self.y_length()):
            for j in range(self.x_length()):
                net_moment=net_moment+self[i][j].state
        return net_moment
    
    def Weighted_Magnitization(self):
        return self.Magnitization()/self.size()
    
    def Energy(self):
        M=self.Weighted_Magnitization()
        #M=self.Magnitization()
        Energy=0
        for i in range(self.y_length()):
            for j in range(self.x_length()):
                Energy=Energy+(M*self[i][j].state)
        
        return (-1*Energy)
    
    def Baseline_DE(self,i,j):
        M=self.Magnitization()
        E_i=self.Energy()
        if self[i][j].state==1:
            new_M=M-2
        elif self[i][j].state==-1:
            new_M=M+2
        else:
            new_M=M
        new_WM=new_M/self.size()
        E_f=(-1)*(new_WM*new_M)
        return E_f-E_i
    
    def Baseline_interaction(self):
        T=self.Temperature
        i=random.randint(0,self.y_length()-1)
        j=random.randint(0,self.x_length()-1)
        DE=self.Baseline_DE(i,j)
        prob=random.random()
        if DE<=0:
            self[i][j].state=self[i][j].state*(-1)
        elif prob<exp((-1*DE)/T):
            self[i][j].state=self[i][j].state*(-1)
    
    def Ising_Bell_State_DE(self,i,j,k,p,direction):
        if direction=='top':
            top1=self[k][p].state
            if i==1:
                top2=self[self.y_length()-1][p].state
            else:
                top2=self[k-1][p].state
            if i==(self.y_length()-1):
                bottom1=self[0][j].state
            else:
                bottom1=self[i+1][j].state
            if j==0:
                left1=self[i][self.x_length()-1].state
                left2=self[k][self.x_length()-1].state
            else:
                left1=self[i][j-1].state
                left2=self[k][p-1].state
            if j==(self.x_length()-1):
                right1=self[i][0].state
                right2=self[k][0].state
            else:
                right1=self[i][j+1].state
                right2=self[k][p+1].state
            DE= (self[i][j].state*(top1+bottom1+left1+right1))+(self[k][p].state*(top2+left2+right2))
        elif direction=='bottom':
            if i==0:
                top1=self[self.y_length()-1][j].state
            else:
                top1=self[i-1][j].state
            bottom1=self[k][p].state
            if k==(self.y_length()-1):
                bottom2=self[0][p].state
            else:
                bottom2=self[k+1][p].state
            if j==0:
                left1=self[i][self.x_length()-1].state
                left2=self[k][self.x_length()-1].state
            else:
                left1=self[i][j-1].state
                left2=self[k][p-1].state
            if j==(self.x_length()-1):
                right1=self[i][0].state
                right2=self[k][0].state
            else:
                right1=self[i][j+1].state
                right2=self[k][p+1].state
            DE=(self[i][j].state*(top1+bottom1+left1+right1))+(self[k][p].state*(bottom2+left2+right2))
        elif direction=='left':
            if i==0:
                top1=self[self.y_length()-1][j].state
                top2=self[self.y_length()-1][p].state
            else:
                top1=self[i-1][j].state
                top2=self[k-1][p].state
            if i==(self.y_length()-1):
                bottom1=self[0][j].state
                bottom2=self[0][p].state
            else:
                bottom1=self[i+1][j].state
                bottom2=self[k+1][p].state
            left1=self[k][p].state
            if p==0:
                left2=self[k][self.x_length()-1].state
            else:
                left2=self[k][p-1].state
            if j==(self.x_length()-1):
                right1=self[i][0].state
            else:
                right1=self[i][j+1].state
            DE=(self[i][j].state*(top1+bottom1+left1+right1))+(self[k][p].state*(top2+bottom2+left2))
        elif direction=='right':
            if i==0:
                top1=self[self.y_length()-1][j].state
                top2=self[self.y_length()-1][p].state
            else:
                top1=self[i-1][j].state
                top2=self[k-1][p].state
            if i==(self.y_length()-1):
                bottom1=self[0][j].state
                bottom2=self[0][p].state
            else:
                bottom1=self[i+1][j].state
                bottom2=self[k+1][p].state
            if j==0:
                left1=self[i][self.x_length()-1].state
            else:
                left1=self[i][j-1].state
            right1=self[k][p].state
            if p==(self.x_length()-1):
                right2=self[k][0].state
            else:
                right2=self[k][p+1].state
            DE=(self[i][j].state*(top1+bottom1+left1+right1))+(self[k][p].state*(top2+bottom2+right2))
        return DE
        
    
    def Bell_State_DE(self,i,j,k,p):
        E_i=self.Energy()
        M=0
        for s in range(self.y_length()):
            for t in range(self.x_length()):
                if s==i and t==j:
                    M=M
                elif s==k and t==p:
                    M=M
                else:
                    M=M+self[s][t].state
        WM=M/self.size()
        E_f=0
        for s in range(self.y_length()):
            for t in range(self.x_length()):
                if s==i and t==j:
                    E_f=E_f
                elif s==k and t==p:
                    E_f=E_f
                else:
                    E_f=E_f+(WM*self[s][t].state)
        E_f=(-1)*E_f
        return E_f-E_i
    
    
    def Bell_State_interaction(self, Ising_Energy=None):
        i=random.randint(0,self.y_length()-1)
        j=random.randint(0,self.x_length()-1)
        d=random.random()
        if d<0.25:
            direction='top'
            if i==0:
                k=self.y_length()-1
            else:
                k=i-1
            p=j
        elif d>=0.25 and d<0.5:
            direction='bottom'
            if i==(self.y_length()-1):
                k=0
            else:
                k=i+1
            p=j
        elif d>=0.5 and d<0.75:
            direction='left'
            k=i
            if j==0:
                p=self.x_length()-1
            else:
                p=j-1
        elif d>=0.75:
            direction='right'
            k=i
            if j==(self.x_length()-1):
                p=0
            else:
                p=j+1
        if Ising_Energy=='Use Ising Energy':
            DE=self.Ising_Bell_State_DE(i,j,k,p,direction)
            #print('Using Ising Energy')
        else:
            DE=self.Bell_State_DE(i,j,k,p)
        T=float(self.Temperature)
        chosen=self[i][j]
        other=self[k][p]
        
        if chosen.pairing==None and other.pairing==None:
            r=random.random()
            if DE<=0:
                chosen.pairing = other
                other.pairing = chosen
                chosen.state=0
                other.state=0
                chosen.bell_state_time=0
                other.bell_state_time=0
                if r<=0.25:
                    chosen.bell_state=1
                    other.bell_state=1
                elif r>0.25 and r<=0.5:
                    chosen.bell_state=2
                    other.bell_state=2
                elif r>0.5 and r<=0.75:
                    chosen.bell_state=3
                    other.bell_state=3
                elif r>0.75 and r<=1.0:
                    chosen.bell_state=4
                    other.bell_state=4
            else:
                if random.random()< np.exp((-1*DE)/T):
                    chosen.pairing = other
                    other.pairing = chosen
                    chosen.state=0
                    other.state=0
                    chosen.bell_state_time=0
                    other.bell_state_time=0
                    if r<=0.25:
                        chosen.bell_state=1
                        other.bell_state=1
                    elif r>0.25 and r<=0.5:
                        chosen.bell_state=2
                        other.bell_state=2
                    elif r>0.5 and r<=0.75:
                        chosen.bell_state=3
                        other.bell_state=3
                    elif r>0.75 and r<=1.0:
                        chosen.bell_state=4
                        other.bell_state=4
        
        elif chosen.pairing==None and other.pairing!=None:
            partner=other.pairing
            r=random.random()
            if other.bell_state==1 or other.bell_state==2:
                if DE<=0:
                    if r<=0.25:
                        partner.state=chosen.state
                        chosen.bell_state=1
                        other.bell_state=1
                    elif r>0.25 and r<=0.5:
                        partner.state=chosen.state
                        chosen.bell_state=2
                        other.bell_state=2
                    elif r>0.5 and r<=0.75:
                        partner.state=(-1)*chosen.state
                        chosen.bell_state=3
                        other.bell_state=3
                    elif r>0.75:
                        partner.state=(-1)*chosen.state
                        chosen.bell_state=4
                        other.bell_state=4
                    chosen.pairing=other
                    other.pairing=chosen
                    partner.pairing=None
                    chosen.state=0
                    other.state=0
                    partner.bell_state=None
                    chosen.bell_state_time=0
                    other.bell_state_time=0
                    partner.bell_state_time=0
                else:
                    if random.random()<np.exp((-1*DE)/T):
                        if r<=0.25:
                            partner.state=chosen.state
                            chosen.bell_state=1
                            other.bell_state=1
                        elif r>0.25 and r<=0.5:
                            partner.state=chosen.state
                            chosen.bell_state=2
                            other.bell_state=2
                        elif r>0.5 and r<=0.75:
                            partner.state=(-1)*chosen.state
                            chosen.bell_state=3
                            other.bell_state=3
                        elif r>0.75:
                            partner.state=(-1)*chosen.state
                            chosen.bell_state=4
                            other.bell_state=4
                        chosen.pairing=other
                        other.pairing=chosen
                        partner.pairing=None
                        chosen.state=0
                        other.state=0
                        partner.bell_state=None
                        chosen.bell_state_time=0
                        other.bell_state_time=0
                        partner.bell_state_time=0
            elif other.bell_state==3 or other.bell_state==4:
                if DE<=0:
                    if r<=0.25:
                        partner.state=(-1)*chosen.state
                        chosen.bell_state=1
                        other.bell_state=1
                    elif r>0.25 and r<=0.5:
                        partner.state=(-1)*chosen.state
                        chosen.bell_state=2
                        other.bell_state=2
                    elif r>0.5 and r<=0.75:
                        partner.state=chosen.state
                        chosen.bell_state=3
                        other.bell_state=3
                    elif r>0.75:
                        partner.state=chosen.state
                        chosen.bell_state=4
                        other.bell_state=4
                    chosen.pairing=other
                    other.pairing=chosen
                    partner.pairing=None
                    chosen.state=0
                    other.state=0
                    partner.bell_state=None
                    chosen.bell_state_time=0
                    other.bell_state_time=0
                    partner.bell_state_time=0
                else:
                    if random.random()<np.exp((-1*DE)/T):
                        if r<=0.25:
                            partner.state=(-1)*chosen.state
                            chosen.bell_state=1
                            other.bell_state=1
                        elif r>0.25 and r<=0.5:
                            partner.state=(-1)*chosen.state
                            chosen.bell_state=2
                            other.bell_state=2
                        elif r>0.5 and r<=0.75:
                            partner.state=chosen.state
                            chosen.bell_state=3
                            other.bell_state=3
                        elif r>0.75:
                            partner.state=chosen.state
                            chosen.bell_state=4
                            other.bell_state=4
                        chosen.pairing=other
                        other.pairing=chosen
                        partner.pairing=None
                        chosen.state=0
                        other.state=0
                        partner.bell_state=None
                        chosen.bell_state_time=0
                        other.bell_state_time=0
                        partner.bell_state_time=0
        
        
        elif chosen.pairing!=None and other.pairing==None:
            partner=chosen.pairing
            r=random.random()
            if chosen.bell_state==1 or chosen.bell_state==2:
                if DE<=0:
                    if r<=0.25:
                        partner.state=other.state
                        chosen.bell_state=1
                        other.bell_state=1
                    elif r>0.25 and r<=0.5:
                        partner.state=other.state
                        chosen.bell_state=2
                        other.bell_state=2
                    elif r>0.5 and r<=0.75:
                        partner.state=(-1)*other.state
                        chosen.bell_state=3
                        other.bell_state=3
                    elif r>0.75:
                        partner.state=(-1)*other.state
                        chosen.bell_state=4
                        other.bell_state=4
                    chosen.pairing=other
                    other.pairing=chosen
                    partner.pairing=None
                    chosen.state=0
                    other.state=0
                    partner.bell_state=None
                    chosen.bell_state_time=0
                    other.bell_state_time=0
                    partner.bell_state_time=0
                else:
                    if random.random()<np.exp((-1*DE)/T):
                        if r<=0.25:
                            partner.state=other.state
                            chosen.bell_state=1
                            other.bell_state=1
                        elif r>0.25 and r<=0.5:
                            partner.state=other.state
                            chosen.bell_state=2
                            other.bell_state=2
                        elif r>0.5 and r<=0.75:
                            partner.state=(-1)*other.state
                            chosen.bell_state=3
                            other.bell_state=3
                        elif r>0.75:
                            partner.state=(-1)*other.state
                            chosen.bell_state=4
                            other.bell_state=4
                        chosen.pairing=other
                        other.pairing=chosen
                        partner.pairing=None
                        chosen.state=0
                        other.state=0
                        partner.bell_state=None
                        chosen.bell_state_time=0
                        other.bell_state_time=0
                        partner.bell_state_time=0
            elif chosen.bell_state==3 or chosen.bell_state==4:
                if DE<=0:
                    if r<=0.25:
                        partner.state=(-1)*other.state
                        chosen.bell_state=1
                        other.bell_state=1
                    elif r>0.25 and r<=0.5:
                        partner.state=(-1)*other.state
                        chosen.bell_state=2
                        other.bell_state=2
                    elif r>0.5 and r<=0.75:
                        partner.state=other.state
                        chosen.bell_state=3
                        other.bell_state=3
                    elif r>0.75:
                        partner.state=other.state
                        chosen.bell_state=4
                        other.bell_state=4
                    chosen.pairing=other
                    other.pairing=chosen
                    partner.pairing=None
                    chosen.state=0
                    other.state=0
                    partner.bell_state=None
                    chosen.bell_state_time=0
                    other.bell_state_time=0
                    partner.bell_state_time=0
                else:
                    if random.random()<np.exp((-1*DE)/T):
                        if r<=0.25:
                            partner.state=(-1)*other.state
                            chosen.bell_state=1
                            other.bell_state=1
                        elif r>0.25 and r<=0.5:
                            partner.state=(-1)*other.state
                            chosen.bell_state=2
                            other.bell_state=2
                        elif r>0.5 and r<=0.75:
                            partner.state=other.state
                            chosen.bell_state=3
                            other.bell_state=3
                        elif r>0.75:
                            partner.state=other.state
                            chosen.bell_state=4
                            other.bell_state=4
                        chosen.pairing=other
                        other.pairing=chosen
                        partner.pairing=None
                        chosen.state=0
                        other.state=0
                        partner.bell_state=None
                        chosen.bell_state_time=0
                        other.bell_state_time=0
                        partner.bell_state_time=0
                    
        elif chosen.pairing!=None and other.pairing!=None:
            r=random.random()
            partner_1 = chosen.pairing
            partner_2 = other.pairing
            if DE<=0:
                partner_1.pairing=partner_2
                partner_2.pairing=partner_1
                chosen.pairing = other
                other.pairing = chosen
                partner_1.state=0
                partner_2.state=0
                chosen.state=0
                other.state=0
                partner_1.bell_state_time=0
                partner_2.bell_state_time=0
                chosen.bell_state_time=0
                other.bell_state_time=0
                if r<=0.25:
                    chosen.bell_state=1
                    other.bell_state=1
                    partner_1.bell_state=1
                    partner_2.bell_state=1
                elif r>0.25 and r<=0.5:
                    chosen.bell_state=2
                    other.bell_state=2
                    partner_1.bell_state=2
                    partner_2.bell_state=2
                elif r>0.5 and r<=0.75:
                    chosen.bell_state=3
                    other.bell_state=3
                    partner_1.bell_state=3
                    partner_2.bell_state=3
                elif r>0.75 and r<=1.0:
                    chosen.bell_state=4
                    other.bell_state=4
                    partner_1.bell_state=4
                    partner_2.bell_state=4
            else:
                if random.random()<np.exp((-1*DE)/T):
                    partner_1.pairing=partner_2
                    partner_2.pairing=partner_1
                    chosen.pairing = other
                    other.pairing = chosen
                    partner_1.state=0
                    partner_2.state=0
                    chosen.state=0
                    other.state=0
                    partner_1.bell_state_time=0
                    partner_2.bell_state_time=0
                    chosen.bell_state_time=0
                    other.bell_state_time=0
                    if r<=0.25:
                        chosen.bell_state=1
                        other.bell_state=1
                        partner_1.bell_state=1
                        partner_2.bell_state=1
                    elif r>0.25 and r<=0.5:
                        chosen.bell_state=2
                        other.bell_state=2
                        partner_1.bell_state=2
                        partner_2.bell_state=2
                    elif r>0.5 and r<=0.75:
                        chosen.bell_state=3
                        other.bell_state=3
                        partner_1.bell_state=3
                        partner_2.bell_state=3
                    elif r>0.75 and r<=1.0:
                        chosen.bell_state=4
                        other.bell_state=4
                        partner_1.bell_state=4
                        partner_2.bell_state=4
                        
                        
    def Entanglement_Density(self):
        count=0
        for i in range(self.y_length()):
            for j in range(self.x_length()):
                if self[i][j].pairing!=None:
                    count = count+1
                else:
                    count=count
        return float(count)/float(self.size())
    
    def Decoherence(self, tau):
        for i in range(self.y_length()):
            for j in range(self.x_length()):
                if self[i][j].pairing!=None:
                    r=random.random()
                    if r<(1.-exp((-1.*self[i][j].bell_state_time)/tau)):
                        prob=random.random()
                        if self[i][j].bell_state==1 or self[i][j].bell_state==2:
                            if prob<=0.5:
                                self[i][j].state=1
                                self[i][j].bell_state=None
                                self[i][j].bell_state_time=None
                                self[i][j].pairing.state=-1
                                self[i][j].pairing.bell_state=None
                                self[i][j].pairing.bell_state_time=None
                                self[i][j].pairing.pairing=None
                                self[i][j].pairing=None
                            else:
                                self[i][j].state=-1
                                self[i][j].bell_state=None
                                self[i][j].bell_state_time=None
                                self[i][j].pairing.state=1
                                self[i][j].pairing.bell_state=None
                                self[i][j].pairing.bell_state_time=None
                                self[i][j].pairing.pairing=None
                                self[i][j].pairing=None
                        elif self[i][j].bell_state==3 or self[i][j].bell_state==4:
                            if prob<=0.5:
                                self[i][j].state=1
                                self[i][j].bell_state=None
                                self[i][j].bell_state_time=None
                                self[i][j].pairing.state=1
                                self[i][j].pairing.bell_state=None
                                self[i][j].pairing.bell_state_time=None
                                self[i][j].pairing.pairing=None
                                self[i][j].pairing=None
                            else:
                                self[i][j].state=-1
                                self[i][j].bell_state=None
                                self[i][j].bell_state_time=None
                                self[i][j].pairing.state=-1
                                self[i][j].pairing.bell_state=None
                                self[i][j].pairing.bell_state_time=None
                                self[i][j].pairing.pairing=None
                                self[i][j].pairing=None
        for k in range(self.y_length()):
            for p in range(self.x_length()):
                if self[k][p].pairing != None:
                    self[k][p].bell_state_time+=1
    
    
    def Decoherence_2(self, tau, Interaction):
        for i in range(self.y_length()):
            for j in range(self.x_length()):
                if self[i][j].pairing!=None:
                    r=random.random()
                    if Interaction=='Ising' or Interaction=='Ising Bell State' or Interaction=='Ising and Bell State':
                        if i==0:
                            top=self[self.y_length()-1][j].state
                        else:
                            top=self[i-1][j].state
                        if i==(self.y_length()-1):
                            bottom=self[0][j].state
                        else:
                            bottom=self[i+1][j].state
                        if j==0:
                            left=self[i][self.x_length()-1].state
                        else:
                            left=self[i][j-1].state
                        if j==(self.x_length()-1):
                            right=self[i][0].state
                        else:
                            right=self[i][j+1].state
                        E_up=(-1*1)*(top+bottom+left+right)
                        E_down=(-1*-1)*(top+bottom+left+right)
                    elif Interaction=='Baseline' or Interaction=='Bell State' or Interactions=='Bell and Baseline':
                        M=self.Magnitization()
                        M_up=M+1
                        M_down=M-1
                        E_up=M_up*1
                        E_down=M_down*(-1)
                    if r<(1.-exp((-1.*self[i][j].bell_state_time)/tau)):
                        prob=random.random()
                        if self[i][j].bell_state==1 or self[i][j].bell_state==2:
                            if E_up<E_down:
                                self[i][j].state=1
                                self[i][j].bell_state=None
                                self[i][j].bell_state_time=None
                                self[i][j].pairing.state=-1
                                self[i][j].pairing.bell_state=None
                                self[i][j].pairing.bell_state_time=None
                                self[i][j].pairing.pairing=None
                                self[i][j].pairing=None
                            elif E_up>E_down:
                                self[i][j].state=-1
                                self[i][j].bell_state=None
                                self[i][j].bell_state_time=None
                                self[i][j].pairing.state=1
                                self[i][j].pairing.bell_state=None
                                self[i][j].pairing.bell_state_time=None
                                self[i][j].pairing.pairing=None
                                self[i][j].pairing=None
                            else:
                                if prob<=0.5:
                                    self[i][j].state=1
                                    self[i][j].bell_state=None
                                    self[i][j].bell_state_time=None
                                    self[i][j].pairing.state=-1
                                    self[i][j].pairing.bell_state=None
                                    self[i][j].pairing.bell_state_time=None
                                    self[i][j].pairing.pairing=None
                                    self[i][j].pairing=None
                                else:
                                    self[i][j].state=-1
                                    self[i][j].bell_state=None
                                    self[i][j].bell_state_time=None
                                    self[i][j].pairing.state=1
                                    self[i][j].pairing.bell_state=None
                                    self[i][j].pairing.bell_state_time=None
                                    self[i][j].pairing.pairing=None
                                    self[i][j].pairing=None
                        elif self[i][j].bell_state==3 or self[i][j].bell_state==4:
                            if E_up<E_down:
                                self[i][j].state=1
                                self[i][j].bell_state=None
                                self[i][j].bell_state_time=None
                                self[i][j].pairing.state=1
                                self[i][j].pairing.bell_state=None
                                self[i][j].pairing.bell_state_time=None
                                self[i][j].pairing.pairing=None
                                self[i][j].pairing=None
                            elif E_up>E_down:
                                self[i][j].state=-1
                                self[i][j].bell_state=None
                                self[i][j].bell_state_time=None
                                self[i][j].pairing.state=-1
                                self[i][j].pairing.bell_state=None
                                self[i][j].pairing.bell_state_time=None
                                self[i][j].pairing.pairing=None
                                self[i][j].pairing=None
                            else:
                                if prob<=0.5:
                                    self[i][j].state=1
                                    self[i][j].bell_state=None
                                    self[i][j].bell_state_time=None
                                    self[i][j].pairing.state=1
                                    self[i][j].pairing.bell_state=None
                                    self[i][j].pairing.bell_state_time=None
                                    self[i][j].pairing.pairing=None
                                    self[i][j].pairing=None
                                else:
                                    self[i][j].state=-1
                                    self[i][j].bell_state=None
                                    self[i][j].bell_state_time=None
                                    self[i][j].pairing.state=-1
                                    self[i][j].pairing.bell_state=None
                                    self[i][j].pairing.bell_state_time=None
                                    self[i][j].pairing.pairing=None
                                    self[i][j].pairing=None
        for k in range(self.y_length()):
            for p in range(self.x_length()):
                if self[k][p].pairing != None:
                    self[k][p].bell_state_time+=1
        

    def Correlation(self):
        if self.x_length()<=self.y_length():
            length=self.x_length()
        else:
            length=self.y_length()
        separation=np.arange(1,length/2,dtype=int)
        correlation=np.zeros(len(separation))
        for k in range(len(separation)):
            cor=0
            for i in range(self.y_length()):
                for j in range(self.x_length()):
                    if j-separation[k]<0:
                        cor=cor+self[i][j].state*self[i][(self.x_length()-1)-(separation[k]-j)].state
                        cor=cor+self[i][j].state*self[i][j+separation[k]].state
                    elif j+separation[k]>(self.x_length()-1):
                        cor=cor+self[i][j].state*self[i][j-separation[k]].state
                        cor=cor+self[i][j].state*self[i][(j+separation[k])-self.x_length()].state
                    else:
                        cor=cor+self[i][j].state*self[i][j-separation[k]].state
                        cor=cor+self[i][j].state*self[i][j+separation[k]].state
                    if i-separation[k]<0:
                        cor=cor+self[i][j].state*self[(self.y_length()-1)-(separation[k]-i)][j].state
                        cor=cor+self[i][j].state*self[i+separation[k]][j].state
                    elif i+separation[k]>(self.y_length()-1):
                        cor=cor+self[i][j].state*self[i-separation[k]][j].state
                        cor=cor+self[i][j].state*self[(i+separation[k])-self.y_length()][j].state
                    else:
                        cor=cor+self[i][j].state*self[i-separation[k]][j].state
                        cor=cor+self[i][j].state*self[i+separation[k]][j].state
            correlation[k]=(cor/(4.*float(self.size())))-((self.Weighted_Magnitization())**2.)
        return separation, correlation        
        
        
        


# In[3]:

import sys

class ProgressBar(object):
    
    def __init__(self, length=20):
        self.length = length
        self.current = None
        
    def printout(self, percent):
        bar = "="*int(round(percent*self.length))
        if self.current!=bar:
            form = "\r[%-"+str(self.length)+"s]"
            sys.stdout.write(form % bar)
            sys.stdout.flush()
            self.current = bar
#pb = ProgressBar(20)
#for i in range(100000):
     #pb.printout(float(i)/100000)


# In[8]:

def Iterate(N, max_vel_temp, tau, Interaction, Movement=None, Decoherence='Yes', Decoherence_type=2, input_gas=None, gas_shape=None, Temperature=None, Seed_Bell_States=None, Number_Seeded_Bell_States=None):
    #Iteration function. Parameters:
    #N is number of iterations
    #gas_shape is shape of gas given in tuple [y_length, x_length]
    #Temperatrue is temp of gas
    #max_vel_temp is used in movement function
    #tau is used in decoherence function
    #Interaction indicates what interaction, given as string. Interactions are, Ising, Ising Bell State, Baseline, Bell State
    #input_gas is gas input into function if the function makes no gas. Defalt is None so that function will make own gas
    I=np.zeros(N)
    E=np.zeros(N)
    E_2=np.zeros(N)
    M=np.zeros(N)
    M_2=np.zeros(N)
    ED=np.zeros(N)
    ED_2=np.zeros(N)
    if input_gas==None:
        g=Gas(gas_shape[0],gas_shape[1], Temperature)
    else:
        g=input_gas
    if Seed_Bell_States=='adjacent':
        for k in range(Number_Seeded_Bell_States):
            seeded='no'
            while seeded=='no':
                i=random.randint(0,g.y_length()-1)
                j=random.randint(0,g.x_length()-1)
                d=random.random()
                prob=random.random()
                if d<=0.25:
                    s=i-1
                    t=j
                elif d>0.25 and d<=0.5:
                    s=i+1
                    t=j
                elif d>0.5 and d<-0.75:
                    s=i
                    t=j-1
                elif d>0.75 and d<=1.0:
                    s=i
                    t=j+1
                if g[i][j].state!=0 and g[s][t].state!=0:
                    g[i][j].state=0
                    g[i][j].pairing=g[s][t]
                    g[i][j].bell_state_time=0
                    g[s][t].state=0
                    g[s][t].pairing=g[i][j]
                    g[s][t].bell_state_time=0
                    if prob<=0.25:
                        g[i][j].bell_state=1
                        g[s][t].bell_state=1
                    elif prob>0.25 and prob<=0.5:
                        g[i][j].bell_state=2
                        g[s][t].bell_state=2
                    elif prob>0.5 and prob<=0.75:
                        g[i][j].bell_state=3
                        g[s][t].bell_state=3
                    elif prob>0.75 and prob<=1.0:
                        g[i][j].bell_state=4
                        g[s][t].bell_state=4
                    seeded='yes'
    if Seed_Bell_States=='separated':
        for k in range(Number_Seeded_Bell_States):
            seeded='no'
            while seeded=='no':
                i=random.randint(0,g.y_length()-1)
                j=random.randint(0,g.x_length()-1)
                find_other='yes'
                while find_other=='yes':
                    s=random.randint(0,g.y_length()-1)
                    t=random.randint(0,g.x_length()-1)
                    if s!=i or t!=j:
                        find_other='no'
                if g[i][j].state!=0 and g[s][t].state!=0:
                    g[i][j].state=0
                    g[i][j].pairing=g[s][t]
                    g[i][j].bell_state_time=0
                    g[s][t].state=0
                    g[s][t].pairing=g[i][j]
                    g[s][t].bell_state_time=0
                    if prob<=0.25:
                        g[i][j].bell_state=1
                        g[s][t].bell_state=1
                    elif prob>0.25 and prob<=0.5:
                        g[i][j].bell_state=2
                        g[s][t].bell_state=2
                    elif prob>0.5 and prob<=0.75:
                        g[i][j].bell_state=3
                        g[s][t].bell_state=3
                    elif prob>0.75 and prob<=1.0:
                        g[i][j].bell_state=4
                        g[s][t].bell_state=4
                    seeded='yes'
    for i in range(N):
        if Interaction=='Ising':
            g.Ising_interaction()
            if Movement=='yes':
                g.move(max_vel_temp)
        elif Interaction=='Ising Bell State':
            g.Bell_State_interaction('Use Ising Energy')
            if Decoherence=='Yes':
                if Decoherence_type==1:
                    g.Decoherence(tau)
                elif Decoherence_type==2:
                    g.Decoherence_2(tau, Interaction)
            if Movement=='yes':
                g.move(max_vel_temp)
        elif Interaction=='Ising and Bell State':
            g.Bell_State_interaction('Use Ising Energy')
            g.Ising_interaction()
            if Decoherence=='Yes':
                if Decoherence_type==1:
                    g.Decoherence(tau)
                elif Decoherence_type==2:
                    g.Decoherence_2(tau,Interaction)
            if Movement=='yes':
                g.move(max_vel_temp)
        elif Interaction=='Baseline':
            g.Baseline_interaction()
            if Decoherence=='Yes':
                if Decoherence_type==1:
                    g.Decoherence(tau)
                elif Decoherence_type==2:
                    g.Decoherence_2(tau, Interaction)
            if Movement=='yes':
                g.move(max_vel_temp)
        elif Interaction=='Bell State':
            g.Bell_State_interaction()
            if Decoherence=='Yes':
                if Decoherence_type==1:
                    g.Decoherence(tau)
                elif Decoherence_type==2:
                    g.Decoherence_2(tau,Interaction)
            if Movement=='yes':
                g.move(max_vel_temp)
        elif Interaction=='Bell and Baseline':
            g.Bell_State_interaction()
            g.Baseline_interaction()
            if Decoherence=='Yes':
                if Decoherence_type==1:
                    g.Decoherence(tau)
                elif Dechoerence_type==2:
                    g.Decoherence_2(tau,Interaction)
            if Movement=='yes':
                g.move(max_vel_temp)
        I[i]=i
        if Interaction=='Ising' or Interaction=='Ising Bell State' or Interaction=='Ising and Bell State':
            E[i]=g.Ising_Energy()
            E_2[i]=(g.Ising_Energy())**2.
        else:
            E[i]=g.Energy()
            E_2[i]=(g.Energy())**2.
        M[i]=g.Magnitization()
        M_2[i]=(g.Magnitization())**2.
        ED[i]=g.Entanglement_Density()
        ED_2[i]=(g.Entanglement_Density())**2.
    
    return g, I, E, E_2, M, M_2, ED, ED_2


def Temperature_Iteration(T_i, T_f, N_Temps, N, max_vel_temp, tau, Interaction, Movement=None, Decoherence='Yes', Decoherence_type=2, gas_in=None, gas_shape=None, Temperature=None, Seed_Bell_States=None, Number_Seeded_Bell_States=None, Extra_Iteration=None, Extra_iteration_num=None):
    #Temperature iteration function
    # T_i=inital temperature, T_f=final temperature, N_Temps is number if temperatures between T_i and T_f
    # all other arguments are the relevent arguments in the Iterate function
    T=np.linspace(T_i,T_f,N_Temps)
    E=np.zeros(len(T))
    CV=np.zeros(len(T))
    M=np.zeros(len(T))
    Chi=np.zeros(len(T))
    ED=np.zeros(len(T))
    DV=np.zeros(len(T))
    if gas_in==None:
        g_in=Gas(gas_shape[0],gas_shape[1],Temperature)
    else:
        g_in=gas_in
    if Seed_Bell_States=='adjacent':
        for k in range(Number_Seeded_Bell_States):
            seeded='no'
            while seeded=='no':
                i=random.randint(0,g_in.y_length()-1)
                j=random.randint(0,g_in.x_length()-1)
                d=random.random()
                prob=random.random()
                if d<=0.25:
                    if i==0:
                        s=g_in.y_length()-1
                    else:
                        s=i-1
                    t=j
                elif d>0.25 and d<=0.5:
                    if i==g_in.y_length()-1:
                        s=0
                    else:
                        s=i+1
                    t=j
                elif d>0.5 and d<=0.75:
                    s=i
                    if j==0:
                        t=g_in.x_length()-1
                    else:
                        t=j-1
                elif d>0.75 and d<=1.0:
                    s=i
                    if j==g_in.x_length()-1:
                        t=0
                    else:
                        t=j+1
                if g_in[i][j].state!=0 and g_in[s][t].state!=0:
                    g_in[i][j].state=0
                    g_in[i][j].pairing=g_in[s][t]
                    g_in[i][j].bell_state_time=0
                    g_in[s][t].state=0
                    g_in[s][t].pairing=g_in[i][j]
                    g_in[s][t].bell_state_time=0
                    if prob<=0.25:
                        g_in[i][j].bell_state=1
                        g_in[s][t].bell_state=1
                    elif prob>0.25 and prob<=0.5:
                        g_in[i][j].bell_state=2
                        g_in[s][t].bell_state=2
                    elif prob>0.5 and prob<=0.75:
                        g_in[i][j].bell_state=3
                        g_in[s][t].bell_state=3
                    elif prob>0.75 and prob<=1.0:
                        g_in[i][j].bell_state=4
                        g_in[s][t].bell_state=4
                    seeded='yes'
        print(g_in.states())
    elif Seed_Bell_States=='separated':
        for k in range(Number_Seeded_Bell_States):
            seeded='no'
            while seeded=='no':
                i=random.randint(0,g_in.y_length()-1)
                j=random.randint(0,g_in.x_length()-1)
                find_other='yes'
                while find_other=='yes':
                    s=random.randint(0,g_in.y_length()-1)
                    t=random.randint(0,g_in.x_length()-1)
                    if s!=i or t!=j:
                        find_other='no'
                prob=random.random()
                if g_in[i][j].state!=0 and g_in[s][t].state!=0:
                    g_in[i][j].state=0
                    g_in[i][j].pairing=g_in[s][t]
                    g_in[i][j].bell_state_time=0
                    g_in[s][t].state=0
                    g_in[s][t].pairing=g_in[i][j]
                    g_in[s][t].bell_state_time=0
                    if prob<=0.25:
                        g_in[i][j].bell_state=1
                        g_in[s][t].bell_state=1
                    elif prob>0.25 and prob<=0.5:
                        g_in[i][j].bell_state=2
                        g_in[s][t].bell_state=2
                    elif prob>0.5 and prob<=0.75:
                        g_in[i][j].bell_state=3
                        g_in[s][t].bell_state=3
                    elif prob>0.75 and prob<=1.0:
                        g_in[i][j].bell_state=4
                        g_in[s][t].bell_state=4
                    seeded='yes'
        print(g_in.states())
    pb = ProgressBar(20)
    for i in range(len(T)):
        g_in.Temperature=T[i]
        if Extra_Iteration=='Yes':
            g_in,a,b,c,d,e,f,g=Iterate(Extra_iteration_num,max_vel_temp,tau,Interaction,input_gas=g_in)
        g_out,I,EI,E_2I,MI,M_2I,EDI,ED_2I=Iterate(N,max_vel_temp,tau,Interaction,Movement=Movement,Decoherence=Decoherence, Decoherence_type=Decoherence_type, input_gas=g_in)
        E[i]=np.average(EI)
        CV[i]=(1./((float(T[i]))**2.))*(np.average(E_2I)-((np.average(EI))**2.))
        M[i]=np.average(MI)
        Chi[i]=(1./float(T[i]))*(np.average(M_2I)-((np.average(MI))**2.))
        ED[i]=np.average(EDI)
        DV[i]=(1./float(T[i]))*(np.average(ED_2I)-((np.average(EDI))**2.))
        g_in=g_out
        pb.printout(float(i)/len(T))
        
    return g_in, T, E, CV, M, Chi, ED, DV


# In[9]:

def sym_derivative(x,y,smooth=None):
    #if smooth=='yes':
     #   y_in=scipy.signal.savgol_filter(y,51,3)
    #elif smooth=='no':
      #  y_in=y
    deriv=np.zeros(len(x))
    for i in range(len(x)):
        if i==0:
            dy=y[i+1]-y[i]
            dx=x[i+1]-x[i]
            deriv[i]=dy/dx
        elif i==len(x)-1:
            dy=y[i]-y[i-1]
            dx=x[i]-x[i-1]
            deriv[i]=dy/dx
        else:
            dy=y[i+1]-y[i-1]
            dx=x[i+1]-x[i-1]
            deriv[i]=dy/dx
    return deriv


# In[ ]:



