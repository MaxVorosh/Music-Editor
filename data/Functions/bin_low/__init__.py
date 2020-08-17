def bin_low(data, elem):
    l = 0
    r = len(data)
    while r - l > 1:
        m = (r + l) // 2
        if data[m] <= elem:
            l = m
        else:
            r = m
    return l
