firstly you should run ddl.sql to create all tables 
then if you want to fill table <- use this file
1) districts <- run dml that uses districts.csv
2) locations <- generate-locations.py
3) raw_temperature <- reader.py + sender.py
4) temperature <- run func.sql 

also func.sql gives you some views to conveniently execute needed info for the frontend 