import pygame

class Item:
    def __init__(self, name, displayName, description, isWeapon=False, damage=0):
        self.name = name
        self.displayName = displayName
        self.description = description
        self.isWeapon = isWeapon
        self.damage = damage

    def addItemsToGame(self, itemlist):
        itemlist.append(self)
