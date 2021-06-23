create table Users (UserID BIGINT NOT NULL AUTO_INCREMENT,Username char(255) NOT NULL , password char(15) NOT NULL, signupDate date, activated boolean DEFAULT True, prevSIdate date DEFAULT NULL,prevSItime time DEFAULT NULL,latestSIdate date DEFAULT NULL,latestSItime time DEFAULT NULL,securityQues char(255) NOT NULL, securityAns char(255) NOT NULL, nature enum ('Public','Private') DEFAULT 'Public', search boolean DEFAULT True,login_times INT default 0,lastseen_d date default null, lastseen_t time default null, PRIMARY KEY (UserID) );

create table biodata (UserID BIGINT NOT NULL PRIMARY KEY, FName char(255) NOT NULL, LName char(255) NOT NULL, birthdate date DEFAULT NULL, gender enum ('male','female','others') NOT NULL, emailid char(50) DEFAULT NULL, contact char(10) DEFAULT NULL, city char(100) DEFAULT NULL, country char(100) DEFAULT NULL, education1 char(100) DEFAULT NULL, education2 char(100) DEFAULT NULL, education3 char(100) DEFAULT NULL, work1 char(100) DEFAULT NULL,designation1 char(100) DEFAULT NULL,work2 char(100) DEFAULT NULL,designation2 char(100) DEFAULT NULL, work3 char(100) DEFAULT NULL,designation3 char(100) DEFAULT NULL);

create table friend_req ( reqID INT NOT NULL AUTO_INCREMENT , user1 BIGINT NOT NULL, user2 BIGINT NOT NULL, accepted enum ('requested','accepted','declined') DEFAULT 'requested',seen boolean DEFAULT False, activity BIGINT NOT NULL, reqDate date, reqTime time,acceptDate date DEFAULT NULL,acceptTime time DEFAULT NULL, PRIMARY KEY(reqID));

create table posts (postID BIGINT NOT NULL AUTO_INCREMENT , userID BIGINT NOT NULL,groupID BIGINT DEFAULT NULL, topicID INT DEFAULT NULL, nature enum ('Public','Private','Personal') DEFAULT 'Public', body varchar(10000) DEFAULT NULL, Date date, Time time, PRIMARY KEY(postID));

create table Comments( commentID BIGINT NOT NULL AUTO_INCREMENT, body varchar(5000), userFrom BIGINT NOT NULL, postID BIGINT, date date, time time, PRIMARY KEY(commentID));


create table postLikes (likeID INT NOT NULL AUTO_INCREMENT, userFrom BIGINT NOT NULL, postID BIGINT NOT NULL, date date, time time, type enum ('like','dislike'), PRIMARY KEY(likeID));


create table media (mediaID INT NOT NULL AUTO_INCREMENT, link varchar(2000) NOT NULL, postID BIGINT DEFAULT NULL, PRIMARY KEY(mediaID));

create table topics (topicID INT NOT NULL AUTO_INCREMENT, name char(255) NOT NULL, no_followers INT DEFAULT 0,PRIMARY KEY(topicID));

create table followers (topicID INT NOT NULL, userID BIGINT NOT NULL,date date, PRIMARY KEY (topicID,userID));

create table group_detail (groupID BIGINT NOT NULL AUTO_INCREMENT, name char(100) NOT NULL, description varchar(500) DEFAULT NULL, admin1 BIGINT NOT NULL, date1 date NOT NULL, time1 time NOT NULL,admin2 BIGINT DEFAULT NULL,date2 date DEFAULT NULL,time2 time DEFAULT NULL, admin3 BIGINT DEFAULT NULL,date3 date DEFAULT NULL,time3 time DEFAULT NULL,privacy enum ('public','private') DEFAULT 'public', no_members INT DEFAULT NULL, activated boolean DEFAULT True, date_created date, PRIMARY KEY(groupID));

create table group_members (groupID BIGINT NOT NULL, userID BIGINT NOT NULL, date date,time time,removed boolean DEFAULT false, PRIMARY KEY (groupID,userID));

create table group_req (reqID INT NOT NULL AUTO_INCREMENT, groupID BIGINT NOT NULL , userID BIGINT NOT NULL, req_date date, req_time time,status enum ('requested','seen','accepted','declined') DEFAULT 'requested', PRIMARY KEY (reqID));

alter table biodata add foreign key (userID) references users(userID);

alter table friend_req add foreign key (user1) references users(UserID);
alter table friend_req add foreign key (user2) references users(UserID);
alter table friend_req add foreign key (activity) references users(UserID);

alter table posts add foreign key (groupID) references group_detail(groupID);
alter table posts add foreign key (userID) references users(UserID);
alter table posts add foreign key (topicID) references topics(topicID);

alter table comments add foreign key (userFrom) references users(UserID);
alter table comments add foreign key (postid) references posts(postid);

alter table postLikes add foreign key (userFrom) references users(userID);
alter table postLikes add foreign key (postid) references posts(postid);

alter table media add foreign key (postid) references posts(postid);

alter table followers add foreign key (userID) references users(UserID);
alter table followers add foreign key (topicID) references topics(topicID);

alter table group_detail add foreign key (admin1) references users(UserID);
alter table group_detail add foreign key (admin2) references users(UserID);
alter table group_detail add foreign key (admin3) references users(UserID);

alter table group_members add foreign key (userID) references users(UserID);
alter table group_members add foreign key (groupID) references group_detail(groupID);

alter table group_req add foreign key (userID) references users(UserID);
alter table group_req add foreign key (groupID) references group_detail(groupID);



