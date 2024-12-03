import re
m=''.join(map(str.strip,open('input.txt')));s=lambda m:sum(int(x)*int(y)for x,y in re.findall(r'mul\((\d+),(\d+)\)',m))
[print(f'Part {i}: {v}')for i,v in((1,s(m)),(2,s(re.sub("don't\(\).*?do\(\)",'',m))))]
