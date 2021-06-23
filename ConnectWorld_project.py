import mysql.connector
from datetime import date
import datetime

#Months with 30/31 days
thirtyone=[1,3,5,7,8,10,12]
thirty=[4,6,9,11]

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="1234",   #ENTER YOUR DATABASE SERVER PASSWORD HERE WITHIN QUOTES        
  database="ConnectWorld"        #ENTER YOUR DATABASE NAME HERE
)

#cursor object of the mysql database connector, to execute mysql commands
mycursor = mydb.cursor()
mycursor2 = mydb.cursor()
count=0
   
def log_out():
    #success logging out
    print("Logout Successfull !!")
    exit()

def askExit():
    #to confirm before exiting the application
    opt=input("Enter Y if you want to exit. To continue press any other key :")
    if opt.lower()=='y':
        print("THANKS for visiting !!")
        exit()
    else:
        return
    
def countusers():
    #to count the total number of users accounts
    mycursor.execute("select count(*) from users")
    for row in mycursor:
        count=int(row[0])
    return count+1
    

def calculateAge(birthDate):
    #to calculate age provided the birthdate
    today = date.today() 
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day)) 
    return age

def createPassword():
    #to create a new password
    while(True):
        password=input("Create new password:")
        password2=input("Confirm password:")
        if password2==password:
            return password
        else:
            print("ERROR !! Passwords don't match")

def get_fname():
    #to get a valid first name
    while(True):
        fname=input("First Name:")
        if len(fname)<255:
            return fname
        else:
            print("ERROR !! character limit is 255")
            
def get_lname():
    #to get a valid last name
    while(True):
        lname=input("Last Name:")
        if len(lname)<255:
            return lname
        else:
            print("ERROR !! character limit is 255")

def get_contact():
    #to get a valid contact number
    while(True):
        contact=input("Contact number:")
        if len(contact)!=10:
            print("ERROR !! character limit is 255")
        else:
            return contact

def get_gender():
    #to get a valid gender entry
    while(True):
        opt=input("Enter M(Male), F(Female) or O(Other)...Gender:")
        if opt.lower()=='m':
            sex="Male"
            return sex
        elif opt.lower()=='f':
            sex="Female"
            return sex
        elif opt.lower=='o':
            sex="Other"
            return sex
        else:
            print("ERROR !! Invalid selection")

def get_birthdate():
    #to get a valid birthdate
    while(True):
        byear=int(input("Birth Year:"))
        bmonth=int(input("Birth Month:"))
        bdate=int(input("Birth Date:"))
        today = date.today()
        if byear<1900 or (bmonth<1 and bmonth>12) or (bdate<0 and bdate>31):
            print("ERROR !! date not valid")
            continue
        if bmonth in thirty:
            if bdate>30 or bdate<1:
                print("ERROR !! date not valid")
                continue
        if bmonth in thirtyone:
            if bdate>31 or bdate<1:
                print("ERROR !! date not valid")
                continue
        if ((byear%400==0)or ((byear%4==0) and (byear%100!=0))):
            #leap year
            if bdate>29 or bdate<0:
                print("ERROR !! date not valid")
                continue
        else:
            #not leap year
            if bdate>28 or bdate<0:
                print("ERROR !! date not valid")
                continue
        age=int(calculateAge(date(byear,bmonth,bdate)))
        if age<16:
            print("Sorry you can't sign in. Age limit 16!")
            homepage()
        else:
            bday="{0}-{1}-{2}".format(byear,bmonth,bdate)
            return bday

def get_email():
    #to get a valid email id
    while(True):
        email=input("Email ID:")
        valid=False
        for char in email:
            if char=='@':
                valid1=True
                break
        for char in email:
            if char=='.':
                valid2=True
                break
        if valid1==True and valid2==True:
            return email
        else:
            print("ERROR !! Invalid email ID")

def get_username():
    #to get a valid username
    while(True):
        print("**Note: Username can be combination of letters, numbers and symbol/('_' only). No spaces allowed. First character must be an alphabet. Username is NOT case sensitive.")
        username=input("Username:")
        valid=True
        sqlquery="select username from users where username=\"{0}\"".format(username)
        mycursor.execute(sqlquery)
        for row in mycursor:
            for str in row:
                if str==username.lower():
                    print("ERROR !! Username already exists")
                    valid=False
        if valid==False:
            continue
        if (username[0].isalpha()==False):
            print("ERROR !! Invalid username format")
            continue
        valid=True
        for char in username:
            if char.isspace():
                valid=False
                break
            if (char.isalnum() or char=='_')==False:
                valid=False
                break
        if valid==True:
            return username
        else:
            print("ERROR !! Invalid username format")

def get_security(security):
    #to get a security question and answer
    while(True):
        ques=input("Enter security question:")
        if len(ques)<3:
            print("Invalid !")
        else:
            ans=input("Enter answer:")
            if len(ans)<1:
                print("Invalid !")
            else:
                security[0]=ques
                security[1]=ans
                return security

def get_text(ask):
    #to get a valid text input
    while(True):
        txt=input(ask)
        if len(txt)<100:
            return txt
        else:
            print("ERROR !! character limit is 255")
 
def get_date():
    #to get current date
    today=date.today()
    d=today.strftime('%Y-%m-%d')
    return d

def get_time():
    #to get current time
    now=datetime.datetime.now()
    t=now.strftime("%H:%M:%S")
    return t

def signup():
    #to signup a new user
    security=["",""]
    text=" Sign-up Space "
    print(text.center(75,'~'))
    print("Enter your Details")
    fname=get_fname()
    lname=get_lname()
    sex=get_gender()
    bday=get_birthdate()       
    email=get_email()
    username=get_username()
    password=createPassword()
    get_security(security)
    ques=security[0]
    ans=security[1]

    signupDate=get_date()
    num=countusers()
    #userid="U{0}".format(num)
    
    sqlquery="insert into users (Username,password,signupdate,securityQues,securityAns) values ('{0}','{1}','{2}','{3}','{4}')".format(username,password,signupDate,ques,ans)
    #print(sqlquery)
    mycursor.execute(sqlquery)
    mydb.commit()
    sqlquery="select userID from users where username='{0}'".format(username)
    mycursor.execute(sqlquery)
    for row in mycursor:
        id=row[0]
    sqlquery="insert into biodata (UserID,Fname,Lname,birthdate,gender,emailid) values ({0},'{1}','{2}','{3}','{4}','{5}')".format(id,fname,lname,bday,sex,email)
    mycursor.execute(sqlquery)
    mydb.commit()
    print("Account creation SUCCESSFULL !! Please sign-in to continue")
    return

def forget_password(user):
    #to set a new password when user forgets his password
    #uses birthdate and security question to verify user identity
    #gives three attempts to the user
    username=""
    while(True):
        sqlquery="select userid,username,securityQues,securityAns from Users where Username={0}".format(user)
        mycursor.execute(sqlquery)
        for row in mycursor:
            userid=row[0]
            username=row[1]
            ques=row[2]
            ans=row[3]
        sqlquery="select birthdate from biodata where Userid={0}".format(userid)
        mycursor.execute(sqlquery)
        for row in mycursor:
                bdate=row[0]
            
        if user==username:
            attempts=0
            while(attempts<=3):
                print("Enter birthdate:")
                byear=int(input("year(yyyy):"))
                bmonth=int(input("month(mm):"))
                bday=int(input("date(dd):"))
                bd=str(bdate).split("-")
                #get_bdate="{0}-{1}-{2}".format(byear,bmonth,bday)
                #print(byear,bmonth,bday,int(bd[0]),int(bd[1]),int(bd[2]),bd, byear==int(bd[0]), bmonth==int(bd[1]) ,bday==int(bd[2]))
                if byear==int(bd[0]) and bmonth==int(bd[1]) and bday==int(bd[2]) :
                    print("Question:",ques)
                    get_ans=input("Answer:")
                    if ans.lower()==get_ans.lower():
                        password=createPassword()
                        sqlquery="update users set password='{0}' where UserID={1}".format(password,userid)
                        mycursor.execute(sqlquery)
                        mydb.commit()
                        print("Password change successfull. Please login again to continue.")
                        return True
                    else:
                        print("Incorrect Answer")
                        attempts+=1
                else:
                    print("Incorrect birthdate")
                    attempts+=1
        else:
            print("Username not found")
            askExit()
            user=input("Enter Username:")
    print("You have reached your limit of 3 incorrect attempts. Please try again later.")
    return False

def display_profile(uid):
    #to display user profile - given the userid i.e. uid
    data=[]
    sqlquery="select * from biodata where UserID='{0}'".format(uid)
    mycursor.execute(sqlquery)
    for row in mycursor:
        for field in row:
                data.append(field)
    print('\n')
    text="{0} {1}'s Profile".format(data[1],data[2])
    print('-'*len(text))
    print(text)
    print('-'*len(text))
    print()
    text="-> Birthdate:{0}\n-> Gender:{1}".format(data[3],data[4])
    print(text)
    print("\n...CONTACT INFORMATION...")
    text="-> Email ID:{0}".format(data[5])
    print(text)
    if data[6]==None:
        value="None"
    else:
        value=data[6]
    text="-> Contact Number:{0}".format(value)
    print(text)
    if data[7]==None and data[8]==None:
        pass
    else:
        print("\n....LOCATION INFORMATION....")
        if data[7]!=None:
            text="-> City:{0}".format(data[8])
            print(text)
        if data[8]!=None:
            text="-> Country:{0}".format(data[9])
            print(text)
    if (data[9]!=None or data[10]!=None or data[11]!=None):
        print("\n....EDUCATION AT....")
        for i in range(9,12):
            if data[i]!=None:
                text="-> {0}".format(data[i])
                print(text)
            else:
                break
    if (data[12]!=None or data[14]!=None or data[16]!=None):
        print("\n....WORK....")
        for i in range(12,17,2):
            if data[i]!=None:
                if data[i+1]!=None:
                    text="-> as {0} at {1}".format(data[i+1],data[i])
                    print(text)
                else:
                    text="-> at {0}".format(data[i])
                    print(text)
            #else:
             #   break
    conti=input("press enter to continue:")
    return

