import oracledb

conexion=oracledb.connect(
    config_dir=r"C:\Users\angel\OneDrive\Documentos\INGENIERÍA\BASES DE DATOS\TEORÍA\PELICULAS_V2\wallet",
    user="admin",
    password="BDPeliculas1204",
    dsn="dcchab547u74py5f_low",
    wallet_location=r"C:\Users\angel\OneDrive\Documentos\INGENIERÍA\BASES DE DATOS\TEORÍA\PELICULAS_V2\wallet",
    wallet_password="BDPeliculas1204"
)
    
cursor=conexion.cursor()
    
#select consulta
cursor.execute("select * from actor")
registros=cursor.fetchall()
for registro in registros:
    print(registro)
    
#insert 
cursor.execute("insert into actor values(2,'Mich','Barrios','ALUMNA DE INGENIERIA','INGENIERIA EN COMPUTACION')")
conexion.commit() #confirmar la transacción

#update
cursor.execute("update actor set nombre='Michelle' where actor_id=2") 
conexion.commit()

#delete
cursor.execute("delete from actor where actor_id=2")
conexion.commit()