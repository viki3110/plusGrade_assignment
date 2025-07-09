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
    task=await asyncio.create_task(async_client.post(url='http://127.0.0.1:8000/predict',json=body))
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
    data="'"+data_load[0]+"'"
    result=await async_client.get(url=f'http://127.0.0.1:8000/result/{data}')
    print(f'results are {result.json()}')
    for i in range(20):
        res=await async_client.get(url=f'http://127.0.0.1:8000/result/{data}')

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


@pytest.mark.xfail
@pytest.mark.asyncio
async def test_future_dated_transaction(async_client):
    test_future_dated_transaction.__doc__="This Test case is to verify that if last purchase date is future dated, Probability can not be more than one, System should alert the user to put present or past date"
    pay_load={'member_id':'M01',
          'balance':10000,
            'last_purchase_size':60,
           'last_purchase_date':'2025-07-10'}

    response=await async_client.post(url='http://127.0.0.1:8000/predict', json=pay_load)
    assert response.status_code==200
    assert response.json()['probability_to_transact']>1



@pytest.mark.asyncio
async def test_edgecase_member_ID_typeCheck(async_client):
    test_edgecase_member_ID_typeCheck.__doc__="This Test case is to verify if member ID is passed as String, the status code should not be 200 OK."
    pay_load={'member_id':200,
          'balance':2000,
            'last_purchase_size':60,
           'last_purchase_date':'2025-06-10'}

    response=await async_client.post(url='http://127.0.0.1:8000/predict', json=pay_load)
    print(response.json())
    assert response.status_code!=200

@pytest.mark.asyncio
async def test_payload_parameter_check(async_client):
    test_payload_parameter_check.__doc__="This Test case is to verify that if payload is not well construct, we should not get 200OK"
    pay_load={'member_id':'M01',
              }
    response=await async_client.post(url='http://127.0.0.1:8000/predict', json=pay_load)
    assert response.status_code!=200


@pytest.mark.asyncio
async def test_incorrect_leap_year_transaction(async_client):
    test_incorrect_leap_year_transaction.__doc__= "This Test is to validate if incorrect date(Feb 29th-2025) was passed in last transaction date "
    pay_load={'member_id':'M01',
          'balance':2000,
            'last_purchase_size':60,
           'last_purchase_date':'2025-02-29'}
    response=await async_client.post(url='http://127.0.0.1:8000/predict', json=pay_load)
    assert response.status_code!=200

@pytest.mark.asyncio
async def test_status_incorrect_jobID(async_client):
    jobid=str(uuid4())
    response=await async_client.get(url=f'http://127.0.0.1:8000/status/{jobid}')
    print(response.json())

