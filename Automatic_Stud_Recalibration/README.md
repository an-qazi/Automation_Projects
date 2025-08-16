# Project Overview
This was **the** project of the term for me, I worked on it for the entirety of my internship. The goal was that the drawn arc studs at the end of the line may start to weld off 
the nominal position, and over time this issue gets worse. To fix this, a robot tech has to stop the line, go into the robot cell, and recalibrate the robot. This adds a lot of downtime
for a 1-2 mil recalibration. Initially, I created Rockwell Automation FactoryTalk HMI screens with new Studio 5000 logic that only allowed one weld position to be recalibrated at a time.

The next step was removing the need for a human to be involved at all. Pulling from the MapVision SQL database, I made queries to get me the average of every stud over the last 25 parts.
I stored this data in an OPC tag for each line to allow me to communicate between Ignition and the PLC, ... (will add more later, project not finished)
