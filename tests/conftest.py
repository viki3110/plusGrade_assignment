import asyncio
import time
from threading import Thread

import pytest_asyncio
import uvicorn
from httpx import AsyncClient
from uvicorn.supervisors.multiprocess import Process

#from application.app import Application
from util.utility import data, job
#app=Application()
app=job.Application()


@pytest_asyncio.fixture
async def launch_app():
    app=job.Application()
    server=uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            host="127.0.0.1",
            port=8000,
            log_level="info"
        )
    )

    thread=Thread(target=server.run, daemon=True)
    thread.start()
    try:
        time.sleep(1)
        yield
    finally:
        server.should_exit=True
        thread.join()

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient() as client:
        yield client


@pytest_asyncio.fixture
async def data_load(data_provider):
    keys,value=data_provider
    completed_jobID = []
    completed_values=[]
    for i in range(len(keys)):
        if value[i]['status'] == 'completed':
            completed_jobID.append(keys[i])
            completed_values.append(value[i])
    print(f'first completed value with valid job {completed_jobID[0]} are {completed_values[0]}')
    return completed_jobID
@pytest_asyncio.fixture
async def data_provider():
    await job.create_job()

    job_value=list(app.jobs.values())
    job_keys=list(app.jobs.keys())
    return job_keys,job_value

'''
    job=list(app.jobs.values())
    print(len(job))
    jobID=list(app.jobs.keys())
    job_status=list(app.jobs.values())
    jobid_valid=[]
    for i in range(len(app.jobs)):
        if job_status[i]['result'] is not None:
            #rint(app.get_result(job_id=jobID[i]))
            jobid_valid.append(jobID[i])
            #print(await app.get_status(job_id=jobID[i]))
            #print(app.get_result((jobID[i])))
    return jobid_valid
    '''