def edit_profile(uid):
    #to let user edit his profile
    while True:
        print("1.Name\n2.Biodata\n3.Contact Information\n4.Location Information\n5.Education\n6.Work\n7.Back to profile")
        opt=input("Enter 1-7 corresponding to the information you want to update:")
        if opt=='5' or opt=='6':
            data=[]
            sqlquery="select * from biodata where UserID='{0}'".format(uid)
            mycursor.execute(sqlquery)
            for row in mycursor:
                for field in row:
                    data.append(field)
        if opt=='1':
            #name
            print("1.First Name\n2.Last Name\n3.Both first and last name\n4.Back to profile")
            opt=input("Enter 1-4 corresponding to the information you want to update:")
            if opt=='1':
                fname=get_fname()
                sqlquery="update biodata set fname='{0}' where UserID='{1}'".format(fname,uid)
                mycursor.execute(sqlquery)
            elif opt=='2':
                lname=get_lname()
                sqlquery="update biodata set lname='{0}' where UserID='{1}'".format(lname,uid)
                mycursor.execute(sqlquery)
            elif opt=='3':
                fname=get_fname()
                lname=get_lname()
                sqlquery="update biodata set fname='{0}',lname='{1}' where UserID='{2}'".format(fname,lname,uid)
                mycursor.execute(sqlquery)
            elif opt=='4':
                continue
            else:
                print("Invalid Response!")
            if opt=='1' or opt=='2' or opt=='3':
                mydb.commit()
        elif opt=='2':
            #biodata
            print("1.birthdate\n2.gender\n3.Both\n4.Back to profile")
            opt=input("Enter 1-4 corresponding to the information you want to update:")
            if opt=='1':
                bdate=get_birthdate()
                sqlquery="update biodata set birthdate='{0}' where UserID='{1}'".format(bdate,uid)
                mycursor.execute(sqlquery)
            elif opt=='2':
                gender=get_gender()
                sqlquery="update biodata set gender='{0}' where UserID='{1}'".format(gender,uid)
                mycursor.execute(sqlquery)
            elif opt=='3':
                bdate=get_birthdate()
                gender=get_gender()
                sqlquery="update biodata set birthdate='{0}',gender='{1}' where UserID='{2}'".format(bdate,gender,uid)
                mycursor.execute(sqlquery)
            elif opt=='4':
                continue
            else:
                print("Invalid Response!")
            if opt=='1' or opt=='2' or opt=='3':
                mydb.commit()
        elif opt=='3':
            #contact
            print("1.Email ID\n2.Contact number\n3.Both\n4.Back to profile")
            opt=input("Enter 1-4 corresponding to the information you want to update:")
            if opt=='1':
                email=get_email()
                sqlquery="update biodata set emailid='{0}' where UserID='{1}'".format(email,uid)
                mycursor.execute(sqlquery)
            elif opt=='2':
                contact=get_contact()
                sqlquery="update biodata set contact='{0}' where UserID='{1}'".format(contact,uid)
                mycursor.execute(sqlquery)
            elif opt=='3':
                email=get_email()
                contact=get_contact()
                sqlquery="update biodata set emailid='{0}',contact='{1}' where UserID='{2}'".format(email,contact,uid)
                mycursor.execute(sqlquery)
            elif opt=='4':
                continue
            else:
                print("Invalid Response!")
            if opt=='1' or opt=='2' or opt=='3':
                mydb.commit()
        elif opt=='4':
                #location
                print("1.City\n2.Country\n3.Both\n4.Back to profile")
                opt=input("Enter 1-4 corresponding to the information you want to update:")
                if opt=='1':
                    city=get_text("City:")
                    sqlquery="update biodata set city='{0}' where UserID='{1}'".format(city,uid)
                    mycursor.execute(sqlquery)
                elif opt=='2':
                    country=get_text("Country:")
                    sqlquery="update biodata set country='{0}' where UserID='{1}'".format(country,uid)
                    mycursor.execute(sqlquery)
                elif opt=='3':
                    city=get_text("City")
                    country=get_text("Country")
                    sqlquery="update biodata set city='{0}',country='{1}' where UserID='{2}'".format(city,country,uid)
                    mycursor.execute(sqlquery)
                elif opt=='4':
                    continue
                else:
                    print("Invalid Response!")
                if opt=='1' or opt=='2' or opt=='3':
                    mydb.commit()
        elif opt=='5':
                #education
                print("Note: you can have upto total three education institutes added.")
                edu=1
                while edu<=3:
                    if data[edu+8]==None:
                        break
                    edu=edu+1
                #print("edu ",edu)
                if edu>1:
                    print("You have {0} entries added already".format(edu-1))
                    opt2=input("Do you want to edit previous entries? Enter y(yes)/n(no):")
                    if opt2.lower()=='y':
                        for i in range(1,edu):
                            print("Education#1: {0}".format(data[i+8]))
                            opt3=input("Do you want to edit this? Enter y(yes)/n(no):")
                            if opt3.lower()=='y':
                                    text=get_text("Education Institute:")
                                    field="education{0}".format(i)
                                    sqlquery="update biodata set {0}='{1}' where UserID='{2}'".format(field,text,uid)
                                    mycursor.execute(sqlquery)
                                    mydb.commit()
                elif edu==1:
                    print("You don't have previous entries.")
                if edu==4:
                    print("You already have 3 entries! You can't add more")
                    continue
                opt2=input("Do you want to add? Enter y(yes)/n(no):")
                if opt2.lower()=='y':
                    for i in range(edu,4):
                            text=get_text("Education Institute:")
                            field="education{0}".format(i)
                            sqlquery="update biodata set {0}='{1}' where UserID='{2}'".format(field,text,uid)
                            mycursor.execute(sqlquery)
                            mydb.commit()
                            if i==3:
                                print("You have reached the limit to add three of your education information!")
                            else:
                                opt4=input("Do you want to add more? Enter y(yes)/n(no):")
                                if opt4.lower()=='n':
                                    break        
        elif opt=='6':
                #work
                print("Note: you can have upto total three work information added.")
                back=False
                edu=1
                while(edu<=3):
                    #for edu in range(1,4):#1,2,3
                    index=(edu*2)+10
                    #print("data[{0}]={1}".format(index,data[index]))
                    if data[index]==None:
                        break
                    edu=edu+1
                if edu>1:
                    print("You have {0} entries added already".format(edu-1))
                    opt2=input("Do you want to edit previous entries? Enter y(yes)/n(no):")
                    if opt2.lower()=='y':
                        w=1
                        while w<edu:
                            i=w*2
                            print("Work#{0}: {1}".format(w,data[i+10]))
                            if data[i+11]!=None:
                                print("Designation: {0}".format(data[i+11]))
                            opt4=input("Do you want to edit this entry? Enter y(yes)/n(no):")
                            if opt4.lower()=='y':
                                print("1.Edit company name\t2.Edit/Add designantion\t3.Both 1 and 2\t4.Back to edit profile menu")
                                opt3=input("Enter your choice:")
                                if opt3=='1' or opt3=='3':
                                    text=get_text("Work Company:")
                                    field="work{0}".format(w)
                                    sqlquery="update biodata set {0}='{1}' where UserID='{2}'".format(field,text,uid)
                                    mycursor.execute(sqlquery)
                                    mydb.commit()
                                if opt3=='2' or opt3=='3':
                                    text=get_text("Designation:")
                                    field="designation{0}".format(w)
                                    sqlquery="update biodata set {0}='{1}' where UserID='{2}'".format(field,text,uid)
                                    mycursor.execute(sqlquery)
                                    mydb.commit()
                                if opt3=='4':
                                    back=True
                                    break
                            w=w+1  
                        if back==True:
                            continue    
                elif edu==1:
                    print("You don't have previous entries.")
                if edu==4:
                    print("You already have 3 entries! You can't add more")
                    continue
                opt2=input("Do you want to add new? Enter y(yes)/n(no):")
                if opt2.lower()=='y':
                    i=edu
                    while i<=3:
                        opt3=input("1.Add company name\t2.Add company and designation\t4.Back to edit profile menu")
                        if opt3=='1' or opt3=='2':
                            text=get_text("Work Company:")
                            field="work{0}".format(i)
                            sqlquery="update biodata set {0}='{1}' where UserID='{2}'".format(field,text,uid)
                            mycursor.execute(sqlquery)
                            mydb.commit()
                        if opt3=='2':
                            text=get_text("Designation:")
                            field="designation{0}".format(i)
                            sqlquery="update biodata set {0}='{1}' where UserID='{2}'".format(field,text,uid)
                            mycursor.execute(sqlquery)
                            mydb.commit()
                        if opt3=='4':
                            break
                        if i==3:
                            print("You have reached the limit to add three of your education information!")
                        else:
                            opt4=input("Do you want to add more? Enter y(yes)/n(no):")
                            if opt4.lower()=='n':
                                break  
                        i=i+1
        elif opt=='7':
            return
        else:
            break
    
def profile(uid):
    #the user profile section of the system
    #allows user to view posts by user, view/edit profile
    display_profile(uid)
    while(True):
        print("\n1.View my posts\n2.Edit or Update Profile\n3.View Profile\n4.Back to Main Menu\n5.Logout")
        opt=input("Select from option 1 to 5:")
        if opt=='1':
            postids=[]
            sqlquery="select postid from posts where userid={0} order by date desc,time desc".format(uid)
            mycursor.execute(sqlquery)
            for row in mycursor:
                postids.append(row[0])
            if len(postids)>0:
                for idx in postids:
                    get=display_posts(uid,idx)
                    if get==1:
                        continue
                    elif get==2:
                        break
            else:
                print("You don't have any posts!")
                conti=input("press enter to continue:")
                
        elif opt=='2':
            edit_profile(uid)
        elif opt=='3':
            display_profile(uid)
        elif opt=='4':
            return
        elif opt=='5':
            log_out()
        else:
            print("ERROR! Invalid option!")
    
def accept_req(uid,seen_value,new_value):
    #to accept/decline a friend request
    
    #seen_value=False, new_value=new for new requests
    #seen_value=True, new_value="" for new requests
    more=True
    sno=0
    total=0
    friend=[]
    reqs=[] #reqid,userid,date
    y=["",""]
    sqlquery="select count(*) from friend_req where ( user1={0} or user2={0} ) and accepted='requested' and activity!={0} and seen={1}".format(uid,seen_value)
    mycursor.execute(sqlquery)
    for row in mycursor:
        total=int(row[0])
    if total!=0:
        print("\nYou have {0}{1}friend requests!! ".format(total,new_value))
        conti=input("press enter to continue:")
        if total>20:
            print("NOTE:Twenty requests will be displayed at once.")
        sqlquery="select reqID,user1,user2,reqDate from friend_req where ( user1={0} or user2={0} ) and accepted='requested' and activity!={0} and seen={1} order by reqDate desc,reqTime desc ".format(uid,seen_value)
        mycursor.execute(sqlquery)
        for row in mycursor:
            #print(row[0],row[1],row[2],uid,row[3],type(uid),type(row[0]))
            if int(row[1])==uid:
                reqs.append([row[0],row[2],row[3]])
            elif int(row[2])==uid:
                reqs.append([row[0],row[1],row[3]])
        #print(reqs)
        for x in reqs:
            #print(x)
            if more==True:
                #fid.append(friend[i][j])
                sqlquery="select fname,lname from biodata where UserID={0}".format(x[1])
                mycursor.execute(sqlquery)
                sno+=1
                for row in mycursor:
                    print("{0}.{1} {2} on {3}".format(sno,row[0],row[1],x[2]), end='\t')
                    if seen_value=="False":
                        sqlquery="update friend_req set seen=True where reqID={0}".format(x[0]) 
                        mycursor.execute(sqlquery)
                        mydb.commit()
                if sno%2==0 or sno==total:
                    print("")
                if (sno%20==0 and sno<total) or sno==total:
                    print()
                    d=get_date()
                    print("To accept request, enter 'ACCEPT' followed by a space and the corresponding serial numbers seperated by spaces (eg: accept 2 5)")
                    print("To decline request, enter 'DECLINE' followed by a space and the corresponding serial numbers seperated by spaces (eg: accept 2 5)")
                    print("To load more pending requests, press the ENTER KEY")
                    print("To go back to Group Menu, enter 'BACK'")
                    while(True):
                        k=input("Enter:")
                        k=k.lower()
                        opt=k.split()
                        valid=True
                        d=get_date() 
                        t=get_time()
                        if len(opt)==0:
                            break
                        elif opt[0]=="back":
                            return
                        elif opt[0]=="accept":
                            for i in range(1,len(opt)):
                                if int(opt[i])>sno or int(opt[i])<1 or opt[i].isdigit==False:
                                    print("ERROR! Invalid command")
                                    valid=False
                                    break
                            if valid==True:
                                for i in range(1,len(opt)):
                                    sqlquery="update friend_req set accepted='accepted', activity={0}, acceptDate='{1}',acceptTime='{3}' where reqID={2}".format(uid,d,reqs[int(opt[i])-1][0],t)
                                    mycursor.execute(sqlquery)
                                    mydb.commit()
                                
                        elif opt[0]=="decline":
                            for i in range(1,len(opt)):
                                if int(opt[i])>sno or int(opt[i])<1 or opt[i].isdigit==False:
                                    print("ERROR! Invalid command")
                                    valid=False
                                    break
                            if valid==True:
                                for i in range(1,len(opt)):
                                    sqlquery="update friend_req set accepted='declined', activity={0}, acceptDate='{1}',acceptTime='{3}' where reqID={2}".format(uid,d,reqs[int(opt[i])-1][0],t)
                                    mycursor.execute(sqlquery)
                                    mydb.commit()
        else:
            print("No more{0}friend requests!!".format(new_value))
            conti=input("press enter to continue:")
    else:
        print("You don't have{0}friend requests!".format(new_value))
        conti=input("press enter to continue:")
    return

