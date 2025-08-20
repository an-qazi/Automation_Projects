	if (not initialChange):
		if currentValue.value >= 25: # look at the past 25 parts only, good sample size
			server = "Ignition OPC-UA Server" # path to the server, needed for system.opc.read/write
			baseaddress = "[800L]AutoRecal_Array" # increment the base address to write to the array
			expectedstuds = 13 # number of studs on L1 LH parts at time of writing (8-13-2025) 
			dbConnection = "MapVisionLH1_Post_SEP_2024" # database name
			logger = system.util.getLogger("StudChecker")
			counterTagPath = "[Tillsonburg]WL_DataCollection/StudAverage/800L_StudAverages"    # tag to reset to 0
			threshold_high =  1.0 # too high off nominal
			threshold_low  = -1.0 # too low off nominal
			sql = """
			With last25 AS (
			  select id
			  FROM "Measurement"
			  ORDER BY measurement_start_time desc
			  LIMIT 25
			),
			joined AS (
			  Select
			    RF.description,
			    P.difference_X,
			    P.difference_Y,
			    P.difference_Z
			From "Result_feature" RF
			Join last25 m   on RF.measurement_id = m.id
			Join "Point3d"    P on P.result_feature_id = RF.id
			Where RF.used_in_evaluation = TRUE
			And RF.description in ('K0739M400', 'K0739M401', 'K0743M400', 'K0743M401', 
			    'K0751M400', 'K0751M401', 'K0751M402', 'K0751M403', 'K0753M002', 'K0753M003', 'K0753M400',
			     'K0757M400', 'K5287M400')
			)
			select
			  description as name,
			  AVG(difference_X)   as avg_diff_x,
			  AVG(difference_Y)   as avg_diff_y,
			  AVG(difference_Z)   as avg_diff_z
			from joined
			group BY description
			order BY description;
                        """
			ds = system.db.runQuery(sql, dbConnection) # run the sql query above
			listsize = expectedstuds * 2 # 3 directions to look at (x, y, z)
			startlist = []
			startlist = [0] * listsize    # creates listsize zeros
            # there will be 5 possible values per stud. 0 = no change, +1 =  needs to move in +Y direction, 2 = needs to move in -Y direction
            # 3 = needs to move in +X direction, 4 = needs to move in -X direction
			rowstocheck = ds.getRowCount()
			if rowstocheck > expectedstuds:
				rowstocheck = expectedstuds # if the number of studs found is too big, truncate
			for l in range(rowstocheck): # loop and check every x, y, z column if it needs recalibration
				startpos = l * 2 # sets where to append in startlist
				if l == 0:
					realX = ds.getValueAt(l, "avg_diff_x")
					if realX is None:
						x = 0.0
					else:
						x = float(realX)
					realY = ds.getValueAt(l, "avg_diff_y")
					logger.info("y = %s" % (realY,))
					if realY is None:
						y = 0.0
					else:
						y = float(realY)
					logger.info("y = %s" % (y,))
					if y > threshold_high:
						startlist[startpos + 1] = 2
					if y < threshold_low:
						startlist[startpos + 1] = 4
					if x > threshold_high:
						startlist[startpos + 0] = 3
					if x < threshold_low:
						startlist[startpos + 0] = 1
				else:
					realX = ds.getValueAt(l, "avg_diff_x")
					if realX is None:
						x = 0.0
						logger.info("no real x value")
					else:
						x = float(realX)
					realZ = ds.getValueAt(l, "avg_diff_y")
					if realZ is None:
						z = 0.0
					else:
						z = float(realZ)
					if z > threshold_high:
						startlist[startpos + 1] = 2
					if z < threshold_low:
						startlist[startpos + 1] = 4
					if x > threshold_high:
						startlist[startpos + 0] = 3
					if x < threshold_low:
						startlist[startpos + 0] = 1 
			for index, newvalue in enumerate(startlist): # increment index, newvalue holds the current iteration num
				path = baseaddress + "[" + str(index) + "]" 
				readResult = system.opc.readValue(server, path) # check the value, if it diff we change
				curVal = readResult.value # need to get the actual value of the read
				if curVal == newvalue:
					continue # skip this iteration of the loop
				try:
					system.opc.writeValue(server, path, newvalue) # write the values that need to be adjusted to the PLC!
					logger.debug("Wrote %s = %s" % (path, str(newvalue))) # debugging logger scripts
				except Exception as e:
					logger.error("Failed to write %s : %s" % (path, str(e))) # just error handling
			try:
				system.tag.writeBlocking([counterTagPath], [0]) # reset the counter back to 0
				logger.info("Reset counter tag %s to 0" % (counterTagPath))
			except Exception as e:
				logger.error("Failed to reset counter tag: %s" % str(e))
            #------------------------------------------------------------done
