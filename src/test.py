from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
#mysql = MySQL(app)


@app.route('/abc')
def users():
    print('---------------------------------------')
    """cur = mysql.connection.cursor()
    cur.execute('''SELECT user, host FROM mysql.user''')
    rv = cur.fetchall()
    return str(rv)"""
    return "122222222222222222222222222222"

if __name__ == '__main__':
    print('111111111111111111111111111111')
    app.run(debug=True, port=9006)
