import re
from collections import deque

saved_ids = {}


def calculator(expression_str):
    rank = {'*': 2, '/': 2, '+': 1, '-': 1}

    # check for invalid operators
    if re.search(r'(\* *\*)|(/ */)', expression_str):  # 3 *** 5
        return 'Invalid expression'

    # remove blanks
    expression_str = re.sub(r' ', '', expression_str)

    elements = re.finditer(r'(\d+)|(\w+)|([-+*/]+)|([()]+)', expression_str)
    # elements = re.finditer(r'(\d+)|(\w+)|([-+\*/]+)|([\(\)]+)', expression_str)
    elements = [el.group() for el in elements]

    postfix = deque()
    operators = deque()
    for el in elements:
        if el.isnumeric():  # --1--
            postfix.append(el)
        elif el in saved_ids:
            postfix.append(saved_ids[el])
        elif el == '(':  # --5--
            operators.append(el)
        elif el == ')':  # --6--
            try:
                while operators[-1] != '(':
                    postfix.append(operators.pop())
                operators.pop()
            except IndexError:
                return "Invalid expression"

        elif re.search(r'[-+*/]', el):
            op = el
            if not operators or operators[-1] == '(':
                operators.append(op)
            elif rank[op] > rank[operators[-1]]:
                operators.append(op)
            elif rank[op] <= rank[operators[-1]]:  # <=  --4-- ???
                while operators and (rank[operators[-1]] >= rank[op] or operators[-1] != '('):
                    postfix.append(operators.pop())
                operators.append(op)
        else:
            return 'Unknown variable'

    if '(' in operators:
        return 'Invalid expression'

    for _i in range(len(operators)):  # --7--
        postfix.append(operators.pop())

    # scan the postfix expression from left to right
    temp = deque()
    for _i in range(len(postfix)):
        el = postfix.popleft()
        if el.isnumeric():
            temp.append(el)
        else:
            if len(temp) >= 2:
                y = int(temp.pop())
                x = int(temp.pop())

                r = None
                if el == '+':
                    r = x + y
                elif el == '-':
                    r = x - y
                elif el == '*':
                    r = x * y
                elif el == '/':
                    r = x // y
                if r is None:
                    return 'Invalid expression'

                res_str = str(r)
                temp.append(res_str)

    return temp[-1]


def assignment(string):
    def validate(operand):
        if re.search(r'(\d[a-zA-Z])|([a-zA-Z]\d)', operand):  # a2, 3a
            return False
        return operand

    if string.count('=') > 1:
        print('Invalid assignment')

    operands = re.search(r'([\w]+) *= *(\w+)', string)
    var, val = (validate(op) for op in operands.group(1, 2))
    if not var or var.isnumeric():
        print('Invalid identifier')
    elif not val:
        print('Invalid assignment')
    else:
        if val.isnumeric():
            saved_ids[var] = val
        else:
            if val not in saved_ids:
                print('Unknown variable')
            else:
                saved_ids[var] = saved_ids[val]


while True:

    user_input = input()

    if not user_input:
        continue

    elif re.match(r'/exit', user_input):
        print('Bye!')
        break

    elif re.match(r'/help', user_input):
        print("The program calculates the sum of numbers.")

    elif re.match(r'^/ *[a-zA-Z]+', user_input):
        print('Unknown command')

    elif re.search(r'=', user_input):
        assignment(user_input)

    else:
        print(calculator(user_input))
