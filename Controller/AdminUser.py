import os
from Models.Database import Database
from flask import Flask, json, jsonify, request, make_response,jsonify
from flask_restful import Resource, Api, fields,reqparse
from web3.contract import ConciseContract
from web3 import Web3, HTTPProvider
from Route.Return import Return
from Route import Functions
from brownie.project import compiler, build
from brownie.project.sources import Sources
from brownie.project.main import Project
from eth_account.messages import encode_defunct
from Route.Bean import *
from Route.Functions import *
from datetime import datetime


key="0x8556b20365c8ecb3cd38225c0693a77a0aa861c0be988e855e3621a55b63561c"
user=UserAccountDetails("https://ropsten.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161","0xA9b8792a494Ae9e130226604595CD6C106385172",key)
w3 = Web3(HTTPProvider(user.WalletHttpProvider))



class AdminUser(Resource):  
    #@handleException
    def post(self):
                      
        data=request.json
        txnReceiptRecord={}
        NFTObjects=data['NFTObjects']

        for NFTobject in NFTObjects:
            try: 
                #validation
                NFTObj=NFTObject(**NFTobject)
            except Exception as e:
                return Return.returnResponse("Invaild NFT fields ",200);
            #Upload file to IPFS 
            #check file is uploaded or not in Upload folder
            FileHash=Functions.UploadFileOnIPFS(NFTObj.filepath)
            if(FileHash=="201"):
                return Return.returnResponse("Unable to Upload file on IPFS ",201)

            #upload jsonFile to IPFS server with NFT's name, description and URI(FileHash).
            JsonURI=Functions.UploadJsonFileOnIPFS(FileHash,NFTObj.name,NFTObj.description)
            if(JsonURI=="201"):
                return Return.returnResponse("Unable to Upload file on IPFS ",201)

            #Deployed and Minted smart contract with JsonURI, dataString.
            txnReceipt=Functions.deployAndMintContract('build/contracts/NFTTokenV1.json',NFTObj,user,JsonURI)      
        
            txnReceiptRecord[NFTObj.name]=txnReceipt
            os.remove(NFTObj.filepath)
         
        return Return.returnResponse(str(txnReceiptRecord),200)
    def get(self):
        #trying apis of etherscan 
        #URL="https://api-ropsten.etherscan.io/api?module=account&action=txlist&address=0xA9b8792a494Ae9e130226604595CD6C106385172&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey=ER2Q3MZ49IK8E4ZQQWXSTH9M68JZHWFCHE";
        URL="https://api-ropsten.etherscan.io/api";
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        para={'module':'account',
              'action':'txlist',
              'address':'0xA9b8792a494Ae9e130226604595CD6C106385172',
              'startblock':0,
              'endblock':99999999,
              'page':1,
              'offset':100,
              'sort':'desc',
              'apikey':'ER2Q3MZ49IK8E4ZQQWXSTH9M68JZHWFCHE',
              }
        res=requests.get(url=URL,params=para,headers=headers);
        txns=""
        contracts={}
        if (res):
            txns=res.json()
            for result in txns['result']:
                if (result.get('contractAddress')!=None and result.get('contractAddress')!='') :
                    contracts[result['hash']]=[{"contractAddress":result.get('contractAddress'),"from":result.get('from')}]
        
        return contracts    
    def put(self):
        URL="https://api-ropsten.etherscan.io/api";
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        para={'module':'contract',
              'action':'getabi',
              'address':'0x6c2805dcfb737cd51601666c38b8fd2ebdfff468',
              'apikey':'ER2Q3MZ49IK8E4ZQQWXSTH9M68JZHWFCHE',
              }
        res=requests.get(url=URL,params=para,headers=headers);
        txns=""
        contractABI=None
        if(res):
            txns=res.json()
            contractABI=txns.get('result')
            Mycontract=web3.eth.contract(contractABI);
            contract=w3.eth.contract(w3.isChecksumAddress(address='0x6da4f7a6cd587f87603dbc19fb123d342d7af0ed'),abi=contractABI)
            return contract

    def puts(self):
        #data=request.json
        #txnReceiptRecord={}
        #NFTObjects=data['NFTObjects']

        #for NFTobject in NFTObjects:
        #    try: 
        #        #validation
        #        NFTObj=NFTObject(**NFTobject)
        #    except Exception as e:
        #        return Return.returnResponse("Invaild NFT fields ",200);
        #    #Upload file to IPFS 
        #    #check file is uploaded or not in Upload folder
        #    FileHash=Functions.UploadFileOnIPFS(NFTObj.filepath)
        #    if(FileHash=="201"):
        #        return Return.returnResponse("Unable to Upload file on IPFS ",201)

        #    #upload jsonFile to IPFS server with NFT's name, description and URI(FileHash).
        #    JsonURI=Functions.UploadJsonFileOnIPFS(FileHash,NFTObj.name,NFTObj.description/7
        #    if(JsonURI=="201"):
        #        return Return.returnResponse("Unable to Upload file on IPFS ",201)

        #    #Deployed and Minted smart contract with JsonURI, dataString.
        #    txnReceipt=Functions.deployAndMintContract('build/contracts/NFTTokenV1.json',NFTObj,user,JsonURI)      
        
        #    txnReceiptRecord[NFTObj.name]=txnReceipt
        #    os.remove(NFTObj.filepath)
         
        #return Return.returnResponse(str(txnReceiptRecord),200);
        data=request.json
        filePath="build/contracts/"+data['contractName']+".json"
        
        try:
            if os.path.isfile(filePath):
                return "compiled",200
            #filePath="Contracts/"+data['contractName']+".sol"
            filePath="C:/Users/cei_l/source/repos/NFTDemoProject/NFTDemoProject/Contracts/"+data['contractName']+".sol"
            contractData=CompileContract(filePath,data['contractName'])
        except Exception as e:
                return Return.returnResponse("Something went wrong ",200);

