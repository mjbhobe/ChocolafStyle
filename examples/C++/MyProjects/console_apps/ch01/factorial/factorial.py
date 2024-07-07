"""
// -------------------------------------------------------------------------
// factorial.py: calculate factorial
// In this example we make use of GNU MPZ class library
//
// @author: Manish Bhobe
// My experiments with C++ & Qt Framework
// This code is meant for learning & educational purposes only!!
// -------------------------------------------------------------------------
"""
import math

"""
Python makes it extremely easy to calculate factorial of arbitrarily
large numbers - just use the math.factorial(...) method
"""
def main():

    while (True):   # NOTE: infinite loop!
        num = input("Enter a number (Enter to quit): ")
        if len(num.strip()) == 0:
            break
        num = int(num)
        print(f"{num}! = {math.factorial(num)}")

if __name__ == "__main__":
    main()

