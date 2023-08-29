from flask import Flask, jsonify
from collections import OrderedDict
import json
app = Flask(__name__)
history = []
def evaluate_and_store(exp):
    try:
        res = eval(exp)
        ent = OrderedDict([('question', exp), ('answer', res)])
        if ent not in history:
            history.append(ent)
        if len(history) > 20:
            history.pop(0)
        return res, exp
    except Exception as e:
        return None, None
@app.route('/')
def home():
    return "Hello to Kalvium Task by VARUN S"
@app.route('/history')
def get_history():
    return jsonify(history)
@app.route('/<path:exp>')
def calculate(exp):
    exp = exp.replace('/', ' ').replace('plus', '+').replace('minus', '-').replace('into', '*').replace(
        'by', '/')
    oper = {
        '+': ' + ',
        '-': ' - ',
        '*': ' * ',
        '/': ' / ',
    }
    for oper, replac in oper.items():
        exp = exp.replace(oper, replac)
    res, ques = evaluate_and_store(exp)
    if res is not None:
        order_dict = OrderedDict([('question', ques), ('answer', res)])
        return json.dumps(order_dict)
    else:
        return jsonify({'error': 'Invalid expression'}), 400
if __name__ == '__main__':
    app.run(debug=True, port=3000)
