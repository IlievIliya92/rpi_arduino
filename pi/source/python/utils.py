#!/usr/bin/python3

def utilsTempConverter(val):
    temp = (val/1024.0)*5000;
    return round(temp/10, 2)
