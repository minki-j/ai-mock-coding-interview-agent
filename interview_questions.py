INTERVIEW_QUESTION_AND_SOLUTION = [
    {
        "difficulty_level": "easy",
        "question": "Write a Python function called is_even that takes an integer as input and returns True if the number is even, and False if the number is odd.",
        "solution": "```python\ndef is_even(number):\n\treturn number % 2 == 0\n```",
    },
    {
        "difficulty_level": "medium",
        "question": "Write a Python function called is_prime that takes an integer as input and returns True if the number is prime, and False if the number is not prime.",
        "solution": "```python\ndef is_prime(number):\n\tif number <= 1:\n\t\treturn False\n\tfor i in range(2, int(number ** 0.5) + 1):\n\t\tif number % i == 0:\n\t\t\treturn False\n\treturn True\n```",
    },
    {
        "difficulty_level": "hard",
        "question": "Write a Python function called fibonacci that takes an integer as input and returns the nth number in the Fibonacci sequence.",
        "solution": "```python\ndef fibonacci(n):\n\tif n <= 0:\n\t\treturn 0\n\telif n == 1:\n\t\treturn 1\n\telse:\n\t\treturn fibonacci(n-1) + fibonacci(n-2)\n```",
    }
]