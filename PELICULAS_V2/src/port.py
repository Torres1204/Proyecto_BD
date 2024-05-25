import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
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

# Función para actualizar el Treeview con los datos de la tabla
def actualizar_treeview(treeview, table, campos):
    for row in treeview.get_children():
        treeview.delete(row)
    cursor.execute(f"SELECT * FROM {table}")
    registros = cursor.fetchall()
    for registro in registros:
        treeview.insert('', tk.END, values=registro)

# Funciones CRUD para Actores
def mostrar_actores(treeview):
    actualizar_treeview(treeview, "actor", ["actor_id", "nombre", "apellido_paterno", "filmografia", "biografia"])

def agregar_actor(entries):
    for entry in entries:
        entry.delete(0, tk.END)
    for entry in entries:
        entry.config(state=tk.NORMAL)

def insertar_actor(treeview, entries):
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
        actualizar_treeview(treeview, "actor", ["actor_id", "nombre", "apellido_paterno", "filmografia", "biografia"])

def seleccionar_actor(treeview, entries):
    seleccionado = treeview.focus()
    if seleccionado:
        registro = treeview.item(seleccionado, 'values')
        for entry, valor in zip(entries, registro):
            entry.delete(0, tk.END)
            entry.insert(0, valor)
            entry.config(state=tk.NORMAL)

def actualizar_actor(treeview, entries):
    seleccionado = treeview.focus()
    if seleccionado:
        actor_id = treeview.item(seleccionado, 'values')[0]
        nuevo_nombre = entries[1].get()
        nuevo_apellido_paterno = entries[2].get()
        nueva_filmografia = entries[3].get()
        nueva_biografia = entries[4].get()
        valores_actuales = obtener_valores_actor_seleccionado(treeview)
        if actor_id and (nuevo_nombre != valores_actuales[1] or nuevo_apellido_paterno != valores_actuales[2] or nueva_filmografia != valores_actuales[3] or nueva_biografia != valores_actuales[4]):
            cursor.execute("UPDATE actor SET nombre = :1, apellido_paterno = :2, filmografia = :3, biografia = :4 WHERE actor_id = :5", (nuevo_nombre, nuevo_apellido_paterno, nueva_filmografia, nueva_biografia, actor_id))
            conexion.commit()
            messagebox.showinfo("Éxito", "Actor actualizado correctamente")
            actualizar_treeview(treeview, "actor", ["actor_id", "nombre", "apellido_paterno", "filmografia", "biografia"])
        else:
            messagebox.showwarning("Advertencia", "No se han realizado cambios en los datos del actor")

def obtener_valores_actor_seleccionado(treeview):
    seleccionado = treeview.focus()
    if seleccionado:
        return treeview.item(seleccionado, 'values')
    return None

def eliminar_actor(treeview):
    seleccionado = treeview.focus()
    if seleccionado:
        actor_id = treeview.item(seleccionado, 'values')[0]
        cursor.execute("DELETE FROM actor WHERE actor_id = :1", (actor_id,))
        conexion.commit()
        messagebox.showinfo("Éxito", "Actor eliminado correctamente")
        actualizar_treeview(treeview, "actor", ["actor_id", "nombre", "apellido_paterno", "filmografia", "biografia"])

# Funciones CRUD para Directores (similares a Actores)
def mostrar_directores(treeview):
    actualizar_treeview(treeview, "director", ["director_id", "nombre", "apellido_paterno", "filmografia", "biografia"])

def agregar_director(entries):
    for entry in entries:
        entry.delete(0, tk.END)
    for entry in entries:
        entry.config(state=tk.NORMAL)

def insertar_director(treeview, entries):
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
        actualizar_treeview(treeview, "director", ["director_id", "nombre", "apellido_paterno", "filmografia", "biografia"])

def seleccionar_director(treeview, entries):
    seleccionado = treeview.focus()
    if seleccionado:
        registro = treeview.item(seleccionado, 'values')
        for entry, valor in zip(entries, registro):
            entry.delete(0, tk.END)
            entry.insert(0, valor)
            entry.config(state=tk.NORMAL)

