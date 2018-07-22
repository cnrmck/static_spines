# coding: utf-8
from math import sqrt
def F(n):
    return ((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5))
def gimme_numbers(x, size=100):
    for n in range(x):
        print((F(n)/2**n)*size)
        
        
def gimme_numbers_graph(x, size=100):
    for n in range(x):
        l = (F(n)/2**n)*size
        print("."*int(l))
        
        
        
gimme_numbers_graph(10)
