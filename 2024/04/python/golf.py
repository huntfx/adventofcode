import numpy as np;a=np.array(list(map(list,open('input.txt'))))[:,:-1]
[print(f'Part {i}: {v}')for i,v in((1,sum(sum(map(all,zip(*[(b[y][x-i]==c,b[y-i][x-i]==(c,i)[y<3])for i,c in enumerate('XMAS')])))for b in(np.rot90(a,i)for i in range(4))for x in range(3,b.shape[1])for y in range(b.shape[0]))),(2,sum({a[y][x],a[y+2][x+2]}=={a[y+2][x],a[y][x+2]}==set('MS')for y,x in zip(*np.where(a[1:-1,1:-1]=='A')))))]
