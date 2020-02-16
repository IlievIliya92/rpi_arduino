#!/usr/bin/python3

def utilsTempConverter(val):
    temp = (val/1024.0)*5000;
    temp =  round(val/10, 2)

    return temp
