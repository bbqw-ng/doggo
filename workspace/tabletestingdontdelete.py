import mysql.connector

db = mysql.connector.connect(
host = 'doggoserver.mysql.database.azure.com',
port = '3306',
user = 'mainadmin',
password = '9jznqua4y5T@',
database = 'userinfo'
)

cursor = db.cursor()
#cursor.execute("CREATE TABLE PostInfo(title VARCHAR(250), username VARCHAR(20), timePosted VARCHAR(30), schedule VARCHAR(200), description VARCHAR(2000)")
#cursor.execute("CREATE TABLE LoginInfo(userID int PRIMARY KEY AUTO_INCREMENT, email VARCHAR(30), password VARCHAR(30), firstName VARCHAR(20), lastName VARCHAR(20), username VARCHAR(20), age smallint UNSIGNED, postalCode VARCHAR(15))")
db.commit()




