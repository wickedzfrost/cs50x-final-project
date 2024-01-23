from helpers import decode

stack = []


def track(input):
    input = decode(input)
    if input in stack:
        return "false"
    else:
        stack.append(input)
        return "true"


def reset_stack():
    global stack
    stack = []