def show_friends(uid):
    #to show the list of all friends for the user with id uid
    more=True
    sno=0
    total=0
    friend=[]
    y=["",""]
    sqlquery="select count(*) from friend_req where ( user1={0} or user2={0} ) and accepted='accepted' ".format(uid)
    mycursor.execute(sqlquery)
    for row in mycursor:
        total=int(row[0])
    if total!=0:
        print("\nYou have {0} friends!!".format(total))
        conti=input("press enter to continue:")
        sqlquery="select user1,user2 from friend_req where ( user1={0} or user2={0} ) and accepted='accepted' ".format(uid)
        mycursor.execute(sqlquery)
        for row in mycursor:
            y[0]=row[0]
            y[1]=row[1]
            friend.append(y)
        for p in friend:
           for q in p:
                if str(uid)!=str(q):
                    sqlquery="select fname,lname from biodata where UserID={0} order by fname".format(str(q))
                    mycursor.execute(sqlquery)
                    for row in mycursor:
                        sno+=1
                        print("-{0} {1}".format(row[0],row[1]), end='\t')
                        if sno%3==0 or sno==total:
                            print("")
                        if sno%30==0:
                            print("To load more friends, press ENTER Key")
                            print("To go back to menu, enter 'BACK'")
                            while(True):
                                opt1=input("Enter:")
                                opt1=opt1.lstrip()
                                opt1=opt1.rstrip()
                                if len(opt1)==0:
                                    break
                                if opt1.lower()=="back":
                                    return
    else:
        print("You don't have any friends. To add friends go to the SEARCH option to find people and add them as your friends")
        conti=input("press enter to continue:")

def links(uid):
    #to display the links menu
    #to view friends, friend requests, groups, followed topics 
    while(True):
        text=" Your Links Menu "
        print(text.center(75,'~'))
        print("View : 1. Your friends\t2. Pending friend requests\t3. Your Groups\t4. Your followed Topics")
        print("Or Press\t\t5. back to Main Menu\t\t6. Logout")
        opt=input("Select from option 1 to 6:")
        if opt=='1':
            show_friends(uid)
        elif opt=='2':
            accept_req(uid,"False"," new ")
            opt2=input("Do you want to view older pending friend requests? Enter y(yes)/n(no):")
            #older requests
            if opt2=='y':
                accept_req(uid,"True"," ")    
        elif opt=='3':
            more=True
            sno=1
            total=0
            gid=[]
            sqlquery="select count(*) from group_members where userID={0}".format(uid)
            mycursor.execute(sqlquery)
            for row in mycursor:
                total=int(row[0])
            if total!=0:
                print("\nYou are in {0} groups!!".format(total))
                sqlquery="select name from group_members,group_detail where group_members.groupID=group_detail.groupID and group_members.userID={0} order by date desc,time desc".format(uid)
                mycursor.execute(sqlquery)
                for row in mycursor:
                    gid.append(row[0])
                for p in gid:
                    if more==True:
                        print("-{0}".format(p), end='\t')
                        if sno%3==0 or sno==total:
                            print("")
                        if sno%30==0:
                            opt1=input("Display more groups? Enter y(yes)/n(no):")
                            if opt1.lower()!='y':
                                more=False
                        sno+=1
            else:
                print("You don't have any groups. To find and add yourself in groups, go to the SEARCH option")
                conti=input("press enter to continue:")
        elif opt=='4':
            more=True
            sno=1
            total=0
            tid=[]
            sqlquery="select count(*) from followers where userID={0}".format(uid)
            mycursor.execute(sqlquery)
            for row in mycursor:
                total=int(row[0])
            if total!=0:
                print("\nYou follow {0} topics!!".format(total))
                sqlquery="select name from followers,topics where followers.topicID=topics.topicID and followers.userID={0} order by date desc".format(uid)
                mycursor.execute(sqlquery)
                for row in mycursor:
                    tid.append(row[0])
                for p in tid:
                    if more==True:
                        print("-{0}".format(p), end='\t')
                        if sno%3==0 or sno==total:
                            print("")
                        if sno%30==0:
                            opt1=input("Display more topics? Enter y(yes)/n(no):")
                            if opt1.lower()!='y':
                                more=False
                        sno+=1
            else:
                print("You don't follow ant topics yet. To follow topics go to the SEARCH option")
                conti=input("press enter to continue:")
        elif opt=='5':
            return
        elif opt=='6':
            log_out()
        else:
            break

def change_privacy(uid):
    #to change the privacy of profile/posts 
    other="Private"
    print("PUBLIC means that everyone can view your posts and your profile information")
    print("PRIVATE means that only your friends can view your posts and your profile information")
    sqlquery="select nature from users where UserID={0}".format(uid)
    mycursor.execute(sqlquery)
    for row in mycursor:
        privacy=row[0]
    print("Currently your privacy is set to {0}".format(privacy))
    conti=input("press enter to continue:")
    if privacy=="Private":
        other="Public"
    opt2=input("Do you want to change privacy setting? Press 'y' for yes, else press any other key to continue:")
    if opt2.lower()=='y':
        opt3=input("Do you want to change it for previous posts? Press 'y' for yes, else press any other key to continue:")
        if opt3.lower()=='y':
            sqlquery="update posts set nature='{0}' where UserID={1}".format(other,uid)
            mycursor.execute(sqlquery)
            mydb.commit()
        sqlquery="update users set nature='{0}' where UserID={1}".format(other,uid)
        mycursor.execute(sqlquery)
        mydb.commit()

def settings(uid):
    #to display the settings menu
    #options: change privacy, username, password, search privacy
    while(True):
        text=" Settings Menu "
        print(text.center(75,'~'))
        print("1.change privacy settings\n2.change username\n3.change password\n4.check if people can search you\n5.back to Main Menu\n6.logout")
        opt=input("Select from option 1 to 7:")
        if opt=='1':
            change_privacy(uid)
        elif opt=='2':
            username=get_username()
            opt2=input("Are you sure you want to change your username? Enter y(yes)/any key(no):")
            if opt2.lower()=='y':
                sqlquery="update users set Username='{0}' where UserID={1}".format(username,uid)
                mycursor.execute(sqlquery)
                mydb.commit()
        elif opt=='3':
            pswd=createPassword()
            opt2=input("Are you sure you want to change your password? Enter y(yes)/any key(no):")
            if opt2.lower()=='y':
                sqlquery="update users set password='{0}' where UserID={1}".format(pswd,uid)
                mycursor.execute(sqlquery)
                mydb.commit()
        elif opt=='4':
            sqlquery="select search from users where UserID={0}".format(uid)
            mycursor.execute(sqlquery)
            for row in mycursor:
                search=row[0]
            if search==True:
                print("Currently, people(who are not youur friends) can find you and send you friend requests.")
                opt2=input("If you want that people are not able to search you, press 'y', else press any other key to continue:")
                if opt2.lower()=='y':
                    sqlquery="update users set search={0} where UserID={1}".format(False,uid)
                    mycursor.execute(sqlquery)
                    mydb.commit()
        elif opt=='5':
            break
        elif opt=='6':
            log_out()
        else:
            print("ERROR! Invalid choice")

def get_input(text,uid,searchResult):
    choice=text.split()
    d=get_date()
    if choice[0].lower()=="request":
        for i in range(1,len(choice)):
            sqlquery="select count(distinct reqID) from friend_req where ((user1={0} and user2={1}) or (user1={1} and user2={0})) and accepted='accepted' ".format(uid,searchResult[int(choice[i])-1][0])
            mycursor.execute(sqlquery)
            for row in mycursor:
                count1=row[0]
            sqlquery="select count(distinct reqID) from friend_req where ((user1={0} and user2={1}) or (user1={1} and user2={0})) and accepted='requested' ".format(uid,searchResult[int(choice[i])-1][0])
            mycursor.execute(sqlquery)
            for row in mycursor:
                count2=row[0]
            if count1==0 and count2==0:
                t=get_time()
                sqlquery="insert into friend_req (user1,user2,activity,reqDate,reqTime) values ({0},{1},{2},'{3}','{4}')".format(uid,searchResult[int(choice[i])-1][0],uid,d,t)
                mycursor.execute(sqlquery)
                mydb.commit()
            elif count1!=0:
                sqlquery="select fname,lname from biodata where userid={0}".format(searchResult[int(choice[i])-1][0])
                for row in mycursor:
                    print("{0} {1} is already your friend!".format(row[0],row[1]))
                    conti=input("press enter to continue:")
            elif count2!=0:
                sqlquery="select fname,lname from biodata where userid={0}".format(searchResult[int(choice[i])-1][0])
                for row in mycursor:
                    print("You had already requested {0} {1} !".format(row[0],row[1]))
                    conti=input("press enter to continue:")
    elif choice[0].lower()=="profile":
        for i in range(1,len(choice)):
            print("searchresult",searchResult[int(choice[i])-1][0])
            display_profile(searchResult[int(choice[i])-1][0])
            opt=input("Do you want to send request? Enter y(yes)/n(no):")
            if opt.lower()=='y':
                t=get_time()
                sqlquery="insert into friend_req (user1,user2,activity,reqDate,reqTime) values ({0},{1},{2},'{3}','{4}')".format(uid,searchResult[int(choice[i])-1][0],uid,d,t)
                mycursor.execute(sqlquery)
                mydb.commit()
            print("\n1.see next profile\n2.get more search results\n3.back to search")
            opt=input("Select from 1 to 3")
            if opt=='1':
                continue
            elif opt=='2':
                return 2
            elif opt=='3':
                return 3
    elif choice[0].lower()=="follow":
        for i in range(1,len(choice)):
            sqlquery="select count(*) from followers where topicID={0} and userID={1}".format(searchResult[int(choice[i])-1][0],uid)
            mycursor.execute(sqlquery)
            for row in mycursor:
                count=row[0]
            if count==0:
                t=get_time()
                sqlquery="insert into followers (topicID,userID,date) values ({0},{1},'{2}')".format(searchResult[int(choice[i])-1][0],uid,d)
                mycursor.execute(sqlquery)
                mydb.commit()
                sqlquery="select count(*) from followers where topicID={0}".format(searchResult[int(choice[i])-1][0])
                mycursor.execute(sqlquery)
                for row in mycursor:
                    no_followers=row[0]
                sqlquery="update topics set no_followers={0} where topicID={1}".format(no_followers,searchResult[int(choice[i])-1][0])
                mycursor.execute(sqlquery)
                mydb.commit()
            else:
                print("You already follow {0}".format(searchResult[int(choice[i])-1][1]))
                conti=input("press enter to continue:")
    elif choice[0].lower()=="join":
        for i in range(1,len(choice)):
            if searchResult[int(choice[i])-1][3]=="private":
                sqlquery="select count(*) from group_req where groupID={0} and userID={1} and status!='declined'".format(searchResult[int(choice[i])-1][0],uid)
                mycursor.execute(sqlquery)
                for row in mycursor:
                    count=row[0]
                if count==0:
                    t=get_time()
                    sqlquery="insert into group_req (groupID,userID,req_date,req_time) values ({0},{1},'{2}','{3}')".format(searchResult[int(choice[i])-1][0],uid,d,t)
                    mycursor.execute(sqlquery)
                    mydb.commit()
                else:
                    print("You had already requested to join {0}".format(searchResult[int(choice[i])-1][1]))
                    conti=input("press enter to continue:")
            else:
                sqlquery="select count(*) from group_members where groupID={0} and userID={1} and removed=false".format(searchResult[int(choice[i])-1][0],uid)
                mycursor.execute(sqlquery)
                for row in mycursor:
                    count=row[0]
                if count==0:
                    t=get_time()
                    sqlquery="insert into group_members (groupID,userID,date,time) values ({0},{1},'{2}','{3}')".format(searchResult[int(choice[i])-1][0],uid,d,t)
                    mycursor.execute(sqlquery)
                    mydb.commit()
                    sqlquery="select count(*) from group_members where groupID={0}".format(searchResult[int(choice[i])-1][0])
                    mycursor.execute(sqlquery)
                    for row in mycursor:
                        no_members=row[0]
                    sqlquery="update group_detail set no_members={0} where groupID={1}".format(no_members,searchResult[int(choice[i])-1][0])
                    mycursor.execute(sqlquery)
                    mydb.commit()
                else:
                    print("You are already a member of {0}".format(searchResult[int(choice[i])-1][1]))
                    conti=input("press enter to continue:")
    return 0

