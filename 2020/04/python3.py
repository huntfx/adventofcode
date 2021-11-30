from string import hexdigits

def valid_pt1(passport):
    return all(x in passport for x in ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'))

def valid_pt2(passport):
    try:
        if not 1920 <= int(passport['byr']) <= 2002:
            return False
        if not 2010 <= int(passport['iyr']) <= 2020:
            return False
        if not 2020 <= int(passport['eyr']) <= 2030:
            return False
        if passport['hgt'].endswith('cm'):
            if not 150 <= int(passport['hgt'][:-2]) <= 193:
                return False
        elif passport['hgt'].endswith('in'):
            if not 59 <= int(passport['hgt'][:-2]) <= 76:
                return False
        else:
            return False
        if passport['hcl'][0] != '#' or set(passport['hcl'][1:]) - set(hexdigits):
            return False
        if passport['ecl'] not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
            return False
        if len(passport['pid']) != 9 or not passport['pid'].isdigit():
            return False
    except KeyError:
        return False
    return True

passports = [{}]
with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            passports.append({})
        for kv in line.strip().split():
            k, v = kv.split(':')
            passports[-1][k] = v

print(f'Part 1: {sum(map(valid_pt1, passports))}')
print(f'Part 2: {sum(map(valid_pt2, passports))}')
