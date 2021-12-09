import math;import numpy as n
m=n.array([list(l.strip())for l in open('input.txt')],dtype=int);s=m.shape
g=lambda c:((c[0]+x,c[1]+y)for x,y in((1,0),(0,1),(-1,0),(0,-1))if 0<=c[0]+x<s[0] and 0<=c[1]+y<s[1])
l=[c for c in n.ndindex(s)if all(m[a]>m[c]for a in g(c))]
def f(c,z=None):
 if z is None:z=n.zeros(s,dtype=bool)
 if z[c]:return z
 z[c]=True;[f(a,z)for a in g(c)if m[a]!=9]
 return z
[print(f'Part {i}: {v}')for i,v in((1,sum(m[c]+1 for c in l)),(2,math.prod(list(sorted(map(n.sum,map(f,l))))[-3:])))]