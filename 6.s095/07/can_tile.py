def canTile(size, missingTiles):
    size = 2 ** size
    half_size = size // 2
    quads = list(range(4))
    for tile in missingTiles:
        quad = 2*(tile[0] >= half_size) + (tile[1] >= half_size)
        if quad not in quads:
            break
        quads.remove(quad)

    if len(quads) == 0:
        return True

    for tile in missingTiles:
        tile_diffs = [(0, 1), (1, 0)]
        for other in missingTiles:
            if tile != other:
                diff = (abs(tile[0] - other[0]), abs(tile[1] - other[1]))
                if diff in tile_diffs:
                    tile_diffs.remove(diff)
        if len(tile_diffs) == 0:
            return True

    return False

print(canTile(3, [(4, 4), (1, 1), (4, 1), (1, 4)]))
print(canTile(3, [(4, 4), (3, 1), (2, 1), (1, 2)]))
print(canTile(3, [(3, 7), (4, 4), (4, 6), (4, 7)]))