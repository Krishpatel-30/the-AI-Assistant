def calculate(expression):
    try:
        answer = eval(expression)
        return f"Answer = {answer}"
    except:
        return "Invalid calculation."