#-*- coding:UTF-8 -*-
from flask_restful import Resource, reqparse
from flask import jsonify


parser = reqparse.RequestParser()
parser.add_argument('getChannel', type=str)
parser.add_argument('channelId', type=str)

class ApiTest(Resource):
    """
    API测试类，最基本的演示功能
    curl http://localhost:5000/getChannel=aaa&channelId=123123123  ---> parser.parser_args() --> {"channelId": "123123123", "getChannel": "aaa"}
    curl -X GET -d "data=haha&data2=heihei" http://localhost:5000 ---> request.form['data'] --> haha
    curl -X POST -d "data=haha&data2=heihei" http://localhost:5000 ---> request.form['data2'] --> heihei
    """
    def get(self):
        tasks = [
        {
            'id': 1,
            'title': u'Buy groceries',
            'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
            'done': False
        }]
        #return jsonify({"tasks":tasks})
        #return parser.parse_args()
        return request.form['data']

    def post(self):
        #return jsonify({"tasks":tasks})
        #return parser.parse_args()
        return request.form['data2']

if __name__ == "__main__":
    at = ApiTest()
    print at.get()