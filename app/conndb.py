#import mysql.connector
import pymysql

class GesConnMysql:
  def __init__(self):                
      
      self.__conn_cali = ''
      self.__conn = ''

      self.getcredenciales()
      self.getcredenciales_cali()


  def getcredenciales(self):    
      cr = {  'localhost':'190.60.100.100', 
              'usuario':'BotCndCen',
              'clave' :'B0tCndC3n24*', 
              'basedatos':'dbcrmgnp', 
              'port':3306
            }
      
      self.__conn = pymysql.connect(
      host=cr["localhost"],
      user=cr["usuario"],
      password=cr["clave"],
      database=cr["basedatos"],
      port=cr["port"],
      charset='utf8mb4'
    )

  def getcredenciales_cali(self):    

      cr = {  'localhost':'190.60.100.100', 
              'usuario':'root',
              'clave' :'Control2023*', 
              'basedatos':'dbcrmgnp', 
              'port':3307
            }

      self.__conn_cali = pymysql.connect(
      host=cr["localhost"],
      user=cr["usuario"],
      password=cr["clave"],
      database=cr["basedatos"],
      port=cr["port"],
      charset='utf8mb4'
    )


  def CloseConn(self):    
    try:
      if self.__conn is not None:
        self.__conn.close()
        self.__conn = None
    except Exception as e:
      print(f'Failed to close the database connection due to: {e}')
  
  def __del__(self):    
    """Close the DB connection."""
    try:
      if self.__conn is not None:
        self.__conn.close()
        self.__conn = None
    except Exception as e:
      print(f'Failed to close the database connection due to: {e}')


  def FuncGetSpr(self, procedimiento, cuidad, Arraydatos=[]):
    data = []
    if cuidad == 'Cali':
      conn = self.__conn_cali.cursor()
    else:
      conn = self.__conn.cursor()

    with conn as cursor:
      if len(Arraydatos) != 0:        
        cursor.callproc(procedimiento, args=(Arraydatos))
      else:
        cursor.callproc(procedimiento)
      data = cursor.fetchone()
      
    self.CloseConn()    
    return data
  
  def FuncGetSprEnc(self, tipo, procedimiento, Arraydatos=[]):        
    cursor = self.__conn.cursor()                            
    cursor.callproc(procedimiento,Arraydatos)            
    results = cursor.fetchall()
    # Procesar los datos en formato de bytes
    for row in results:
        datos_bytes = row[0]
    self.CloseConn()    
    return datos_bytes

  def FuncUpdSpr(self,procedimiento, Arraydatos=[]):
    cursor=self.__conn.cursor()
    if len(Arraydatos)!=None:
      cursor.callproc(procedimiento, args=(Arraydatos))
    else:
      cursor.callproc(Arraydatos)
    self.__conn.commit()
    self.CloseConn()        
    return True

  def FuncUpdGetSpr(self,procedimiento, Arraydatos=[]):
    cursor=self.__conn.cursor()
    if len(Arraydatos)!=None:
      cursor.callproc(procedimiento, args=(Arraydatos))
    else:
      cursor.callproc(Arraydatos)
    self.__conn.commit()
    data = cursor.fetchone()
    self.CloseConn()            
    return data


  def FuncGetQuery(self, tipo, procedimiento, Arraydatos=[]):
    data = []
    with self.__conn.cursor() as cursor:
      if len(Arraydatos) != 0:
        cursor.execute(procedimiento, args=(Arraydatos))
      else:
        cursor.execute(procedimiento)
      if tipo == 1:
        data = cursor.fetchone()
      else:
        data = cursor.fetchall()
    self.CloseConn()
    return data

  def FuncUpdQuery(self,Consulta, Arraydatos=[]):
    cursor=self.__conn.cursor()
    if len(Arraydatos)!=None:
      cursor.execute(Consulta, args=(Arraydatos))
    else:
      cursor.execute(Consulta)
    self.CloseConn()
    return True



