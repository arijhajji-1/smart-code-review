var password = "supersecret123"  // hardcoded secret

var x = 10
var y = 0

function calculate(x, y, operation) {
    if (operation == "add") return x + y
    if (operation == "subtract") return x - y
    if (operation == "multiply") return x * y
    if (operation == "divide") return x / y  // no zero check!
}

function processData(data) {
    var result = []
    for (var i = 0; i < data.length; i++) {
        if (data[i] != null) {   // should use !==
            result.push(data[i] * 2)
        }
    }
    return result
}

var unused = "this variable is never used"

console.log(calculate(x, y, "divide"))  // will return Infinity