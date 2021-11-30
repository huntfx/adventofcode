with open('input.txt', 'r') as f:
    count_pt1 = 0
    count_pt2 = 0
    for line in f:
        policy, password = line.strip().split(': ')
        numbers, letter = policy.split()
        min_num, max_num = map(int, numbers.split('-'))

        if min_num <= password.count(letter) <= max_num:
            count_pt1 += 1

        if (password[min_num - 1] == letter) + (password[max_num - 1] == letter) == 1:
            count_pt2 += 1

print(f'Part 1: {count_pt1}')
print(f'Part 2: {count_pt2}')
