import main
import asyncio
from httpx import AsyncClient
import data
from application.app import Application
from models import prediction_request

app = Application()
async def data():
    await main.create_job()
    job_value=list(app.jobs.values())
    job_keys=list(app.jobs.keys())
    return job_keys,job_value




keys,value=asyncio.run(data())



completed_jobID=[]
valid_value=[]

for i in range(len(keys)):
    if value[i]['status'] =='completed':
        completed_jobID.append(keys[i])
        valid_value.append(value[i])

for id in completed_jobID:
    pass
    #print(id)
for val in valid_value:
    pass
    #print(val)

valid_id=[]

getStatus=asyncio.run(app.get_status(job_id=completed_jobID[0]))
getStatus=asyncio.run(app.get)

print(getStatus)
res=[]
#for id in completed_jobID:
#    res.append(asyncio.run(AsyncClient.get(url=f'http://127.0.0.1:8000/result/{id}')))
async def result():
    d= AsyncClient.get(url=f'http://127.0.0.1:8000/result/{completed_jobID[0]}')
    r=await d
    print(r.status_code)

print(asyncio.run(result()))




#print(asyncio.run(AsyncClient.get(url=f'http://127.0.0.1:8000/result/{completed_jobID[0]}')).status_code)

'''
for i in range(len(res)):
    if res['status'][i] == 'completed':
        completed_job.append(res['result'][i])


for j in range(len(completed_job)):
    print(completed_job[j])

'''