def actualizar_director(treeview, entries):
    seleccionado = treeview.focus()
    if seleccionado:
        director_id = treeview.item(seleccionado, 'values')[0]
        nuevo_nombre = entries[1].get()
        nuevo_apellido_paterno = entries[2].get()
        nueva_filmografia = entries[3].get()
        nueva_biografia = entries[4].get()
        valores_actuales = obtener_valores_director_seleccionado(treeview)
        if director_id and (nuevo_nombre != valores_actuales[1] or nuevo_apellido_paterno != valores_actuales[2] or nueva_filmografia != valores_actuales[3] or nueva_biografia != valores_actuales[4]):
            cursor.execute("UPDATE director SET nombre = :1, apellido_paterno = :2, filmografia = :3, biografia = :4 WHERE director_id = :5", (nuevo_nombre, nuevo_apellido_paterno, nueva_filmografia, nueva_biografia, director_id))
            conexion.commit()
            messagebox.showinfo("Éxito", "Director actualizado correctamente")
            actualizar_treeview(treeview, "director", ["director_id", "nombre", "apellido_paterno", "filmografia", "biografia"])
        else:
            messagebox.showwarning("Advertencia", "No se han realizado cambios en los datos del director")

def obtener_valores_director_seleccionado(treeview):
    seleccionado = treeview.focus()
    if seleccionado:
        return treeview.item(seleccionado, 'values')
    return None

def eliminar_director(treeview):
    seleccionado = treeview.focus()
    if seleccionado:
        director_id = treeview.item(seleccionado, 'values')[0]
        cursor.execute("DELETE FROM director WHERE director_id = :1", (director_id,))
        conexion.commit()
        messagebox.showinfo("Éxito", "Director eliminado correctamente")
        actualizar_treeview(treeview, "director", ["director_id", "nombre", "apellido_paterno", "filmografia", "biografia"])

# Funciones CRUD para Películas (similares a Actores)
def mostrar_peliculas(treeview):
    actualizar_treeview(treeview, "pelicula", ["pelicula_id", "titulo", "sinopsis", "duracion", "fecha_lanzamiento", "clasificacion", "genero_id"])

def agregar_pelicula(entries):
    for entry in entries:
        entry.delete(0, tk.END)
    for entry in entries:
        entry.config(state=tk.NORMAL)

def insertar_pelicula(treeview, entries):
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
        actualizar_treeview(treeview, "pelicula", ["pelicula_id", "titulo", "sinopsis", "duracion", "fecha_lanzamiento", "clasificacion", "genero_id"])

def seleccionar_pelicula(treeview, entries):
    seleccionado = treeview.focus()
    if seleccionado:
        registro = treeview.item(seleccionado, 'values')
        for entry, valor in zip(entries, registro):
            entry.delete(0, tk.END)
            entry.insert(0, valor)
            entry.config(state=tk.NORMAL)

def actualizar_pelicula(treeview, entries):
    seleccionado = treeview.focus()
    if seleccionado:
        pelicula_id = treeview.item(seleccionado, 'values')[0]
        nuevo_titulo = entries[1].get()
        nueva_sinopsis = entries[2].get()
        nueva_duracion = entries[3].get()
        nueva_fecha_lanzamiento = entries[4].get()
        nueva_clasificacion = entries[5].get()
        nuevo_genero_id = entries[6].get()
        valores_actuales = obtener_valores_pelicula_seleccionado(treeview)
        if pelicula_id and (nuevo_titulo != valores_actuales[1] or nueva_sinopsis != valores_actuales[2] or nueva_duracion != valores_actuales[3] or nueva_fecha_lanzamiento != valores_actuales[4] or nueva_clasificacion != valores_actuales[5] or nuevo_genero_id != valores_actuales[6]):
            cursor.execute("UPDATE pelicula SET titulo = :1, sinopsis = :2, duracion = :3, fecha_lanzamiento = :4, clasificacion = :5, genero_id = :6 WHERE pelicula_id = :7", (nuevo_titulo, nueva_sinopsis, nueva_duracion, nueva_fecha_lanzamiento, nueva_clasificacion, nuevo_genero_id, pelicula_id))
            conexion.commit()
            messagebox.showinfo("Éxito", "Película actualizada correctamente")
            actualizar_treeview(treeview, "pelicula", ["pelicula_id", "titulo", "sinopsis", "duracion", "fecha_lanzamiento", "clasificacion", "genero_id"])
        else:
            messagebox.showwarning("Advertencia", "No se han realizado cambios en los datos de la película")

