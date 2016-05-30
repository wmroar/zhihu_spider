# -*- coding:utf-8 -*-
import flask
import dbtool
app = flask.Flask(__name__)

@app.route('/user/list/')
def user_list():
    result = dbtool.get_data_from_db('user')
    return flask.jsonify({'data': result})


@app.route('/answer/list/')
def answer_list():
    result = dbtool.get_data_from_db('answer')
    return flask.jsonify({'data': result})

if __name__ == '__main__':
    print dbtool.get_data_from_db('user')
    app.run('localhost',8999,debug=True)
