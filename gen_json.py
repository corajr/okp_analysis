from forum.models import *
import json

tree = Message.dump_bulk()[0]

def traverse(d):
    temp = dict(d, **d['data'])
    del temp['data']  
    temp['date_time'] = temp['date_time'].isoformat()
    if 'children' in d:
        temp['children'] = [traverse(i) for i in d['children']]
    return temp

newTree = traverse(tree)

js = open("okp.json", "w")
json.dump(newTree, js)
js.close()