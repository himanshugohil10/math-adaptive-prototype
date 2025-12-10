
import random
import operator

def generate_puzzle(difficulty):
    """
    Generates a math puzzle with strict rules for difficulty levels.

    Args:
        difficulty (str): 'Easy', 'Medium', or 'Hard'.

    Returns:
        dict: {
            'question_text': str,
            'answer': int,
            'difficulty': str
        }
    """
    
    # --- EASY ---
    # Operations: +, -, *
    # +,-: Answers single digit (<10). Operands single digit.
    # *: Single digit x Single digit. Result < 100 (always true).
    # No Division.
    if difficulty == 'Easy':
        op_func, op_symbol = random.choice([(operator.add, '+'), (operator.sub, '-'), (operator.mul, '*')])
        
        if op_symbol == '+':
            # Result < 10. a+b < 10.
            # Pick a in 1-8 (since b must be at least 1)
            a = random.randint(1, 8)
            b = random.randint(1, 9 - a)
        elif op_symbol == '-':
            # Result single digit (always true if operands are single digit positive integers and a>b)
            # a in 1-9, b in 1-9.
            a = random.randint(1, 9)
            b = random.randint(1, a) # includes a=b -> 0
        elif op_symbol == '*':
            # Single digit x Single digit
            a = random.randint(1, 9)
            b = random.randint(1, 9)
            
        answer = op_func(a, b)
        question = f"{a} {op_symbol} {b}"

    # --- MEDIUM ---
    # Operations: +, -, *, /
    # *: 1-digit x 2-digit.
    # /: Whole number answers.
    # +, -: Can involve 2-digit numbers. Answers usually < 100 (2 digits).
    elif difficulty == 'Medium':
        op_func, op_symbol = random.choice([
            (operator.add, '+'), 
            (operator.sub, '-'), 
            (operator.mul, '*'), 
            (operator.floordiv, '/')
        ])
        
        if op_symbol == '*':
            # 1-digit x 2-digit
            # Pick which is 1-digit
            if random.random() < 0.5:
                a = random.randint(2, 9)
                b = random.randint(10, 99)
            else:
                a = random.randint(10, 99)
                b = random.randint(2, 9)
        elif op_symbol == '/':
            # Whole number answer.
            # Pick divisor (b) and quotient (q). a = b*q.
            # Keep numbers reasonable for Medium (2-digit operands mainly).
            # b in 2-9 is good for mental math.
            b = random.randint(2, 12)
            # q (answer) in 2-20?
            q = random.randint(2, 20)
            a = b * q
        elif op_symbol == '+':
            # Result < 100 preferred but not strictly enforced "Answer usually 2 digits".
            # Let's target result < 100.
            a = random.randint(5, 80)
            b = random.randint(5, 99 - a)
        elif op_symbol == '-':
            # 2-digits involvement.
            a = random.randint(20, 99)
            b = random.randint(5, a)
            
        answer = op_func(a, b)
        question = f"{a} {op_symbol} {b}"

    # --- HARD ---
    # Operations: +, -, *, /
    # Answer may reach 3 digits.
    # /: Whole number.
    # *: 2-3 digit result.
    # Carrying/Borrowing likely (standard random logic usually covers this).
    elif difficulty == 'Hard':
        op_func, op_symbol = random.choice([
            (operator.add, '+'), 
            (operator.sub, '-'), 
            (operator.mul, '*'), 
            (operator.floordiv, '/')
        ])
        
        if op_symbol == '*':
            # Result 2-3 digits. 10-999.
            # Could be 2-digit x 2-digit (small ones) or 1-digit x 3-digit?
            # User said: "Multiplication may produce two- or three-digit answers"
            # Let's do 2-digit x 1-digit (large) or 2-digit x 2-digit (small).
            a = random.randint(10, 50)
            b = random.randint(2, 20)
            # Check strictly? random is fine.
        elif op_symbol == '/':
            # Harder division.
            # b in 5-20. q in 5-50?
            b = random.randint(5, 25)
            q = random.randint(10, 40)
            a = b * q
        elif op_symbol == '+':
            # Result up to 3 digits (e.g. 150).
            a = random.randint(20, 500)
            b = random.randint(20, 500)
        elif op_symbol == '-':
            # Result 2-3 digits.
            a = random.randint(100, 999)
            b = random.randint(10, a - 10) # ensure not single digit result usually
            
        answer = op_func(a, b)
        question = f"{a} {op_symbol} {b}"

    else:
        return generate_puzzle('Easy')

    return {
        'question_text': question,
        'answer': answer,
        'difficulty': difficulty
    }
