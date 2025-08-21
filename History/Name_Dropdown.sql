Select Distinct FULLNAME
From ABC.OPCYCLE_ALL
Where DT >= {Root Container.History.Name_Dropdown.Get_Name_Start}
Order by 
  FULLNAME Asc
-- :)
