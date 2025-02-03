import kociemba
import random

def reverse_matrix(matrix):
    matrix_reversed = []
    for i in range(len(matrix)):
        matrix_reversed.append(matrix[-1-i][::-1])
    return matrix_reversed

def change_values(array: list[str]):
    aux_array =[]
    for i in range(len(array)):
        if array[i][-1] == "2":
            for j in range (2):
                aux_array.append(array[i][:-1])
        else:
            aux_array.append(array[i])

    print(aux_array)
    return aux_array

class CuboAI:
    def __init__(self): #Propiedades del cubo (caras)
        self.front = [["F"] * 3 for _ in range(3)] #Blanco
        self.back = [["B"] * 3 for _ in range(3)] #Naranja
        self.left = [["L"] * 3 for _ in range(3)] #Verde
        self.right = [["R"] * 3 for _ in range(3)] #Azul
        self.up = [["U"] * 3 for _ in range(3)] #Blanco
        self.down = [["D"] * 3 for _ in range(3)] #Amarillo
        self.functions = []
        self.functions.append(self.U)
        self.functions.append(self.U_prima)
        self.functions.append(self.F)
        self.functions.append(self.F_prima)
        self.functions.append(self.B)
        self.functions.append(self.B_prima)
        self.functions.append(self.D)
        self.functions.append(self.D_prima)
        self.functions.append(self.L)
        self.functions.append(self.L_prima)
        self.functions.append(self.R)
        self.functions.append(self.R_prima)



    def set_sides(self, sides):
        self.up = sides[0]
        self.front = sides[1]
        self.right = sides[2]
        self.left = sides[3]
        self.back = sides[4]
        self.down = sides[5]



    def randomize(self):
        for i in range(50):
            self.functions[random.randint(0, 11)]()




    def mostrar_cubo(self): #Mostrar cada cara del cubo en forma de matrices.
        print("Cara U (Centro blanco):")
        for fila in self.up:
            print(fila)
        print("Cara F (Centro rojo):")
        for fila in self.front:
            print(fila)
        print("Cara R (Centro azul):")
        for fila in self.right:
            print(fila)
        print("Cara L (Centro verde):")
        for fila in self.left:
            print(fila)
        print("Cara B (centro naranja):")
        for fila in self.back:
            print(fila)
        print("Cara Low (Centro amarillo):")
        for fila in self.down:
            print(fila)


    def solve(self):
        s = self.toString()
        print(s)
        solution = kociemba.solve(s)
        print(solution)
        return kociemba.solve(self.toString())

    def toString(self):
        rubik_str = ""
        rubik_str += self.sideToStr(self.up)
        rubik_str += self.sideToStr(self.right)
        rubik_str += self.sideToStr(self.front)
        rubik_str += self.sideToStr(reverse_matrix(self.down))
        rubik_str += self.sideToStr(self.left)
        rubik_str += self.sideToStr(self.back)

        return rubik_str

    def sideToStr(self, side):
        side_str:str = ""
        for i in range(3):
            for j in range(3):
               side_str +=side[i][j]
        return side_str




    def U(self): #Movimiento up horario.
        self.up = girar_cara(self.up) #Girar la cara en sentido horario.
        #[:] Crea una copia, no reescribe:)
        front_row = self.front[0][:] #Guardar la fila (0) del front para cuando se se reescriba:)
        self.front[0] = self.right[0][:] #Reescribiendo las filas que se mueven.
        self.right[0] = self.back[0][:]
        self.back[0] = self.left[0][:]
        self.left[0] = front_row
    def U_prima(self): #Movimiento up anti-horario.

        self.up = girar_antihorario(self.up) #Girar la cara en sentido anti-horario.
        front_row = self.front[0][:] #Reescribiendo las filas que se mueven.
        self.front[0] = self.left[0][:]
        self.left[0] = self.back[0][:]
        self.back[0] = self.right[0][:]
        self.right[0] = front_row

    def F(self): #Movimiento front horario.
        self.front = girar_cara(self.front) #Girar la cara f de forma horario.
        up_row = self.up[2][:] #Guardando las filas y columnas a mover:)
        right_col = [self.right[i][0] for i in range(3)]
        down_row = self.down[2][:]
        left_col = [self.left[i][2] for i in range(3)]
        
        down_row = down_row[::-1] #Reverseando fila que se inserta al reves:)

        # Actualizar las filas.
        self.up[2] = left_col[::-1]
        self.down[2] = right_col
        for i in range(3):
            self.right[i][0] = up_row[i] 
            self.left[i][2] = down_row[i]

    def F_prima(self): #Movimiento front anti-horario.
        self.front = girar_antihorario(self.front)  #Girar la cara f de forma anti-horario.
        up_row = self.up[2][:] #Guardando filas y columnas a mover.
        right_col = [self.right[i][0] for i in range(3)]
        down_row = self.down[2][:]
        left_col = [self.left[i][2] for i in range(3)]

        #Reverseando fila que se inserta mal.
        up_row = up_row[::-1]

        #Actualizando las filas.
        self.up[2] = right_col
        self.down[2] = left_col[::-1]
        for i in range(3):
            self.right[i][0] = down_row[i]
            self.left[i][2] = up_row[i]

    def R(self): #Movimiento right horario.
        self.right = girar_cara(self.right) 
        up_col = [self.up[i][2] for i in range(3)]
        front_col = [self.front[i][2] for i in range(3)]
        back_col = [self.back[i][0] for i in range(3)]
        down_col = [self.down[i][0] for i in range(3)]

        #Reverseando filas que se insertan al reves.
        up_col,down_col = reverse_col(up_col,down_col)

        for i in range(3):
            self.up[i][2] = front_col[i]
            self.back[i][0] = up_col[i]
            self.down[i][0] = back_col[i]
            self.front[i][2] = down_col[i]

    def R_prima(self): #Movimiento right anti-horario.
        self.right = girar_antihorario(self.right)
        up_col = [self.up[i][2] for i in range(3)]
        front_col = [self.front[i][2] for i in range(3)]
        back_col = [self.back[i][0] for i in range(3)]
        down_col = [self.down[i][0] for i in range(3)]

        front_col,back_col = reverse_col(front_col,back_col)
        
        for i in range(3):
            self.up[i][2] = back_col[i]
            self.back[i][0] = down_col[i]
            self.down[i][0] = front_col[i]
            self.front[i][2] = up_col[i]
            
    def L(self): #Movimiento left horario.
        self.left = girar_cara(self.left)
        up_col = [self.up[i][0] for i in range(3)]
        front_col = [self.front[i][0] for i in range(3)]
        down_col = [self.down[i][2] for i in range(3)]
        back_col = [self.back[i][2] for i in range(3)]
        
        front_col,back_col = reverse_col(front_col,back_col)
        
        for i in range(3):
            self.up[i][0] = back_col[i]
            self.back[i][2] = down_col[i]
            self.down[i][2] = front_col[i]
            self.front[i][0] = up_col[i]
            
    def L_prima(self): #Movimiento left anti-horario.
        self.left = girar_antihorario(self.left)
        up_col = [self.up[i][0] for i in range(3)]
        front_col = [self.front[i][0] for i in range(3)]
        down_col = [self.down[i][2] for i in range(3)]
        back_col = [self.back[i][2] for i in range(3)]
        
        up_col,down_col = reverse_col(up_col,down_col)
        
        for i in range(3):
            self.up[i][0] = front_col[i]
            self.front[i][0] = down_col[i]
            self.down[i][2] = back_col[i]
            self.back[i][2] = up_col[i]
            
    def B(self): #Movimiento back horario.
        self.back = girar_cara(self.back)
        up_row = self.up[0][:]
        right_col = [self.right[i][2] for i in range(3)]
        left_col = [self.left[i][0] for i in range(3)]
        down_row = self.down[0][:]
        
        up_row,left_col = reverse_col(up_row,left_col)
        
        self.up[0] = right_col
        self.down[0] = left_col
        for i in range(3):
            self.right[i][2] = down_row[i]
            self.left[i][0] = up_row[i]
            
    def B_prima(self): #Movimiento back anti-horario.
        self.back = girar_antihorario(self.back)
        up_row = self.up[0][:]
        right_col = [self.right[i][2] for i in range(3)]
        left_col = [self.left[i][0] for i in range(3)]
        down_row = self.down[0][:]
        
        left_col,down_row = reverse_col(left_col,down_row)
        
        self.up[0] = left_col
        self.down[0] = right_col
        for i in range(3):
            self.right[i][2] = up_row[i]
            self.left[i][0] = down_row[i]
            
    def D(self): #Movimiento down horario.
        self.down = girar_cara(self.down)
        front_row = self.front[2][:]
        self.front[2] = self.left[2][:]
        self.left[2] = self.back[2][:]
        self.back[2] = self.right[2][:]
        self.right[2] = front_row
        
    def D_prima(self): #Movimiento down anti-horario.
        self.down =girar_antihorario(self.down)
        front_row = self.front[2][:]
        self.front[2] = self.right[2][:]
        self.right[2] = self.back[2][:]
        self.back[2] = self.left[2][:]
        self.left[2] = front_row
    
def girar_cara(cara): #Funcion girar cara de forma horario.
    cara[:] = [list(reversed(col)) for col in zip(*cara)] #[:] Crea una copia de la lista:)
    return cara
        
def girar_antihorario(cara): #Funcion girar cara de forma anti-horario.
    cara[:] = [list(reversed(col)) for col in cara]
    cara = [list(col) for col in zip(*cara)]
    return cara

def reverse_col(columna1,columna2): #Funcion reversear columnas que se insertan mal [1,2,3] -> [3,2,1]
    columna1 = columna1[::-1]
    columna2 = columna2[::-1]
    return columna1,columna2