def popular_topics(uid):
    #to show and follow popular topics
    searchResult=[]
    total=0
    
    sqlquery="select topicID,name from topics where topicID not in (select topicID from followers where userID={0})order by no_followers desc limit 5".format(uid)
    mycursor.execute(sqlquery)
    for row in mycursor:
        y=[row[0],row[1]]
        if y not in searchResult:
            searchResult.append(y) 
            total+=1

    topics=["'%news%'","'%politics%'","'%art%'","'%tech%'","'%photo%'","'%tour%'","'%sport%'"]
    limit=[2,1,2,2,2,2,2]
    n=0

    for topic in topics:
        sqlquery="select topicID,name from topics where topicID not in (select topicID from followers where userID={0}) and name like {1} order by no_followers desc limit {2}".format(uid,topic,limit[n])
        mycursor.execute(sqlquery)
        for row in mycursor:
            y=[row[0],row[1]]
            if y not in searchResult:
                searchResult.append(y) 
                total+=1
        n=n+1
    
    count=0
    if total!=0:
        for i in range(0,len(searchResult)):
            count+=1
            print("{0}. {1}".format(count,searchResult[i][1]))
            
            if count%20==0 or i==len(searchResult)-1:
                print("\nTo follow--type: FOLLOW followed by the serial no. seperated by space\n(eg: follow 2 5)")
                print("\nTo go back type : BACK")
                text=input("Enter:")
                if text.lower()=="back":
                    return
                else:
                    opt2=get_input(text,uid,searchResult)
                    print("You have started following the topic(s)..")
                    conti=input("press enter to continue:")
                    return

def searchMenu(uid):
    #to display the search menu
    #options: search other people/topics/groups
    while(True):
        searchResult=[]
        total=0
        text=" Search Section "
        print(text.center(75,'~'))
        keyword=input("Enter name to search:")
        word=keyword.split()
        opt1=input("1.Search People\t2.Search Topics\t3.Search Groups\n4.Popular topic suggestions\t5.Back to Main Menu\nSelect from option 1 to 5:")
        if opt1=='1':
            for x in word:
                sqlquery="select users.userid,fname,lname from biodata,users where biodata.userid=users.userid and users.userid!={1} and (fname='{0}' or lname='{0}') and search=True".format(x,uid)
                mycursor.execute(sqlquery)
                for row in mycursor:
                    y=[row[0],row[1],row[2]]
                    if y not in searchResult:
                        searchResult.append(y) 
                        total+=1
            count=0
            if total!=0:
                for i in range(0,len(searchResult)):
                    count+=1
                    print("{0}. {1} {2}".format(count,searchResult[i][1],searchResult[i][2]))
                    print()
                    if count%10==0 or i==total-1:
                        print("Ten results are displayed at once.")
                        print("\nTo view profile--type: profile followed by the serial no. seperated by space\n(eg: profile 2 5)")
                        print("\nTo request--type: request followed by the serial no. seperated by space\n(eg: request 2 5)")
                        print("\nTo see more search results type : more")
                        print("\nTo go back type : back")
                        text=input("Enter:")
                        if text=="more":
                            if i==len(searchResult)-1:
                                print("No more matches found.")
                                break
                            else:
                                continue
                        elif text=="back":
                            break
                        else:
                            opt2=get_input(text,uid,searchResult)
                            if opt2==2:
                                continue
                            elif opt2==3 or opt2==0:
                                break
            else:
                print("No matches found!")
                conti=input("press enter to continue:")
        elif opt1=='2':
            for x in word:
                sqlquery="select topicID,name from topics where name like '%{0}%'".format(x)
                mycursor.execute(sqlquery)
                for row in mycursor:
                    y=[row[0],row[1]]   #topicid,name
                    searchResult.append(y) 
                    total+=1
            count=1
            if total!=0:
                for i in range(0,len(searchResult)):
                    print("{0}. {1}".format(count,searchResult[i][1]))
                    count+=1
                    if count%20==0 or i==len(searchResult)-1:
                        print("Twenty results are displayed at once.")
                        print("\nTo follow--type: follow followed by the serial no. seperated by space\n(eg: follow 2 5)")
                        print("\nTo see more search results type : more")
                        print("\nTo go back type : back")
                        text=input("Enter:")
                        if text=="more":
                            if i==len(searchResult)-1:
                                print("No more matches found.")
                                conti=input("press enter to continue:")
                                break
                            else:
                                continue
                        elif text=="back":
                            break
                        else:
                            opt2=get_input(text,uid,searchResult)
                            if opt2==2:
                                continue
                            elif opt2==3 or opt2==0:
                                break
            else:
                print("No matches found!")  
                conti=input("press enter to continue:")
        elif opt1=='3':
            for x in word:
                sqlquery="select groupID,name,description,privacy from group_detail where name like '%{0}%'".format(x)
                mycursor.execute(sqlquery)
                for row in mycursor:
                    y=[row[0],row[1],row[2],row[3]]
                    searchResult.append(y)  #gid,name,descr,privacy
                    total+=1
            count=1
            if total!=0:
                for i in range(0,len(searchResult)):
                    print("{0}. {1} ({2})".format(count,searchResult[i][1],searchResult[i][3]))
                    if searchResult[i][2]!=None:
                        print("  Description:{0}".format(searchResult[i][2]))
                    count+=1
                    if count%20==0 or i==len(searchResult)-1:
                        print("**NOTE: To join PRIVATE groups, request will be automatically sent to the group admins")
                        print("Twenty results are displayed at once.")
                        print("\nTo join--type: join followed by the serial no. seperated by space\n(eg: join 2 5)")
                        print("\nTo see more search results type : more")
                        print("\nTo go back type : back")
                        text=input("Enter:")
                        if text=="more":
                            if i==len(searchResult)-1:
                                print("No more matches found.")
                                conti=input("press enter to continue:")
                                break
                            else:
                                continue
                        elif text=="back":
                            break
                        else:
                            opt2=get_input(text,uid,searchResult)
                            if opt2==2:
                                continue
                            elif opt2==3 or opt2==0:
                                break
            else:
                print("No matches found!")  
                conti=input("press enter to continue:")
        elif opt1=='4':
            popular_topics(uid)
        elif opt1=='5':
            return
            
def add_Admin(uid,gid,admin_no):
    #to add a admin to the group with id - gid
    
    #print(type(uid),uid,gid,admin_no)
    added=False
    keyword=input("Enter name to search:")
    word=keyword.split()
    ids=[]
    searchResult=[]
    total=0
    for x in word:
        #print(x)
        sqlquery="select user1,user2 from friend_req where (user1={0} or user2={0}) and accepted='accepted'".format(uid)
        mycursor.execute(sqlquery)
        for row in mycursor:
            #print(type(row[0]),row[0],type(row[1]),row[1])
            if row[0]!=uid and row[0] not in ids:
                ids.append(row[0]) 
            elif row[1]!=uid and row[1] not in ids:
                ids.append(row[1]) 
        #print(ids)
        for id1 in ids:
            sqlquery="select userid,fname,lname from biodata where userID={0} and (fname='{1}' or lname='{1}')".format(id1,x)
            mycursor.execute(sqlquery)
            for row in mycursor:
                y=[row[0],row[1],row[2]]
                #print(y,"For2")
                if y not in searchResult:
                    searchResult.append(y) 
                    total+=1
        sqlquery="select biodata.userid,fname,lname from biodata,users where biodata.userid=users.userid and biodata.userid!={1} and (fname='{0}' or lname='{0}') and search=True".format(x,uid)
        mycursor.execute(sqlquery)
        for row in mycursor:
            y=[row[0],row[1],row[2]]
            #print(y,"FOR3")
            if y not in searchResult:
                searchResult.append(y) 
                total+=1
    count=1
    #print(searchResult,total)
    if total!=0:
        for i in range(0,len(searchResult)):
            print("{0}. {1} {2}".format(count,searchResult[i][1],searchResult[i][2]))
            count+=1
            if count%10==0 or i==len(searchResult)-1:
                print("Ten results are displayed at once.")
                print("\nTo add a admin, enter add followed by a space and the s.no corresponding to the name of the person you want to add as admin.")
                print("\nTo see more search results type : more")
                print("\nTo go back type : back")
                text=input("Enter:")
                if text=="more":
                    if i==len(searchResult)-1:
                        print("No more matches found.")
                        return added
                    else:
                        continue
                elif text=="back":
                    return added
                elif text[0:3].lower()=="add" and text[3].isspace()==True:
                    ind=text[4:]
                    if ind.isdigit()==True and int(ind)<=count and int(ind)>0:
                        d=get_date()
                        t=get_time()
                        sqlquery="update group_detail set admin{0}={1},date{0}='{3}',time{0}='{4}' where groupID={2}".format(admin_no,searchResult[int(ind)-1][0],gid,d,t)
                        mycursor.execute(sqlquery)
                        mydb.commit()
                        sqlquery="select count(*) from group_members where groupID={0} and userID={1} and removed=true".format(gid,searchResult[int(ind)-1][0])
                        mycursor.execute(sqlquery)
                        for row in mycursor:
                            no_row1=row[0]
                        if no_row1!=0:
                            sqlquery="update group_members set removed=false, date='{2}', time='{3}' where groupID={0} and userID={1}".format(gid,searchResult[int(ind)-1][0],d,t)
                            sqlquery="insert into group_members (groupID,userID,date) values ({0},{1},'{2}')".format(gid,searchResult[int(ind)-1][0],d)
                            mycursor.execute(sqlquery)
                            mydb.commit()
                        else:
                            sqlquery="select count(*) from group_members where groupID={0} and userID={1} and removed=false".format(gid,searchResult[int(ind)-1][0])
                            mycursor.execute(sqlquery)
                            for row in mycursor:
                                no_row1=row[0]
                            if no_row1==0:
                                sqlquery="insert into group_members (groupID,userID,date,time) values ({0},{1},'{2}','{3}')".format(gid,searchResult[int(ind)-1][0],d,t)
                                mycursor.execute(sqlquery)
                                mydb.commit()
                        added=True
                        return added
                    else:
                        added=False
                        return added
                else:
                    print("Invalid command")
                    added=False
                    return added
                    
                    
    else:
        print("No matches found!")
        conti=input("press enter to continue:")
        return added

def createGroup(uid):
    #to create a new group
    #a group can have upto 3 admins
    print("**Note:You can leave the optional fields blank and simply press ENTER")
    adminNo=1
    while(True):
        name=input("Enter group name:")
        name=name.lstrip(' ')
        name=name.rstrip(' ')
        sqlquery="select name from group_detail where name like '%{0}%'".format(name)
        mycursor.execute(sqlquery)  
        for row in mycursor:
            if name.lower()==row[0].lower():
                print("ERROR! Group name already present. Please try another one.")
                break
        if len(name)>100 :
            print("ERROR! Group name limited to 100 characters.")
        elif  name=="":
            print("ERROR! Name is Compulsory, can't be left blank")
        else:
            break
    while(True):
        descr=input("Enter group description(optional):")
        descr=descr.lstrip(' ')
        descr=descr.rstrip(' ')
        if len(descr)>1000:
            print("ERROR! Description limited to 1000 characters.")
        elif  descr=="":
            descr='NULL'
            break
        else:
            break
    d=get_date()
    #print(d)
    opt_priv=input("This is a public group by default. Do you want to change privacy to private? Enter y(yes)/any key(no):")
    t=get_time()
    if opt_priv.lower()=='y':
        sqlquery="insert into group_detail (name,description,admin1,date1,time1,no_members,privacy,date_created) values ('{0}','{1}',{2},'{3}','{4}',1,'private','{3}')".format(name,descr,uid,d,t)
    else:
        sqlquery="insert into group_detail (name,description,admin1,date1,time1,no_members,date_created) values ('{0}','{1}',{2},'{3}','{4}',1,'{3}')".format(name,descr,uid,d,t)
    mycursor.execute(sqlquery)
    mydb.commit()
    print()
    print("You are the admin!! A group can have upto three admin")
    conti=input("press enter to continue:")
    sqlquery="select groupid from group_detail where name='{0}'".format(name)
    mycursor.execute(sqlquery)  
    for row in mycursor:
        gid=row[0]
    sqlquery="insert into group_members (groupID,userID,date,time) values ({0},{1},'{2}','{3}')".format(gid,uid,d,t)
    mycursor.execute(sqlquery)
    mydb.commit()
    print("You can add two more now or later. You can also change all the admins later")
    opt=input("Add more admins? Enter y(yes)/any key(no):")
    
    while(adminNo<3 and opt.lower()=='y'):
        if opt.lower()=='y':
            success=add_Admin(uid,gid,adminNo+1)
            if success==True:
                adminNo+=1
                print("Admin added !!")
            else:
                opt=input("Try adding admin again? Enter y(yes)/any key(no):")
                continue
        opt=input("Add more admins? Enter y(yes)/any key(no):")
    sqlquery="select count(*) from group_members where groupID={0}".format(gid)
    mycursor.execute(sqlquery)
    for row in mycursor:
        num=row[0]
    sqlquery="update group_detail set no_members={0} where groupID={1}".format(num,gid)
    mycursor.execute(sqlquery)
    mydb.commit()      
    if adminNo==3:
        print("You have successfully added three admins for your group!")
        conti=input("press enter to continue:")
 
