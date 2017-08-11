#-*- coding:UTF-8 -*-
from flask_restful import Resource, reqparse
from falsk import jsonify

parser = reqparse.RequestParser()
parser.add_argument('domain', type=str)
parser.add_argument('ip', type=str)

class domain(Resource):
    """
    1. 接收json格式参数:{"domain":"www.test.com", "ip":"10.10.10.10"}
    2. 根据参数将域名重新解析或者新增解析
    3. 返回json格式结果:{"status":"success|failed"}
    """
    def get(self):
        pass

    def post(self):
        pass

    def update(self):
        pass

    def check(self):
        pass

