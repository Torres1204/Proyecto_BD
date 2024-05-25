import tkinter as tk
from tkinter import messagebox
import oracledb

# Configuración de la conexión a la base de datos
conexion = oracledb.connect(
    config_dir=r"D:\Documentos\INGENIERIA\BASES DE DATOS\TEORÍA\Proyecto_BD\PELICULAS_V2\wallet",
    user="admin",
    password="BDPeliculas1204",
    dsn="dcchab547u74py5f_low",
    wallet_location=r"D:\Documentos\INGENIERIA\BASES DE DATOS\TEORÍA\Proyecto_BD\PELICULAS_V2\wallet",
    wallet_password="BDPeliculas1204"
)

cursor = conexion.cursor()

def abrir_ventana_principal():
    ventana_bienvenida.destroy()
    principal = tk.Tk()
    principal.geometry("500x400")
    principal.title("MovieArchive")
    principal.iconbitmap('PELICULAS_V2/img/icon1.ico') 

    # Título de bienvenida
    label_bienvenida = tk.Label(principal, text="¡Hola!", font=("Helvetica", 20, "bold"))
    label_bienvenida.pack(pady=20)

    # Frame para los botones principales
    frame_botones = tk.Frame(principal)
    frame_botones.pack(pady=20)

    button_font = ("Helvetica", 12)
    button_width = 12
    button_height = 2

    btn_actor = tk.Button(frame_botones, text="Actor", bg="black", fg="white", font=button_font, width=button_width, height=button_height, cursor='hand2', command=lambda: crear_ventana_crud("Actores", mostrar_actores, agregar_actor, insertar_actor, seleccionar_actor, actualizar_actor, eliminar_actor, ["ID", "Nombre", "Apellido", "Filmografía", "Biografía"]))
    btn_actor.pack(side=tk.LEFT, padx=10)

    btn_director = tk.Button(frame_botones, text="Director", bg="black", fg="white", font=button_font, width=button_width, height=button_height, cursor='hand2', command=lambda: crear_ventana_crud("Directores", mostrar_directores, agregar_director, insertar_director, seleccionar_director, actualizar_director, eliminar_director, ["ID", "Nombre", "Apellido", "Filmografía", "Biografía"]))
    btn_director.pack(side=tk.LEFT, padx=10)

    btn_pelicula = tk.Button(frame_botones, text="Película", bg="black", fg="white", font=button_font, width=button_width, height=button_height, cursor='hand2', command=lambda: crear_ventana_crud("Películas", mostrar_peliculas, agregar_pelicula, insertar_pelicula, seleccionar_pelicula, actualizar_pelicula, eliminar_pelicula, ["ID", "Título", "Sinopsis", "Duración", "Fecha de Lanzamiento", "Clasificación", "Género ID"]))
    btn_pelicula.pack(side=tk.LEFT, padx=10)
    principal.mainloop()
    
# Función para crear la ventana de bienvenida
def crear_ventana_bienvenida():
    global ventana_bienvenida
    
    ventana_bienvenida = tk.Tk()
    ventana_bienvenida.title("¡Bienvenido a MovieArchive!")
    ventana_bienvenida.geometry("1100x400")
    ventana_bienvenida.iconbitmap('PELICULAS_V2/img/icon1.ico') 

    # Texto de bienvenida
    texto_bienvenida = """
    ¡Te damos la bienvenida a MovieArchive!

    Con MovieArchive podrás registrar todas las películas, directores, directoras, actores y actrices.  

    Para empezar, te sugerimos:

    1. Añadir Actor, Director o Película: Dirígete al botón correspondiente para añadir la información correspondiente y agregarlo a la Base de Datos.
    2. Cada botón te desplegará la información actual de esa tabla así como sus registros guardados hasta ese momento.
    3. Es posible obtener funcionalidades tales como mostrar, agregar, guardar, seleccionar, actualizar y eliminar.

    ¡Gracias por elegir MovieArchive!
    """
    
    # Etiqueta con el texto de bienvenida
    etiqueta_bienvenida = tk.Label(ventana_bienvenida, text=texto_bienvenida, font=12, justify="left", padx=10, pady=10)
    etiqueta_bienvenida.pack()
    
    button_font = ("Helvetica", 12)
    button_width = 12
    button_height = 2

    # Botón de inicio
    boton_inicio = tk.Button(ventana_bienvenida, text="Inicio", bg="black", fg="white", font=button_font, width=button_width, height=button_height, cursor='hand2', command=abrir_ventana_principal)
    boton_inicio.pack(pady=10)

    ventana_bienvenida.mainloop()

# Función para actualizar el Listbox con los datos de la tabla
def actualizar_listbox(listbox, table):
    listbox.delete(0, tk.END)
    cursor.execute(f"SELECT * FROM {table}")
    registros = cursor.fetchall()
    for registro in registros:
        listbox.insert(tk.END, registro)

