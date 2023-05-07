class User():
    #Constructors
    def __init__(self, account):
        self.__userID = account[0]
        self.__username = account[5]
        self.__isLoggedIn = True
        #self.__profilePicture = profilePicture
    
    #Setters/Getters
    def getUserID(self):
        return self.__userID
    
    def getUsername(self):
        return self.__username
    
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
        