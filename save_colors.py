class CuboColores: 
    def __init__(self): #Propiedades del cubo (caras) Matrices vacias para guardar las caras.
        self.front = [[""] * 3 for _ in range(3)] #Blanco
        self.back = [[""] * 3 for _ in range(3)] #Naranja
        self.left = [[""] * 3 for _ in range(3)] #Verde
        self.right = [[""] * 3 for _ in range(3)] #Azul
        self.up = [[""] * 3 for _ in range(3)] #Blanco
        self.down = [[""] * 3 for _ in range(3)] #Amarillo
        self.front[1][1] = "F"
        self.back[1][1] = "B"
        self.left[1][1] = "L" 
        self.right[1][1] = "R"
        self.up[1][1] = "U"
        self.down[1][1] = "D"
        
    def actualizar_matriz(self, cara, fila, columna, color): #Actualiza el color de la cara correspondiente en la fila y columna correespondientes.
        if color == "white": #Cambia los nombres de los colores por movimientos.
            mov = "U"
        elif color == "red":
            mov = "F"
        elif color == "blue":
            mov = "R"
        elif color == "green":
            mov = "L"
        elif color == "orange":
            mov = "B"
        elif color == "yellow":
            mov = "D"
            
        if cara == 1:
            self.front[fila][columna] = mov
        elif cara == 4:
            self.back[fila][columna] = mov
        elif cara == 3:
            self.left[fila][columna] = mov
        elif cara == 2:
            self.right[fila][columna] = mov
        elif cara == 0:
            self.up[fila][columna] = mov
        elif cara == 5:
            self.down[fila][columna] = mov
            
    def obtener_caras(self): #Mostrar cada cara del cubo en forma de matrices.
        return [self.up,self.front,self.right,self.left,self.back,self.down]
            