# Funciones CRUD para Actores
def mostrar_actores(listbox):
    actualizar_listbox(listbox, "actor")

def agregar_actor(entries):
    for entry in entries:
        entry.delete(0, tk.END)
    for entry in entries:
        entry.config(state=tk.NORMAL)

def insertar_actor(listbox, entries):
    actor_id = entries[0].get()
    nombre = entries[1].get()
    apellido_paterno = entries[2].get()
    filmografia = entries[3].get()
    biografia = entries[4].get()
    if actor_id and nombre and apellido_paterno and filmografia and biografia:
        cursor.execute("INSERT INTO actor VALUES (:1, :2, :3, :4, :5)", 
                       (actor_id, nombre, apellido_paterno, filmografia, biografia))
        conexion.commit()
        messagebox.showinfo("Éxito", "Actor insertado correctamente")
        actualizar_listbox(listbox, "actor")

def seleccionar_actor(listbox, entries):
    seleccionado = listbox.curselection()
    if seleccionado:
        registro = listbox.get(seleccionado)
        for entry, valor in zip(entries, registro):
            entry.delete(0, tk.END)
            entry.insert(0, valor)
            entry.config(state=tk.NORMAL)

def actualizar_actor(listbox, entries):
    seleccionado = listbox.curselection()
    if seleccionado:
        actor_id = listbox.get(seleccionado)[0]  # Obtener el ID del actor seleccionado
        nuevo_nombre = entries[1].get()  # Obtener el nuevo nombre del actor desde el campo de entrada
        nuevo_apellido_paterno = entries[2].get()  # Obtener el nuevo apellido paterno del actor desde el campo de entrada
        nueva_filmografia = entries[3].get()  # Obtener la nueva filmografía del actor desde el campo de entrada
        nueva_biografia = entries[4].get()  # Obtener la nueva biografía del actor desde el campo de entrada
        
        # Obtener los valores actuales del actor seleccionado en la lista
        valores_actuales = obtener_valores_actor_seleccionado(listbox)
        
        # Verificar si se han realizado cambios en los valores del actor
        print("Valores actuales:", valores_actuales)  # Debugging: Mostrar valores actuales antes de la actualización
        print("Nuevos valores:", nuevo_nombre, nuevo_apellido_paterno, nueva_filmografia, nueva_biografia)  # Debugging: Mostrar nuevos valores
        if actor_id and (nuevo_nombre != valores_actuales[1] or nuevo_apellido_paterno != valores_actuales[2] or nueva_filmografia != valores_actuales[3] or nueva_biografia != valores_actuales[4]):
            cursor.execute("UPDATE actor SET nombre = :1, apellido_paterno = :2, filmografia = :3, biografia = :4 WHERE actor_id = :5", (nuevo_nombre, nuevo_apellido_paterno, nueva_filmografia, nueva_biografia, actor_id))
            conexion.commit()
            messagebox.showinfo("Éxito", "Actor actualizado correctamente")
            actualizar_listbox(listbox, "actor")
        else:
            messagebox.showwarning("Advertencia", "No se han realizado cambios en los datos del actor")

# Función auxiliar para obtener los valores del actor seleccionado en la lista
def obtener_valores_actor_seleccionado(listbox):
    seleccionado = listbox.curselection()
    if seleccionado:
        # Obtener el índice del elemento seleccionado en la lista
        indice = seleccionado[0]
        
        # Obtener la película seleccionada en base al índice
        actor_seleccionado = listbox.get(indice)
        
        # Verificar si la película seleccionada no está vacía
        if actor_seleccionado:
            return actor_seleccionado  # Retornar los valores de la película seleccionada
    return None

def eliminar_actor(listbox):
    seleccionado = listbox.curselection()
    if seleccionado:
        actor_id = listbox.get(seleccionado)[0]  # Obtenemos el ID del actor seleccionado
        cursor.execute("DELETE FROM actor WHERE actor_id = :1", (actor_id,))
        conexion.commit()
        messagebox.showinfo("Éxito", "Actor eliminado correctamente")
        actualizar_listbox(listbox, "actor")

# Funciones CRUD para Directores
def mostrar_directores(listbox):
    actualizar_listbox(listbox, "director")

def agregar_director(entries):
    for entry in entries:
        entry.delete(0, tk.END)
    for entry in entries:
        entry.config(state=tk.NORMAL)

