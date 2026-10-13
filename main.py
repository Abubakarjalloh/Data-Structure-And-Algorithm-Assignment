"""DCOMP320: Evaluate arithmetic expressions using two explicit stacks."""
import re
from pathlib import Path

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise ValueError("Cannot pop from an empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise ValueError("Cannot peek into an empty stack")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)

PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}
TOKEN_PATTERN = re.compile(r'\d+(?:\.\d+)?|[()+\-*/]')

def tokenize(expression):
    compact = re.sub(r'\s+', '', expression)
    tokens = TOKEN_PATTERN.findall(compact)
    if ''.join(tokens) != compact or not tokens:
        raise ValueError('Invalid expression or unsupported character')
    # Turn unary minus into (0 - value), including before parentheses.
    result = []
    for i, token in enumerate(tokens):
        unary = token in ('-', '+') and (i == 0 or tokens[i-1] in ('(', '+', '-', '*', '/'))
        if unary:
            if i + 1 >= len(tokens):
                raise ValueError('Missing number after unary operator')
            if token == '+':
                continue
            if tokens[i+1] == '(':
                # Represent -(... ) as 0-(...); nested arithmetic requires grouping.
                result.extend(['(', '0', '-'])
                depth = 0
                for j in range(i+1, len(tokens)):
                    if tokens[j] == '(': depth += 1
                    if tokens[j] == ')':
                        depth -= 1
                        if depth == 0: break
                # For simplicity, reject unary before parenthesis rather than mis-evaluate.
                raise ValueError('Unary minus before parentheses is not supported')
            continue  # negative number added when next token processed
        if i and tokens[i-1] == '-' and (i == 1 or tokens[i-2] in ('(', '+', '-', '*', '/')):
            if re.fullmatch(r'\d+(?:\.\d+)?', token):
                result.append('-' + token)
                continue
        result.append(token)
    return result

def apply_operator(values, operators):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()
    if operator == '+': answer = left + right
    elif operator == '-': answer = left - right
    elif operator == '*': answer = left * right
    else:
        if right == 0: raise ZeroDivisionError('Division by zero')
        answer = left / right
    values.push(answer)

def evaluate(expression):
    values, operators = Stack(), Stack()
    for token in tokenize(expression):
        if re.fullmatch(r'-?\d+(?:\.\d+)?', token):
            values.push(float(token))
        elif token == '(':
            operators.push(token)
        elif token == ')':
            while not operators.is_empty() and operators.peek() != '(':
                apply_operator(values, operators)
            if operators.is_empty(): raise ValueError('Unmatched closing parenthesis')
            operators.pop()
        else:
            while (not operators.is_empty() and operators.peek() != '('
                   and PRECEDENCE[operators.peek()] >= PRECEDENCE[token]):
                apply_operator(values, operators)
            operators.push(token)
    while not operators.is_empty():
        if operators.peek() == '(': raise ValueError('Unmatched opening parenthesis')
        apply_operator(values, operators)
    if len(values) != 1: raise ValueError('Malformed expression')
    return values.pop()

def format_result(value):
    return str(int(value)) if value.is_integer() else f'{value:.10g}'

def process_file(input_path='input.txt', output_path='output.txt'):
    lines = Path(input_path).read_text(encoding='utf-8').splitlines()
    output = []
    for line in lines:
        stripped = line.strip()
        if not stripped or re.fullmatch(r'-{3,}', stripped):
            output.append(line)
        else:
            try:
                output.append(format_result(evaluate(stripped)))
            except (ValueError, IndexError, ZeroDivisionError, KeyError) as error:
                output.append(f'ERROR: {error}')
    Path(output_path).write_text('\n'.join(output) + '\n', encoding='utf-8')
    print(f'Processed {len(lines)} lines. Results saved to {output_path}')

if __name__ == '__main__':
    process_file()
