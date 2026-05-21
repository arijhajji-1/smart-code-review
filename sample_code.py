import os
import sys
import os  # duplicate import

def calculate(x,y,operation):
    if operation == "add":
        return x+y
    elif operation == "subtract":
        return x-y
    elif operation == "multiply":
        return x*y
    elif operation == "divide":
        if y == 0:
            return None  # should raise an exception
        return x/y
    elif operation=="power":
        return x**y
    else:
        return None  # silent failure

def process_data(data):
    result = []
    for i in range(len(data)):   # should use enumerate
        if data[i] != None:      # should use `is not None`
            result.append(data[i] * 2)
    return result

password = "supersecret123"   # hardcoded secret!

def unused_function():
    pass