def accept_groupReq(gid):
    #to accept a group request
    reqs=[]
    total=0
    sqlquery="select reqID,biodata.userID,fname,lname,req_date from group_req,biodata where group_req.userID=biodata.userID and groupID={0} and status='requested'".format(gid)
    mycursor.execute(sqlquery)
    for row in mycursor:
        reqs.append([row[0],row[1],row[2],row[3],row[4]])
        total+=1
    sqlquery="select reqID,biodata.userID,fname,lname,req_date from group_req,biodata where group_req.userID=biodata.userID and groupID={0} and status='seen'".format(gid)
    mycursor.execute(sqlquery)
    for row in mycursor:
        reqs.append([row[0],row[1],row[2],row[3],row[4]])
        total+=1
    more=True
    index=0
    d=get_date()
    if total>0:
        for x in reqs:
            if more==True:
                more=True
                back=False
                index+=1
                print("{0}.{1} {2} ({3})".format(index,x[2],x[3],x[4]))
                print()
                sqlquery="update group_req set status='seen' where reqID={0}".format(x[0])
                mycursor.execute(sqlquery)
                mydb.commit()
                if index%10==0 or index==total:
                        print("*NOTE:Ten results are displayed at once. You can load more.")
                        print("To view profile, enter 'show' followed by corresponding serial numbers seperated by space.(eg:show 2 5)")
                        print("To accept, enter 'accept' followed by corresponding serial numbers seperated by space.(eg:accept 2 5)")
                        print("To decline, enter 'decline' followed by corresponding serial numbers seperated by space.(eg:decline 2 5)")
                        print("To load more request, enter 'more'")
                        print("To go back to Group Menu, enter 'back'")
                        while(True):
                            inp=input("Enter:")
                            opt=inp.split()
                            if opt[0].lower()=="show" or opt[0]=="accept" or opt[0]=="decline":
                                for i in range(1,len(opt)):
                                    if opt[i].isdigit()==False and (int(opt[i])>index or int(opt[i])<1):
                                        print("ERROR! Invalid command")
                                        break
                            if opt[0].lower()=="show":
                                for i in range(1,len(opt)):
                                    display_profile(reqs[int(opt[i])-1][1])
                                    if i!=len(opt)-1:
                                        opt2=input("Show next profile? Enter y(yes)/any key(no):")
                                        if opt2.lower()!='y':
                                            break
                            elif opt[0].lower()=="accept":
                                for i in range(1,len(opt)):
                                    sqlquery="update group_req set status='accepted' where reqID={0}".format(reqs[int(opt[i])-1][0])
                                    mycursor.execute(sqlquery)
                                    mydb.commit()
                                    sqlquery="select count(*) from group_members where userID={0} and groupID={1} and removed=true".format(reqs[int(opt[i])-1][1],gid)
                                    mycursor.execute(sqlquery)
                                    t=get_time()
                                    for row in mycursor:
                                        row_count=row[0]
                                    if row_count>0:
                                        sqlquery="update group_members set removed=false, date='{0}',time='{3}' where userID={1} and groupID={2} ".format(d,reqs[int(opt[i])-1][1],gid,t)
                                    else:
                                        sqlquery="insert into group_members (userID,groupID,date,time) values ({0},{1},'{2}','{3}')".format(reqs[int(opt[i])-1][1],gid,d,t)
                                    mycursor.execute(sqlquery)
                                    mydb.commit()
                            elif opt[0].lower()=="decline":
                                for i in range(1,len(opt)):
                                    sqlquery="update group_req set status='declined' where reqID={1}".format(reqs[int(opt[i])-1][0])
                                    mycursor.execute(sqlquery)
                                    mydb.commit()
                            elif opt[0].lower()=="more":
                                if index==total:
                                    print("No more requests")
                                    conti=input("press enter to continue:")
                                break
                            elif opt[0].lower()=="back":
                                back=True
                                break
                        if back==True:
                            return
    else:
        print("No pending requests !")
        conti=input("press enter to continue:")
        
def group_Detail(uid,gid):
    #to display group details - admins, members
    while(True):
        print("1.Group Admins\t2.Group Members\t3.Change or add group admins\n4.Back to Group Menu")
        opt=input("Enter your choice:")
        if opt=='1':
            adminIDs=[]
            sqlquery="select admin1,admin2,admin3 from group_detail where groupID={0}".format(gid)
            mycursor.execute(sqlquery)
            for row in mycursor:
                adminIDs.append(row[0])
                adminIDs.append(row[1])
                adminIDs.append(row[2])
            index=0
            print("GROUP ADMINS:")
            for admin in adminIDs:
                if admin!=None:
                    index+=1
                    sqlquery="select fname,lname from biodata where userID={0}".format(int(admin))
                    mycursor.execute(sqlquery)
                    print()
                    for row in mycursor:
                        print("{0}. {1} {2}".format(index,row[0],row[1]))
                else:
                    break
            conti=input("press enter to continue:")
        elif opt=='2':
            memID=[]
            back=False
            sqlquery="select userID from group_members where groupID={0} and removed=false order by date desc".format(gid)
            mycursor.execute(sqlquery)
            for row in mycursor:
                memID.append(int(row[0]))
            index=0
            for id1 in memID:
                if back==True:
                    break
                index+=1
                sqlquery="select fname,lname from biodata where userID={0}".format(id1)
                mycursor.execute(sqlquery)
                print()
                print("GROUP MEMBERS:")
                for row in mycursor:
                    if back==True:
                        break
                    print("{0}. {1} {2}".format(index,row[0],row[1]),end='\t')
                    if index%2==0:
                        print()
                    print()
                    if index%20==0:
                        print("To remove a group member, enter REMOVE followed by corresponding serial number(s) seperated by spaces (eg: remove 2 5)")
                        print("Press ENTER KEY to load more, enter BACK to return to Menu.")
                        back=False
                        more=True
                        while(True):
                            opt2=input("Enter:")
                            opt2=opt2.lower()
                            inp=opt2.split()
                            if len(inp)==0:
                                more=True
                                break
                            elif inp[0]=="back":
                                back=True
                                break
                            elif inp[0]=="remove":
                                invalid=False
                                for i in range (1,len(inp)):
                                    if inp[i].isdigit()==False and (int(inp[i])>index or int(inp[i])<1):
                                        print("ERROR! Invalid command")
                                        invalid=True
                                        break
                                if invalid==False:
                                    for i in range(1,len(inp)):
                                        sqlquery="update group_members set removed=true where userID={0}".format(memID[int(inp[i])-1])
                                        mycursor.execute(sqlquery)
                                        mydb.commit()
                                    print("Group Member(s) have been removed successfully.")
                                    conti=input("press enter to continue:")
                            else:
                                print("ERROR! Invalid command.")
                            if back==True:
                                break
                 
        elif opt=='3':
            adminID=[]
            adminNames=[]#id,fname,lname
            back=False
            sqlquery="select admin1,admin2,admin3 from group_detail where groupID={0}".format(gid)
            mycursor.execute(sqlquery)
            for row in mycursor:
                adminID.append(row[0])
                adminID.append(row[1])
                adminID.append(row[2])
            index=0
            for id1 in adminID:
                if id1!=None:
                    index+=1
                    sqlquery="select fname,lname from biodata where userID={0}".format(id1)
                    mycursor.execute(sqlquery)
                    for row in mycursor:
                        adminNames.append([int(id1),row[0],row[1]])
                else:
                    break
            total=index
            index=0
            print("Currently, your group has {0} admins.".format(total))
            for admin in adminNames:
                index+=1
                print("{0}. {1} {2}".format(index,admin[1],admin[2]))  
            print()
            print("To add a admin, enter ADD.(eg: add)")
            print("To change an admin, enter CHANGE followed by corresponding serial number(s) seperated by spaces (eg: change 2 5)")
            print("To remove an admin, enter REMOVE followed by corresponding serial number(s) seperated by spaces")
            print("Enter BACK to return to Menu.")
            back=False
            more=True
            while(True):
                #print("TOTAL=",total)
                opt2=input("Enter:")
                opt2=opt2.lower()
                inp=opt2.split()
                if inp[0]=="back":
                    back=True
                    break
                elif inp[0]=="remove":
                    invalid=False
                    for i in range (1,len(inp)):
                        #print(inp[i].isdigit(),int(inp[i])>total,int(inp[i])<1)
                        if inp[i].isdigit()==False or (int(inp[i])>total or int(inp[i])<1):
                            print("ERROR! Invalid command")
                            invalid=True
                            break
                        if total<=1:
                            print("ERROR! You can't remove all admins, change the admin to edit")
                            invalid=True
                            break
                    if invalid==False:
                        for i in range(1,len(inp)):
                            current=[]#[admin,date]
                            if int(inp[i])==1:
                                sqlquery="select admin2,date2,admin3,date3 from group_detail where groupid={0}".format(gid)
                                mycursor.execute(sqlquery)
                                for row in mycursor:
                                    current.append(row[0])
                                    current.append(row[1])
                                    current.append(row[2])
                                    current.append(row[3])
                                if current[0]!=None:
                                    sqlquery="update group_detail set admin1={0}, date1='{1}' where groupid={2}".format(current[0],current[1],gid)
                                    mycursor.execute(sqlquery)
                                    mydb.commit()
                                    if current[2]!=None:
                                        sqlquery="update group_detail set admin2={0}, date2='{1}' where groupid={2}".format(current[2],current[3],gid)
                                        mycursor.execute(sqlquery)
                                        mydb.commit()
                                        sqlquery="update group_detail set admin3=NULL, date3=NULL where groupid={0}".format(gid)
                                        mycursor.execute(sqlquery)
                                        mydb.commit()
                                        
                                    else:
                                        sqlquery="update group_detail set admin2=NULL, date2=NULL where groupid={0}".format(gid)
                                        mycursor.execute(sqlquery)
                                        mydb.commit()
                                total-=1
                                
                            elif int(inp[i])==2:
                                sqlquery="select admin3,date3 from group_detail where groupid={0}".format(gid)
                                mycursor.execute(sqlquery)
                                for row in mycursor:
                                    current.append(row[0])
                                    current.append(row[1])
                                if current[0]!=None:
                                    sqlquery="update group_detail set admin2={0}, date2='{1}' where groupid={2}".format(current[0],current[1],gid)
                                    mycursor.execute(sqlquery)
                                    mydb.commit()
                                    sqlquery="update group_detail set admin3=NULL, date3=NULL where groupid={0}".format(gid)
                                    mycursor.execute(sqlquery)
                                    mydb.commit()
                                else:
                                    sqlquery="update group_detail set admin2=NULL, date2=NULL where groupid={0}".format(gid)
                                    mycursor.execute(sqlquery)
                                    mydb.commit()
                                total-=1
                            elif int(inp[i])==3:
                                sqlquery="update group_detail set admin3=NULL, date3=NULL where groupid={0}".format(gid)
                                mycursor.execute(sqlquery)
                                mydb.commit()
                                total-=1
                                
                            
                elif inp[0]=="add" and len(inp)==1:
                    if total>=3:
                        print("You can only have total three admins, you already have three.")
                    else:
                        success=add_Admin(uid,gid,total+1)
                        if success==True:
                            print("Group Admin added successfully.")
                            total+=1
                        else:
                            print("Group Admin not added. Please try again!")
                            print()
                            print("To add a admin, enter ADD.(eg: add)")
                            print("To change an admin, enter CHANGE followed by corresponding serial number(s) seperated by spaces (eg: change 2 5)")
                            print("To remove an admin, enter REMOVE followed by corresponding serial number(s) seperated by spaces")
                            print("Enter BACK to return to Menu.")
                elif inp[0]=="change":
                    invalid=False
                    for i in range (1,len(inp)):
                        if inp[i].isdigit()==False and (int(inp[i])>total or int(inp[i])<1):
                            print("ERROR! Invalid command")
                            invalid=True
                            break
                    if invalid==False:
                        for i in range(1,len(inp)):
                            success=add_Admin(uid,gid,inp[i])
                            if success==True:
                                print("Group Admin {0} changed successfully.".format(inp[i]))
                                total+=1
                            else:
                                print("Group Admin {0} not changed. Please try again!".format(inp[i]))
                                print()
                                print("To add a admin, enter ADD.(eg: add)")
                                print("To change an admin, enter CHANGE followed by corresponding serial number(s) seperated by spaces (eg: change 2 5)")
                                print("To remove an admin, enter REMOVE followed by corresponding serial number(s) seperated by spaces")
                                print("Enter BACK to return to Menu.")
                else:
                    print("ERROR! Invalid command.")
                if back==True:
                    break
        elif opt=='4':
            return
        else:
            print("Invalid choice")
            
        
        
