import pygame

class MapsManager:
    def __init__(self):
        self.maps = {}

    def load_map(self, filename, tile_size):
        tiles = []
        collidable_tiles = []
        with open(filename, "r") as file:
            for row_index, line in enumerate(file):
                for col_index, char in enumerate(line.strip()):
                    x = col_index * tile_size
                    y = row_index * tile_size
                    rect = pygame.Rect(x, y, tile_size, tile_size)
                    
                    if char == "1":
                        tiles.append((rect, "1"))  
                    elif char == "2":
                        tiles.append((rect, "2"))
                        collidable_tiles.append(rect) 
                    elif char == "0":
                        tiles.append((rect, "0"))  
                    elif char == "3":
                        tiles.append((rect, "3"))
                        collidable_tiles.append(rect)
                    elif char == "4":
                        tiles.append((rect, "4"))
                        collidable_tiles.append(rect)
                    elif char == "5":
                        tiles.append((rect, "5"))
                        collidable_tiles.append(rect)
                    elif char == "6":
                        tiles.append((rect, "6"))
                        collidable_tiles.append(rect)
                    elif char == "7":
                        tiles.append((rect, "7"))
                        collidable_tiles.append(rect)
                    elif char == "8":
                        tiles.append((rect, "8"))
                        collidable_tiles.append(rect)
                    elif char == "9":
                        tiles.append((rect, "9"))
                        collidable_tiles.append(rect)
                    elif char == "p":
                        tiles.append((rect, "p")) # pridane pre planks
                    elif char == "s":
                        tiles.append((rect, "s")) # wall
                        collidable_tiles.append(rect)
                    elif char == "f":
                        tiles.append((rect, "f")) # wall front
                        collidable_tiles.append(rect)
                    elif char == "w":
                        tiles.append((rect, "w")) # wall top
                        collidable_tiles.append(rect)
                    elif char == "a":
                        tiles.append((rect, "a")) # wall left
                        collidable_tiles.append(rect)
                    elif char == "d":
                        tiles.append((rect, "d")) # wall right
                        collidable_tiles.append(rect)
                    elif char == "e":
                        tiles.append((rect, "e")) # wall RT
                        collidable_tiles.append(rect)
                    elif char == "q":
                        tiles.append((rect, "q")) # wall LT
                        collidable_tiles.append(rect)
                    elif char == "c":
                        tiles.append((rect, "c")) # wall RD
                        collidable_tiles.append(rect)
                    elif char == "z":
                        tiles.append((rect, "z")) # wall LD
                        collidable_tiles.append(rect)
                    elif char == "n":
                        tiles.append((rect, "n")) # wheat wall
                        collidable_tiles.append(rect)
                    elif char == "m":
                        tiles.append((rect, "m")) # wheat wall top
                        collidable_tiles.append(rect)

                        
        return tiles, collidable_tiles
