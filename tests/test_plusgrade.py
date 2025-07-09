import asyncio

import asyncio
import time

import pytest

import main
from application.app import Application
from data import prediction_mock_data
from models import prediction_request

from models import prediction_request

app = Application()
url='http://127.0.0.1:8000/predict'

@pytest.mark.asyncio
async def test_createSession(async_client):
    res=await async_client.get('http://127.0.0.1:8000/ping')

    print(res.status_code)
    assert res.status_code==200

@pytest.mark.asyncio
async def test_POST_API(async_client):
    test_POST_API.__doc__="This test validates whether the POST call works as expected"
    body={'member_id':'M01',
          'balance':10000,
            'last_purchase_size':60,
           'last_purchase_date':'2025-02-02'}
    #job=await async_client.post(url='http://127.0.0.1:8000/predict',json=body)
    task=await asyncio.create_task(async_client.post(url='http://127.0.0.1:8000/predict',json=body))
    #print(job.content)
    print(task.status_code)
    print(task.content)
    print(app.jobs.keys())
    assert task.status_code==200

@pytest.mark.asyncio
async def test_status_API(async_client):
    test_status_API.__doc__="This test validates whether status API works as expected"
    print(app.jobs.keys())
    body = {'member_id': 'M01',
            'balance': 40000,
            'last_purchase_size': 60,
            'last_purchase_date': '2025-02-02'}
    job=await async_client.post(url='http://127.0.0.1:8000/predict',json=body)



@pytest.mark.asyncio
async def test_result_API(async_client,data_load):
    result=await async_client.get(url=f'http://127.0.0.1:8000/result/{"'"+data_load[0]+"'"}')
    print(f'results are {result.json()}')
    for i in range(100):
        res=await async_client.get(url=f'http://127.0.0.1:8000/result/{"'" + data_load[i] + "'"}')

        print(res.json())

    print(result.status_code)
    assert result.status_code==200

@pytest.mark.asyncio
async def test_status_API(async_client):
    pay_load={'member_id':'M01',
          'balance':10000,
            'last_purchase_size':60,
           'last_purchase_date':'2025-02-02'}

    data=await async_client.post(url='http://127.0.0.1:8000/predict', json=pay_load)
    assert data.status_code==200
    res=await async_client.get("http://127.0.0.1:8000")
    print(res.json())


    print(app.jobs.values())

@pytest.mark.asyncio
async def test_mock_data(async_client):
    payload = prediction_mock_data
    for i in range(len(payload)):
        mock = {'member_id': payload.values[i][0],
                'balance': payload.values[i][1],
                'last_purchase_size': payload.values[i][2],
                'last_purchase_date': payload.values[i][3]}
        response = await async_client.post(url=url, json=mock)
        print(response.status_code)
        print(app.jobs.values())






