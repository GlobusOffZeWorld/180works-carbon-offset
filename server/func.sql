CREATE PROCEDURE get_table_for_analysis()
LANGUAGE PLPGSQL 
AS $$
BEGIN
	WITH stoves_statuses AS (SELECT *
							 FROM (SELECT id_stove,
										  "date",
										  CASE
											  WHEN LAG(s)
												   OVER (PARTITION BY "date"::TIMESTAMP::DATE, id_stove ORDER BY "date") =
												   0 THEN s
											  ELSE 0
											  END AS status
								   FROM (SELECT id_stove,
												"date",
												(LEAD(temperature, 3)
												 OVER (PARTITION BY "date"::TIMESTAMP::DATE, id_stove ORDER BY "date") -
												 raw_temperature.temperature > 17)::INT -
												(LEAD(temperature, 3)
												 OVER (PARTITION BY "date"::TIMESTAMP::DATE, id_stove ORDER BY "date") -
												 raw_temperature.temperature < -17)::INT AS s
										 FROM raw_temperature) t) t
							 WHERE status != 0)
	INSERT INTO temperature ("date", id_district, stoves_num, work_num, work_time)
	SELECT t1.DATE, t1.id_district, stoves_num, work_num, ROUND(EXTRACT(EPOCH FROM work_time) / 60 / 60, 2) AS work_time
	FROM (SELECT d AS DATE, id_district, SUM((c > 0)::INT) AS stoves_num, SUM(c) AS work_num
		  FROM (SELECT id_district, "date"::TIMESTAMP::DATE AS d, SUM((status = 1)::INT) AS c
				FROM stoves_statuses
				JOIN locations ON locations.id_stove = stoves_statuses.id_stove
				GROUP BY stoves_statuses.id_stove, locations.id_district, "date"::TIMESTAMP::DATE) t
		  GROUP BY d, id_district
		  ORDER BY d, id_district) t1
			 JOIN (SELECT DATE::TIMESTAMP::DATE AS DATE, id_district, SUM(TIME) AS work_time
				   FROM (SELECT id_stove,
								DATE,
								(DATE -
								 LAG(DATE) OVER (PARTITION BY "date"::TIMESTAMP::DATE, id_stove ORDER BY "date")) AS TIME,
								status
						 FROM stoves_statuses) t
					JOIN locations ON locations.id_stove = t.id_stove
				   WHERE status = -1
				   GROUP BY DATE::TIMESTAMP::DATE, id_district) t2 ON t1.DATE = t2.DATE AND t1.id_district = t2.id_district;
END;$$;

CALL get_table_for_analysis();

CREATE VIEW overall_temperature AS
SELECT "date", SUM(stoves_num) AS stoves_num, SUM(work_num) AS work_num, SUM(work_time) AS work_time
FROM temperature
GROUP BY DATE
ORDER BY DATE;
 
CREATE VIEW district_temperature AS
SELECT "date", district,  stoves_num, work_num, work_time
FROM temperature JOIN districts ON temperature.id_district = districts.id_district
ORDER BY "date", district;