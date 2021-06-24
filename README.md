# Social-Networking

This project is a basic database model for a social networking site. The data for this is taken from Kaggle and modified so as to comply with the relations on the database. 

This project uses Python 3.7 and MySQL8. The client side is a command line interface coded in python. 

## Steps to run the interface

1. Make a database for the project (I named it ConnectWorld).
2. Create tables and define keys using the source file "project_tables.sql".
3. Add data to the tables using source file "proj_data.sql".

4. Open the python source code file "ConnectWorld_project.py" using python 3.7. In this part of python code :




&nbsp;&nbsp;&nbsp;&nbsp;mydb = mysql.connector.connect( <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;host="localhost",<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;user="root",<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;passwd="1234",&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#ENTER YOUR DATABASE SERVER PASSWORD HERE WITHIN QUOTES        
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;database="ConnectWorld" &nbsp;&nbsp;&nbsp;&nbsp; #ENTER YOUR DATABASE NAME HERE<br/>
&nbsp;&nbsp;&nbsp;&nbsp;)<br/>


5. Add the password of your mysql server where specified, right at the very beginning of the file "ConnectWorld_project.py".

7. Change the database name if your database name is not "ConnectWorld".
Also, replace the host and user, if different for your mysql client.

8. Make sure mysql connector extention is added to python for running the program.

9. Run the file "ConnectWorld_project.py" using python 3.7 IDLE.
