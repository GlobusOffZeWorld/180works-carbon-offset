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
INSERT INTO temperature ("date", stoves_num, work_num, work_time)
SELECT t1.DATE, stoves_num, work_num, round(EXTRACT(EPOCH FROM work_time) / 60 /60, 2) as work_time
FROM (SELECT d AS DATE, SUM((c > 0)::INT) AS stoves_num, SUM(c) AS work_num
      FROM (SELECT "date"::TIMESTAMP::DATE AS d, SUM((status = 1)::INT) AS c
            FROM stoves_statuses
            GROUP BY id_stove, "date"::TIMESTAMP::DATE) t
      GROUP BY d
	  ORDER BY d) t1
         JOIN (SELECT DATE::TIMESTAMP::DATE AS DATE, SUM(TIME) AS work_time
               FROM (SELECT DATE,
                            (DATE -
                             LAG(DATE) OVER (PARTITION BY "date"::TIMESTAMP::DATE, id_stove ORDER BY "date")) AS TIME,
                            status
                     FROM stoves_statuses) t
               WHERE status = -1
               GROUP BY DATE::TIMESTAMP::DATE) t2 ON t1.DATE = t2.DATE;
			   