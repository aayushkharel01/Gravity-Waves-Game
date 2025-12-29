add_library('minim')
import math
import random
import os

#global variables
WIDTH = 800
HEIGHT = 600
PATH = os.getcwd()
player = Minim(this)

#spaceship class
class Spaceship: 
    def __init__(self):
        #photos
        self.spaceship_up_img = loadImage(PATH + "/images/space_up.png")
        self.spaceship_down_img = loadImage(PATH + "/images/space_down.png")
        self.spaceship_normal_img = loadImage(PATH + "/images/space_normal.png")
        #ship starting at a fixed position
        self.x = 100 
        self.y = HEIGHT // 2
        self.vy = 0 #vertical velocity
        self.r = 20 #radius for collision
        self.vx = 0 #horizontal velocity
        
        #these define the boundary of the tunnel space
        self.lower_limit = HEIGHT - 105
        self.upper_limit = 60
                
        #trail system
        self.trail = []  #list of trail positions

        #thrust up, -1: thrust down, 0: neutral/float
        self.space_handler = 0

    def update(self):
        #movement based on input
        if self.space_handler == 1:
            self.vx = 5
            self.vy = -5 #diagonal up-right
        elif self.space_handler == -1:
            self.vx = 5
            self.vy = 5 #diagonal down-right
        else:
            self.vx = 5
            self.vy = 5

    
        #apply movement
        self.x += self.vx
        self.y += self.vy
    
        #prevent going through borders
        if self.y < self.upper_limit:
            self.y = self.upper_limit
            self.vy = 0
        elif self.y > self.lower_limit:
            self.y = self.lower_limit
            self.vy = 0
    
        #scrolling system - when spaceship reaches middle of screen
        if self.x >= WIDTH // 2:
            self.x = WIDTH // 2 #don't let spaceship move further right, scroll the world instead
       

        #trail system
        if self.vx != 0 or self.vy != 0:
            self.trail.append([self.x, self.y])
            if len(self.trail) > 150:
                del self.trail[0]  # remove oldest point to save memory
    
    def display(self):
        #draw trail first (behind the spaceship)
        for i in range(len(self.trail)-1):
            x1 = self.trail[i][0]
            y1 = self.trail[i][1]
            x2 = self.trail[i+1][0]
            y2 = self.trail[i+1][1]
            
            stroke(255,255,255)  #white trail
            strokeWeight(10)
            line(x1+25, y1+25, x2+25, y2+25)
        
        #draw spaceship
        if self.vy == -5:
            image(self.spaceship_up_img, self.x, self.y, 50, 50)
        elif self.vy == 5:
            image(self.spaceship_down_img, self.x, self.y, 50, 50)
        else:
            image(self.spaceship_normal_img, self.x, self.y, 50, 50)

