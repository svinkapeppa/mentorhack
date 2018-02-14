import json
import os

arr = ['cb3a3b3c080047af57ad3d4f37ac45e252aecf11ba5e577d6ff01072d899954e','5a820d4e3ec5319990007898','name','desc','5a820cba70681bd03232e176,5a820cba70681bd03232e176','2018-01-01']

to_exec = "echo '" +  json.dumps(arr) + "' | " + os.getcwd() + "/totrello/index.js"

d = os.popen(to_exec).read()

print('py')
print(json.loads(d))