def insertar_director(listbox, entries):
    director_id = entries[0].get()
    nombre = entries[1].get()
    apellido_paterno = entries[2].get()
    filmografia = entries[3].get()
    biografia = entries[4].get()
    if director_id and nombre and apellido_paterno and filmografia and biografia:
        cursor.execute("INSERT INTO director VALUES (:1, :2, :3, :4, :5)", 
                       (director_id, nombre, apellido_paterno, filmografia, biografia))
        conexion.commit()
        messagebox.showinfo("Éxito", "Director insertado correctamente")
        actualizar_listbox(listbox, "director")

def seleccionar_director(listbox, entries):
    seleccionado = listbox.curselection()
    if seleccionado:
        registro = listbox.get(seleccionado)
        for entry, valor in zip(entries, registro):
            entry.delete(0, tk.END)
            entry.insert(0, valor)
            entry.config(state=tk.NORMAL)

def actualizar_director(listbox, entries):
    seleccionado = listbox.curselection()
    if seleccionado:
        director_id = listbox.get(seleccionado)[0]  # Obtener el ID del director seleccionado
        nuevo_nombre = entries[1].get()  # Obtener el nuevo nombre del director desde el campo de entrada
        nuevo_apellido_paterno = entries[2].get()  # Obtener el nuevo apellido paterno del director desde el campo de entrada
        nueva_filmografia = entries[3].get()  # Obtener la nueva filmografía del director desde el campo de entrada
        nueva_biografia = entries[4].get()  # Obtener la nueva biografía del director desde el campo de entrada
        
        # Obtener los valores actuales del director seleccionado en la lista
        valores_actuales = obtener_valores_director_seleccionado(listbox)
        
        # Verificar si se han realizado cambios en los valores del director
        if director_id and (nuevo_nombre != valores_actuales[1] or nuevo_apellido_paterno != valores_actuales[2] or nueva_filmografia != valores_actuales[3] or nueva_biografia != valores_actuales[4]):
            cursor.execute("UPDATE director SET nombre = :1, apellido_paterno = :2, filmografía = :3, biografía = :4 WHERE director_id = :5", (nuevo_nombre, nuevo_apellido_paterno, nueva_filmografia, nueva_biografia, director_id))
            conexion.commit()
            messagebox.showinfo("Éxito", "Director actualizado correctamente")
            actualizar_listbox(listbox, "director")
        else:
            messagebox.showwarning("Advertencia", "No se han realizado cambios en los datos del director")

# Función auxiliar para obtener los valores del director seleccionado en la lista
def obtener_valores_director_seleccionado(listbox):
    seleccionado = listbox.curselection()
    if seleccionado:
        return listbox.get(seleccionado)  # Valores del director seleccionado
    return None

def eliminar_director(listbox):
    seleccionado = listbox.curselection()
    if seleccionado:
        director_id = listbox.get(seleccionado)[0]  # Obtenemos el ID del director seleccionado
        cursor.execute("DELETE FROM director WHERE director_id = :1", (director_id,))
        conexion.commit()
        messagebox.showinfo("Éxito", "Director eliminado correctamente")
        actualizar_listbox(listbox, "director")

# Funciones CRUD para Películas
def mostrar_peliculas(listbox):
    actualizar_listbox(listbox, "pelicula")

def agregar_pelicula(entries):
    for entry in entries:
        entry.delete(0, tk.END)
    for entry in entries:
        entry.config(state=tk.NORMAL)

def insertar_pelicula(listbox, entries):
    pelicula_id = entries[0].get()
    titulo = entries[1].get()
    sinopsis = entries[2].get()
    duracion = entries[3].get()
    fecha_lanzamiento = entries[4].get()
    clasificacion = entries[5].get()
    genero_id = entries[6].get()
    if pelicula_id and titulo and sinopsis and duracion and fecha_lanzamiento and clasificacion and genero_id:
        cursor.execute("INSERT INTO pelicula VALUES (:1, :2, :3, :4, :5, :6, :7)", 
                       (pelicula_id, titulo, sinopsis, duracion, fecha_lanzamiento, clasificacion, genero_id))
        conexion.commit()
        messagebox.showinfo("Éxito", "Película insertada correctamente")
        actualizar_listbox(listbox, "pelicula")

def seleccionar_pelicula(listbox, entries):
    seleccionado = listbox.curselection()
    if seleccionado:
        registro = listbox.get(seleccionado)
        for entry, valor in zip(entries, registro):
            entry.delete(0, tk.END)
            entry.insert(0, valor)
            entry.config(state=tk.NORMAL)

