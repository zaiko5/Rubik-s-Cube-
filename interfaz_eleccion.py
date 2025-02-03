import tkinter as tk
from save_colors import CuboColores
#import threading

# Generales.
def crear_frame(ventana): #Crear unn frame para cualquier cosa xd.
    frame = tk.Frame(ventana)
    frame.pack(pady=(30, 0))  # Tendrán un padding en Y de 30px.
    return frame


def botones_cubo(frame): #Crear los botones del cubo.
    colores_centro = ["white", "red", "blue", "green", "orange", "yellow"]  # Colores a poner en el centro
    botones = [[tk.Button(frame, width=11, height=5, bg="gray", bd=5) for j in range(3)] for i in range(3)]  # Creando los botones.
    
    for i, fila in enumerate(botones):
        for j, boton in enumerate(fila):
            # Si estamos en el centro de la cara, cambiamos el color
            if i == 1 and j == 1:
                # Asignamos el color de la cara central
                boton.config(bg=colores_centro[cara_actual])
    for i, fila in enumerate(botones):
        for j, boton in enumerate(fila):
            boton.grid(row=i, column=j)
    
    return botones


# Funcionalidad al seleccionar cubos.
boton_actual = None


def ventana_colores(boton_principal, cubo, cara, fila, columna): #Funcion nque abre una subventana de colores.
    colores = ["white", "red", "blue", "green", "orange", "yellow"]  # Colores a elegir
    ventana = tk.Toplevel()  # Crear una nueva ventana
    ventana.resizable(False, False)  # Deshabilitar el cambio de tamaño
    ventana.title("Selección de colores")
    ventana.geometry("600x300+370+200")  # Dimensiones y posición de la ventana
    
    # Crear título
    titulo = tk.Label(ventana, text="Selecciona un color:", font=("Times New Roman", 30))
    titulo.pack(pady=10)
    
    # Crear frame para botones
    frame = tk.Frame(ventana)
    frame.pack(pady=20)
    
    # Crear y configurar botones de color
    for color in colores:
        boton = tk.Button(
            frame, bg=color, width=11, height=5, command=lambda c=color: asignar_color(boton_principal, c, ventana, cubo, cara, fila, columna)
        )
        boton.pack(side=tk.LEFT, padx=5)


def seleccionar_boton(boton, cubo, cara, fila, columna): #Funcion que selecciona el boton del cubo.
    global boton_actual
    boton_actual = boton  # Establecemos el botón actual
    ventana_colores(boton_actual, cubo, cara, fila, columna)  # Abrimos la ventana de colores para ese botón


def asignar_color(boton_principal, color, ventana_colores, cubo, cara, fila, columna): #Funcion que asigna el color al boton seleccionado.
    boton_principal.configure(bg=color)  # Cambiamos el color del botón principal
    cubo.actualizar_matriz(cara, fila, columna, color)
    ventana_colores.destroy()  # Cerramos la ventana de colores


def poner_color(botones, cubo, cara_actual): #Funcion llevada al main.
    global fila_seleccionada, columna_seleccionada
    global boton_actual  # Usamos la variable global para rastrear el botón actual
    
    for i, fila in enumerate(botones):  # Enumeramos las filas para obtener el índice i
        for j, boton in enumerate(fila):  # Enumeramos los botones en cada fila para obtener el índice j
            # Saltar el botón del centro
            if i == 1 and j == 1:  # Posición del centro
                continue  # Continúa con el siguiente botón
            # Al presionar el botón, se establece como botón actual
            boton.configure(command=lambda i=i, j=j, b=boton: seleccionar_boton(b, cubo, cara_actual, i, j))


# Funcionalidad de los botones anterior y siguiente.
def botones_siguiente(frame, ventana, cubo): #Crea los botones.
    global cara_actual

    # Crear botones "Cara anterior" y "Cara siguiente"
    boton_anterior = tk.Button(frame, width=10, height=2, text="Cara anterior", command=lambda:ventana_anterior())
    boton_siguiente = tk.Button(frame, width=10, height=2, text="Cara siguiente", 
                                command=lambda: cambiar_cara(ventana, 1, cubo))

    # Posicionar los botones en el grid
    boton_anterior.grid(row=0, column=0, padx=5, pady=5)
    boton_siguiente.grid(row=0, column=1, padx=5, pady=5)
    
    # Retornar los botones en una lista bidimensional
    return [[boton_anterior, boton_siguiente]]


def cambiar_cara(ventana, direccion, cubo): # Acción de cambiar cara.
    global cara_actual

    nueva_cara = cara_actual + direccion
    
    if 0 <= nueva_cara < 6:  # Solo permitir caras dentro del rango válido
        cara_actual = nueva_cara

        if len(ventanas_abiertas) == 0:
            ventanas_abiertas.append(ventana)  # Guardamos la primera ventana

        ventana.withdraw()  # Ocultar la ventana actual

        ventana_siguiente(cubo)  # Guardar la nueva ventana


