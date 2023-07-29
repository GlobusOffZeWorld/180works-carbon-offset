truncate table districts;

-- change directory
copy districts(id_district, district, country)
from 'D:\2-13\practice\districts.csv'
delimiter ','
csv header;