def obtener_valores_pelicula_seleccionado(treeview):
    seleccionado = treeview.focus()
    if seleccionado:
        return treeview.item(seleccionado, 'values')
    return None

def eliminar_pelicula(treeview):
    seleccionado = treeview.focus()
    if seleccionado:
        pelicula_id = treeview.item(seleccionado, 'values')[0]
        cursor.execute("DELETE FROM pelicula WHERE pelicula_id = :1", (pelicula_id,))
        conexion.commit()
        messagebox.showinfo("Éxito", "Película eliminada correctamente")
        actualizar_treeview(treeview, "pelicula", ["pelicula_id", "titulo", "sinopsis", "duracion", "fecha_lanzamiento", "clasificacion", "genero_id"])

# Función para crear la ventana CRUD
def crear_ventana_crud(titulo, mostrar_func, agregar_func, insertar_func, seleccionar_func, actualizar_func, eliminar_func, campos):
    ventana_crud = tk.Toplevel()
    ventana_crud.title(titulo)
    ventana_crud.geometry("600x400")
    ventana_crud.iconbitmap('PELICULAS_V2/img/icon1.ico') 

    # Frame para el Treeview
    frame_treeview = tk.Frame(ventana_crud)
    frame_treeview.pack(pady=10)

    # Configuración del Treeview
    columnas = [f"#{i+1}" for i in range(len(campos))]
    treeview = ttk.Treeview(frame_treeview, columns=columnas, show='headings')
    for i, campo in enumerate(campos):
        treeview.heading(f"#{i+1}", text=campo)
        treeview.column(f"#{i+1}", width=100)
    treeview.pack()

    mostrar_func(treeview)

    # Frame para los campos de entrada
    frame_entradas = tk.Frame(ventana_crud)
    frame_entradas.pack(pady=10)
    entries = []
    for i, campo in enumerate(campos):
        label = tk.Label(frame_entradas, text=campo)
        label.grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(frame_entradas)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)

    # Botones CRUD
    frame_botones = tk.Frame(ventana_crud)
    frame_botones.pack(pady=10)

    btn_agregar = tk.Button(frame_botones, text="Agregar", command=lambda: agregar_func(entries))
    btn_agregar.grid(row=0, column=0, padx=5, pady=5)

    btn_insertar = tk.Button(frame_botones, text="Insertar", command=lambda: insertar_func(treeview, entries))
    btn_insertar.grid(row=0, column=1, padx=5, pady=5)

    btn_seleccionar = tk.Button(frame_botones, text="Seleccionar", command=lambda: seleccionar_func(treeview, entries))
    btn_seleccionar.grid(row=0, column=2, padx=5, pady=5)

    btn_actualizar = tk.Button(frame_botones, text="Actualizar", command=lambda: actualizar_func(treeview, entries))
    btn_actualizar.grid(row=0, column=3, padx=5, pady=5)

    btn_eliminar = tk.Button(frame_botones, text="Eliminar", command=lambda: eliminar_func(treeview))
    btn_eliminar.grid(row=0, column=4, padx=5, pady=5)

    ventana_crud.mainloop()

# Ventana CRUD para Actores
def ventana_crud_actores():
    crear_ventana_crud("CRUD Actores", mostrar_actores, agregar_actor, insertar_actor, seleccionar_actor, actualizar_actor, eliminar_actor, ["actor_id", "nombre", "apellido_paterno", "nacionalidad", "biografia"])

# Ventana CRUD para Directores
def ventana_crud_directores():
    crear_ventana_crud("CRUD Directores", mostrar_directores, agregar_director, insertar_director, seleccionar_director, actualizar_director, eliminar_director, ["director_id", "nombre", "apellido_paterno", "filmografia", "biografia"])

# Ventana CRUD para Películas
def ventana_crud_peliculas():
    crear_ventana_crud("CRUD Películas", mostrar_peliculas, agregar_pelicula, insertar_pelicula, seleccionar_pelicula, actualizar_pelicula, eliminar_pelicula, ["pelicula_id", "titulo", "sinopsis", "duracion", "fecha_lanzamiento", "clasificacion", "genero_id"])


def main():
    crear_ventana_bienvenida()
    
    conexion.close()
    cursor.close()

if __name__ == "__main__":
    main()
