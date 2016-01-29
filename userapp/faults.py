'''
Created on Nov 27, 2015

@author: sonu
'''


class UserNotFoundException(Exception):
    pass


class UserSessionNotFoundException(Exception):
    pass


class UserNotAuthorizedException(Exception):
    pass


class UserAlreadyExist(Exception):
    pass
