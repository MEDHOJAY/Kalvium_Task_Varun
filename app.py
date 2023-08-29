from flask import Flask, jsonify
import operator

app = Flask(__name__)

# List to store history
history = []

# Map operator strings to actual operator functions
operators = {
    'plus': operator.add,
    'minus': operator.sub,
    'into': operator.mul,
    # Add more operators here
}

@app.route('/')
def available_endpoints():
    endpoints = [
        '/',
        '/history',
        '/<float:number>/<operator>/<float:number>',
        # Add more operators here
    ]
    return '<br>'.join(endpoints)

@app.route('/history')
def get_history():
    return jsonify(history)

@app.route('/<float:number>/<operator>/<float:number>')
def perform_operation(number, operator, number2):
    if operator in operators:
        operation = f"{number} {operator} {number2}"
        answer = operators[operator](number, number2)
        history.append({'question': operation, 'answer': answer})

        if len(history) > 20:
            history.pop(0)  # Remove the oldest entry if history exceeds 20 operations

        return jsonify({'question': operation, 'answer': answer})
    else:
        return jsonify({'error': 'Invalid operator'}), 400

if __name__ == '__main__':
    app.run(debug=True)
