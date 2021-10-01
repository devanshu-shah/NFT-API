from Models import Database
from Route.Bean import *
class BALUser:
    
    def getUserList(self, contarctAddress=None):
        UserContarctAddressList=[]
        query="select * from user_contract_addresses "
        where=""
        if(status):
            where =" status ="+str(status)+" and"
        if(id):
            where =where+" id ="+str(id)+" and"
        if(where !=""):
            where=where.rsplit(" ",1)
            query=query+" where "+where[0]
        cursor=Database.getCursor(query)
        if(cursor==None):
                return UserContarctAddressList         
        for row in cursor:
            element=UserContarctAddress()
            element.id=row[0]
            element.creationTimestamp=str(row[1])
            element.createdById=row[2]
            element.name=row[3]
            element.email=row[4]
            element.mobile=row[5]
            element.deleted=row[7]
            element.deletedTimestamp=row[8]
            element.deletedById=row[9]
            element.status=row[10]
            
            UserContarctAddressList.append(element.__dict__)
        return UserContarctAddressList
