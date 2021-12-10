from functools import reduce
a,b=[],[];c,d='([{<',')]}>';r=dict(zip(c,d));y=reversed;z=list.append
for l in open('input.txt').read().split('\n'):
 t=[]
 for x in y(l):
  if x in d:z(t,x)
  elif t and x in c:
   v=t.pop()
   if r[x]!=v:
    z(a,v)
    break
 else:
  for x in l:
   if x in c:z(t,x)
   elif x in d:t.pop()
  z(b,''.join(map(r.get,y(t))))
e=list(sorted(reduce(lambda a,b:a*5+d.index(b)+1,x,0)for x in b))
[print(f'Part {i}: {v}')for i,v in((1,sum(map(dict(zip(d,(3,57,1197,25137))).get,a))),(2,e[len(e)//2]))]