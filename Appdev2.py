# wsowebapp by Dorcas Lanyero

import bottle
from datetime import datetime
import time
from mysql.connector import connect

# return the first page with the services archive
@bottle.route('/')
def hello():
    con = connect(user='root', password='Jesuslives@2019', database='wsoapp', host='cps301-dlany853webapp.cecf4oiulleb.us-east-1.rds.amazonaws.com')
    cursor = con.cursor()

# select service records
    cursor.execute("""
		select Svc_DateTime, title
		from service
		""")

# retrieve the results
    result = cursor.fetchall()

# create first table to display the service
    Services = ''

# place service archive results in table
    for row in result:
        (date, title) = row
        Previous_Services = """
			<form action = "/select">
			  <div class = 'from-group'>
				<label for = 'Datetime' style = "color:black; text-transform: uppercase; font-weight: 200;"> {1}</label>
				<input style = 'font-weight: 200;'readonly class="form-control-plaintext" type = 'text' name = 'Datetime' type='text' value='{0}' onclick > 
				</div>
				
					<input class = 'btn btn-outline-info float-right' type='submit' value='select'>
				
			</form> 
			<br style = 'line-height: 50%;'>
			<hr style = 'border-top: 1px solid #8ce8fa'>
        """.format(date, title)
        Services += Previous_Services
    return HTML_DOC_StartingPage.format(Services)

#Get a person's name using their ID
def GetName(id):
    con = connect(user='admin', password='Yesumara2019', database='wsoapp', host='cps301-dlany853webapp.cecf4oiulleb.us-east-1.rds.amazonaws.com')
    cursor = con.cursor()

    cursor.execute(""" 
		select Last_Name
		from person
		where Person_ID = %s
	""", (id,))
    result = cursor.fetchall()
    Person_ID = ''
    for row in result:
        (row1) = row
        (Person_ID,) = row1
    if Person_ID is None:
        return 'Not assigned'
    else:
        return Person_ID

#Gets an event name based on the ID
def GetEventName(id):
    con = connect(user='admin', password='Yesumara2019', database='wsoapp', host='cps301-dlany853webapp.cecf4oiulleb.us-east-1.rds.amazonaws.com')
    cursor = con.cursor()
    cursor.execute(""" 
		select Description
		from event_type
		where EventType_ID = %s
	""", (id,))
    result = cursor.fetchall()
    Event_ID = ''
    for row in result:
        (row1) = row
        (Event_ID,) = row1
    if Event_ID is None:
        return 'Not assigned'
    else:
        return Event_ID

#Gets an ensemble name based on the provided ID
def GetEnssemble(id):
    con = connect(user='admin', password='Yesumara2019', database='wsoapp', host='cps301-dlany853webapp.cecf4oiulleb.us-east-1.rds.amazonaws.com')
    cursor = con.cursor()

    cursor.execute(""" 
		select Name
		from ensemble
		where Ensemble_ID = %s
	""", (id,))
    result = cursor.fetchall()
    Ensemble_ID = ''
    for row in result:
        (row1) = row
        (Ensemble_ID,) = row1
    if Ensemble_ID is None:
        return 'Not assigned'
    else:
        return Ensemble_ID

