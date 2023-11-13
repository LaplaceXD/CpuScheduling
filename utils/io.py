from typing import Optional

def input_bounded_num(prompt: object = "", min: int = 1, max: Optional[int] = None):
    """ Get a number input from the user that satisfies a certain minimum and maximum. """
    result: Optional[int] = None
    
    while result is None:
        try:
            result = int(input(prompt))
            if min > result or (max is not None and max < result):
                result = None
                raise ValueError()
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            exit(1)
        except:
            if max is None:
                print("The input should be a number that is at least equal to {}.".format(min))
            else:
                print("The input should be a number between {} and {}.".format(min, max))
   
    return result