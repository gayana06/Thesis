__author__ = 'Gayana'

import math
import random

class ZipfianGenerator:

    ZIPFIAN_CONSTANT=3.0
    items=0
    base=0
    zipfianconstant=0.0
    alpha=zetan=eta=theta=zeta2theta=0.0
    countforzeta=0
    lastint=0
    allowitemcountdecrease=False



    #def ZipfianGenerator(self,_items):
    #    ZipfianGenerator(0,_items-1)

    #def ZipfianGenerator(self, _min,  _max):
    #    ZipfianGenerator(_min,_max,self.ZIPFIAN_CONSTANT)

    #def ZipfianGenerator(self, _items,  _zipfianconstant):
    #    ZipfianGenerator(0,_items-1,_zipfianconstant)

    #def ZipfianGenerator(self, min,  max,  _zipfianconstant):
    #    ZipfianGenerator(min,max,_zipfianconstant,self.zetastatic(max-min+1,_zipfianconstant))


    def Start(self, _min,  _max):
        self.Step2(_min,_max,self.ZIPFIAN_CONSTANT)

    def Step2(self, min,  max,  _zipfianconstant):
        self.Generator(min,max,_zipfianconstant,self.zetastatic2(max-min+1,_zipfianconstant))

    def Generator(self, min,  max,  _zipfianconstant,  _zetan):
        self.items=max-min+1
        self.base=min
        self.zipfianconstant=_zipfianconstant

        self.theta=self.zipfianconstant
        self.zeta2theta=self.zeta2(2,self.theta)


        self.alpha=1.0/(1.0-self.theta)
        #zetan=zeta(self.items,self.theta)
        self.zetan=_zetan
        self.countforzeta=self.items
        self.eta=(1-math.pow(2.0/self.items,1-self.theta))/(1-self.zeta2theta/self.zetan)
        self.nextInt()


    def zeta2(self, n,  theta):
        self.countforzeta=n
        return self.zetastatic2(n,theta)

    def zetastatic2(self, n, theta):
        return self.zetastatic4(0,n,theta,0)

    def zeta4(self, st,  n,  theta,  initialsum):
        self.countforzeta=n
        return self.zetastatic4(st,n,theta,initialsum)

    def zetastatic4(self, st,  n,  theta,  initialsum):
        sum=initialsum
        for i in range(st,n):
            sum+=1/math.pow(i+1,theta)
        return sum

    def nextInt1(self,itemcount):
        return  int(self.nextLong(itemcount))

    def nextLong1(self, itemcount):
        if (itemcount!=self.countforzeta):
            if (itemcount>self.countforzeta):
                self.zetan=self.zeta(self.countforzeta,itemcount,self.theta,self.zetan)
                self.eta=(1-math.pow(2.0/self.items,1-self.theta))/(1-self.zeta2theta/self.zetan)
            elif ( (itemcount<self.countforzeta) and (self.allowitemcountdecrease) ):
                self.zetan=self.zeta(itemcount,self.theta)
                self.eta=(1-math.pow(2.0/self.items,1-self.theta))/(1-self.zeta2theta/self.zetan)


        u= random.uniform(0.0, 1.0)
        uz=u*self.zetan

        if uz<1.0:
            return 0

        if (uz<1.0+math.pow(0.5,self.theta)):
            return 1


        ret=self.base+((itemcount) * math.pow(self.eta*u - self.eta + 1, self.alpha));
        self.setLastInt(int(ret))
        return ret


    def setLastInt(self, last):
        self.lastint=last;

    def nextInt(self):
        return int(self.nextLong1(self.items))

    def nextLong(self):
        return self.nextLong1(self.items)



gen=ZipfianGenerator()
gen.Start(0,100)
map={}
for i in range(0,3500):
    val=gen.nextInt()
    if val in map.keys():
        map[val]+=1
    else:
        map[val]=1
print(map)