#Returns the services table and the service event table
def fetchTables(Datetime):
    con = connect(user='admin', password='Yesumara2019', database='wsoapp', host='cps301-dlany853webapp.cecf4oiulleb.us-east-1.rds.amazonaws.com')
    cursor = con.cursor()

    # services table
    table1 = """
				<div class  = 'collapse'  id = 'service_table'>
				<table class = 'table table-striped' style = "padding: 5px;">
				<thead class = '' style = 'background-color:#0f8796; color: white;'>
				<tr>
					<th scope="col">Service_ID </th>
					<th scope="col">Svc_DateTime </th>
					<th scope="col">Theme </th>
					<th scope="col">Title </th>
					<th scope="col">Notes </th>
					<th scope="col">Organist_Conf </th>
					<th scope="col">Songleader_Conf </th>
					<th scope="col">Pianist_Conf </th>
					<th scope="col">Organist </th>
					<th scope="col">Songleader</th>
					<th scope="col">Pianist</th>
				</tr>,
				</thead>
				"""

    #  service events table
    table2 = """
			<div class  = 'collapse'  id = 'service_events'>
			<table class = 'table table-striped' style = "">
			<thead style = 'background-color:#0f8796; color: white;'>
			<tr>
			<th scope="col">Seq,Num</th>
			<th scope="col">EventType_ID</th>
			<th scope="col">Title</th> 
			<th scope="col">Notes</th>
			<th scope="col">Confirmed</th>
			<th scope="col">Person</th> 
			<th scope="col">Ensemble</th>
			<th scope="col">Song	</th>
			<t/r>
			</thead>
		"""
	#collopse button used to display tables
    table_collapase = """ 
		<div class = "d-flex justify-content-center">
		<p> 
		<button class="btn btn-info" type="button" data-toggle="collapse" data-target="#service_table" aria-expanded="false" aria-controls="service_table">
			Service details
		</button>
		<button class="btn btn-info" type="button" data-toggle="collapse" data-target="#service_events" aria-expanded="false" aria-controls="service_events">
			Service events
		</button>
		</p>
		</div>
		"""

    cursor.execute("""
        select *
        from service
        where Svc_DateTime = %s
        """, (Datetime,))

    result = cursor.fetchall()

    for row in result:
        (Service_ID, Svc_DateTime, Theme, Title, Notes, Organist_Conf,
         Songleader_Conf, Pianist_Conf, Organist_ID, Songleader_ID, Pianist_ID) = row
        tableRow = """
			<tbody>
			<tr>
				<td>{0}</td>
				<td>{1}</td>
				<td>{2}</td>
				<td>{3}</td>
				<td>{4}</td>
				<td>{5}</td>
				<td>{6}</td>
				<td>{7}</td>
				<td>{8}</td>
				<td>{9}</td>
				<td>{10}</td>
			</tr>
			
			""".format(Service_ID, Svc_DateTime, Theme, Title, Notes, Organist_Conf, Songleader_Conf, Pianist_Conf, GetName(Organist_ID), GetName(Songleader_ID), GetName(Pianist_ID))
        table1 += tableRow
    table1 += """ </tbody> </table> </div>"""

    cursor.execute(""" 
				select Service_ID 
				from service
				where Svc_DateTime = %s
			""", (Datetime,))

    result = cursor.fetchall()

    first = ''
    for row in result:
        (ID) = row
        (first,) = ID

    
    cursor.execute("""
			select Seq_Num, EventType_ID, Title, Notes, Confirmed, Person_ID, Ensemble_ID, Song_ID
			from service_event
			where Service_ID = %s
		""", (first,))

 
    result = cursor.fetchall()
    for row in result:
        (Seq_Num, EventType_ID, Title, Notes, Confirmed,
         Person_ID, Ensemble_ID, Song_ID) = row
        table2Row = """ 
			<tbody>
			 <tr>
				<td> {0} </td>
				<td> {1} </td>
				<td> {2} </td>
				<td> {3} </td>
				<td> {4} </td>
				<td> {5} </td>
				<td> {6} </td>
				<td> {7} </td>
			 </tr>
			 """.format(Seq_Num,  GetEventName(EventType_ID), Title, Notes, Confirmed, GetName(Person_ID), GetEnssemble(Ensemble_ID), Song_ID)

        table2 += table2Row
    table2 += """ </tbody> </table> </div>"""

    result = table_collapase + table1 + table2
    return result

#Retrieves a list of former song leaders
def GetSongLeaders():
    con = connect(user='admin', password='Yesumara2019', database='wsoapp', host='cps301-dlany853webapp.cecf4oiulleb.us-east-1.rds.amazonaws.com')
    cursor = con.cursor()

    cursor.execute(""" 
		select Distinct Songleader_ID
		from service
	""")

    result = cursor.fetchall()

    songLeader_IDs = []
    songLeaders = []
    first = ''
    for row in result:
        (ID) = row
        (first,) = ID
        songLeader_IDs.append(first)

    name = ''
    fullname = ''

    for value in songLeader_IDs:
        cursor.execute(""" 
		select CONCAT(First_Name, " ", Last_Name) as Name
		from person
		where Person_ID = %s
		order by Name
		""", (value,))
        result = cursor.fetchall()
        for row in result:
            (ID) = row
            (name,) = ID
        fullname = str(value) + "-" + str(name)
        songLeaders.append(fullname)
    output = ""
    for value in songLeaders:
        row = """ 
		<option>{0}</option>
		""".format(value)
        output += row
    return output

