import functools as f
a=[lambda p,u:[p[0],p[1]-u],lambda p,u:[p[0],p[1]+u],lambda p,u:[p[0]+u,p[1]],lambda p,u:[p[0]-u,p[1]]]
b=[lambda p,u:p[:2]+[p[2]-u],lambda p,u:p[:2]+[p[2]+u],lambda p,u:[p[0]+u,p[1]+p[2]*u,p[2]],lambda p,u:[p[0]-u]+p[1:]]
c=[(m[0],int(m[1]))for m in(l.split()for l in open('input.txt'))]
d=map(lambda n:n[0]*n[1],(f.reduce(lambda e,f,g=h:g[('up','down','forward','backward').index(f[0])](e,f[1]),c,[0]*3)[:2]for h in(a,b)))
[print(f'Part {i}: {next(d)}')for i in(1,2)]