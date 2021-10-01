import pypyodbc   
DatabaseName="demoNFT"
ConnectionString="Driver={SQL Server Native Client 11.0};Server=(localdb)\ProjectsV13;Database="+DatabaseName+";Trusted_Connection=yes;"
class Database:
    
    
    @staticmethod
    def insertData(sql):
        connection=None
        try:

            connection = pypyodbc.connect(ConnectionString)
            cursor = connection.cursor()
            cursor.execute(sql)
            cursor.commit()
            connection.close()
        except BaseException as e:
            return e
        finally:
            if(connection.connect==1):
                connection.close()
        return "200"

    @staticmethod
    def getCursor(sql):
        connection=None
        data=None
        try:
            connection = pypyodbc.connect(ConnectionString)
            cursor = connection.cursor()
            cursor.execute(sql)
            data=cursor.fetchall()            
            connection.close()
        except Exception as e:
            return None
        finally:
            if(connection.connect==1):
                connection.close()
        return data

    @staticmethod
    def getValue(sql):
        connection=None
        try:
            connection = pypyodbc.connect(ConnectionString)
            cursor = connection.cursor()
            cursor.execute(sql)
            if(not len(cursor.rowcount)> 0):
                return "data not found ",201
            str=cursor.fetchone();
            connection.close()
        except Exception as e:
            return None
        finally:
            if(connection.connect==1):
                connection.close()
        return str

    
        

