# Project 1
# Professor Troy
# Humzah Hashmi
# This Program we use python and sql to output stats of the cta to console and a map
#
#

import sqlite3
import matplotlib.pyplot as plt


##################################################################  

#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General stats:")

    # Counts the total number of stations
    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone();
    print("  # of stations:", f"{row[0]:,}")

    # Counts the total number of stops
    dbCursor.execute("Select count(*) From Stops;")
    row = dbCursor.fetchone();
    print("  # of stops:", f"{row[0]:,}")

    # Counts the total number of ride entries
    dbCursor.execute("Select count(*) From Ridership;")
    row = dbCursor.fetchone();
    print("  # of ride entries:", f"{row[0]:,}")

    # Calls the min and max fucntion for dates
    dbCursor.execute("Select min(date(Ride_Date)), max(date(Ride_Date)) from ridership;")
    row = dbCursor.fetchone();
    print("  date range:", row[0], "-", row[1])

    # Counts the total number of riders
    dbCursor.execute("Select sum(Num_Riders) from Ridership;")
    row = dbCursor.fetchone();
    print("  Total ridership:", f"{row[0]:,}")

    # Counts the total number of weekday ridership
    dbCursor.execute("Select sum(Num_Riders) from Ridership where Type_of_Day = 'W';")
    row = dbCursor.fetchone();
    sqlTotal = ("Select sum(Num_Riders) from Ridership")
    dbCursor.execute(sqlTotal)
    total = dbCursor.fetchone()
    percent = ((row[0]/total[0]) * 100)
    print("  Weekday ridership:", f"{row[0]:,}", f"({percent:.2f}%)")

    # Counts the total number of Saturday ridership
    dbCursor.execute("Select sum(Num_Riders) from Ridership where Type_of_Day = 'A';")
    row = dbCursor.fetchone();
    sqlTotal = ("Select sum(Num_Riders) from Ridership")
    dbCursor.execute(sqlTotal)
    total = dbCursor.fetchone()
    percent = ((row[0]/total[0]) * 100)
    print("  Saturday ridership:", f"{row[0]:,}", f"({percent:.2f}%)")

    # Counts the total number of Sunday/holiday ridership
    dbCursor.execute("Select sum(Num_Riders) from Ridership where Type_of_Day = 'U';")
    row = dbCursor.fetchone();
    sqlTotal = ("Select sum(Num_Riders) from Ridership")
    dbCursor.execute(sqlTotal)
    total = dbCursor.fetchone()
    percent = ((row[0]/total[0]) * 100)
    print("  Sunday/holiday ridership:", f"{row[0]:,}", f"({percent:.2f}%)")
  
    print()

################################################################## 


# retrieve the stations that are like the user’s input and outputs station names in ascending order

def command_one(dbConn):
  print()
  name = input("Enter partial station name (wildcards _ and %): ")
  
  sql = ("Select Station_ID, Station_Name from Stations where Station_Name like ? order by Station_Name asc")
  
  dbCursor = dbConn.cursor()
  dbCursor.execute(sql, [name])
  rows = dbCursor.fetchall()
  
  if len(rows) == 0: # no stations found:
    print("**No stations found...")
    print()
  else:
    for row in rows: 
      print(row[0], ":", row[1])
  print()

################################################################## 

# Output the ridership at each station, in ascending order by station name and along with each value, output the percentage this value represents across the total L ridership. 

def command_two(dbConn):
  print("** ridership all stations **")
  
  sql = ("Select Stations.Station_Name, sum(Ridership.Num_Riders) from Ridership join Stations on RiderShip.Station_ID = Stations.Station_id group by Stations.Station_ID order by Stations.Station_Name asc")
  
  sqlTotal = ("Select sum(Num_Riders) from Ridership")
  
  dbCursor = dbConn.cursor()
  dbCursor.execute(sqlTotal)
  total = dbCursor.fetchone()
  dbCursor.execute(sql) 
  rows = dbCursor.fetchall()

  for row in rows:
    percent = ((row[1]/total[0]) * 100)
    print(row[0], ":", f"{row[1]:,}", f"({percent:.2f}%)")

################################################################## 

# Output the top-10 busiest stations in terms of ridership, in descending order by ridership

def command_three(dbConn):
  print("** top-10 stations **")
  
  sql = ("Select Stations.Station_Name, sum(Ridership.Num_Riders) from Ridership join Stations on RiderShip.Station_ID = Stations.Station_id group by Stations.Station_ID order by sum(Ridership.Num_Riders) desc limit 10")
  
  sqlTotal = ("Select sum(Num_Riders) from Ridership")
  
  dbCursor = dbConn.cursor()
  dbCursor.execute(sqlTotal)
  total = dbCursor.fetchone()
  dbCursor.execute(sql) 
  rows = dbCursor.fetchall()

  for row in rows:
    percent = ((row[1]/total[0]) * 100) # calculate percent
    print(row[0], ":", f"{row[1]:,}", f"({percent:.2f}%)")

