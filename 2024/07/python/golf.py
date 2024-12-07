import itertools as i,functools as f
v,n=zip(*(l[:-1].split(':')for l in open('input.txt')))
[print(f'Part {j+1}: {sum(a for a,b in zip(map(int,v),([*map(int,x.split())]for x in n))if any(a==f.reduce(lambda c,d:d[1](c,b[d[0]+1]),enumerate(p),b[0])for p in i.product([lambda a,b:a+b,lambda a,b:a*b,lambda a,b:int(f"{a}{b}")][:2+j],repeat=len(b)-1)))}')for j in(0,1)]
