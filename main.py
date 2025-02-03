from ursina import * #For 3D Rubik
from cube import Rubik, Side
from movimientos import CuboAI, change_values
from interfaz_eleccion import select_colors
import tkinter as tk #For GUI 2D Rubik
from threading import Thread #For tkinter's sub-threads.
import queue #For data processment:)

app = Ursina() #Creation of a ursina object.
rubik_ai = CuboAI() #Creation of a CuboAI object.

# queue for comunicattion between threads.
tk_queue = queue.Queue()

#GLobals variables to controlate Tkinter.
tk_root = None
current_tk_window = None

#Specify the colors of each side
colors = {"U": color.white, "F":color.red, "R": color.blue, "L": color.green, "B": color.orange, "D": color.yellow}
rubik = Rubik(rubik_ai, colors)
#Create three buttons
button_randon = Button("Randomize", parent=camera.ui,position = (-0.2,-0.42), scale = (0.17, 0.06))
solve_button = Button("Solve", parent=camera.ui, position = (0.1, -0.42), scale = (0.13, 0.06))
next_button = Button(">", parent=camera.ui, position= (0.2, -0.42), scale = (0.06, 0.06))
button_import_rubik = Button("Import", parent=camera.ui, position = (0.4, -0.42), scale = (0.13, 0.06))

#An iterator to access to movements_array
iterator = 0
movments_array = []

# Thread for use tkinter w/o block ursina.
def tk_thread():
    global sides
    tk_root = tk.Tk() #Create of a tk object.
    tk_root.withdraw()  #Hide the principal window.

    #Return the colors of the matrices.
    sides = select_colors(tk_root)

    #Sent the data to the queue, so ursina process the data.
    tk_queue.put(sides)

    # Close tkinter.
    tk_root.quit()
    
def process_tk_queue(): #Process the queue
    global rubik, iterator
    while not tk_queue.empty(): #While the queue isn't empty:)
        sides = tk_queue.get() #Return the sides processed to the variable sides.
        rubik_ai.set_sides(sides) #Giving color to the rubik 3D.
        rubik.destroy()
        rubik = Rubik(rubik_ai, colors)
        iterator = 0

def import_rubik(): #Import the thread
    thread = Thread(target=tk_thread, daemon=True)
    thread.start() #Start the secundary-thread:)
    
#Add processment of the queue per frame
def update():
    process_tk_queue()

#Randomize event
def random_rubik():
    global iterator
    global rubik
    rubik_ai.randomize()
    rubik.destroy()
    rubik = Rubik(rubik_ai, colors)
    rubik.front_center.square.input = spin
    iterator = 0

def disable_button():
    next_button.enabled = True

def next_event():
    global iterator
    #if lenght og movments_array doesn´t have any element, is because there aren´t solutions, and if iterator is greater than length of
    #movments_array, that means it finished to do the movements
    if len(movments_array) > 0 and iterator<len(movments_array):
        solve(movments_array[iterator])
        iterator += 1
        next_button.enabled = False
        invoke(disable_button, delay = 0.2)

#Function that is called if we click in solve button
def solve_event():
    global iterator 
    global movments_array
    iterator = 0
    movimientos = rubik_ai.solve()
    movments_array = change_values(movimientos.split())
    print(movments_array)
 

#function that allow us to rotate the cube depending the side that we click
def spin(key):
    if mouse.hovered_entity == rubik.front_center.square:
        if key == "left mouse down":
           rubik.rotate(Side.FRONT, -1, 0.2) 
           rubik_ai.F_prima()
        elif key == "right mouse down":
            rubik.rotate(Side.FRONT, 1, 0.2)
            rubik_ai.F()
    elif mouse.hovered_entity == rubik.back_center.square:
        if key == "left mouse down":
           rubik.rotate(Side.BACK, 1, 0.2) 
           rubik_ai.B_prima()
        elif key == "right mouse down":
            rubik.rotate(Side.BACK, -1, 0.2)
            rubik_ai.B()
    elif mouse.hovered_entity == rubik.top_center.square:
        if key == "left mouse down":
            rubik.rotate(Side.TOP, -1, 0.2)
            rubik_ai.U_prima()
        elif key =="right mouse down":
            rubik.rotate(Side.TOP, 1, 0.2)
            rubik_ai.U()
    elif mouse.hovered_entity == rubik.bottom_center.square:
        if key == "left mouse down":
            rubik.rotate(Side.BOTTOM, 1, 0.2)
            rubik_ai.D_prima()
        elif key == "right mouse down":
            rubik.rotate(Side.BOTTOM, -1, 0.2)
            rubik_ai.D() 
    elif mouse.hovered_entity == rubik.right_center.square:
        if key == "left mouse down":
            rubik.rotate(Side.RIGHT, -1, 0.2)
            rubik_ai.R_prima()
        if key == "right mouse down":
            rubik.rotate(Side.RIGHT, 1, 0.2)
            rubik_ai.R()
    elif mouse.hovered_entity == rubik.left_center.square:
        if key == "left mouse down":
            rubik.rotate(Side.LEFT, 1, 0.2)
            rubik_ai.L_prima()
        if key == "right mouse down":
            rubik.rotate(Side.LEFT, -1, 0.2)
            rubik_ai.L()
    
        
    rubik_ai.mostrar_cubo()
    print()


def solve(mov):
        if mov == "U":
            rubik.rotate(Side.TOP, 1, 0.2)
            rubik_ai.U()
        elif mov == "U'":
            rubik.rotate(Side.TOP, -1, 0.2)
            rubik_ai.U_prima()
        elif mov== "R":
            rubik.rotate(Side.RIGHT, 1, 0.2)
            rubik_ai.R()
        elif mov== "R'":
            rubik.rotate(Side.RIGHT, -1, 0.2)
            rubik_ai.R_prima()
        elif mov== "L":
            rubik.rotate(Side.LEFT, -1, 0.2)
            rubik_ai.L()
        elif mov == "L'":
            rubik.rotate(Side.LEFT, 1, 0.2)
            rubik_ai.L_prima()
        elif mov == "F":
            rubik.rotate(Side.FRONT, 1, 0.2)
            rubik_ai.F()
        elif mov == "F'":
           rubik.rotate(Side.FRONT, -1, 0.2) 
           rubik_ai.F_prima()
        elif mov == "B":
            rubik.rotate(Side.BACK, -1, 0.2)
            rubik_ai.B()
        elif mov == "B'":
           rubik.rotate(Side.BACK, 1, 0.2) 
           rubik_ai.B_prima()
        elif mov == "D":
            rubik.rotate(Side.BOTTOM, -1, 0.2)
            rubik_ai.D() 
        elif mov == "D'":
            rubik.rotate(Side.BOTTOM, 1, 0.2)
            rubik_ai.D_prima()


button_randon._on_click = random_rubik
solve_button._on_click = solve_event
next_button._on_click = next_event
button_import_rubik._on_click = import_rubik
rubik.front_center.square.input = spin


EditorCamera()  # add camera controls for orbiting and moving the camera
app.run()