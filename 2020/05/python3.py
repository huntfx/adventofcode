def find_position(line):
    col = int(''.join('01'[c == 'B'] for c in line[:7]), 2)
    row = int(''.join('01'[c == 'R'] for c in line[7:]), 2)
    return col, row

def get_seat_id(col, row):
    return col * 8 + row

def find_missing_seat(seat_ids):
    columns = tuple(sorted(col for col, row in seat_ids.values()))
    last_seat = -3
    for seat_id in sorted(seat_ids):
        if seat_id == last_seat + 2 and seat_ids[seat_id][0] not in (columns[0], columns[-1]):
            return seat_id - 1
        last_seat = seat_id

boarding_passes = []
with open('input.txt', 'r') as f:
    for line in f:
        boarding_passes.append(line.strip())
seat_ids = {get_seat_id(*position): position for position in map(find_position, boarding_passes)}

print(f'Part 1: {max(seat_ids)}')
print(f'Part 2: {find_missing_seat(seat_ids)}')
