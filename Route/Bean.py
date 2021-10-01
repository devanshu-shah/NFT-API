from flask_restful import fields,reqparse

class UserAccountDetails():
    def __init__(self, WalletHttpProvider,AccountAddress,Key=None):
        self.WalletHttpProvider=WalletHttpProvider
        self.AccountAddress=AccountAddress
        self.Key=Key

class NFTObject:
    def __init__(self,nftname=fields.String,nftsymbol=fields.String,name=fields.String,filepath=fields.String,description=fields.String):
        self.nftname=nftname
        self.nftsymbol=nftsymbol
        self.name=name
        self.filepath=filepath
        self.description=description

class NFTObj:
    nftname= fields.String(None)
    nftsymbol= fields.String(None)
    name= fields.String(None)
    filepath= fields.String(None)
    description= fields.String(None)


class UserContarctAddress:

    id= fields.Integer(None)
    creationTimestamp = fields.String(None)
    createdById= fields.Integer(None)
    userAddress= fields.String(None)
    NFTType = fields.String(None)
    nftName = fields.String(None)
    nftSymbol = fields.String(None)
    contarctAddress = fields.String(None)
    transactionAddress= fields.String(None)
    deleted = fields.Integer(0)
    deletedTimestamp= fields.String(None)
    deletedById = fields.Integer(None)
    status= fields.Integer(0)
