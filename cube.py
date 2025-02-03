from time import sleep
from movimientos import CuboAI
from ursina import *
from enum import Enum
import random

class Side(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    FRONT = 4
    BACK = 5

class Cube():
    def __init__(self,paren ,pos , top = False, bottom = False, right = False, left = False,front = False, back = False, color_top = None, color_down = None, color_left = None, color_right = None, color_back = None, color_front = None ):
        self.square = Entity(model = "cube", color = color.black,collider = "box", parent = paren, position = pos)
        self.colors = []
        
        if top:
            self.top = Entity(model= "side", position = (0,0.5,0), color = color_top, scale = 0.5, parent = self.square)
            self.colors.append(self.top)
        if bottom:
            self.bottom = Entity(model= "side", position = (0,-0.5,0), color = color_down, scale = 0.5, parent = self.square)
            self.colors.append(self.bottom)
        if front:
            self.fron = Entity(model = "side", position = (0,0,-0.5), color = color_front, scale = 0.5, rotation_x = 90,parent = self.square)
            self.colors.append(self.fron)
        if back:
            self.back =  Entity(model = "side", position = (0,0,0.5), color = color_back, scale = 0.5, rotation_x = 90,parent = self.square)
            self.colors.append(self.back)
        if left:
            self.left = Entity(model = "side", position = (-0.5,0,0), color = color_left, scale = 0.5, rotation_z = 90,parent = self.square)
            self.colors.append(self.left)
        if right:
            self.right = Entity(model = "side", position = (0.5,0,0), color = color_right, scale = 0.5, rotation_z = 90,parent = self.square)
            self.colors.append(self.right)

    #Destroy cube
    def destroy(self):
        for color in self.colors:
            destroy(color)
        destroy(self.square)

class Rubik():
    def __init__(self, rubik_ai: CuboAI , colors: dict):
        front_p = rubik_ai.front
        down_p= rubik_ai.down
        left_p = rubik_ai.left
        right_p = rubik_ai.right
        back_p = rubik_ai.back
        top_p = rubik_ai.up


        self.rubik_pieces = [[[],[],[]],[[],[],[]],[[],[],[]]]
        #Create the centre
        self.centre:Entity = Entity(model='cube', color=hsv(201,34,3), scale=1, collider='box')
        #Create the models , and adds it into an array
        self.rubik_pieces[0][0].append(Cube(self.centre,pos = (-1,1,-1), top=True, left=True, front=True, color_top=colors[top_p[2][0]], color_front=colors[front_p[0][0]], color_left=colors[left_p[0][2]]))
        self.rubik_pieces[0][0].append(Cube(self.centre,pos = (-1,1,0), top=True, left=True, color_top=colors[top_p[1][0]], color_left = colors[left_p[0][1]]))
        self.rubik_pieces[0][0].append(Cube(self.centre,pos = (-1,1,1), top=True, left=True, back=True, color_top = colors[top_p[0][0]], color_left=colors[left_p[0][0]], color_back=colors[back_p[0][2]]))

        self.rubik_pieces[0][1].append(Cube(self.centre,pos = (0,1,-1), top=True, front = True, color_top=colors[top_p[2][1]], color_front = colors[front_p[0][1]]))
        self.rubik_pieces[0][1].append(Cube(self.centre,pos = (0,1,0), top=True, color_top = colors[top_p[1][1]]))
        self.rubik_pieces[0][1].append(Cube(self.centre,pos = (0,1,1), top=True, back = True , color_top=colors[top_p[0][1]], color_back=colors[back_p[0][1]]))

        self.rubik_pieces[0][2].append(Cube(self.centre,pos = (1,1,-1), top=True, right = True, front=True, color_top = colors[top_p[2][2]], color_right=colors[right_p[0][0]], color_front=colors[front_p[0][2]] ))
        self.rubik_pieces[0][2].append(Cube(self.centre,pos = (1,1,0), top=True, right = True, color_top=colors[top_p[1][2]], color_right=colors[right_p[0][1]] ))
        self.rubik_pieces[0][2].append(Cube(self.centre,pos = (1,1,1), top=True, back = True, right=True, color_top = colors[top_p[0][2]], color_back = colors[back_p[0][0]], color_right=colors[right_p[0][2]]))

        self.rubik_pieces[1][0].append(Cube(self.centre,pos = (-1,0,-1),  left = True, front=True , color_left= colors[left_p[1][2]], color_front=colors[front_p[1][0]]))
        self.rubik_pieces[1][0].append(Cube(self.centre,pos = (-1,0,0),  left=True, color_left=colors[left_p[1][1]] ))
        self.rubik_pieces[1][0].append(Cube(self.centre,pos = (-1,0,1),  back = True, left=True, color_back = colors[back_p[1][2]], color_left=colors[left_p[1][0]] ))

        self.rubik_pieces[1][1].append(Cube(self.centre,pos = (0,0,-1), front=True, color_front=colors[front_p[1][1]] ))
        self.rubik_pieces[1][1].append(self.centre)
        self.rubik_pieces[1][1].append(Cube(self.centre,pos = (0,0,1),  back=True, color_back = colors[back_p[1][1]] ))

        self.rubik_pieces[1][2].append(Cube(self.centre, (1,0,-1), front=True, right=True, color_front=colors[front_p[1][2]], color_right=colors[right_p[1][0]]))
        self.rubik_pieces[1][2].append(Cube(self.centre, (1,0,0),  right=True, color_right=colors[right_p[1][1]]))
        self.rubik_pieces[1][2].append(Cube(self.centre, (1,0,1), right=True, back=True, color_right= colors[right_p[1][2]], color_back=colors[back_p[1][0]]))

        self.rubik_pieces[2][0].append(Cube(self.centre, (-1,-1,-1), left=True, bottom=True, front=True,color_left=colors[left_p[2][2]], color_down=colors[down_p[2][2]], color_front=colors[front_p[2][0]] ))
        self.rubik_pieces[2][0].append(Cube(self.centre, (-1,-1,0), left=True, bottom=True, color_left=colors[left_p[2][1]], color_down=colors[down_p[1][2]]))
        self.rubik_pieces[2][0].append(Cube(self.centre, (-1,-1,1), back=True, bottom=True, left=True, color_back=colors[back_p[2][2]], color_down=colors[down_p[0][2]], color_left=colors[left_p[2][0]]))

        self.rubik_pieces[2][1].append(Cube(self.centre, (0,-1,-1),  bottom=True, front=True, color_down= colors[down_p[2][1]], color_front=colors[front_p[2][1]]))
        self.rubik_pieces[2][1].append(Cube(self.centre, (0,-1,0), bottom=True, color_down=colors[down_p[1][1]]))
        self.rubik_pieces[2][1].append(Cube(self.centre, (0,-1,1),  bottom=True, back=True, color_down=colors[down_p[0][1]], color_back=colors[back_p[2][1]]))

        self.rubik_pieces[2][2].append(Cube(self.centre, (1,-1,-1),  bottom=True, front=True, right=True, color_down=colors[down_p[2][0]], color_front=colors[front_p[2][2]], color_right=colors[right_p[2][0]]))
        self.rubik_pieces[2][2].append(Cube(self.centre, (1,-1,0), right=True, bottom=True, color_right=colors[right_p[2][1]], color_down=colors[down_p[1][0]]))
        self.rubik_pieces[2][2].append(Cube(self.centre, (1,-1,1), right=True, bottom=True, back = True, color_right= colors[right_p[2][2]], color_down=colors[down_p[0][0]], color_back=colors[back_p[2][0]]))

        #Save centers on variables for an easy access 
        self.front_center = self.rubik_pieces[1][1][0]
        self.top_center = self.rubik_pieces[0][1][1]
        self.left_center = self.rubik_pieces[1][0][1]
        self.right_center = self.rubik_pieces[1][2][1]
        self.back_center = self.rubik_pieces[1][1][2]
        self.bottom_center = self.rubik_pieces[2][1][1] 
    
    def disable(self, value: bool): #Disabel hover in all centers
        self.top_center.square.ignore = value
        self.bottom_center.square.ignore = value
        self.right_center.square.ignore = value
        self.left_center.square.ignore = value
        self.front_center.square.ignore = value
        self.back_center.square.ignore = value


    def rotate(self, side: int, dir: int, dur): #rotate a side passed by argument
        if side == Side.TOP or side == Side.BOTTOM:
            #Change the parent
            self.set_parent_top_or_bottom(side)
            #Animate
            self.animate(side, dir, dur)
            #Exchange positions
            self.exchange_squads_top_or_bottom(side, dir)
        elif side == Side.FRONT or side == Side.BACK:
            self.set_parent_front_or_back(side)
            self.animate(side, dir, dur)
            self.exchange_squads_front_back(side, dir)
        elif side == Side.RIGHT or side == Side.LEFT:
            self.set_parent_right_or_left(side)
            self.animate(side, dir, dur)
            self.exchange_squads_right_left(side, dir)

    def set_parent(self,side : int):#Set a parent depending the side that we wanna rotate
        if side == Side.FRONT or side == Side.BACK:
            self.set_parent_front_or_back(side)
        elif side == Side.BOTTOM or side == Side.TOP:
            self.set_parent_top_or_bottom(side)
        elif side == Side.RIGHT or side == Side.LEFT:
            self.set_parent_right_or_left(side)

    def destroy(self): #Destroy all models of the rubik cube
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if i==1 and j == 1 and k == 1:
                        #if is in the center we use the normal function destroy because that model is not an object Cube, is an Entity provided by Ursina
                        destroy(self.rubik_pieces[i][j][k])
                    else:
                        self.rubik_pieces[i][j][k].destroy()

    def set_parent_right_or_left(self,side: int):#Set the parent to the sides, right or left, in order to be able to rotate the center
        # and that all children follow the movment 
        if side == Side.RIGHT:
            index_side = 2
            parent = self.right_center
        else:
            index_side = 0
            parent = self.left_center

        for j in range(3):
            for k in range(3):
                if self.rubik_pieces[j][index_side][k] != parent: 
                    #get the current position
                    aux_pos =self.rubik_pieces[j][index_side][k].square.world_position
                    aux_pos_colors = []
                    aux_rot_colors = []

                    #Save the currect position of the colors models
                    for color in self.rubik_pieces[j][index_side][k].colors:
                       aux_pos_colors.append(color.world_position) 
                       aux_rot_colors.append(color.world_rotation)

                    #Change the parent
                    self.rubik_pieces[j][index_side][k].square.parent = parent.square
                    #Set again the position
                    self.rubik_pieces[j][index_side][k].square.world_position = aux_pos

                    #Set again the position of the colors models
                    for i in range(len(aux_pos_colors)):
                        self.rubik_pieces[j][index_side][k].colors[i].world_position = aux_pos_colors[i]
                        self.rubik_pieces[j][index_side][k].colors[i].world_rotation = aux_rot_colors[i]



    def set_parent_top_or_bottom(self, side:int):#Set the parent to the sides, top or bottom, in order to be able to rotate the center
        # and that all children follow the movment
        if side == Side.TOP:
            index_side = 0
            parent = self.top_center
        else: 
            index_side = 2
            parent = self.bottom_center

        for j in range(3):
            for k in range(3):
                if self.rubik_pieces[index_side][j][k] != parent: 
                    #get the current position
                    aux_pos =self.rubik_pieces[index_side][j][k].square.world_position
                    aux_pos_colors = []
                    aux_rot_colors = []
                    for color in self.rubik_pieces[index_side][j][k].colors:
                       aux_pos_colors.append(color.world_position) 
                       aux_rot_colors.append(color.world_rotation)

                    #Change the parent
                    self.rubik_pieces[index_side][j][k].square.parent = parent.square
                    #Set again the position
                    self.rubik_pieces[index_side][j][k].square.world_position = aux_pos

                    for i in range(len(aux_pos_colors)):
                        self.rubik_pieces[index_side][j][k].colors[i].world_position = aux_pos_colors[i]
                        self.rubik_pieces[index_side][j][k].colors[i].world_rotation = aux_rot_colors[i]

    def set_parent_front_or_back(self, side:int):#Set the parent to the sides, front or back, in order to be able to rotate the center
        # and that all children follow the movment
        if side == Side.FRONT:
            index_side = 0
            parent = self.front_center
        else: 
            print("back")
            index_side = 2
            parent = self.back_center

        for i in range(3):
            for k in range(3):
                if self.rubik_pieces[k][i][index_side] != parent: 
                    #get the current position
                    aux_pos =self.rubik_pieces[k][i][index_side].square.world_position
                    aux_pos_colors = []
                    aux_rot_colors = []
                    for color in self.rubik_pieces[k][i][index_side].colors:
                       aux_pos_colors.append(color.world_position) 
                       aux_rot_colors.append(color.world_rotation)

                   #Change the parent
                    self.rubik_pieces[k][i][index_side].square.parent = parent.square                    #Set again the position
                    self.rubik_pieces[k][i][index_side].square.world_position = aux_pos
                    for j in range(len(aux_pos_colors)):
                        self.rubik_pieces[k][i][index_side].colors[j].world_position = aux_pos_colors[j]
                        self.rubik_pieces[k][i][index_side].colors[j].world_rotation = aux_rot_colors[j]

    def exchange_squads_right_left(self, side: int, dir):#Exchange positions in the sides right or left of the rubik_pieces when a side is rotated
        index_side = 0 if side == Side.LEFT else 2
        if dir == -1:
            aux = self.rubik_pieces[0][index_side][2]
            self.rubik_pieces[0][index_side][2] = self.rubik_pieces[2][index_side][2] 
            self.rubik_pieces[2][index_side][2] = self.rubik_pieces[2][index_side][0]
            self.rubik_pieces[2][index_side][0] = self.rubik_pieces[0][index_side][0]
            self.rubik_pieces[0][index_side][0] = aux

            aux = self.rubik_pieces[0][index_side][1] 
            self.rubik_pieces[0][index_side][1] = self.rubik_pieces[1][index_side][2] 
            self.rubik_pieces[1][index_side][2] = self.rubik_pieces[2][index_side][1]
            self.rubik_pieces[2][index_side][1] = self.rubik_pieces[1][index_side][0]
            self.rubik_pieces[1][index_side][0] = aux
        elif dir == 1:
            aux = self.rubik_pieces[0][index_side][2]
            self.rubik_pieces[0][index_side][2] = self.rubik_pieces[0][index_side][0] 
            self.rubik_pieces[0][index_side][0] = self.rubik_pieces[2][index_side][0]
            self.rubik_pieces[2][index_side][0] = self.rubik_pieces[2][index_side][2]
            self.rubik_pieces[2][index_side][2] = aux

            aux = self.rubik_pieces[0][index_side][1] 
            self.rubik_pieces[0][index_side][1] = self.rubik_pieces[1][index_side][0] 
            self.rubik_pieces[1][index_side][0] = self.rubik_pieces[2][index_side][1]
            self.rubik_pieces[2][index_side][1] = self.rubik_pieces[1][index_side][2]
            self.rubik_pieces[1][index_side][2] = aux

    def exchange_squads_front_back(self, side: int, dir):#Exchange positions in the sides front or back of the rubik_pieces when a side is rotated

        index_side = 0 if side == Side.FRONT else 2
        if dir == -1:
            aux = self.rubik_pieces[0][2][index_side]
            self.rubik_pieces[0][2][index_side] = self.rubik_pieces[2][2][index_side]
            self.rubik_pieces[2][2][index_side] = self.rubik_pieces[2][0][index_side]
            self.rubik_pieces[2][0][index_side] = self.rubik_pieces[0][0][index_side]
            self.rubik_pieces[0][0][index_side] = aux 
            aux = self.rubik_pieces[0][1][index_side]
            self.rubik_pieces[0][1][index_side] = self.rubik_pieces[1][2][index_side]
            self.rubik_pieces[1][2][index_side] = self.rubik_pieces[2][1][index_side]
            self.rubik_pieces[2][1][index_side] = self.rubik_pieces[1][0][index_side]
            self.rubik_pieces[1][0][index_side] = aux 
        elif dir == 1: 
            aux = self.rubik_pieces[0][2][index_side]
            self.rubik_pieces[0][2][index_side] = self.rubik_pieces[0][0][index_side]
            self.rubik_pieces[0][0][index_side] = self.rubik_pieces[2][0][index_side]
            self.rubik_pieces[2][0][index_side] = self.rubik_pieces[2][2][index_side]
            self.rubik_pieces[2][2][index_side] = aux 
            aux = self.rubik_pieces[0][1][index_side]
            self.rubik_pieces[0][1][index_side] = self.rubik_pieces[1][0][index_side]
            self.rubik_pieces[1][0][index_side] = self.rubik_pieces[2][1][index_side]
            self.rubik_pieces[2][1][index_side] = self.rubik_pieces[1][2][index_side]
            self.rubik_pieces[1][2][index_side] = aux 

    def exchange_squads_top_or_bottom(self, side:int, dir):#Exchange positions in the sides front or back of the rubik_pieces when a side is rotated

        index_side = 0 if side == Side.TOP else 2
        if dir == 1:
            aux = self.rubik_pieces[index_side][2][0]
            self.rubik_pieces[index_side][2][0] = self.rubik_pieces[index_side][2][2]
            self.rubik_pieces[index_side][2][2] = self.rubik_pieces[index_side][0][2]
            self.rubik_pieces[index_side][0][2] = self.rubik_pieces[index_side][0][0]
            self.rubik_pieces[index_side][0][0] = aux
            aux = self.rubik_pieces[index_side][1][0]
            self.rubik_pieces[index_side][1][0] = self.rubik_pieces[index_side][2][1]
            self.rubik_pieces[index_side][2][1] = self.rubik_pieces[index_side][1][2]
            self.rubik_pieces[index_side][1][2] = self.rubik_pieces[index_side][0][1]
            self.rubik_pieces[index_side][0][1] = aux
        elif dir == -1:
            aux = self.rubik_pieces[index_side][2][0]
            self.rubik_pieces[index_side][2][0] = self.rubik_pieces[index_side][0][0]
            self.rubik_pieces[index_side][0][0] = self.rubik_pieces[index_side][0][2]
            self.rubik_pieces[index_side][0][2] = self.rubik_pieces[index_side][2][2]
            self.rubik_pieces[index_side][2][2] = aux
            aux = self.rubik_pieces[index_side][1][0]
            self.rubik_pieces[index_side][1][0] = self.rubik_pieces[index_side][0][1]
            self.rubik_pieces[index_side][0][1] = self.rubik_pieces[index_side][1][2]
            self.rubik_pieces[index_side][1][2] = self.rubik_pieces[index_side][2][1]
            self.rubik_pieces[index_side][2][1] = aux




    def animate(self,side: int, direction, dur): #Animate the a side that is passed by argument
        if side == Side.TOP:
            self.top_center.square.animate("rotation_y", self.top_center.square.rotation_y + 90*direction, duration = dur, curve = curve.in_out_expo)
        elif side == Side.BOTTOM:
            self.bottom_center.square.animate("rotation_y", self.bottom_center.square.rotation_y + 90*direction, duration = dur, curve = curve.in_out_expo)
        elif side == Side.FRONT:
            self.front_center.square.animate("rotation_z", self.front_center.square.rotation_z + 90 * direction, duration = dur, curve = curve.in_out_expo )
        elif side == Side.BACK:
            self.back_center.square.animate("rotation_z", self.back_center.square.rotation_z + 90 * direction, duration = dur, curve = curve.in_out_expo )
        elif side == Side.RIGHT:
            self.right_center.square.animate("rotation_x", self.right_center.square.rotation_x + 90 * direction, duration = dur, curve = curve.in_out_expo )
        elif side == Side.LEFT:
            self.left_center.square.animate("rotation_x", self.left_center.square.rotation_x + 90 * direction, duration = dur, curve = curve.in_out_expo )
        self.disable(True)
        invoke(self.disable, False,delay = dur)