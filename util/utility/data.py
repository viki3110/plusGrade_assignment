import pandas as pd


ID=['M01','M02','M03','M04','M05','M06']
Balance=[10000,1001,5000,10,15155,12345]
last_purchase_size=[60,10,5,81,71,90]
last_purchase_date=['2024-08-02','2025-02-02','2025-01-04','2025-03-02','2025-06-06','2025-04-04']




prediction_mock_data=pd.DataFrame({"ID":ID,'Balance':Balance,'last_purchase_size':last_purchase_size,'last_purchase_date':last_purchase_date})