def groupMenu(uid,admin_count,adminOf):
    #to display the group menu
    
    #adminOF=[groupid,name,privacy]
    #print(uid,admin_count,adminOf)
    while True:
        text=" Group Menu "
        print(text.center(75,'~'))
        sqlquery="select prevSIdate from users where userID={0}".format(uid)
        mycursor.execute(sqlquery)
        for row in mycursor:
            prev_date=row[0]
        no_req=[]   #no of new requests per private group id
        req=False
        if admin_count!=0:
            for x in adminOf:
                if x[2]=="private":
                    req=True
                    if prev_date==None:
                        sqlquery="select count(*) from group_req where groupID={0} and status='requested' ".format(x[0])
                    else:
                        sqlquery="select count(*) from group_req where groupID={0} and status='requested' and req_date>='{1}'".format(x[0],prev_date)
                    mycursor.execute(sqlquery)
                    for row in mycursor:
                        if row[0]>0:
                            no_req.append([x[0],row[0]])
        #print("adminof",adminOf)
        #print("no_req",no_req)
        print("1.Group posts\t2.Create a new group",end="\t")
        if admin_count!=0 and req==True:
            print("3.My group requests\t4.My group details")
            print("5.Back to Main Menu")
        elif admin_count!=0 and req==False:
            print("3.My group details\t4.Back to Main Menu")
        else:
            print("3.Back to Main Menu")
        opt=input("Enter your choice:")
        if opt=='1':#group posts
            g_detail=[]
            sqlquery="select group_detail.groupid,name from group_members,group_detail where group_members.groupid=group_detail.groupid and userid={0} and removed=false".format(uid)
            mycursor.execute(sqlquery)
            for row in mycursor:
                g_detail.append([row[0],row[1]])
            index=0
            if len(g_detail)>0:
                for grp in g_detail:
                    index+=1
                    print("{0}. {1}".format(index,grp[1]))
                print("To show posts of a group, enter SHOW followed by space and corresponding serial number\nTo go back to group menu, enter BACK\npress ENTER to show next post")
                go=True
                while(go):
                        opt2=input("Enter:")
                        opt2=opt2.lstrip()
                        opt2=opt2.rstrip()
                        opt2=opt2.lower()
                        #print(opt2)
                        if opt2.lower()=="back":
                            break
                        elif opt2[0:4].lower()=="show" and opt2[4].isspace()==True:
                            vals=opt2.split()
                            postids=[]
                            if len(vals)==2 and vals[1].isdigit()==True and int(vals[1])<=index and int(vals[1])>0:
                                sqlquery="select postid from posts where groupid={0} order by date desc,time desc".format(g_detail[int(vals[1])-1][0])
                                mycursor.execute(sqlquery)
                                for row in mycursor:
                                    postids.append(row[0])
                                #print(postids)
                                if len(postids)>0:
                                    for idx in postids:
                                        get=display_posts(uid,idx)
                                        if get==1:
                                            continue
                                        elif get==2:
                                            go=False
                                            break
                                    else:
                                        print("No more posts!")
                                        conti=input("press enter to continue:")
                                        go=False
                                        break
                                else:
                                    print("No posts!")
                                    conti=input("press enter to continue:")
                                    go=False
                                    break
                                    
                            else:
                                print("ERROR! Invalid Input")
                        else:
                            print("Invalid input")
                        
            else:
                print("You are not a member of any group.")
        elif opt=='2':#new group
            createGroup(uid)
        elif opt=='3' and admin_count!=0 and req==True:#group reqs
            show=[]
            sno=0
            print()
            if len(no_req)>0:
                for group in no_req:
                    sqlquery="select name from group_detail where groupID={0}".format(int(group[0]))
                    mycursor.execute(sqlquery)
                    for row in mycursor:
                        name=row[0]
                    sno+=1
                    print("{2}.You have {0} new requests in {1}".format(group[1],name,sno))
                
            else:
                print("You have no new requests")
                opt3=input("Do you want to check previous requests? enter y(yes)/any key(no):")
                if opt3.lower()!='y':
                    continue
            index=0
            gids=[] #private group ids
            for x in adminOf:
              if x[2]=="private":
                    index+=1
                    gids.append([x[0],x[1]])#private groupids
                    print("{0}. {1}".format(index,x[1]))
            if index>1:
                opt3=input("Type 'show' followed by the corresponding serial number(s) seperated by space. (eg: show 2 5)/nEnter 'back' to go back to Menu")
                if opt3.lower()=="back":
                    continue
                else:
                    show=opt3.split()
            elif index==1:
                show=["show","1"]
                
            if show[0]=="show":
                for i in range (1,len(show)):
                    text=" Requests for {0} ".format(gids[i-1][1] )
                    print(text.center(75,'~'))
                    accept_groupReq(gids[i-1][0])
            else:
                print("Invalid Command")
                
        elif (opt=='4' and admin_count!=0 and req==True) or (opt=='3' and admin_count!=0 and req==False):#group members
            show=[]
            gids=[]
            print()
            index=0
            
            for x in adminOf:
                    index+=1
                    gids.append(x[0])
                    print("{0}. {1}".format(index,x[1]))
            if index>1:
                opt3=input("Type 'details' followed by the corresponding serial number(s) seperated by space. (eg: details 2 5)/nEnter 'back' to go back to Menu")
                if opt3.lower()=="back":
                    continue
                else:
                    show=opt3.split()
            elif index==1:
                show.append("details")
                show.append("1")
                
            if show[0]=="details":
                for i in range (1,len(show)):
                    text=" Details for {0} ".format(adminOf[i-1][1])
                    print(text.center(75,'~'))
                    group_Detail(uid,adminOf[i-1][0])
            else:
                print("Invalid Command")
                
        elif (opt=='3' and admin_count==0) or (opt=='5' and admin_count!=0 and req==True) or (opt=='4' and admin_count!=0 and req==False):#back
            return
        else:
            print("Invalid response")
                
def newPost(uid):
    #to create a new post
    print("To add body, enter BODY followed by the text")
    print("To add topic, enter TOPIC followed by a space and the topic name")
    print("To add your post to a group, enter GROUP followed by a space and the group name. Only one group at a time")
    print("To add media (picture/video/link), enter MEDIA followed by a space and the url of media. You can add more than one media")
    print("Privacy is by DEFAULT as per your setting. To change it for this post, enter PRIVACY followed by a space and 'Public' or 'Private'")
    print("To post, enter POST")
    print("Enter BACK to return to Main Menu.")
    print("*NOTE: the most recent values of all fields before POSTING, will be posted.")
    print()
    body=topic=group=privacy='NULL'
    media=[]
    gids=[]
    tids=[]
    content=False
    while(True):
        opt=input("Enter:")
        opt=opt.lstrip()
        opt=opt.rstrip()
        if opt[0:4].lower()=="body" and opt[4].isspace():
            body=opt[5:]
            content=True
            if len(body)>1000:
                print("ERROR! Character limit of body is exceeding 1000 characters. Please enter again.")
                body='NULL'
                content=False
            elif body=="":
                print("ERROR! No content in post body")
                body='NULL'
                content=False
        elif opt[0:5].lower()=="topic" and opt[5].isspace():
            follow=[]
            topic=opt[6:]
            sqlquery="select topics.topicID,name from topics,followers where topics.topicID=followers.topicID and userID={0}".format(uid)
            mycursor.execute(sqlquery)
            for row in mycursor:
                follow.append(row[1].lower())
                tids.append(row[0])
            if topic.lower() not in follow:
                choice1=input("You do not follow the topic, are you sure you want to add it? Enter y(yes)/any key(no):")
                if choice1.lower()!='y':
                    topic='NULL' 
            else:
                for i in range(0,len(follow)):
                    if topic.lower()==follow[i]:
                        tid=tids[i]
            sqlquery="select count(*) from topics where name='{0}'".format(topic)
            mycursor.execute(sqlquery)
            for row in mycursor:
                row_count=row[0]
            if row_count==0:
                sqlquery="insert into topics (name) values ('{0}')".format(topic)
                mycursor.execute(sqlquery)
                mydb.commit()
        elif opt[0:5].lower()=="group" and opt[5].isspace():
            memOf=[]
            group=opt[6:]
            sqlquery="select group_detail.groupID,name from group_detail,group_members where group_detail.groupID=group_members.groupID and userID={0}".format(uid)
            mycursor.execute(sqlquery)
            for row in mycursor:
                gids.append(row[0])
                memOf.append(row[1].lower())
            if group.lower() not in memOf:
                print("You are not a member of the group. You can't post to the group.")
                group='NULL'
            else:
                for i in range(0,len(memOf)):
                    if group.lower()==memOf[i]:
                        gid=gids[i]
        elif opt[0:5].lower()=="media" and opt[5].isspace():
            x=opt[6:]
            content=True
            if len(x)>1000:
                print("ERROR! media url exceeding limit 0f 1000 characters")
                media='NULL'
                content=False
            elif x=="":
                print("ERROR! No media added.")
                x='NULL'
                content=False
            else:
                media.append(opt[6:])
        elif opt[0:7].lower()=="privacy" and opt[7].isspace():
            privacy=opt[8:].lower()
            if privacy!="public" or privacy!="private":
                privacy='NULL'
                print("ERROR! Invalid privacy value")
        elif opt.lower()=="post":
            d=get_date()
            t=get_time()
            if content==True:
                if privacy=='NULL':
                    sqlquery="select nature from users where userid={0}".format(uid)
                    for row in mycursor:
                        privacy=row[0]
                if body=='NULL':
                    sqlquery="insert into posts (userID,nature,date,time) values ({0},{1},'{2}','{3}') ".format(uid,privacy,d,t)
                else:
                    sqlquery="insert into posts (userID,nature,body,date,time) values ({0},{1},'{2}','{3}','{4}') ".format(uid,privacy,body,d,t)
                mycursor.execute(sqlquery)
                mydb.commit()
                sqlquery="select postid from posts where userID={0} order by date desc,time desc".format(uid)
                mycursor.execute(sqlquery)
                #print("#",uid,privacy,d,t)
                for row in mycursor:
                    postid=row[0]
                    #print("#",postid)
                if len(media)!=0:
                    for x in media:
                        sqlquery="insert into media (link,postid)values ('{0}',{1})".format(x,postid)
                if group!='NULL':
                    sqlquery="select groupid from group_detail where name='{0}'".format(group)
                    mycursor.execute(sqlquery)
                    for row in mycursor:
                        gid=row[0]
                    sqlquery="update posts set groupID={1} where postID={0}".format(postid,gid)
                    mycursor.execute(sqlquery)
                    mydb.commit()
                if topic!='NULL':
                    sqlquery="select topicid from topics where name='{0}'".format(topic)
                    mycursor.execute(sqlquery)
                    for row in mycursor:
                        tid=row[0]
                    sqlquery="update posts set topicID={1} where postID={0}".format(postid,tid)
                    mycursor.execute(sqlquery)
                    mydb.commit()
            else:
                print("ERROR! Your post has no content. Add media or body to the post")
        elif opt.lower()=="back":
            return
        else:
            print("ERROR! Invalid Command.")
            
