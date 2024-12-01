l,r=map(sorted,zip(*(map(int,l.split())for l in open('input.txt'))))
[print(f'Part {i}: {v}')for i,v in((1,sum(abs(l-r)for l,r in zip(l,r))),(2,sum(n*r.count(n)for n in l)))]