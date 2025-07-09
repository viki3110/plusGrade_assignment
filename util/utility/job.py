import asyncio

import data
from application.app import Application
from models import prediction_request

app = Application()



async def create_job():
    for i in range(len(data.prediction_mock_data)):
        jobs=asyncio.create_task(app.predict(prediction_request=prediction_request.PredictionRequest(member_id=data.prediction_mock_data['ID'][i],
                                                                                                           balance=data.prediction_mock_data['Balance'][i],
                                                                                                           last_purchase_size=data.prediction_mock_data['last_purchase_size'][i],
                                                                                                           last_purchase_date=data.prediction_mock_data['last_purchase_date'][i])))
    jobs=await jobs
    #job=asyncio.create_task(app.predict(prediction_request=prediction_request.PredictionRequest(member_id='M01',balance=10000,last_purchase_size=60,last_purchase_date='2025-02-02')))
    #task=await job
    #job=await jobs


#asyncio.run(create_job())