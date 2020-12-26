prompt = "Welcome aho calculator,\nWrite down the formula you want to calculate."
prompt += "\nEnter 'quit' to end the program. \n-->"

active = True
while active:
    message = input(prompt)

    if message == 'quit':
        break
    else:
        print("You wanna know the result of:", message)