def ventana_siguiente(cubo): #Toda la logica de la siguiente ventana xd.
    titulos = ["Cara blanca:)", "Cara roja:)", "Cara azul:)", "Cara verde:)", "Cara naranja:)", "Cara amarilla:)"]

    # Crear la nueva ventana
    ventana = tk.Toplevel()
    ventana.geometry("800x500+270+120")  # Dimensiones y posicionamiento de la ventana
    ventana.resizable(False, False)
    ventana.title(titulos[cara_actual])

    # Mostrar el texto de la cara actual
    texto = tk.Label(ventana, text=titulos[cara_actual], font=("Times new roman", 30))
    texto.pack()

    # Dividir el cubo y mostrarlo en la nueva ventana
    div_cubo = tk.Frame(ventana, width=400, height=400, bg="gray")
    div_cubo.pack(pady=20)
    botones_funcion = botones_cubo(div_cubo)  # Aquí se pasan las funciones necesarias
    poner_color(botones_funcion, cubo, cara_actual)

    # Crear el frame para los botones y agregar los botones de siguiente
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=20)

    # Llamar a la función botones_siguiente para crear los botones "Anterior" y "Siguiente"
    botones_nav = botones_siguiente(frame_botones, ventana, cubo)
    
    if cara_actual == 5:
        boton_final = tk.Button(frame_botones,width=10, height=2, text="Finalizar:)", command=lambda: finalizar())
        boton_final.grid(row=0, column=2, padx=5, pady=5)

    # Bloquear botones antes de cambiar la cara
    bloquear_boton(botones_nav, cara_actual)
    
    if len(ventanas_abiertas) == cara_actual: #Si la cantidad de elementos en ventanas abiertas es igual a la cara actual, agregamos la ventana actual.
        ventanas_abiertas.append(ventana)


def bloquear_boton(botones, cara_actual): #Bloquea los botones de anterior y siguiente cuando es la primer o ultima cara.
    # Se obtiene el botón "Anterior" y "Siguiente"
    boton_anterior = botones[0][0]
    boton_siguiente = botones[0][1]
    
    # Si estamos en la primera cara, deshabilitar el botón "Anterior"
    if cara_actual == 0:
        boton_anterior.config(state=tk.DISABLED)
    
    # Si estamos en la última cara, deshabilitar el botón "Siguiente"
    elif cara_actual == 5:
        boton_siguiente.config(state=tk.DISABLED)
    else:
        # Si no estamos ni en la primera ni en la última cara, habilitar ambos botones
        boton_anterior.config(state=tk.NORMAL)
        boton_siguiente.config(state=tk.NORMAL)
        
def ventana_anterior(): #Casos para cuando se de al botton de anterior-
    global cara_actual
    
    match cara_actual:
        case 1:    
            ventanas_abiertas[0].deiconify()   
            ventanas_abiertas[1].withdraw()
            cara_actual -= 1
        case 2: 
            ventanas_abiertas[1].deiconify()
            ventanas_abiertas[2].withdraw()
            cara_actual -= 1
        case 3: 
            ventanas_abiertas[2].deiconify()
            ventanas_abiertas[3].withdraw()
            cara_actual -= 1
        case 4: 
            ventanas_abiertas[3].deiconify()
            ventanas_abiertas[4].withdraw()
            cara_actual -= 1
        case 5: 
            ventanas_abiertas[4].deiconify()
            ventanas_abiertas[5].withdraw()
            cara_actual -= 1
            
def finalizar(): #Funcion para terminar la interfaz de eleccion.
    for ventana in ventanas_abiertas: #Para todas las ventanas en la lista de ventanas.
        ventana.destroy() #Se destruiran.
    ventana.destroy() #Destruir la principal.
        
def select_colors(tk_root):
    return main(tk_root)  # Pasamos tk_root a main

def main(tk_root): #Funcion que junta todas las funciones xd.
    global ventanas_abiertas, cara_actual, cubo
    
    ventanas_abiertas = []
    cara_actual = 0
    cubo = CuboColores()
    
    # Ventana principal (usando Toplevel)
    ventana = tk.Toplevel(tk_root)
    ventana.title("Cubo Rubik")
    ventana.geometry("800x500+270+120")
    ventana.resizable(False, False)
    
    # Título
    texto = tk.Label(ventana, text="Cara blanca:)", font=("Times new roman", 30))
    texto.pack()
    
    # Frame para los botones del cubo
    frame = tk.Frame(ventana)
    frame.pack(pady=20)
    
    # Botones del cubo
    botones = botones_cubo(frame)
    poner_color(botones, cubo, cara_actual)
    
    # Frame para botones de navegación
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=20)
    
    # Botones "Anterior" y "Siguiente"
    botones_nav = botones_siguiente(frame_botones, ventana, cubo)
    bloquear_boton(botones_nav, cara_actual)
    
    # Esperar a que el usuario termine de interactuar
    ventana.wait_window() 
    
    # Obtener y retornar los datos
    caras = cubo.obtener_caras()
    return caras