#Displays the select page which contains a form for creating a new servcie and the details of the selected services
@bottle.route('/select')
def select():
    con = connect(user='admin', password='Yesumara2019', database='wsoapp', host='cps301-dlany853webapp.cecf4oiulleb.us-east-1.rds.amazonaws.com')
    cursor = con.cursor()

    Datetime = 0
    if 'Datetime' in bottle.request.params:
        Datetime = bottle.request.params['Datetime']

    form = """ 
	<div class = "container">
	<div class = "row">
	<div class = "col" style = "margin:10px;">
	<div class = "card" style = "width: 30rem; padding-bottom: 10px;">
	<div class = "card-header" style = 'background-color: #0f8796; color: white;'>
		<h3>Create a new service schedule</h3>
	</div>
	<div classs = "card-body" >
	<form class = from-group' action = '/result' style = 'margin: 10px;'>
		<input type="hidden" name="used_dateTime" value="{0}">
		<label for = 'service_date' style = "color:black; text-transform: uppercase; font-weight: 200;"> Service Date</label>
		<input required = 'ture' class="form-control"  type='input' name='service_date' value='' placeholder = 'eg.2010-10-03 16:00:00.000000'> <br>
		<label  for = 'title' style = "color:black; text-transform: uppercase; font-weight: 200;"> Service Title </label>
		<input class="form-control"  type='input' name='title' value=''><br>
		<label for = 'theme' style = "color:black; text-transform: uppercase; font-weight: 200;"> Service Theme </label>
		<input class="form-control" type='input' name='theme' value=''><br> 
		<label for = 'song_leader' style = "color:black; text-transform: uppercase; font-weight: 200;"> Song Leader </label>
		<select class="form-control" name = "song_leader" id="exampleFormControlSelect1">
		  {1}
		</select> 
		<br>
		<input class = 'btn btn-outline-info float-right' type='submit' value='Create Service'>
	 </form>
	 
	</div>
	</div>
	</div>

	<div class = "col align-self-center">
	<h5 style = "text-decoration: underline; text-align: center;">Note</h5>
	<p> To create a new service, please fill out this form. Ensure the servcie date is entered according to the specified formart. If not you will get an error. 
	    If you wish to return to the archive page, select if from the nav bar</p>
	</div>
	</div>
	</div>
	<br>
	""".format(Datetime, GetSongLeaders())

    tables = fetchTables(Datetime)
    return HTML_DOC_SelestedServicePage.format(form, tables)

#displays the results page which displays two tables, the services table and the service events table
@bottle.route('/result')
def result():
    con = connect(user='admin', password='Yesumara2019', database='wsoapp', host='cps301-dlany853webapp.cecf4oiulleb.us-east-1.rds.amazonaws.com')
    cursor = con.cursor()
    
    date = ''
    error = ''
    Service_ID = ''

    if 'service_date' in bottle.request.params and 'title' in bottle.request.params and 'theme' in bottle.request.params and 'used_dateTime' in bottle.request.params:
        date = bottle.request.params['service_date']
        title = bottle.request.params['title']
        theme = bottle.request.params['theme']
        song_leader = bottle.request.params['song_leader']
        used_date = bottle.request.params['used_dateTime']

    # splitting the song leader value
    song_leader_ID = song_leader.split('-')
    leader_ID = 0
    if type(int(song_leader_ID[0])) == int:
        leader_ID = song_leader_ID[0]

    cursor.execute(""" 
		call create_service(%s,%s,%s,%s,%s,@error)
	""", (date, title, theme,leader_ID, used_date))

    cursor.execute(""" 
		select @error 
	""",)

   
    result = cursor.fetchall()

    for row in result:
        (the_error) = row
        (error,) = the_error

    # retrieve newly created service or return an error message
    if error is None:
        results = fetchTables(date)
        return HTML_DOC_CreatedServicdePage.format(results)
    else:
        return HTML_DOC_CreatedServicdePage.format(error)

#The first page which shows service archives
HTML_DOC_StartingPage = """<html>
	<head>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
	</head>
	<body style = 'background-color: #ebeded;'>
	<nav class="shadow-sm navbar navbar-light bg-light sticky-top">
		<a class="navbar-brand " href="#" style = "font-weight: bold; ">
			Hildale Baptist Church
		</a>
		</nav>
		<br>
	<div class = 'd-flex justify-content-center'>
	<div class="card" style= "width:50rem;" >
		<div class="card-header d-flex justify-content-center " style = 'background-color: #0f8796; color: white;'>
			<h4> Past Services Archive </h4>
		</div>
		<div class="card-body">
			{0}
		</div>
	</div>
	</div>
		<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
		<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
	</body>
	</html>"""
#Second page which shows the selected service
HTML_DOC_SelestedServicePage = """<html>
<head>
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
</head>
<body style = 'background-color: #ebeded;'>
	<nav class="shadow-sm navbar navbar-light bg-light sticky-top">
		<a class="navbar-brand " href="#" style = "font-weight: bold; ">
			Hildale Baptist Church
		</a>
	</nav>
	<br>
	{0}
	{1}
	<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
</body>
</html>"""
#The last page which shows the created service
HTML_DOC_CreatedServicdePage = """ 
	<html>
	<head>
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
	</head>
	<body style = 'background-color: #ebeded;'> 
	<nav class="shadow-sm navbar navbar-light bg-light sticky-top">
		<a class="navbar-brand " href="#" style = "font-weight: bold; ">
			Hildale Baptist Church
		</a>
	</nav>
	<br>
		<div style = "text-align: center">
		<br>
		<h3> New Service <h3></br>
		</div>
		{0}
	<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
	</body>
	</html>
"""
# Launch the BottlePy dev server
if __name__ == "__main__":
    bottle.run(host='', port=80, debug=True)
