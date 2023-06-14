import sqlite3

def crear_tabla_personajes_bd():
    with sqlite3.connect("bd_btf.db") as conexion:
        try:
            sentencia = ''' create  table personajes
            (
            id integer primary key autoincrement,
            nombre text,
            puntos real
            )
            '''
            conexion.execute(sentencia)
            print("Se creo la tabla personajes")                       
        except sqlite3.OperationalError:
            print("La tabla personajes ya existe")

#INSERT:
def guardar_puntaje_bd(nombre, score):
    if not nombre:
        nombre = "Desconocido"
    with sqlite3.connect("bd_btf.db") as conexion:
        try:
            conexion.execute("insert into personajes(nombre,puntos) values (?,?)", (nombre, score))
            conexion.commit()# Actualiza los datos realmente en la tabla        
        except:
            print("Error")

def eliminar_personajes():
    with sqlite3.connect("bd_btf.db") as conexion:
        cursor = conexion.execute("SELECT * FROM personajes ORDER by puntos DESC")
        personajes = cursor.fetchall()

        if len(personajes) > 10:
            personajes_eliminar = personajes[10:]
            ids_eliminar = []
            for personaje in personajes_eliminar:
                ids_eliminar.append(personaje[0])
            
            for id_personaje in ids_eliminar:
                conexion.execute("DELETE FROM personajes WHERE id=?", (id_personaje,))
                print(f"Personaje con ID {id_personaje} eliminado")
            conexion.commit()

#SELECT:
def obtener_puntajes_bd():
    with sqlite3.connect("bd_btf.db") as conexion:
        cursor = conexion.execute("SELECT * FROM personajes ORDER by puntos DESC")
        puntajes = cursor.fetchall()
        return puntajes