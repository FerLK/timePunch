from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    #return render_template('index.html', actives=True)
    return "this is working"


if __name__ == '__main__':
    app.run()