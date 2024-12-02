d=[[*map(int,l.split())]for l in open('input.txt')]
s=lambda l:(min(f:=[i-j if l[0]>l[-1]else j-i for i,j in zip(l,l[1:])])>0 and max(f)<4)*((all(s:=[i>=0 for i in f])or not any(s)))
[print(f'Part {p+1}: {sum(any(s(l[:i-1]+l[i:])if i else s(l)for i in (range(len(l)*p+1)))for l in d)}')for p in(0,1)]