################################################################## 

# Output the least-10 busiest stations in terms of ridership, in ascending order by ridership

def command_four(dbConn):
  print("** least-10 stations **")
  
  sql = ("Select Stations.Station_Name, sum(Ridership.Num_Riders) from Ridership join Stations on RiderShip.Station_ID = Stations.Station_id group by Stations.Station_ID order by sum(Ridership.Num_Riders) asc limit 10")
  
  sqlTotal = ("Select sum(Num_Riders) from Ridership")
  
  dbCursor = dbConn.cursor()
  dbCursor.execute(sqlTotal)
  total = dbCursor.fetchone()
  dbCursor.execute(sql) 
  rows = dbCursor.fetchall()

  for row in rows:
    percent = ((row[1]/total[0]) * 100) # calculate percent
    print(row[0], ":", f"{row[1]:,}", f"({percent:.2f}%)")
  print()
  

################################################################## 

# Input a line color from the user and output all stop names that are part of that line, in ascending order

def command_five(dbConn):
  print()
  color = input("Enter a line color (e.g. Red or Yellow): ")

  sql = ("Select Stops.Stop_Name, Stops.Direction, Stops.ADA from Lines join StopDetails on StopDetails.Line_ID = Lines.Line_ID join Stops on Stops.Stop_ID = StopDetails.Stop_ID where Lines.Color like ? group by Stops.Stop_ID order by Stops.Stop_Name asc")

  dbCursor = dbConn.cursor()
  dbCursor.execute(sql, [color])
  rows = dbCursor.fetchall()

  if len(rows) == 0: # no stations found:
    print("**No such line...")
  else:
    for row in rows:
      if row[2] == 1:
        accessible = ("yes")
      else:
        accessible = ("no")
      
      print(row[0] + " : direction = " + row[1] + " (accessible? " + accessible +")")
  
################################################################## 

# Outputs total ridership by month, in ascending order by month then gives the option to plot and if y is inputed plots the graph

def command_six(dbConn):
  print("** ridership by month **")

  sql = ("Select strftime('%m', Ride_Date), sum(Num_Riders) from Ridership group by strftime('%m', Ride_Date) order by strftime('%m', Ride_Date) asc")
  
  dbCursor = dbConn.cursor()
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  
  if len(rows) == 0: # no stations found:
    print("**No stations found...")
  else:
    for row in rows:
      print(row[0], ":", f"{row[1]:,}")


  # plots the graph
  print()
  plotMonth = input("Plot? (y/n) ")

  if plotMonth == "y":
    x = []
    y = []

    for row in rows:
      x.append(row[0])
      y.append(row[1])
    
    plt.xlabel("month")
    plt.ylabel("number of riders (x * 10^8")
    plt.title("montly ridership")
    plt.plot(x, y)
    plt.ion()
    plt.show()

  print()

################################################################## 

# Outputs total ridership by year, in ascending order by year then gives the option to plot and if y is inputed plots the graph

def command_seven(dbConn):
  print("** ridership by year **")

  sql = ("Select strftime('%Y', Ride_Date), sum(Num_Riders) from Ridership group by strftime('%Y', Ride_Date) order by strftime('%Y', Ride_Date) asc")
  
  dbCursor = dbConn.cursor()
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  
  if len(rows) == 0: # no stations found:
    print("**No stations found...")
  else:
    for row in rows:
      print(row[0], ":", f"{row[1]:,}")


  # plots the graph
  print()
  plotYear = input("Plot? (y/n) ")

  if plotYear == "y":
    x = []
    y = []

    for row in rows:
      x.append(row[0])
      y.append(row[1])
    
    plt.xlabel("year")
    plt.ylabel("number of riders (x * 10^8")
    plt.title("yearly ridership")
    plt.plot(x, y)
    plt.ion()
    plt.show()
  print()

################################################################## 

# Inputs a year and the names of two stations names and then outputs the daily ridership at each station for that year then gives the option to plot and if y is inputed plots the graph

