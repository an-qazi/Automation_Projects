With LoginCTE as (
Select
    ASSET   as station,
    DT      as login_dt
    From ABC.RFID_LOG
    Where
    FULLNAME = '{Root Container.History.Name_Dropdown.selectedStringValue}'
    and TAG not in ('0000','0001') -- login tags
    and DT between '{Root Container.History.Start_Time.date}' AND '{Root Container.History.End_Time.date}'),

LogoutCTE as (
    Select
    ASSET   as station,
    DT      as logout_dt
    From ABC.RFID_LOG
    Where
    TAG in ('0000','0001') -- logout tags
    and DT between '{Root Container.History.Start_Time.date}' AND '{Root Container.History.End_Time.date}'),

Paired AS (
    Select
    l.station,
    l.login_dt,
    o.logout_dt
    From LoginCTE l
    Cross Apply ( -- use to find matching logouts for each login
    Select MIN(logout_dt) AS logout_dt -- find the logout after this login on the same station
    From LogoutCTE
    Where
    station   = l.station
    and logout_dt > l.login_dt) o
    Where o.logout_dt is not null), -- error handling for unmatched logouts

Durations as (
    Select
    station,
    DATEDIFF(minute, login_dt, logout_dt) as minutes_here -- find difference between login and logout from Paired CTE
    From Paired)

Select
station as Station,
SUM(minutes_here) as Total_Minutes_On_Station -- sum minutes calculated in Durations
From Durations
Group by station -- group by station to summarize total time
Order by station; -- order by station for better readability
