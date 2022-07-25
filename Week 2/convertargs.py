import sys

def tempconvert(temp, dir='f2c'):
    """
    This function converts Fahrenheit to Celsius (default),
    and vice versa
    """
    if dir == 'f2c':
        c = (temp-32)*5/9
        return c
    elif dir == 'c2f':
        f = temp*9/5 + 32
        return f
    else:
        print(f'dir must be f2c or c2f, got {dir} instead')

def main():
    args = len(sys.argv) # command line arguments
    
    # no parameters given (first arg is program name)
    # or too many parameters
    if args == 1 or args > 3:
        print(f'usage: {sys.argv[0]} temperature ["f2c"|"c2f"]')
        return 
    
    if args == 2: # one argument, temperature
        res = tempconvert(float(sys.argv[1]))
    else:
        res = tempconvert(float(sys.argv[1]), sys.argv[2])
    print(res)
    
main()