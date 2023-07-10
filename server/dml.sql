truncate table raw_temperature;

-- change directory
copy raw_temperature(id_stove, "date", temperature)
from 'D:\2-13\practice\temperature.csv'
delimiter ',';