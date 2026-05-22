import os
import sys

# Removed duplicate import

def calculate(x, y, operation):
    # Improved error handling
    if operation == "add":
        return x + y
    elif operation == "subtract":
        return x - y
    elif operation == "multiply":
        return x * y
    elif operation == "divide":
        # Raise an exception for division by zero
        if y == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return x / y
    elif operation == "power":
        return x ** y
    else:
        # Raised an exception for invalid operation
        raise ValueError("Invalid operation")

def process_data(data):
    result = []
    # Using enumerate for clearer code
    for i, item in enumerate(data):
        # Using 'is not None' for correct comparison
        if item is not None:
            result.append(item * 2)
    return result

# Removed hardcoded secret, consider using environment variables or secure storage
import dotenv
dotenv.load_dotenv()
password = os.getenv("PASSWORD")

# Removed unused function

# Consider adding main function or guard clause for script execution
if __name__ == "__main__":
    # Example usage
    print(calculate(5, 2, "add"))
    print(process_data([1, 2, None, 4]))