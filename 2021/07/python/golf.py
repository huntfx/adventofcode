p=list(map(int,next(open('input.txt')).split(',')))
f=((1,lambda v:sum(abs(q-v)for q in p)),(2,lambda v:sum(n*(n+1)//2 for n in(abs(q-v)for q in p))))
[print(f'Part {i}: {min(map(x,range(max(p)+1)))}')for(i,x)in f]