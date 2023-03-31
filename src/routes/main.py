from flask import Blueprint, request, jsonify, render_template

bpMain = Blueprint('bpMain', __name__)

@bpMain.route('/')
def main():
    return render_template('index.html')
