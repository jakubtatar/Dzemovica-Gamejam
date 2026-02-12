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
                    elif char == "v":
                        tiles.append((rect, "v")) # voda
                        collidable_tiles.append(rect)

                        
        return tiles, collidable_tiles

    def drawTilemap(self, screen, tile_type, rect, camera, tile1_img, tile2_img, hedgefront_img, hedgetopfront_img, hedgeRD_img, hedgeLD_img, hedgetopwall_img, hedgeLT_img, hedgeRT_img, floor_planks_img, wall_img, wall_front_img, wall_top_img, wall_left_img, wall_right_img, wall_RT_img, wall_LT_img, wall_RD_img, wall_LD_img, wheat_wall_img, wheat_wall_top_img, water_gif):
        if tile_type == "1":
            screen.blit(tile1_img, camera.apply(rect))
        elif tile_type == "0":
            screen.blit(tile2_img, camera.apply(rect))
        elif tile_type == "3":
            screen.blit(hedgefront_img, camera.apply(rect))
        elif tile_type == "4":
            screen.blit(hedgetopfront_img, camera.apply(rect))
        elif tile_type == "5":
            screen.blit(hedgeRD_img, camera.apply(rect))
        elif tile_type == "6":
            screen.blit(hedgeLD_img, camera.apply(rect))
        elif tile_type == "7":
            screen.blit(hedgetopwall_img, camera.apply(rect))
        elif tile_type == "8":
            screen.blit(hedgeLT_img, camera.apply(rect))
        elif tile_type == "9":
            screen.blit(hedgeRT_img, camera.apply(rect))
        elif tile_type == "p":
            screen.blit(floor_planks_img, camera.apply(rect))
        elif tile_type == "s":
            screen.blit(wall_img, camera.apply(rect))
        elif tile_type == "f":
            screen.blit(wall_front_img, camera.apply(rect))
        elif tile_type == "w":
            screen.blit(wall_top_img, camera.apply(rect))
        elif tile_type == "a":
            screen.blit(wall_left_img, camera.apply(rect))
        elif tile_type == "d":
            screen.blit(wall_right_img, camera.apply(rect))
        elif tile_type == "e":
            screen.blit(wall_RT_img, camera.apply(rect))
        elif tile_type == "q":
            screen.blit(wall_LT_img, camera.apply(rect))
        elif tile_type == "c":
            screen.blit(wall_RD_img, camera.apply(rect))
        elif tile_type == "z":
            screen.blit(wall_LD_img, camera.apply(rect))
        elif tile_type == "n":
            screen.blit(wheat_wall_img, camera.apply(rect))
        elif tile_type == "m":
            screen.blit(wheat_wall_top_img, camera.apply(rect))
        elif tile_type == "v":
            screen.blit(water_gif, camera.apply(rect))