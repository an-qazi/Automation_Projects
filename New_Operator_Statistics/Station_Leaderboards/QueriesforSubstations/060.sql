Select Top 5
	FULLNAME AS Operator, -- operator name
	Round(Avg(Cast(VAL AS Float)), 2) as Mean_Cycle_Time --  average time to 2 decimal places

From ABC.OPCYCLE_ALL

Where
	ASSET = '060' 	-- only this station
	and DT >= DATEADD(week,
	datediff(week, '1900-01-07', getdate()), -- get # of weeks from known sunday
	cast('1900-01-07' AS date)) -- start date, add weeks from this date
	-- starts data at Sunday of current week
	and DT <= getdate() 
	and VAL between 3 and 100 -- plausible times only
	and FULLNAME <> 'N/A' -- exclude no operator entries

Group By FULLNAME

Having COUNT(*) >= 200 -- must have at least 200 cycles

Order By Mean_Cycle_Time ASC;