#Tunnel class
class Tunnel:

    def __init__(self):
        #list of obstacle dictionaries
        #format: {'type': 'rect'/'triangle_down'/'triangle_up', 'x': x_coord, 'y': y_coord, 'w': width, 'h': height}
        self.obstacles = [] # collect obstacles
        self.coins = [] #collect coins
        self.power_potions = [] #collect power_potions
        #all levels run at this speed(visual effect)
        self.level_speed = 5
        
        #photos
        self.moon_img = loadImage(PATH + "/images/moon.png")
        self.lava_img = loadImage(PATH + "/images/lava.png")
        self.cube1_img = loadImage(PATH + "/images/lavacube1.png")
        self.cube2_img = loadImage(PATH + "/images/lavacube2.png")
    
    def generate_easy_level(self):
        #easy level
        self.obstacles = []
        self.coins = []
        self.power_potions = []
        current_x = 200
        
        for i in range(6):
            #first section
            #Creates a wide safe path that moves
            self.add_borders(current_x, 1000)
            
            self.obstacles.append({'type': 'triangle_down', 'x': current_x + 200, 'y': 60, 'w': 200, 'h': 260})
            self.obstacles.append({'type': 'rect','subtype':'cube1','x': current_x + 450, 'y': 250, 'w': 60, 'h': 60})
            self.obstacles.append({'type': 'triangle_up', 'x': current_x + 600, 'y': 340, 'w': 180, 'h': 200})
            
            current_x += 1000
            
            #spawn a coin chain
            if i%2 == 0:
                self.spawn_coin_chain(current_x - 200, 6, 40, random.randint(330,430))
                self.spawn_coin_chain(current_x + 80, 6, 40, random.randint(210,250))
                self.spawn_coin_chain(current_x + 750, 6, 40, random.randint(330,430))
            else:
                self.spawn_coin_chain(current_x - 450, 6, 40, random.randint(150,250))
                self.spawn_coin_chain(current_x + 800, 6, 40, random.randint(450, 460))
                self.spawn_coin_chain(current_x + 100, 6, 40, random.randint(250,300))

            #second section
            #thicker borders rectangles
            self.obstacles.append({'type': 'rect', 'subtype':'lava','x': current_x, 'y': 0, 'w': 800, 'h': 100}) 
            self.obstacles.append({'type': 'rect', 'subtype':'lava','x': current_x, 'y': 500, 'w': 800, 'h': 100})
            
            self.obstacles.append({'type': 'rect','subtype':'cube1', 'x': current_x, 'y': 270, 'w': 50, 'h': 50}) 
            self.obstacles.append({'type': 'triangle_down', 'x': current_x + 200, 'y': 100, 'w': 120, 'h': 120})
            self.obstacles.append({'type': 'rect', 'subtype':'cube2','x': current_x + 400, 'y': 270, 'w': 50, 'h': 50}) 
            self.obstacles.append({'type': 'triangle_up', 'x': current_x + 600, 'y': 380, 'w': 120, 'h': 120})
            self.obstacles.append({'type': 'rect', 'subtype':'cube2','x': current_x+800, 'y': 270, 'w': 50, 'h': 50}) 

            current_x += 800

    def generate_medium_level(self):
        #medium level
        self.obstacles = []
        self.coins = []
        self.power_potions = []
        current_x = 200
        
        for i in range(6):
            #section 1: mixed obstacles
            self.add_borders(current_x, 1200)
            
            self.obstacles.append({'type': 'triangle_down', 'x': current_x + 50, 'y': 60, 'w': 90, 'h': 180})
            self.obstacles.append({'type': 'triangle_up', 'x': current_x + 200, 'y': 360, 'w': 90, 'h': 180})
            self.obstacles.append({'type': 'rect', 'subtype':'cube1','x': current_x + 400, 'y': 60, 'w': 80, 'h': 50})
            self.obstacles.append({'type': 'rect', 'subtype':'cube2','x': current_x + 400, 'y': 290, 'w': 80, 'h': 250})
            self.obstacles.append({'type': 'triangle_down', 'x': current_x + 650, 'y': 60, 'w': 90, 'h': 180})
            self.obstacles.append({'type': 'triangle_up', 'x': current_x + 800, 'y': 360, 'w': 90, 'h': 180})
            self.obstacles.append({'type': 'triangle_down', 'x': current_x + 1000, 'y': 60, 'w': 90, 'h': 180})
            self.obstacles.append({'type': 'rect', 'subtype':'cube1','x': current_x + 1000, 'y': 460, 'w': 40, 'h': 60})
            
            current_x += 1200
            
            #section 2
            self.obstacles.append({'type': 'rect', 'subtype':'lava','x': current_x, 'y': 0, 'w': 800, 'h': 150})
            self.obstacles.append({'type': 'rect', 'subtype':'lava','x': current_x, 'y': 450, 'w': 800, 'h': 150})
            
            #spawn coins
            if i%2 == 0:
                self.spawn_coin_chain(current_x - 650, random.randint(5, 8), 40, random.randint(240, 250))
                self.spawn_coin_chain(current_x + 80, random.randint(5, 8), 40, random.randint(210,250))
                self.spawn_coin_chain(current_x + 750, random.randint(4, 6), 40, random.randint(330,430))
            else:
                self.spawn_coin_chain(current_x - 450, random.randint(3, 6), 40, random.randint(150,250))
                self.spawn_coin_chain(current_x + 800, random.randint(3, 5), 40, random.randint(320, 340))
                self.spawn_coin_chain(current_x + 100, random.randint(3, 5), 40, random.randint(250,300))

            #spawning power potion
            if i % 4 == 0: 
                self.spawn_power_potion(current_x + 600, HEIGHT / 2)
                
            #adding small triangle spike obstacles
            for k in range(3):
                self.obstacles.append({'type': 'triangle_down', 'x': current_x + 200 + (k*200), 'y': 150, 'w': 60, 'h': 60})
                self.obstacles.append({'type': 'triangle_up', 'x': current_x + 100 + (k*200), 'y': 390, 'w': 60, 'h': 60})
            current_x += 800
        
    #hard level
    def generate_hard_level(self):
        
        self.obstacles = []
        self.coins = []
        self.power_potions = []
        current_x = 200
        
        for i in range(8):
            #section 1
            self.add_borders(current_x, 800)
            
            for j in range(5):
                self.obstacles.append({'type': 'triangle_down', 'x': current_x + (j*160), 'y': 60, 'w': 80, 'h': 180})
                self.obstacles.append({'type': 'triangle_up', 'x': current_x + (j*160) + 80, 'y': 360, 'w': 80, 'h': 180})
                
            current_x += 800
            
            #spawn coins
            if i%2 == 0:
                self.spawn_coin_chain(current_x - 650, random.randint(4, 7), 40, random.randint(250, 270))
                self.spawn_coin_chain(current_x + 750, random.randint(3, 5), 40, random.randint(290, 310))
            else:
                self.spawn_coin_chain(current_x - 450, random.randint(3, 6), 40, random.randint(250, 270))
                self.spawn_coin_chain(current_x + 100, random.randint(3, 5), 40, random.randint(250, 270))
                
            #spawn power potion
            if i % 3 == 0:
                self.spawn_power_potion(current_x + 550, 250)
            
            #section 2
            self.obstacles.append({'type': 'rect','subtype':'lava', 'x': current_x, 'y': 0, 'w': 900, 'h': 80})
            self.obstacles.append({'type': 'rect', 'subtype':'lava','x': current_x, 'y': 520, 'w': 900, 'h': 80})
            
            self.obstacles.append({'type': 'rect', 'subtype':'cube1','x': current_x + 100, 'y': 80, 'w': 100, 'h': 100})
            self.obstacles.append({'type': 'rect','subtype':'cube2', 'x': current_x + 100, 'y': 420, 'w': 100, 'h': 100}) 
            self.obstacles.append({'type': 'rect','subtype':'cube1', 'x': current_x + 400, 'y': 80, 'w': 100, 'h': 250})
            self.obstacles.append({'type': 'rect','subtype':'cube2' ,'x': current_x + 400, 'y': 470, 'w': 100, 'h': 50}) 
            self.obstacles.append({'type': 'rect', 'subtype':'cube1','x': current_x + 700, 'y': 80, 'w': 100, 'h': 120})
            self.obstacles.append({'type': 'rect', 'subtype':'cube2','x': current_x + 700, 'y': 380, 'w': 100, 'h': 140})
            
            current_x += 900
            
    #just to add two rectangles on top and botton, a border
    def add_borders(self, x, w):
        self.obstacles.append({'type': 'rect', 'x': x, 'y': 0, 'w': w, 'h': 60})
        self.obstacles.append({'type': 'rect', 'x': x, 'y': 540, 'w': w, 'h': 60})
        
    #helps to spawn a horizontal chain of coins
    def spawn_coin_chain(self, start_x, num_coins, gap, y):
        for i in range(num_coins):
            self.coins.append(Coin(start_x + i * gap, y))
            
    #helps to spawn a power potion depending on levels 
    def spawn_power_potion(self, x, y):
        self.power_potions.append(PowerPotion(x, y))
        
    #removes off screen objects, optimized for performance --> cause it created lag when i keep generating and not deleting'''
    def update(self):
        #cleanup obstacles
        temp_obstacles = []
        for o in self.obstacles:
            if o['x'] > -WIDTH:
                temp_obstacles.append(o)
        self.obstacles = temp_obstacles

        #cleanup coins
        temp_coins = []
        for c in self.coins:
            if c.x > -WIDTH:
                temp_coins.append(c)
        self.coins = temp_coins

    def display(self):
    #draws obstacles
        for obs in self.obstacles:
            #obstacle color(purple/blue)
            noStroke()
            # stroke(255,255,255)
            # strokeWeight(3)
            if obs['type'] == 'rect':
                if obs.get('subtype') == 'lava':
                    image(self.lava_img, obs['x'] - game.x_shift, obs['y'], obs['w'], obs['h'])
                elif obs.get('subtype') == 'cube1':
                    image(self.cube1_img, obs['x'] - game.x_shift, obs['y'], obs['w'], obs['h'])
                elif obs.get('subtype') == 'cube2':
                    image(self.cube2_img, obs['x'] - game.x_shift, obs['y'], obs['w'], obs['h'])
                else:
                    image(self.moon_img, obs['x'] - game.x_shift, obs['y'], obs['w'], obs['h'])


                #inner line
                if obs['y'] == 0: 
                    line(obs['x'] - game.x_shift, obs['h'], obs['x'] - game.x_shift + obs['w'], obs['h'])
                else: 
                    line(obs['x'] - game.x_shift, obs['y'], obs['x'] - game.x_shift + obs['w'], obs['y'])
            
            elif obs['type'] == 'triangle_down':
                fill(252, 57, 0) 
                x1, y1 = obs['x'] - game.x_shift, obs['y']
                x2, y2 = obs['x'] - game.x_shift + obs['w'], obs['y']
                x3, y3 = obs['x'] - game.x_shift + obs['w']/2, obs['y'] + obs['h']
                triangle(x1, y1, x2, y2, x3, y3)
                
            elif obs['type'] == 'triangle_up':
                fill(252, 57, 0) 
                x1, y1 = obs['x'] - game.x_shift, obs['y'] + obs['h']
                x2, y2 = obs['x'] - game.x_shift + obs['w'], obs['y'] + obs['h']
                x3, y3 = obs['x'] - game.x_shift + obs['w']/2, obs['y']
                triangle(x1, y1, x2, y2, x3, y3)
    
        #draw coins
        for coin in self.coins:
            if not coin.collected:
                coin.display()
        
        #draw potions
        for potion in self.power_potions:
            if not potion.used:
                potion.display()
            
