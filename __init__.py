from flask import Flask, jsonify, abort, request
import redis
import json
from collections import OrderedDict

app = Flask(__name__)

local_host = '10.37.5.156'

r = redis.Redis(host=local_host, port=6379, decode_responses=True)

# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web', 
#         'done': False
#     }
# ]

# r.delete('mylist')

# for values in tasks:
#     r.rpush('mylist', json.dumps(values, sort_keys=False))

@app.route('/')
def hello():
    return 'hello!'


@app.route('/api/tasks', methods = ['GET'])
def get():
    data = []
    for values in r.lrange('mylist', 0, -1):
        temp = json.loads(values)
        data.append(temp)
        #print(temp)
    return jsonify({'tasks': data})


@app.route('/api/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    #检查tasks内部的元素，是否有元素的id值和参数相匹配
    data = []
    for values in r.lrange('mylist', 0, -1):
        temp = json.loads(values)
        data.append(temp)
    task = list(filter(lambda t : t['id'] == task_id, data))
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route('/api/tasks', methods = {'POST'})
def create_task():
    #如果请求里面没有json数据，或者json数据里面title的内容为空
    if not request.json or not 'title' in request.json:
        abort(404)
    #检查id是否重复
    data = []
    for values in r.lrange('mylist', 0, -1):
        temp = json.loads(values)
        data.append(temp)
    task = list(filter(lambda t : t['id'] == request.json['id'], data))
    if len(task) != 0:
        abort(400)
    task = {
        'id': request.json['id'], 
        'title': request.json['title'], 
        'description': request.json.get('description', ""),
        'done': False
    }
    task = json.dumps(task)
    r.rpush('mylist', task)
    data = []
    for values in r.lrange('mylist', 0, -1):
        values = json.loads(values)
        data.append(values)
    return jsonify({'task':data}), 201


@app.route('/api/tasks/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    #检查是否有这个id数据
    data = []
    for values in r.lrange('mylist', 0, -1):
        temp = json.loads(values)
        data.append(temp)
    task = list(filter(lambda t : t['id'] == task_id, data))
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    #如果请求中没有附带json数据，则报错400
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    #如果title对应的值，不是字符串类型，则报错400
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    #检查done对应的值是否是布尔值
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    #如果上述条件全部通过的话，更新title的值，同时设置默认值
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    task1 = json.dumps(task[0])
    r.lset('mylist', task_id - 1, task1)
    #返回修改后的数据
    return jsonify({'task': task1})


@app.route('/api/tasks/<int:task_id>', methods = ['PATCH'])
def update_task2(task_id):
    #检查是否有这个id数据
    data = []
    for values in r.lrange('mylist', 0, -1):
        temp = json.loads(values)
        data.append(temp)
    task = list(filter(lambda t : t['id'] == task_id, data))
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    #如果请求中没有附带json数据，则报错400
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    #如果title对应的值，不是字符串类型，则报错400
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    #检查done对应的值是否是布尔值
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    #如果上述条件全部通过的话，更新title的值，同时设置默认值
    if task[0]['title']:
        task[0]['title'] = request.json.get('title', task[0]['title'])
    if task[0]['description']:
        task[0]['description'] = request.json.get('description', task[0]['description'])
    if task[0]['done']:
        task[0]['done'] = request.json.get('done', task[0]['done'])
    task1 = json.dumps(task[0])
    r.lset('mylist', task_id - 1, task1)
    #返回修改后的数据
    return jsonify({'task': task1})


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    #检查是否有这个数据
    data = []
    for values in r.lrange('mylist', 0, -1):
        temp = json.loads(values)
        data.append(temp)
    task = list(filter(lambda t: t['id'] == task_id, data))
    if len(task) == 0:
        abort(404)
    #从tasks列表中删除这个值
    task1 = json.dumps(task[0])
    r.lrem('mylist', 0, task1)
    #返回结果状态，自定义的result
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(host = local_host, debug = True)