def actualizar_pelicula(listbox, entries):
    seleccionado = listbox.curselection()
    if seleccionado:
        pelicula_id = listbox.get(seleccionado)[0]  # Obtener el ID de la película seleccionada
        nuevo_titulo = entries[1].get()  # Obtener el nuevo título de la película desde el campo de entrada
        nueva_sinopsis = entries[2].get()  # Obtener la nueva sinopsis de la película desde el campo de entrada
        nueva_duracion = entries[3].get()  # Obtener la nueva duración de la película desde el campo de entrada
        nueva_fecha_lanzamiento = entries[4].get()  # Obtener la nueva fecha de lanzamiento de la película desde el campo de entrada
        nueva_clasificacion = entries[5].get()  # Obtener la nueva clasificación de la película desde el campo de entrada
        
        # Obtener los valores actuales de la película seleccionada en la lista
        valores_actuales = obtener_valores_pelicula_seleccionada(listbox)
        
        # Verificar si se han realizado cambios en los valores de la película
        if pelicula_id and (nuevo_titulo != valores_actuales[1] or nueva_sinopsis != valores_actuales[2] or nueva_duracion != valores_actuales[3] or nueva_fecha_lanzamiento != valores_actuales[4] or nueva_clasificacion != valores_actuales[5]):
            cursor.execute("UPDATE pelicula SET titulo = :1, sinopsis = :2, duracion = :3, fecha_lanzamiento = :4, clasificacion = :5 WHERE pelicula_id = :6", (nuevo_titulo, nueva_sinopsis, nueva_duracion, nueva_fecha_lanzamiento, nueva_clasificacion, pelicula_id))
            conexion.commit()
            messagebox.showinfo("Éxito", "Película actualizada correctamente")
            actualizar_listbox(listbox, "pelicula")
        else:
            messagebox.showwarning("Advertencia", "No se han realizado cambios en los datos de la película")

# Función auxiliar para obtener los valores de la película seleccionada en la lista
def obtener_valores_pelicula_seleccionada(listbox):
    seleccionado = listbox.curselection()
    if seleccionado:
        return listbox.get(seleccionado)  # Valores de la película seleccionada
    return None

def eliminar_pelicula(listbox):
    seleccionado = listbox.curselection()
    if seleccionado:
        pelicula_id = listbox.get(seleccionado)[0]  # Obtenemos el ID de la película seleccionada
        cursor.execute("DELETE FROM pelicula WHERE pelicula_id = :1", (pelicula_id,))
        conexion.commit()
        messagebox.showinfo("Éxito", "Película eliminada correctamente")
        actualizar_listbox(listbox, "pelicula")

# Función para crear una nueva ventana con operaciones CRUD
def crear_ventana_crud(titulo, mostrar_func, agregar_func, insertar_func, seleccionar_func, actualizar_func, eliminar_func, campos):
    ventana_crud = tk.Toplevel()
    ventana_crud.geometry("450x600")
    ventana_crud.title(f"CRUD de {titulo}")

    # Frame para los botones y etiquetas
    frame_top = tk.Frame(ventana_crud)
    frame_top.pack(fill=tk.X, padx=10, pady=10)

    entries = []
    for campo in campos:
        frame = tk.Frame(frame_top)
        frame.pack(fill=tk.X, pady=5)
        label = tk.Label(frame, text=campo, width=20, anchor='w')
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame)
        entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        entry.config(state=tk.DISABLED)
        entries.append(entry)

    btn_mostrar = tk.Button(frame_top, text="Mostrar", bg="black", fg="white", cursor='hand2', command=lambda: mostrar_func(listbox))
    btn_mostrar.pack(side=tk.LEFT, padx=5, pady=5)

    btn_agregar = tk.Button(frame_top, text="Agregar", bg="black", fg="white", cursor='hand2', command=lambda: agregar_func(entries))
    btn_agregar.pack(side=tk.LEFT, padx=5, pady=5)

    btn_insertar = tk.Button(frame_top, text="Guardar", bg="black", fg="white", cursor='hand2', command=lambda: insertar_func(listbox, entries))
    btn_insertar.pack(side=tk.LEFT, padx=5, pady=5)

    btn_seleccionar = tk.Button(frame_top, text="Seleccionar", bg="black", fg="white", cursor='hand2', command=lambda: seleccionar_func(listbox, entries))
    btn_seleccionar.pack(side=tk.LEFT, padx=5, pady=5)

    btn_actualizar = tk.Button(frame_top, text="Actualizar", bg="black", fg="white", cursor='hand2', command=lambda: actualizar_func(listbox, entries))
    btn_actualizar.pack(side=tk.LEFT, padx=5, pady=5)

    btn_eliminar = tk.Button(frame_top, text="Eliminar", bg="black", fg="white", cursor='hand2', command=lambda: eliminar_func(listbox))
    btn_eliminar.pack(side=tk.LEFT, padx=5, pady=5)

    # Listbox en la parte inferior
    listbox = tk.Listbox(ventana_crud)
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, anchor='s')

# Ventana principal
def main():
    crear_ventana_bienvenida()
    
    conexion.close()
    cursor.close()

if __name__ == "__main__":
    main()

