def print_cover(text, tent_size, depth, covered_squares, bag_squares = set()):
    out = ''.join(['  ' for _ in range(depth)]) + text + '\n'
    if covered_squares == None:
        print(out)
        return out
    for x in range(tent_size[0]+2):
        out += ''.join(['  ' for _ in range(depth)])
        for y in range(tent_size[1]+2):
            if (x, y) in covered_squares and (x, y) in bag_squares:
                out += '\033[105m   '
            elif (x, y) in covered_squares:
                out += '\033[106m   '
            elif (x, y) in bag_squares:
                out += '\033[101m   '
            elif x < tent_size[0] and y < tent_size[1]:
                out += '\033[47m   '
            else:
                out += '\033[107m   '
        out += '\033[0m\n'



    print(out)

    return out

def print_pack(tent_size, rocks, bag_list, pack, depth=0):
    colors = ['\033[41m', '\033[43m', '\033[103m', '\033[42m', '\033[44m', '\033[45m']
    tent = [['\033[107m . ' for _ in range(tent_size[1])] for _ in range(tent_size[0])]
    for x,y in rocks:
        tent[x][y] = '\033[107m * '
    for i, p in enumerate(pack):
        x,y = p['anchor']
        shape = p['shape']
        for xi, yi in bag_list[shape]:
            tent[x+xi][y+yi] =  colors[shape] + ' ' + str(i) + ' '

    out = ''
    for x in range(tent_size[0]):
        out += ''.join(['  ' for _ in range(depth)])
        for y in range(tent_size[1]):
            out += tent[x][y]
        out += '\033[0m\n'
    print(out)
    return out

def print_packings(tent_size, rocks, bag_list, packings, depth=0):
    if packings:
        for pack in packings:
            print_pack(tent_size, rocks, bag_list, pack, depth)

