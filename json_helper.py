import json


def json_loads(data):
    return json.loads(data)


def json_dumps(data):
    return json.dumps(data)


def json_result(data):
    data['result'] = True
    return json.dumps(data)


def json_error(error):
    return json.dumps({'result': False, 'error': error})
