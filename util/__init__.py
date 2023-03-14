import json


def ResultJson(code, msg, data):
    ret = {
        'code': code,
        'msg': msg,
        'data': data
    }
    print('返回的数据：', ret)
    return json.dumps(ret, ensure_ascii=False)
