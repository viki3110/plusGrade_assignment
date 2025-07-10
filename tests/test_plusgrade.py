import asyncio

import asyncio
import time
from uuid import uuid4
import pytest
import data
#import data
import main
from application.app import Application
from data import prediction_mock_data
#from data import prediction_mock_data
from models import prediction_request

from models import prediction_request

app = Application()
url='http://127.0.0.1:8000/predict'

@pytest.mark.asyncio
async def test_createSession(launch_app,async_client):
    res=await async_client.get('http://127.0.0.1:8000/ping')

    print(res.status_code)
    assert res.status_code==200

@pytest.mark.asyncio
async def test_POST_API(launch_app,async_client):
    test_POST_API.__doc__="This test validates whether the POST call works as expected"
    body={'member_id':'POST_PREDICT_API',
          'balance':10000,
            'last_purchase_size':60,
           'last_purchase_date':'2025-02-02'}
    task=await asyncio.create_task(async_client.post(url='http://127.0.0.1:8000/predict',json=body))
    #print(task.status_code)
    #print(task.content)
    #print(app.jobs.keys())
    assert task.status_code==200

@pytest.mark.asyncio
async def test_status_API(launch_app,async_client):
    test_status_API.__doc__="This test validates whether status API works as expected"
    body = {'member_id': 'GET_STATUS_API',
            'balance': 40000,
            'last_purchase_size': 60,
            'last_purchase_date': '2025-02-02'}
    job=await async_client.post(url='http://127.0.0.1:8000/predict',json=body)
    #job=await asyncio.create_task(async_client.post(url='http://127.0.0.1:8000/predict',json=body))

    assert job.status_code==200
    await asyncio.sleep(5)
    completed_jobID,completed_values=[],[]
    keys=list(app.jobs.keys())
    value=list(app.jobs.values())
    for i in range(len(keys)):
        if value[i]['status'] == 'completed':
            completed_jobID.append(keys[i])
            completed_values.append(value[i])

    status=await async_client.get(url=f'http://127.0.0.1:8000/status/{completed_jobID[0]}')
    print(status.json())
    assert status.status_code==200
    #print(f'keys are {keys[0]}')


@pytest.mark.asyncio
async def test_result_API(launch_app,async_client,data_load):
    test_status_API.__doc__="This test validates whether status API works as expected"
    body = {'member_id': 'GET_RESULT_API',
            'balance': 40000,
            'last_purchase_size': 60,
            'last_purchase_date': '2025-02-02'}
    job=await async_client.post(url='http://127.0.0.1:8000/predict',json=body)
    #job=await asyncio.create_task(async_client.post(url='http://127.0.0.1:8000/predict',json=body))

    assert job.status_code==200
    await asyncio.sleep(5)
    completed_jobID,completed_values=[],[]
    keys=list(app.jobs.keys())
    value=list(app.jobs.values())
    for i in range(len(keys)):
        if value[i]['status'] == 'completed':
            completed_jobID.append(keys[i])
            completed_values.append(value[i])

    status=await async_client.get(url=f'http://127.0.0.1:8000/result/{completed_jobID[0]}')
    print(status.json())
    assert status.status_code==200


@pytest.mark.asyncio
async def test_mock_data(launch_app,async_client):
    test_mock_data.__doc__="This test is to validate if mock data fetch the predict"
    payload = prediction_mock_data
    for i in range(len(payload)):
        mock = {'member_id': payload.values[i][0],
                'balance': payload.values[i][1],
                'last_purchase_size': payload.values[i][2],
                'last_purchase_date': payload.values[i][3]}
        response = await async_client.post(url=url, json=mock)
        print(response.status_code)
        print(app.jobs.values())


@pytest.mark.xfail
@pytest.mark.asyncio
async def test_future_dated_transaction(launch_app,async_client):
    test_future_dated_transaction.__doc__="This Test case is to verify that if last purchase date is future dated, Probability can not be more than one, System should alert the user to put present or past date"
    pay_load={'member_id':'M01',
          'balance':10000,
            'last_purchase_size':60,
           'last_purchase_date':'2025-07-10'}

    response=await async_client.post(url='http://127.0.0.1:8000/predict', json=pay_load)
    assert response.status_code==200
    assert response.json()['probability_to_transact']>1

@pytest.mark.asyncio
async def test_edgecase_member_ID_typeCheck(launch_app,async_client):
    test_edgecase_member_ID_typeCheck.__doc__="This Test case is to verify if member ID is passed as String, the status code should not be 200 OK."
    pay_load={'member_id':200,
          'balance':2000,
            'last_purchase_size':60,
           'last_purchase_date':'2025-06-10'}

    response=await async_client.post(url='http://127.0.0.1:8000/predict', json=pay_load)
    print(response.json())
    assert response.status_code!=200

@pytest.mark.asyncio
async def test_payload_parameter_check(launch_app,async_client):
    test_payload_parameter_check.__doc__="This Test case is to verify that if payload is not well construct, we should not get 200OK"
    pay_load={'member_id':'M01',
              }
    response=await async_client.post(url='http://127.0.0.1:8000/predict', json=pay_load)
    assert response.status_code!=200


@pytest.mark.asyncio
async def test_incorrect_leap_year_transaction(launch_app,async_client):
    test_incorrect_leap_year_transaction.__doc__= "This Test is to validate if incorrect date(Feb 29th-2025) was passed in last transaction date "
    pay_load={'member_id':'M01',
          'balance':2000,
            'last_purchase_size':60,
           'last_purchase_date':'2025-02-29'}
    response=await async_client.post(url='http://127.0.0.1:8000/predict', json=pay_load)
    assert response.status_code!=200

@pytest.mark.asyncio
async def test_status_incorrect_jobID(launch_app,async_client):
    jobid=str(uuid4())
    response=await async_client.get(url=f'http://127.0.0.1:8000/status/{jobid}')
    print(response.json())