def display_comment(cid):
    #to display a comment
    sqlquery="select fname,lname,body,date,time from comments,biodata where userfrom=userid and commentid={0}".format(cid)
    mycursor2.execute(sqlquery)
    for row in mycursor2:
        print("..{0} {1}->{2}\non {3}, {4}".format(row[0],row[1],row[2],row[3],row[4]))
    return
            
def display_posts(uid,pid):
    #to display a post
    no_displayed=0 #no of comments displayed
    info=[]
    sqlquery="select userID,groupID,topicID,body,Date,Time from posts where postid={0}".format(pid)
    mycursor2.execute(sqlquery)
    for row in mycursor2:
        info=[row[0],row[1],row[2],row[3],row[4],row[5]]

    if len(info)!=0:
        
        text="==="
        print(text.center(75,'='))
        
        sqlquery="select fname,lname from biodata where userid={0}".format(info[0])
        mycursor2.execute(sqlquery)
        for row in mycursor2:
            print("Post by -> ",row[0]," ",row[1],"\t on ",info[4]," ",info[5])
        if info[1]!=None:
            sqlquery="select name from group_detail where groupid={0}".format(info[1])
            mycursor2.execute(sqlquery)
            for row in mycursor2:
                print("Group -> ",row[0])
        if info[2]!=None:
            sqlquery="select name from topics where topicid={0}".format(info[2])
            mycursor2.execute(sqlquery)
            for row in mycursor2:
                print("Topic -> ",row[0])
        print()
        sqlquery="select count(*) from media where postid={0}".format(pid)
        mycursor2.execute(sqlquery)
        for row in mycursor2:
            media_count=row[0]
        if media_count>0:
            sqlquery="select url from media where postid={0}".format(pid)
            mycursor2.execute(sqlquery)
            for row in mycursor2:
                print("Link -> ",row[0])
            print()
        if info[3]!=None:
            print(info[3])  
            
        text="---"
        print(text.center(75,'-'))
        
        sqlquery="select count(*) from postLikes where postid={0} and type='like'".format(pid)
        mycursor2.execute(sqlquery)
        for row in mycursor2:
            likes=row[0]
        sqlquery="select count(*) from postLikes where postid={0} and type='dislike'".format(pid)
        mycursor2.execute(sqlquery)
        for row in mycursor2:
            dislikes=row[0]
        sqlquery="select count(*) from comments where postid={0}".format(pid)
        mycursor2.execute(sqlquery)
        for row in mycursor2:
            no_comments=row[0]
            
        print(likes," LIKES\t",dislikes," DISLIKES\t",no_comments," Comments")
        text="---"
        print(text.center(75,'-'))
        cids=[]#all comment ids
        sqlquery="select commentid from comments where postid={0} order by date desc,time desc".format(pid)
        mycursor2.execute(sqlquery)
        for row in mycursor2:
            cids.append(row[0])
        
        if no_comments<3:
            for i in range(len(cids)-no_comments,len(cids)):
                display_comment(cids[i])
                no_displayed+=1
                print() 
        else:
            for i in range(len(cids)-3,len(cids)):
                display_comment(cids[i])
                no_displayed+=1
                print()
        text="==="
        print(text.center(75,'='))    
        print()
        print("To see next post, press ENTER Key")
        print("To comment, enter 'COMMENT' followed by a space and your text")
        print("To like/dislike the post, enter 'LIKE' or 'DISLIKE'")
        print("To see likes/dislikes, enter 'SHOW LIKES' or 'SHOW DISLIKES', 50 results displayed at once..to load more enter 'MORE'")
        print("To load previous comments, enter 'LOAD PREVIOUS'")
        print("To go to Main Menu, enter 'BACK'")
        back=False
        next_p=False
        
        
        
        while(True):
            opt=input("Enter:")
            opt=opt.lstrip()
            opt=opt.rstrip()
            d=get_date()
            t=get_time()
            
            if len(opt)==0:
                return 1 #next
            elif opt.lower()=="back":
                return 2 #back
            elif opt[0:7].lower()=="comment" and opt[7].isspace():
                comment=opt[8:]
                if len(comment)>1000:
                    print("ERROR! number of characters are greater than 1000")
                else:
                    sqlquery="insert into comments (body, userfrom,postid,date,time) values ('{0}',{1},{2},'{3}','{4}')".format(comment,uid,pid,d,t)
                    mycursor2.execute(sqlquery)
                    mydb.commit()
            elif opt.lower()=="like" :
                sqlquery="insert into postLikes (userfrom,postid,date,time,type) values ({0},{1},'{2}','{3}','like')".format(uid,pid,d,t)
                mycursor2.execute(sqlquery)
                mydb.commit()
                
            elif opt.lower()=="dislike" :
                sqlquery="insert into postLikes (userfrom,postid,date,time,type) values ({0},{1},'{2}','{3}','dislike')".format(uid,pid,d,t)
                mycursor2.execute(sqlquery)
                mydb.commit()
                
            elif opt.lower()=="load previous":
                temp=0
                limit2=len(cids)-no_displayed
                limit1=len(cids)-no_displayed-1-3
                if limit1<0:
                    limit1=0
                for i in range(limit1,limit2):
                    if no_displayed+i<len(cids):
                        display_comment(cids[i])
                        temp+=1
                        print()
                else:
                    print("\nNo more comments!")
                no_displayed+=temp
            elif opt.lower()=="show likes":
                sqlquery="select count(*) from postLikes where postid={0} and type='like'".format(pid)
                mycursor2.execute(sqlquery)
                for row in mycursor2:
                    no_likes=row[0]
                if no_likes>0:
                    sqlquery="select fname,lname from postlikes,biodata where userfrom=userid and type='like' and postid={0} ".format(pid)
                    mycursor2.execute(sqlquery)
                    index=0
                    for row in mycursor2:
                        index+=1
                        print("-{0} {1}".format(row[0],row[1]))
                        if index==no_likes:
                            print()
                        
                        if index%50==0 or index==no_likes:
                            opt=input("Enter1:")
                            if opt.lower()=="more":
                                if index==no_likes:
                                    print("No more likes!")
                                else:
                                    continue
                            else:
                                break
                else:
                    print("Post has zero likes!")
            elif opt.lower()=="show dislikes":
                sqlquery="select count(*) from postLikes where postid={0} and type='dislike'".format(pid)
                mycursor2.execute(sqlquery)
                for row in mycursor2:
                    no_dislikes=row[0]
                if no_dislikes>0:
                    sqlquery="select fname,lname from postlikes,biodata where userfrom=userid and type='dislike' and postid={0} ".format(pid)
                    mycursor2.execute(sqlquery)
                    index=0
                    for row in mycursor2:
                        index+=1
                        print("-{0} {1}".format(row[0],row[1]))
                        if index==no_dislikes:
                            print()
                        #print(index,no_dislikes)
                        if index%50==0 or index==no_dislikes:
                            opt=input("Enter:")
                            if opt.lower()=="more":
                                if index==no_dislikes:
                                    print("No more dislikes!")
                                else:
                                    continue
                            else:
                                break
                else:
                    print("Post has zero dislikes!")
            else:
                print("ERROR! Invalid command")

def home_feed(uid,d_prev,t_prev):
    #to decide the post ids of older posts that will display in home feed of user uid
    
    postids=[]
    fids=[]
    temp=[]
    gids=[]
    tids=[]
    #new postsby me
    sqlquery="select postid from posts where (userid={0} and date='{1}' and time<'{2}') or (userid={0} and date<'{1}') order by date desc,time desc".format(uid,d_prev,t_prev)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0] not in postids:
            postids.append(row[0])
    #new likes or comments on my posts
    sqlquery="select distinct posts.postid from posts inner join comments on posts.postid=comments.postid where posts.userid={0} and ((comments.date='{1}' and comments.time<'{2}') or comments.date<'{1}') ".format(uid,d_prev,t_prev)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0] not in postids:
            postids.append(row[0])
    #getting friends  
    sqlquery="select user1,user2 from friend_req where (user1={0} or user2={0}) and accepted='accepted'".format(uid,d_prev)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0]!=uid and row[0] not in fids:
            fids.append(row[0])
        if row[1]!=uid and row[1] not in fids:
            fids.append(row[1])
    #print("fids",fids,uid)
    #new posts by friends
    for fid in fids:        
        sqlquery="select postid from posts where userid={0} and groupid is NULL and ((date='{1}' and time<'{2}') or date<'{1}') order by date desc,time desc".format(fid,d_prev,t_prev)
        mycursor.execute(sqlquery)
        for row in mycursor:
            if row[0] not in postids:
                postids.append(row[0])
    #print(sqlquery)
    #print("postid",postids)
    #posts by friends where uid commented
    for fid in fids:
        sqlquery="select distinct postid from comments where postid in (select distinct posts.postid from posts inner join comments on posts.postid=comments.postid where posts.userid={0} and userFrom={1} and groupid=NULL) and ((comments.date='{2}' and comments.time<'{3}') or comments.date<'{2}') order by date desc,time desc".format(fid,uid,d_prev,t_prev)
        mycursor.execute(sqlquery)
        for row in mycursor:
            if row[0] not in postids:
                postids.append(row[0])
    #get gids
    sqlquery="select groupid from group_members where userid={0} and removed=false".format(uid)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0] not in gids:
            gids.append(row[0])
    #group posts by others
    #sqlquery="select postid from posts where groupid in (select groupid from group_members where userid={0} and removed=false) and ((date='{1}' and time<='{2}') or date<'{1}') order by date desc,time desc".format(uid,d_prev,t_prev)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0] not in postids:
            postids.append(row[0])
    for gid in gids:
        sqlquery="select distinct postid from comments where postid in (select distinct posts.postid from posts inner join comments on posts.postid=comments.postid where groupid={0}) and ((comments.date='{1}' and comments.time<'{2}') or comments.date<'{1}') order by date desc,time desc".format(gid,d_prev,t_prev)
        mycursor.execute(sqlquery)
        for row in mycursor:
            if row[0] not in postids:
                postids.append(row[0])
                
    #get tids
    sqlquery="select topicid from followers where userid={0} ".format(uid)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0] not in tids:
            tids.append(row[0])
    #group posts by others
    sqlquery="select postid from posts where topicid in (select topicid from followers where userid={0} ) and ((date='{1}' and time<='{2}') or date<'{1}') and nature='public' order by date desc,time desc".format(uid,d_prev,t_prev)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0] not in postids:
            postids.append(row[0])
    for tid in tids:
        sqlquery="select distinct postid from comments where postid in (select distinct posts.postid from posts inner join comments on posts.postid=comments.postid where topicid={0} and nature='public') and ((comments.date='{1}' and comments.time<'{2}') or comments.date<'{1}') order by date desc,time desc".format(tid,d_prev,t_prev)
        mycursor.execute(sqlquery)
        for row in mycursor:
            if row[0] not in postids:
                postids.append(row[0])
    #print(postids)
    if len(postids)>0:
        for idx in postids:
            get=display_posts(uid,idx)
            if get==1:
                continue
            elif get==2:
                return
            
    else:
        print("No more posts!")
            

