// TODO: add explanations
const INTERVIEW_QUESTIONS = [
  {
    id: 1,
    difficulty_level: "easy",
    question: `Write a Python function is_even that takes an integer num as input and returns True if num is an even number and False if it is an odd number.

The function should not use any built-in Python functions for checking evenness or oddness (such as num % 2 == 0 or num & 1 == 0). Instead, implement the logic to check if the number is even using only basic arithmetic or bitwise operations.

Examples:
Example 1:

Input: num = 4
Output: True
Explanation: 4 is even, so the function returns True.

Example 2:

Input: num = 7
Output: False
Explanation: 7 is odd, so the function returns False.

Example 3:

Input: num = -10
Output: True
Explanation: -10 is even, so the function returns True.

Constraints:
The input integer num will be in the range of -10^9 <= num <= 10^9.
Follow-up:
Can you think of a way to determine evenness using only bitwise operators, which can be more efficient than traditional arithmetic methods?`,
    solution: `function isEven(number) {
    return number % 2 === 0;
}`,
  },
  {
    id: 2,
    difficulty_level: "medium",
    question: `Write a Python function is_prime that takes an integer num as input and returns True if num is a prime number and False if it is not.

A prime number is defined as an integer greater than 1 that has no positive divisors other than 1 and itself.

Your function should implement an efficient algorithm for checking primality and avoid using built-in libraries for this purpose.

Examples:
Example 1:

Input: num = 7
Output: True
Explanation: 7 has no divisors other than 1 and 7, so it is a prime number.

Example 2:

Input: num = 10
Output: False
Explanation: 10 is divisible by 2 and 5, so it is not a prime number.

Example 3:

Input: num = 1
Output: False
Explanation: 1 is not considered a prime number.

Constraints:
The input integer num will be in the range of 0 <= num <= 10^6.
Follow-up:
Can you optimize your algorithm to achieve a time complexity of 𝑂(root(n)) by minimizing the number of divisibility checks? Consider edge cases, such as very small numbers, and account for efficiency in the algorithm design.`,
    solution: `function isPrime(number) {
    if (number <= 1) {
        return false;
    }
    for (let i = 2; i <= Math.sqrt(number); i++) {
        if (number % i === 0) {
            return false;
        }
    }
    return true;
}`,
  },
  {
    id: 3,
    difficulty_level: "hard",
    question: `Write a Python function fibonacci that takes a non-negative integer n as input and returns the nth number in the Fibonacci sequence.

The Fibonacci sequence is defined as follows:

fibonacci(0) = 0
fibonacci(1) = 1
fibonacci(n) = fibonacci(n - 1) + fibonacci(n - 2) for n > 1
Examples:
Example 1:

Input: n = 5
Output: 5
Explanation: The Fibonacci sequence up to the 5th position is [0, 1, 1, 2, 3, 5], so fibonacci(5) returns 5.

Example 2:

Input: n = 0
Output: 0
Explanation: By definition, fibonacci(0) is 0.

Example 3:

Input: n = 10
Output: 55
Explanation: The 10th number in the Fibonacci sequence is 55.

Constraints:
The input integer n will satisfy 0 <= n <= 30.
Aim to achieve an efficient solution that avoids recalculating values unnecessarily.
Follow-up:
Can you optimize your function to handle larger values of n (e.g., up to n = 10^6)? Consider techniques such as memoization or iterative solutions to reduce time complexity.`,
    solution: `function fibonacci(n) {
    if (n <= 0) {
        return 0;
    } else if (n === 1) {
        return 1;
    } else {
        return fibonacci(n-1) + fibonacci(n-2);
    }
}`,
  },
];

export default INTERVIEW_QUESTIONS;