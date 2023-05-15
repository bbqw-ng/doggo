from flask_login import UserMixin

class User(UserMixin):
    __uniqueID = 00000000
    #Constructors
    def __init__(self, account):
        self.__userID = account[0]
        self.__username = account[5]
        self.__isLoggedIn = True
        self.__profilePicture = 'dog2.img'
        User.__uniqueID += account[0] + 1
    
    #Setters/Getters
    def getUserID(self):
        return int(self.__userID)
    
    def getUsername(self):
        return str(self.__username)
    
    def getLoginStatus(self):
        return self.__isLoggedIn
    #~Account Settings~
    #TBD

    def logout(self):
        self.__isLoggedIn = False
        self.__userID = None
        self.__username = None
        

#Admin Class
class Admin(User):    
    def __init__(self, account):
        super().__init__(account)
        