#coin class
class Coin():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False #used to see collected or not
        self.coin_img = loadImage(PATH + "/images/coin.png")
    def display(self):
        image(self.coin_img, self.x - game.x_shift, self.y, 50, 50)
        
#powerpotion class
class PowerPotion():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.used = False #used to see collected or not
        self.potion_img = loadImage(PATH+"/images/powerpotion.png")
    def display(self):
        image(self.potion_img, self.x - game.x_shift, self.y, 60, 60)
        
class Game:
    def __init__(self):
        self.state = "MENU"
        self.paused = False
        self.selected_level = ""
        self.tunnel = None
        self.distance = 0
        self.spaceship = Spaceship()
        self.coins_collected = 0
        self.invisible = False
        self.invisible_time = 0
        self.level_length = 0 #track level length
        self.game_over_reason = ""
        self.x_shift = 0
        self.w = WIDTH
        self.explosion_sound = player.loadFile(PATH + "/sounds/explosion.mp3")
        self.coin_sound = player.loadFile(PATH + "/sounds/coin.mp3")
        self.potion_sound = player.loadFile(PATH + "/sounds/potion.mp3")
        self.bg_sound = player.loadFile(PATH + "/sounds/background.mp3")
        self.bg_sound.loop()
        self.bg_imgs = []
    

    def start_game(self, level):
        #initializing the tunnel with selected difficulty
        self.state = "PLAYING"
        self.paused = False
        self.selected_level = level
        self.distance = 0
        self.x_shift = 0 
        self.coins_collected = 0
        self.spaceship = Spaceship()

        self.tunnel = Tunnel()

        if level == "EASY":
            self.tunnel.generate_easy_level()
            self.level_length = 1100
        elif level == "MEDIUM":
            self.tunnel.generate_medium_level()
            self.level_length = 1200
        elif level == "HARD":
            self.tunnel.generate_hard_level()
            self.level_length = 1350

    def update(self):
        if self.state == "PLAYING" and not self.paused:
            #update spaceship first
            self.spaceship.update()
            
            #handle world scrolling when spaceship is at middle
            if self.spaceship.x >= WIDTH//2:
                self.x_shift += self.spaceship.vx
                #move tunnel
                self.tunnel.update()
                
                #move trail points
                for point in self.spaceship.trail:
                    point[0] -= self.tunnel.level_speed
                    
            #Increment distance score
            self.distance += self.tunnel.level_speed * 0.1
            
            self.check_coin_collisions()
            self.check_potion_collisions()
            
            if self.check_obstacle_collision():
                self.explosion_sound.rewind()
                self.explosion_sound.play()
                self.state = "GAME_OVER"
                self.game_over_reason = "CRASHED"
                
            
            #check if level completed (win condition)
            if self.distance >= self.level_length:
                self.state = "GAME_OVER"
                self.game_over_reason = "WON"
                
            #update immunity timer
            if self.invisible:
                self.invisible_time -= 1
                if self.invisible_time <= 0:
                    self.invisible = False
        elif self.state == "GAME_OVER":
            pass

    def display(self):
        x_shift = 0
        cnt = 0
        for bg_img in self.bg_imgs:
            if cnt == 0:
                x_shift = game.x_shift//4
            elif cnt == 1:
                x_shift = game.x_shift//3
            elif cnt == 2:
                x_shift = game.x_shift//2
            else:
                x_shift = game.x_shift
            
            
            width_right = x_shift % self.w
            width_left = self.w - width_right
            
            image(bg_img, 0 - width_right, 0)
            image(bg_img, width_left, 0)
            
            cnt += 1
            
        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "PLAYING":
            self.draw_playing()
        elif self.state == "GAME_OVER":
            self.draw_game_over()
        
     #returns if there is collision with rectangle   
    def spaceship_touches_rectangle(self, obs):
        #Spaceship circle center
        ship_x = self.spaceship.x + 25
        ship_y = self.spaceship.y + 25
        ship_radius = self.spaceship.r  #25
        
        #rectangle coordinates
        rect_x = obs['x'] - self.x_shift
        rect_y = obs['y']
        rect_w = obs['w']
        rect_h = obs['h']
        
        #find the closest point on the rectangle to the circle center
        if ship_x < rect_x:
            closest_x = rect_x  #left of rectangle
        elif ship_x > rect_x + rect_w:
            closest_x = rect_x + rect_w  #right of rectangle
        else:
            closest_x = ship_x
        
        #y-axis
        if ship_y < rect_y:
            closest_y = rect_y  #above rectangle
        elif ship_y > rect_y + rect_h:
            closest_y = rect_y + rect_h  #below rectangle
        else:
            closest_y = ship_y
        
        #calculate distance from circle center to closest point
        dx = ship_x - closest_x
        dy = ship_y - closest_y
        distance = math.sqrt(dx*dx + dy*dy)
            
        #collision if distance is less than circle radius
        return distance < ship_radius
        
    #returns if there is collision with downward triangle
    def spaceship_touches_triangle_down(self, obs):
        ship_x = self.spaceship.x + 25
        ship_y = self.spaceship.y + 25
        
        #triangle vertices
        x1 = obs['x'] - self.x_shift
        y1 = obs['y']
        x2 = obs['x'] - self.x_shift + obs['w']
        y2 = obs['y']
        x3 = obs['x'] - self.x_shift + obs['w']/2
        y3 = obs['y'] + obs['h']
        
        return self.point_in_triangle(ship_x, ship_y, x1, y1, x2, y2, x3, y3)
    
    #returns if there is collision with upward triangle:
    def spaceship_touches_triangle_up(self, obs):
        ship_x = self.spaceship.x + 25
        ship_y = self.spaceship.y + 25
        
        #triangle vertices
        x1 = obs['x'] - self.x_shift
        y1 = obs['y'] + obs['h']
        x2 = obs['x'] - self.x_shift + obs['w']
        y2 = obs['y'] + obs['h']
        x3 = obs['x'] - self.x_shift + obs['w']/2
        y3 = obs['y']
        
        return self.point_in_triangle(ship_x, ship_y, x1, y1, x2, y2, x3, y3)
    
    #helper function to find area of triangle
    def triangle_area(self, ax, ay, bx, by, cx, cy):
        #area of triangle using formula
        area = ax*(by - cy) + bx*(cy - ay) + cx*(ay - by)
        return abs(area) / 2
    
    #returns if there is collision or not
    def point_in_triangle(self, px, py, x1, y1, x2, y2, x3, y3):
        #big area
        big_area = self.triangle_area(x1, y1, x2, y2, x3, y3) 
        
        #three small area
        area1 = self.triangle_area(px, py, x2, y2, x3, y3)
        area2 = self.triangle_area(x1, y1, px, py, x3, y3) 
        area3 = self.triangle_area(x1, y1, x2, y2, px, py)
        
        sum_small = area1 + area2 + area3
        
        return abs(big_area - sum_small) < 0.01
    
    #returns coin collision
    def spaceship_touches_coin(self, coin):
        #find center of spaceship
        ship_x = self.spaceship.x + 25
        ship_y = self.spaceship.y + 25
        
        #find center of coin
        #as coins also move with x_shift
        coin_x = coin.x - self.x_shift + 25
        coin_y = coin.y + 25
        
        #calculate distance between center
        dx = ship_x - coin_x
        dy = ship_y - coin_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        #suppose distance less than 25 is touching(looks realistic)
        return distance < 25
    
    #returns spaceship collision with potion
    def spaceship_touches_potion(self, potion):
        #find center of spaceship
        ship_x = self.spaceship.x + 25
        ship_y = self.spaceship.y + 25
        
        #find center of potion
        potion_x = potion.x - self.x_shift + 30
        potion_y = potion.y + 30
        
        #calculate distance
        dx = ship_x - potion_x
        dy = ship_y - potion_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        #suppose distance less than 30 is touching(looks realistic)
        return distance < 30
    
    def check_coin_collisions(self):
        for coin in self.tunnel.coins:
            if not coin.collected:
                if self.spaceship_touches_coin(coin):
                    self.coin_sound.rewind()
                    self.coin_sound.play()
                    coin.collected = True
                    self.coins_collected += 1

    def check_potion_collisions(self):
    #loop through all power potions
        for potion in self.tunnel.power_potions:
            #only check potion that haven't been used
            if not potion.used:
                #check if spaceship touches this potion
                if self.spaceship_touches_potion(potion):
                    self.potion_sound.rewind()
                    self.potion_sound.play()
                    potion.used = True
                    self.activate_invisibility()
                    
   #main function that combines all collision and gives result
    def check_obstacle_collision(self):
        #Check if spaceship hits any obstacle
        #skip collision check if invisible
        if self.invisible:
            return False
        
        for obs in self.tunnel.obstacles:
            #skip obstacles that are far off screen (optimization)
            obs_screen_x = obs['x'] - self.x_shift
            if obs_screen_x < -200 or obs_screen_x > WIDTH + 200:
                continue
            
            collision = False
            
            if obs['type'] == 'rect':
                collision = self.spaceship_touches_rectangle(obs)
            elif obs['type'] == 'triangle_down':
                collision = self.spaceship_touches_triangle_down(obs)
            elif obs['type'] == 'triangle_up':
                collision = self.spaceship_touches_triangle_up(obs)
            
            if collision:
                return True  #collision detected
        
        return False  #no collision

    def activate_invisibility(self):
        self.invisible = True
        self.invisible_time = 300  # 5 seconds at 60 fps
                
    def draw_menu(self):
        fill(255)
        textSize(60)
        textAlign(CENTER)
        text("GRAVITY WAVES", WIDTH / 2, HEIGHT-450)

        textSize(24)
        text("MAIN MENU - Select Your Level", WIDTH / 2, HEIGHT-400)

        self.draw_button(WIDTH/2 - 350, 300, 200, 80, "EASY", color(109, 157, 200))
        self.draw_button(WIDTH/2 - 100, 300, 200, 80, "MEDIUM", color(78, 116, 150))
        self.draw_button(WIDTH/2 + 150, 300, 200, 80, "HARD", color(30,69,106))

        textSize(18)
        fill(0)
        text("Use SPACEBAR to control the spaceship. Dodge lava obstacles. Collect coins.", WIDTH / 2, 450)

    def draw_button(self, x, y, w, h, label, button_color):
        if mouseX > x and mouseX < x + w and mouseY > y and mouseY < y + h:
            noStroke()
            fill(23, 32, 59)
        else:
            noStroke()
            fill(button_color)

        rect(x, y, w, h, 10)

        fill(255)
        textSize(30)
        textAlign(CENTER, CENTER)
        text(label, x + w/2, y + h/2)

    def draw_playing(self):
        self.tunnel.display()
        self.spaceship.display()
        self.draw_ui()

    def draw_ui(self):
        #level
        fill(0,0,0,125)
        strokeWeight(3)
        stroke(255)
        rect(5, 15, 110, 30, 5)
        fill(255)
        textSize(14)
        text("Level: " + self.selected_level, 60, 30)
        
        #distance
        fill(0,0,0,125)
        strokeWeight(3)
        stroke(255)
        rect(120, 15, 140, 30, 5)
        fill(255)
        textSize(14)
        text("Distance: " + str(int(self.distance)) + "m", 185, 30)
        
        #coins
        fill(0,0,0,125)
        strokeWeight(3)
        stroke(255)
        rect(265, 15, 100, 30, 5)
        fill(255)
        textSize(14)
        text("Coins: " + str(self.coins_collected), 315, 30)
        
        #pause
        fill(0,0,0,125)
        strokeWeight(3)
        stroke(255)
        rect(600, 15, 180, 30, 5)
        fill(255)
        textSize(14)
        text("Press N to Pause", 700, 30)
        
        #immunity
        if self.invisible:
            fill(0, 150, 0,125)
            strokeWeight(3)
            stroke(255)
            rect(375, 15, 130, 30, 5)
            fill(255)
            textSize(14)
            text("Immunity: " + str(int(self.invisible_time / 60)) + "s", 440, 30)
        
        if self.paused:
            fill(0, 0, 0,125)
            strokeWeight(3)
            stroke(255)
            rect(WIDTH/2 - 100, HEIGHT/2 - 50, 200, 100, 10)
            fill(255)
            textSize(32)
            text("PAUSED", WIDTH/2, HEIGHT/2 - 10)
            textSize(16)
            text("Press N to Resume", WIDTH/2, HEIGHT/2 + 20)
            
    def draw_game_over(self):
        #still show the game state in background
        self.tunnel.display()
        self.spaceship.display()
        fill(0,0,0, 200)
        noStroke()
        rect(0, 0, WIDTH, HEIGHT)
        if self.game_over_reason == "WON":
            fill(139, 227, 101)
            textSize(72)
            textAlign(CENTER)
            text("LEVEL COMPLETE", WIDTH/2, HEIGHT/2 - 80)
                        
        else:
            #game over text
            fill(255)
            textSize(72)
            textAlign(CENTER)
            text("GAME OVER", WIDTH/2, HEIGHT/2 - 100)
            
            textSize(24)
            text("Distance: " + str(int(self.distance)) + "m", WIDTH/2, HEIGHT/2)
            text("Coins: " + str(self.coins_collected), WIDTH/2, HEIGHT/2 + 40)
        
        #restart button
        noStroke()
        textSize(20)
        self.draw_button(WIDTH/2 - 150, HEIGHT/2 + 100, 300, 60, "RESTART LEVEL", color(78, 116, 150))
        
        textSize(20)
        fill(200)
        text("Click RESTART LEVEL or press R to return to MENU", WIDTH/2, HEIGHT - 50)
                
    def handle_mouse_click(self):
    #check if buttons are clicked
        if self.state == "MENU":
            if WIDTH/2 - 350 < mouseX < WIDTH/2 - 150 and 300 < mouseY < 380:
                self.start_game("EASY")
            elif WIDTH/2 - 100 < mouseX < WIDTH/2 + 100 and 300 < mouseY < 380:
                self.start_game("MEDIUM")
            elif WIDTH/2 + 150 < mouseX < WIDTH/2 + 350 and 300 < mouseY < 380:
                self.start_game("HARD")
        elif self.state == "GAME_OVER":
        #Restart button
            if WIDTH/2 - 150 < mouseX < WIDTH/2 + 150 and HEIGHT/2 + 100 < mouseY < HEIGHT/2 + 160:
                self.start_game(self.selected_level)
game = Game()

def setup():
    size(WIDTH, HEIGHT)
    game.bg_imgs = []
    for i in range(5,3,-1):
        game.bg_imgs.append(loadImage(PATH + "/images/layer_0" + str(i) + ".png"))
    
def draw():
    if game:
        game.update()
        game.display()

def mousePressed():
    if game:
        game.handle_mouse_click()
        
def keyPressed():
    if game and game.state == "PLAYING":
        if key == ' ':
            game.spaceship.space_handler = 1
        elif key == 'r' or key == 'R':
            game.state = "MENU"
        elif key == 'n' or key == 'N':
            game.paused = not game.paused
    elif game and game.state == "GAME_OVER":
        if key == 'r' or key == 'R':
            game.state = "MENU"
            
def keyReleased():
    if game and game.state == "PLAYING":
        if key == ' ':
            game.spaceship.space_handler = -1
            
            
