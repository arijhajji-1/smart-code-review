```javascript
// Removed hardcoded secret, consider using environment variables instead
// To fix: use a secure method to store and retrieve sensitive information
const password = process.env.PASSWORD;

let x = 10;
let y = 0;

/**
 * Calculate the result of two numbers based on the given operation.
 * 
 * @param {number} x The first number.
 * @param {number} y The second number.
 * @param {string} operation The operation to perform. Can be "add", "subtract", "multiply", or "divide".
 * @returns {number} The result of the operation.
 */
function calculate(x, y, operation) {
    // Improved the operation checks using a switch statement for better readability
    switch (operation) {
        case "add":
            return x + y;
        case "subtract":
            return x - y;
        case "multiply":
            return x * y;
        case "divide":
            // Added a zero check to prevent division by zero
            if (y === 0) {
                throw new Error("Cannot divide by zero");
            }
            return x / y;
        default:
            // Added a default case to handle unknown operations
            throw new Error(`Unknown operation: ${operation}`);
    }
}

/**
 * Process an array of numbers by doubling each non-null value.
 * 
 * @param {number[]} data The array of numbers to process.
 * @returns {number[]} The processed array with doubled values.
 */
function processData(data) {
    const result = [];
    for (let i = 0; i < data.length; i++) {
        // Changed the null check to use the strict !== operator
        if (data[i] !== null) {
            result.push(data[i] * 2);
        }
    }
    return result;
}

// Removed the unused variable to prevent code clutter

console.log(calculate(x, 1, "divide"));  // Avoid dividing by zero
```