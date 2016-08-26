'''
Created on Aug 21, 2016

@author: sonu
'''


class ShoppingMall(object):
    def __init__(self):
        self._typename = "ShoppingMall"
        self._category = "shopping playing carnival"
        self._typespec = {"dummykey1": "dummyval1"}
        self._typedesc = "Leisure shopping"


    @property
    def typename(self):
        return self._typename

    @typename.setter
    def typename(self, val):
        self._typename = val

    @property
    def category(self):
        return self._category

    @property
    def typespec(self):
        return self.typespec

    @property
    def typedesc(self):
        return self._typedesc


class Hospital(object):
    def __init__(self):
        self._typename = "Hospital"
        self._category = "healthcare treatment medicines"
        self._typespec = {"dummykey1": "dummyval1"}
        self._typedesc = "Wellness Center"

    @property
    def typename(self):
        return self._typename

    @typename.setter
    def typename(self, val):
        self._typename = val

    @property
    def category(self):
        return self._category

    @property
    def typespec(self):
        return self._typespec

    @property
    def typedesc(self):
        return self._typedesc
