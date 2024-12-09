e=enumerate;r=[0,0];s={()}
d=[*map(str.strip,open('input.txt'))];b=d.index('');x=[i.split('|')for i in d[:b]];u=[i.split(',') for i in d[b+1:]]
o={a:{i for i,j in x if j==a} for b,a in x}.get
def g(x):
 while i:=[i for i,p in e(x[1:],1)if x[i-1]not in o(p,s)]:i=i[0];x[i-1],x[i]=x[i],x[i-1]
 return x
for x in u:r[any(o(p,s)&{*x[i:]}for i,p in e(x))]+=int(g(x)[len(x)//2])
[print(f'Part {i+1}: {r[i]}')for i in (0,1)]
