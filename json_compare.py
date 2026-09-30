"""Bounded JSON structural comparison; inputs are never persisted."""
import collections
import json
import math

def parse(text):
    if not isinstance(text,str) or len(text.encode('utf-8'))>262144:raise ValueError('Each input must be text under 256 KiB')
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('Duplicate object key: '+key[:80])
            result[key]=value
        return result
    def bad(value):raise ValueError('Non-finite JSON number')
    try:value=json.loads(text,object_pairs_hook=pairs,parse_constant=bad)
    except (json.JSONDecodeError,RecursionError) as error:raise ValueError('Invalid JSON or excessive nesting') from error
    count=[0]
    def check(node,depth=0):
        count[0]+=1
        if depth>64 or count[0]>10000:raise ValueError('JSON exceeds depth/node limit')
        if isinstance(node,float) and not math.isfinite(node):raise ValueError('Non-finite JSON number')
        if isinstance(node,dict):
            for child in node.values():check(child,depth+1)
        elif isinstance(node,list):
            for child in node:check(child,depth+1)
    check(value)
    return value

def compare(left,right,ignore_paths=None,unordered=False):
    a,b=parse(left),parse(right)
    paths=ignore_paths or []
    if not isinstance(paths,list) or len(paths)>50 or any(not isinstance(p,str) or not p.startswith('/') or len(p)>512 for p in paths):
        raise ValueError('Ignore paths must be up to 50 exact JSON pointers starting with /')
    ignored=set(paths);changes=[];total=[0]
    def child(path,key):return path+'/'+str(key).replace('~','~0').replace('/','~1')
    def canonical(node,path):
        if isinstance(node,dict):return ['object',[(k,canonical(v,child(path,k))) for k,v in sorted(node.items()) if child(path,k) not in ignored]]
        if isinstance(node,list):
            values=[canonical(v,child(path,i)) for i,v in enumerate(node) if child(path,i) not in ignored]
            if unordered:values.sort(key=lambda v:json.dumps(v,sort_keys=True))
            return ['array',values]
        return [type(node).__name__,node]
    def add(path,kind,old=None,new=None):
        total[0]+=1
        if len(changes)<200:changes.append({'path':path or '', 'kind':kind,'before':old,'after':new})
    def walk(x,y,path=''):
        if path in ignored:return
        if type(x)!=type(y):add(path,'changed',x,y);return
        if isinstance(x,dict):
            for key in sorted(x.keys()|y.keys()):
                p=child(path,key)
                if p in ignored:continue
                if key not in x:add(p,'added',None,y[key])
                elif key not in y:add(p,'removed',x[key],None)
                else:walk(x[key],y[key],p)
        elif isinstance(x,list):
            if unordered:
                if canonical(x,path)!=canonical(y,path):add(path,'array_changed',x,y)
            else:
                for i in range(max(len(x),len(y))):
                    p=child(path,i)
                    if p in ignored:continue
                    if i>=len(x):add(p,'added',None,y[i])
                    elif i>=len(y):add(p,'removed',x[i],None)
                    else:walk(x[i],y[i],p)
        elif x!=y:add(path,'changed',x,y)
    walk(a,b)
    return {'equal':total[0]==0,'change_count':total[0],'changes':changes,'truncated':total[0]>len(changes),
            'scope':'Exact JSON-pointer exclusions; unordered arrays preserve duplicate counts; JSON number types compared strictly.'}
