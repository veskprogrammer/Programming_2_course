def gen_bin_tree(height=5, root=6):
    if height == 0:
        return None
    left = (root * 2) - 2
    right = root + 4
    return {
        'value': root,
        'left': gen_bin_tree(height - 1, left),
        'right': gen_bin_tree(height - 1, right)
    }