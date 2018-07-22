# coding: utf-8
from spiney import b_to_order

b_to_orders = []
for n in range(65):
    b_to_orders.append((n, b_to_order(n, 6), "Prime" if isprime(n) else ""))

for order in b_to_orders:
    if order[2] == "Prime":
        print(order[:2])
