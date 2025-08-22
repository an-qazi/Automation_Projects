# Project Overview
This was **the** project of the term. The goal was that the drawn arc studs at the end of the line may start to weld off 
the nominal position, and over time this issue can get worse. To fix this, a tech has to stop the line, go into the cell, and recalibrate the robot. This adds a lot of downtime
for a 1-2 mil recalibration. Initially, I created Rockwell Automation FactoryTalk HMI screens with new Studio 5000 logic that only allowed one weld position to be recalibrated at a time, the automatic allows for both manual (HMI) and aitoamtic stud recalibration, with one not overwrtiting the other.

 The script is writtin on an OPC tag, pulling from the SQL database every 25 parts and sending its data to the PLC. The PLC has logic to check the studs one by one and send the information needed to recalibrate to the corrent stud gun.
