# coding: utf-8
from spiney import get_point
from spiney import sum_partial_sum
hell_yeah = []
for n in range(256):
    hell_yeah.append(get_point(n))



double_hell_yeah = []
for partial_sum in hell_yeah:
    partial_sum = partial_sum[1]
    double_hell_yeah.append(sum_partial_sum(partial_sum))