class User(Resource):
    def post(self):
        req=reqparse.RequestParser()
        
        req.add_argument('userAddress',type=str,default=None,required=True,help='Please enter Wallet Address ')
        req.add_argument('nftname',type=str,default=None,required=True,help='Please enter nftname ')
        req.add_argument('nftsymbol',type=str,default=None,required=True,help='Please enter nftsymbol ')
        req.add_argument('filename',type=str,default=None,required=True,help='Please enter name of NFT ')
        req.add_argument('filepath',type=str,default=None,required=True,help='Please select file ')
        req.add_argument('description',type=str,default=None,required=True,help='Please enter description ')
        data=req.parse_args()
        query="select id,user_address,nft_type,nft_name,nft_symbol,contract_address, transaction_hash from user_contract_address where user_address='" + data['userAddress']+ "' and nft_name='"+data['nftname']+"' and nft_symbol='"+data['nftsymbol']+"'  and status = 'true'"
        cursor=Database.getCursor(query)
        UserContarctAddressObj=UserContarctAddress()
        contract=Functions.getContract('build/contracts/NFTTokenV1.json')
        txnReceipt={}
        if(cursor==None or cursor==[]):
            if(w3.isConnected()==False):
                return "201"
            acct = w3.eth.account.privateKeyToAccount(user.Key)
            deploy_receipt=Functions.deployContract(contract.constructor(data['nftname'],data['nftsymbol']),user,acct)
            txnReceipt['deploy_receipt']=deploy_receipt
            strdatetime = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

            #print(deploy_receipt.transactionHash.hex())
            #print(str(deploy_receipt.transactionHash.hex()))
            query="insert into user_contract_address values ('"+strdatetime+"', '1', '"+user.AccountAddress+"', 'ERC721', '"+data['nftname']+"', '"+data['nftsymbol']+"', '"+str(deploy_receipt['contractAddress'])+"','"+str(deploy_receipt.transactionHash.hex())+"',null,null, 0, null,null, 1)"
            output=Database.insertData(query)
            if(output != "200"):
                return Return.returnResponse("Some Internal Issue Occured while saving data ",201)
            UserContarctAddressObj.contractAddress=deploy_receipt['contractAddress']
            UserContarctAddressObj.userAddress=user.AccountAddress
            UserContarctAddressObj.NFTType="ERC721"
            UserContarctAddressObj.nftName=data['nftname']
            UserContarctAddressObj.nftSymbol=data['nftsymbol']
            UserContarctAddressObj.transactionAddress=deploy_receipt['transactionHash']
        else:
            id=cursor[0][0]
            UserContarctAddressObj.userAddress=cursor[0][1]
            UserContarctAddressObj.NFTType=cursor[0][2]
            UserContarctAddressObj.nftName=cursor[0][3]
            UserContarctAddressObj.nftSymbol=cursor[0][4]
            UserContarctAddressObj.contractAddress=cursor[0][5]
            UserContarctAddressObj.transactionAddress=cursor[0][6]
            
        jsonFileURL=getJsonFileHash(data['filepath'],data['filename'],data['description'])
        acct = w3.eth.account.privateKeyToAccount(user.Key)
        
        tx_receipt=MintNFTForContract('build/contracts/NFTTokenV1.json',contract,UserContarctAddressObj.contractAddress,jsonFileURL,acct)

        txnReceipt['mint_receipt']=tx_receipt
        os.remove(data['filepath'])

        return Return.returnResponse(str(txnReceipt),200)
        