def command_eight(dbConn):
  print()
  year = input("Year to compare against? ")
  print()
  station_one = input("Enter station 1 (wildcards _ and %): ")

  sql_one = ("Select Station_ID, Station_Name from Stations where Station_Name like ? order by Station_Name asc")
  
  dbCursor = dbConn.cursor()
  dbCursor.execute(sql_one, [station_one])
  rows = dbCursor.fetchall()
  
  if len(rows) == 0: # no stations found:
    print("**No station found...")
    return 0

  elif len(rows) > 1: 
    print("**Multiple stations found...")
    return 0

  # gets stations 2
  print()
  station_two = input("Enter station 2 (wildcards _ and %): ")
  sql_two = ("Select Station_ID, Station_Name from Stations where Station_Name like ? order by Station_Name asc")

  dbCursor = dbConn.cursor()
  dbCursor.execute(sql_two, [station_two])
  rows2 = dbCursor.fetchall()

  if len(rows2) == 0: # no stations found:
    print("**No station found...")
    return 0
  elif len(rows2) > 1:
    print("**Multiple stations found...")
    return 0
  # prints station 1
  for row in rows:
      print("Station 1:", row[0], row[1])
      firstStation = row[0]

  statOneFirstTotal = ("Select strftime('%Y-%m-%d', Ride_Date), Num_Riders from Ridership where strftime('%Y', Ride_Date) = ? and Station_ID like "+str(firstStation)+" group by strftime('%Y-%m-%d', Ride_Date) order by strftime('%Y-%m-%d', Ride_Date) asc")

  dbCursor.execute(statOneFirstTotal, [year])
  line1 = dbCursor.fetchall()

  counter = 0
  while(counter != len(line1)):
    print(line1[counter][0], line1[counter][1])
    counter = counter + 1
    if (counter == 5):
      counter = len(line1)-5

  # prints station 2
  for row in rows2:
      print("Station 2:", row[0], row[1])
      secondStation = row[0]

  statTwoFirstTotal = ("Select strftime('%Y-%m-%d', Ride_Date), Num_Riders from Ridership where strftime('%Y', Ride_Date) = ? and Station_ID like "+str(secondStation)+" group by strftime('%Y-%m-%d', Ride_Date) order by strftime('%Y-%m-%d', Ride_Date)")

  dbCursor.execute(statTwoFirstTotal, [year])
  line2 = dbCursor.fetchall()

  counter = 0
  while(counter != len(line2)):
    print(line2[counter][0], line2[counter][1])
    counter = counter + 1
    if (counter == 5):
      counter = len(line2)-5

  # Plots graph with two different labels
  print()
  plotStat = input("Plot? (y/n) ")
  
  if plotStat == "y":
    x = []
    y = []
    x2 = []
    y2 = []
    counter = 0
    for i in line1:
      x.append(counter)
      y.append(i[1])
      counter = counter + 1

    counter = 0
    for i in line2:
      x2.append(counter)
      y2.append(i[1])
      counter = counter + 1
    
    plt.xlabel("day")
    plt.ylabel("number of riders ")
    plt.title("riders each day of 2020")
    plt.plot(x, y)
    plt.plot(x2, y2)
    plt.ion()
    plt.show()
  print()
  
################################################################## 

# Input a line color from the user and output all station names that are part of that line, in ascending order then gives the option to plot and if y is inputed plots the graph

def command_nine(dbConn):
  print()
  color = input("Enter a line color (e.g. Red or Yellow): ")

  sql = ("Select distinct Stations.Station_Name, Stops.Latitude, Stops.Longitude from Lines join StopDetails on StopDetails.Line_ID = Lines.Line_ID join Stops on Stops.Stop_ID = StopDetails.Stop_ID join Stations on Stations.Station_ID = Stops.Station_ID where Lines.Color like ? order by Stations.Station_Name asc")

  dbCursor = dbConn.cursor()
  dbCursor.execute(sql, [color])
  rows = dbCursor.fetchall()

  if len(rows) == 0: # no stations found:
    print("**No such line...")
    return 0
  else:
    for row in rows:
      print(row[0] + " : (" +  str(row[1]) + ", " +  str(row[2]) +  ")")
 
  print()
  plotStat = input("Plot? (y/n) ")
  
  if plotStat == "y":
    #
    # populate x and y lists with (x, y) coordinates --- note that longitude
    # are the X values and latitude are the Y values
    #
    x = []
    y = []

    image = plt.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868] # area covered by the map:
    plt.imshow(image, extent=xydims)
    plt.title(color + " line")
    #
    # color is the value input by user, we can use that to plot the
    # figure *except* we need to map Purple-Express to Purple:
    #
      
    if (color.lower() == "purple-express"):
      color = "Purple" # color="#800080"
      
    for row in rows:
      x.append(row[2])
      y.append(row[1])
      
    plt.plot(x, y, "o", c=color)
        #
        # annotate each (x, y) coordinate with its station name:
        #

    for row in rows:
      plt.annotate(row[0], (row[2], row[1]))
      
    plt.xlim([-87.9277, -87.5569])
    plt.ylim([41.7012, 42.0868])
    plt.ion()
    plt.show()

  print()

##################################################################  

#
# main
#
  
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)
  
command = input("Please enter a command (1-9, x to exit): ")

# calls each function
while command != "x": 
  if command == "1":
    command_one(dbConn)
  elif command == "2":
    command_two(dbConn)
  elif command == "3":
    command_three(dbConn)
  elif command == "4":
    command_four(dbConn)
  elif command == "5":
    command_five(dbConn)
  elif command == "6":
    command_six(dbConn)
  elif command == "7":
    command_seven(dbConn)
  elif command == "8":
    command_eight(dbConn)
  elif command == "9":
    command_nine(dbConn)
  else:
      print("**Error, unknown command, try again...")
      print()
  command = input("Please enter a command (1-9, x to exit): ")

#
# done
#