def home_feed_new(uid,d_prev,t_prev):
    #to decide the post ids of new posts that will display in home feed of user uid
    #new posts are the post since the last login of the user
    text=" HOME FEED "
    print(text.center(75,'~'))
    postids=[]
    fids=[]
    temp=[]
    gids=[]
    tids=[]
    #new postsby me
    sqlquery="select postid from posts where (userid={0} and date='{1}' and time>'{2}') or (userid={0} and date>'{1}') order by date desc,time desc".format(uid,d_prev,t_prev)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0] not in postids:
            postids.append(row[0])
    #new likes or comments on my posts
    sqlquery="select distinct posts.postid from posts inner join comments on posts.postid=comments.postid where posts.userid={0} and ((comments.date='{1}' and comments.time>'{2}') or comments.date>'{1}') ".format(uid,d_prev,t_prev)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0] not in postids:
            postids.append(row[0])
    #getting friends  
    sqlquery="select user1,user2 from friend_req where (user1={0} or user2={0}) and accepted='accepted'".format(uid,d_prev)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0]!=uid and row[0] not in fids:
            fids.append(row[0])
        if row[1]!=uid and row[1] not in fids:
            fids.append(row[1])
    #print("fids",fids,uid)
    #new posts by friends
    for fid in fids:        
        sqlquery="select postid from posts where userid={0} and groupid is NULL and ((date='{1}' and time>'{2}') or date>'{1}') order by date desc,time desc".format(fid,d_prev,t_prev)
        mycursor.execute(sqlquery)
        for row in mycursor:
            if row[0] not in postids:
                postids.append(row[0])
    #print(sqlquery)
    #print("postid",postids)
    #posts by friends where uid commented
    for fid in fids:
        sqlquery="select distinct postid from comments where postid in (select distinct posts.postid from posts inner join comments on posts.postid=comments.postid where posts.userid={0} and userFrom={1} and groupid=NULL) and ((comments.date='{2}' and comments.time>'{3}') or comments.date>'{2}') order by date desc,time desc".format(fid,uid,d_prev,t_prev)
        mycursor.execute(sqlquery)
        for row in mycursor:
            if row[0] not in postids:
                postids.append(row[0])
    #get gids
    sqlquery="select groupid from group_members where userid={0} and removed=false".format(uid)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0] not in gids:
            gids.append(row[0])
    #group posts by others
    sqlquery="select postid from posts where groupid in (select groupid from group_members where userid={0} and removed=false) and ((date='{1}' and time>='{2}') or date>'{1}') order by date desc,time desc".format(uid,d_prev,t_prev)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0] not in postids:
            postids.append(row[0])
    for gid in gids:
        sqlquery="select distinct postid from comments where postid in (select distinct posts.postid from posts inner join comments on posts.postid=comments.postid where groupid={0}) and ((comments.date='{1}' and comments.time>'{2}') or comments.date>'{1}') order by date desc,time desc".format(gid,d_prev,t_prev)
        mycursor.execute(sqlquery)
        for row in mycursor:
            if row[0] not in postids:
                postids.append(row[0])
                
    #get tids
    sqlquery="select topicid from followers where userid={0} ".format(uid)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0] not in tids:
            tids.append(row[0])
    #group posts by others
    sqlquery="select postid from posts where topicid in (select topicid from followers where userid={0} ) and ((date='{1}' and time>='{2}') or date>'{1}') and nature='public' order by date desc,time desc".format(uid,d_prev,t_prev)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0] not in postids:
            postids.append(row[0])
    for tid in tids:
        sqlquery="select distinct postid from comments where postid in (select distinct posts.postid from posts inner join comments on posts.postid=comments.postid where topicid={0} and nature='public') and ((comments.date='{1}' and comments.time>'{2}') or comments.date>'{1}') order by date desc,time desc".format(tid,d_prev,t_prev)
        mycursor.execute(sqlquery)
        for row in mycursor:
            if row[0] not in postids:
                postids.append(row[0])
    #print(postids)
    if len(postids)>0:
        for idx in postids:
            get=display_posts(uid,idx)
            if get==1:
                continue
            elif get==2:
                return 0
            
    else:
        print("No new posts!")
        return 1
        
            
def notify(uid):
    #to display notifications
    noti=[]
    
    sqlquery="select prevSIdate,prevSItime from users where userid={0}".format(uid)
    mycursor.execute(sqlquery)
    for row in mycursor:
        prev_date=row[0]
        prev_time=row[1]
    sqlquery="select count(*) from friend_req where (user1={0} or user2={0}) and accepted='requested' and activity!={0} ".format(uid,prev_date,prev_time)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0]>0:
            z="->You have {0} new friend requests".format(row[0])
            noti.append(z)
    sqlquery="select count(*) from friend_req where (user1={0} or user2={0}) and accepted='accepted' and activity!={0} and ((acceptDate='{1}' and acceptTime>='{2}') or (acceptDate>'{1}'))".format(uid,prev_date,prev_time)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0]>0:
            z="->{0} people accepted your friend requests".format(row[0])
            noti.append(z)
    sqlquery="select count(likeid) from postlikes,posts where posts.postid=postlikes.postid and posts.userid={0} and ((postlikes.date='{1}' and postlikes.time>='{2}') or (postlikes.date>'{1}'))".format(uid,prev_date,prev_time)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0]>0:
            z="->You have new activity on your post(s)".format(row[0])
            noti.append(z)
    sqlquery="select count(commentid) from comments,posts where posts.postid=comments.postid and posts.userid={0} and ((comments.date='{1}' and comments.time>='{2}') or (comments.date>'{1}'))".format(uid,prev_date,prev_time)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0]>0:
            z="->You have new comments on your post(s)".format(row[0])
            noti.append(z)
            
    admin_count=0
    adminOf=[]
    sqlquery="select groupID,name,privacy from group_detail where admin1={0} or admin2={0} or admin3={0}".format(uid)
    mycursor.execute(sqlquery)
    for row in mycursor:
        adminOf.append([row[0],row[1],row[2]])
        admin_count+=1
    if admin_count>0:
        for grp in adminOf:
            if grp[2]=='private':
                sqlquery="select count(*) from group_req where groupID={0} and status='requested' and ((req_date='{1}' and req_time>='{2}') or (req_date>'{1}'))".format(grp[0],prev_date,prev_time)
                mycursor.execute(sqlquery)
                for row in mycursor:
                    if row[0]>0:
                        z="->You have {0} new requests in Group {1}".format(row[0],grp[1])
                        noti.append(z)
    sqlquery="select name from group_detail where (admin1={0} and date1='{1}' and time1>='{2}') or (admin1={0} and date1>'{1}') or (admin2={0} and date2='{1}' and time2>='{2}') or (admin2={0} and date2>'{1}') or (admin3={0} and date3='{1}' and time3>='{2}') or (admin3={0} and date3>'{1}') ".format(uid,prev_date,prev_time)
    mycursor.execute(sqlquery)
    for row in mycursor:
        z="->You are added as admin for group {0}".format(row[0])
        noti.append(z)
    
    sqlquery="select name from group_members,group_detail where group_members.groupid=group_detail.groupid and group_members.userid={0} and privacy='private' and removed=false and ((group_members.date='{1}' and group_members.time>='{2}') or (group_members.date>'{1}'))".format(uid,prev_date,prev_time)
    mycursor.execute(sqlquery)
    for row in mycursor:
        z="->You are now member of group {0}".format(row[0])
        noti.append(z)
    
    gids=[]
    sqlquery="select count(postid),group_detail.groupid,group_detail.name from posts,group_detail where posts.groupid=group_detail.groupid and group_detail.groupid in (select distinct groupid from group_members where userid={0} and removed=false) and ((date='{1}' and time>='{2}') or date>'{1}') group by groupid".format(uid,prev_date,prev_time)
    mycursor.execute(sqlquery)
    for row in mycursor:
        z="->You have {0} new posts in group {1}".format(row[0],row[2])
        noti.append(z)
    if len(noti)>0:
        text=" Notifications "
        print(text.center(75,'~'))
        for txt in noti:
            print(txt)
    else:
        print("You don't have new notifications")

                      
def mainMenu(uid):
    #to display the main menu
    sqlquery="select login_times from users where userid={0}".format(uid)
    mycursor.execute(sqlquery)
    for row in mycursor:
        if row[0]>1:
            notify(uid)
    while(True):
        text=" Main Menu "
        print(text.center(75,'~'))
        print("1.Home Feed\t \t2.Create new post\n3.My Groups\t \t4.My Profile\n5.Search\t \t6.My Links\n7.Settings\t \t8.Logout")
        opt=input("Select from option 1 to 7:")
        if opt=='1':
            sqlquery="select lastseen_d,lastseen_t from users where userid={0}".format(uid)
            mycursor.execute(sqlquery)
            for row in mycursor:
                d_prev=row[0]
                t_prev=row[1]
            if d_prev==None:
                d=get_date()
                t=get_time()
                yr=int(d[0:4])
                yr=yr-1
                d_prev=str(yr)+d[4:]
                t_prev=t
            nxt=home_feed_new(uid,d_prev,t_prev)
            if nxt==1:
                home_feed(uid,d_prev,t_prev)
            d=get_date()
            t=get_time()
            sqlquery="update users set lastseen_d='{1}',lastseen_t='{2}' where userid={0}".format(uid,d,t)
            mycursor.execute(sqlquery)
            mydb.commit()
        elif opt=='2':
            newPost(uid)
        elif opt=='3':
            admin_count=0
            adminOf=[]
            sqlquery="select groupID,name,privacy from group_detail where admin1={0} or admin2={0} or admin3={0}".format(uid)
            mycursor.execute(sqlquery)
            for row in mycursor:
                adminOf.append([row[0],row[1],row[2]])
                admin_count+=1
            groupMenu(uid,admin_count,adminOf)
             
        elif opt=='4':
            profile(uid)
        elif opt=='5':
            searchMenu(uid)
        elif opt=='6':
            links(uid)
        elif opt=='7':
            settings(uid)
        elif opt=='8':
            log_out()
        else:
            break
        


def signin():
    #to sign-in into a account
    print("**NOTE :you will be prompted for forget password after 3 attempts")
    incorrect=0
    username=""
    passwod=""
    while(True):
        user=input("Username:")
        pswd=input("password:")
        sqlquery="select UserID,Username,password,latestSIdate,latestSItime from users where Username='{0}'".format(user)
        mycursor.execute(sqlquery)
        for row in mycursor:
            uid=int(row[0])
            username=row[1]
            password=row[2]
            prev_date=row[3]
            prev_time=row[4]
        if username==user:
            if password==pswd:
                print("Login Successfull !!")
                sqlquery="select login_times from users where userid={0}".format(uid)
                mycursor.execute(sqlquery)
                for row in mycursor:
                    login_time=row[0]
                login_time+=1
                signin_date=get_date()
                t=get_time()
                if prev_date==None:
                    sqlquery="update users set latestSIdate='{0}',latestSItime='{2}',login_times={3} where userid={1}".format(signin_date,uid,t,login_time)
                else:
                    sqlquery="update users set prevSIdate='{0}',prevSItime='{3}', latestSIdate='{1}',latestSItime='{4}',login_times={5} where userid={2}".format(prev_date,signin_date,uid,prev_time,t,login_time)
                mycursor.execute(sqlquery)
                mydb.commit()

                '''sql="select * from posts"
                mycursor.execute(sql)
                for row in mycursor:
                    print(row)'''
                mainMenu(int(uid))
                break
            else:
                print("Incorrect Username or Password. Try Again!")
                incorrect+=1
        else:
            print("Incorrect Username or Password. Try Again!")
            incorrect+=1
        if incorrect>=3:
            while(True):
                print("Menu:\n1. Forget password\n2. Try again\n3. Exit to home")
                opt=input("Enter response:")
                if opt=='1':
                    success=forget_password(user)
                    if success==False:
                        return
                    else:
                        incorrect=0
                        break
                elif opt=='2':
                    incorrect=0
                    break
                elif opt=='3':
                    return
                else:
                    print("Invalid Response")
                    


def homepage():
    #to display the homepage content
    #options: sign in / sign up / exit
    print()
    text=" Welcome to ConnectWorld "
    print(text.center(75,'*'))
    flag=True
    while(flag):
        print("Menu: \n1. Enter 1 to sign-in\n2. New User? Enter 2 to sign-up\n3. Enter 3 to exit")
        option=input("Enter:")
        if option=='1':
            signin()
            flag=False
            break
        elif option=='2':
            signup()
            flag=False
            break
        elif option=='3':
            exit()
        else:
            print("Error! Not valid command")   


while(True):
    homepage()




