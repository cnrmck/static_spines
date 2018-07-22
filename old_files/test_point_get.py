# coding: utf-8
def b_to_order(n, b):
    orders = []
    while n > 0:
        order = 1
        b_order = b**order
        while n - b_order >= b_order:
            order+=1
            b_order = b**order
        if n == 1:
            # this is used to save a little computation. Could alternatively start
            # order at 0. Should do performance tests
            orders.append(0)
            n -= 1
        else:
            orders.append(order)
            n -= b_order
    return tuple(orders)
