import mysql.connector

class sqlconnector:
    db = mysql.connector.connect(
    host = 'doggoserver.mysql.database.azure.com',
    port = '3306',
    user = 'mainadmin',
    password = '9jznqua4y5T@',
    database = 'userinfo'
    )

