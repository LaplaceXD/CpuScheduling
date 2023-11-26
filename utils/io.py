from typing import List, Optional

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

def input_choice(prompt: object = "", choices: List[str] = [], default: str = ""):
    """ Make a user select between a set of values. """
    result: Optional[str] = None
    prompt_suffix = "(" + "/".join(choices) + (", default: " + default if default else "") + ")"
    prompt_text = prompt + " " + prompt_suffix + " "
    choices_lowered = list(map(lambda s : s.lower(), choices))

    while result is None:
        try:
            result = input(prompt_text).strip()
            if result == "":
                result = default
            elif result.lower() not in choices_lowered:
                result = None
                raise ValueError()
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            exit(1)
        except:
            print("Please input {} only.".format("(" + "/".join(choices) + ")"))
   
    return result