import functools as t
from collections import Counter as C
def f(x):l=C();[l.update(a)for a in x];return l
h=lambda d:sum(t.reduce(lambda x,i:f(dict(a)for a in[[[i-1,v]]if i else[[6,v],[8,v]]for i,v in x.items()]),range(d),C(map(int,next(open('input.txt')).split(',')))).values())
[print(f'Part {i+1}: {h(80+i*176)}')for i in(0,1)]
