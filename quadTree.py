# quadTree Pj
import numpy
import matplotlib.pyplot

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Rect:
    def __init__(self, c, w, h):
        self.c = c
        self.w = w
        self.h = h
        self.left = c.x - w
        self.right = c.x + w
        self.top = c.y - h
        self.bot = c.y + h

    def contains(self, point):
        return (self.left <= point.x < self.right 
            and self.top <= point.y < self.bot)
    
    def draw(self, ax, c='k', lw=1, **kwargs):
        x = self.left
        y = self.top
        x2 = self.right
        y2 = self.bot
        x1, y1 = self.left, self.top
        x2, y2 = self.right, self.bot
        ax.plot([x,x2,x2,x,x], [y,y,y2,y2,y], c=c, lw=lw, **kwargs)

class quadTree:
    def __init__(self, bounds, capacity = 4):
        self.bounds = bounds
        self.capacity = capacity
        self.points = []
        self.subDivided = False
    
    def insert(self, point):
        #if point is not in bounds/range than insert nothing
        if self.bounds.contains(point) == False:
            return False

        #if number of points is within capactiy
        if self.capacity > len(self.points):
            self.points.append(point)
            return True
        
        if self.subDivided == False:
            self.subDivide()
        
        #TopLeft, TopRight, BottomLeft and BottomRight refer to the new quadrants
        return (self.TL.insert(point) or self.TR.insert(point) 
            or self.BL.insert(point) or self.BR.insert(point))
    
    def subDivide(self):
        x = self.bounds.c.x
        y = self.bounds.c.y
        halfWidth = self.bounds.w / 2
        halfHeight = self.bounds.h / 2

        self.TL = quadTree(Rect(Point(x - halfWidth, y - halfHeight), halfWidth, halfHeight))
        self.TR = quadTree(Rect(Point(x + halfWidth, y - halfHeight), halfWidth, halfHeight))
        self.BL = quadTree(Rect(Point(x - halfWidth, y + halfHeight), halfWidth, halfHeight))
        self.BR = quadTree(Rect(Point(x + halfWidth, y + halfHeight), halfWidth, halfHeight))
        self.subDivided = True

    def __len__(self):
        num = len(self.points)
        if self.subDivided == True:
            num += len(self.TL) + len(self.TR) + len(self.BL) + len(self.BR)
        return num

    def draw(self, ax):
        self.bounds.draw(ax)
        if self.subDivided == True:
            self.TL.draw(ax)
            self.TR.draw(ax)
            self.BL.draw(ax)
            self.BR.draw(ax)

class main():
   n = 750
   x = numpy.random.rand(n) * 600
   y = numpy.random.rand(n) * 400
   points = []
  
   for i in range(n):
       points.append(Point(x[i], y[i]))
   domain = Rect(Point(600/2, 400/2), 600/2, 400/2)
   qt = quadTree(domain)
 
   for p in points:
       qt.insert(p)

   gr = matplotlib.pyplot.subplot()
   gr.set_xlim(0, 600)
   gr.set_ylim(0, 400)
   qt.draw(gr)
 
   for p in points:
       qt.insert(p)
       gr.scatter(p.x, p.y, s=5)
 
   gr.set_xticks([])
   gr.set_yticks([])
   gr.invert_yaxis()
   matplotlib.pyplot.show()
main()

