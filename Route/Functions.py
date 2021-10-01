import ipfsApi
import requests
import io
import os
import json
from Route.Bean import UserAccountDetails
from web3 import Web3, HTTPProvider
from solc import compile_source, compile_files

w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161"))




def getJsonFileHash(path,name,description):
    #Upload file to IPFS 
    #check file is uploaded or not in Upload folder
    FileHash=UploadFileOnIPFS(path)
    if(FileHash=="201"):
        return Return.returnResponse("Unable to Upload file on IPFS ",201)

    #upload jsonFile to IPFS server with NFT's name, description and URI(FileHash).
    JsonURI=UploadJsonFileOnIPFS(FileHash,name,description)
    return JsonURI

def UploadFileOnIPFS(path):
    try:
        #Making connection with IPFS
        #api=ipfsApi.Client('localhost', 5001)
        file = {'upload_file': open(path,'rb')}
        res=requests.post('https://ipfs.infura.io:5001/api/v0/add',files=file);
        #res = api.add(path)
        resjson=res.json()
        #hash=resjson['Hash']
    except Exception as e:
        return "201"
    if(resjson):
        return resjson
    else:
        return '201'


def UploadJsonFileOnIPFS(Hash,name,description):
    try:
        
        #api=ipfsApi.Client('127.0.0.1', 5001)
        jsName=Hash['Name'].split('/')
        jsName=jsName[-1].split('.')
        jsonFile=open("Files/"+jsName[0]+".json","w")

        #creating json string for json file.
        jstr={"name":name, "description":description,"file":"https://ipfs.io/ipfs/"+str(Hash['Hash'])}
        jsonFile.write(json.dumps(jstr))
        jsonFile.close()

        #Adding file in ipfs server
        #jsonhash = api.add("Files/"+jsName[0]+".json")
        res=UploadFileOnIPFS("Files/"+jsName[0]+".json")
        jsonhash="https://ipfs.io/ipfs/"+res['Hash']
    except:
        return "201"
    if not jsonhash:
       return "201"
    return jsonhash


def deployAndMintContract(contractjsonpath,dataString,user,JsonURI):
    #Making connection with wallet link https://ropsten.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161
    w3 = Web3(HTTPProvider(user.WalletHttpProvider))
    if(w3.isConnected()==False):
        return "201"

    #created account for sign and send transactions
    acct = w3.eth.account.privateKeyToAccount(user.Key)

    #contractjsonpath is path of json file 
    contract=getContract(contractjsonpath)
    
    #deploying smart contract 
    deploy_receipt=deployContract(contract.constructor(dataString.nftname,dataString.nftsymbol),user,acct)
    contractAddress=deploy_receipt['contractAddress']

    #converting contractAddress into uint256 
    uContractAddress=int(contractAddress,16)

    #getting contract Instance with contractAddress and contractJsonFile
    contract_instance=GetContractInstance(contractjsonpath,contractAddress)

    #constructing transaction mintNFT function from smartcontract and passing gas Limit, gas price
    construct_txn=contract_instance.functions.mintNFT(user.AccountAddress,uContractAddress,JsonURI).buildTransaction(getTxnFilter(acct.address,w3,1728712,'21'))
    signed_tx = acct.signTransaction(construct_txn)

    #sending transaction
    tx_hash= w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    
    #return both deployed and minted transaction Receipt
    txnReceipt={'deploy_receipt':deploy_receipt,'mint_receipt':tx_receipt}
    return txnReceipt

def deployContract(contract,user,acct):
    #constructing transaction of smartcontract
    construct_txn = contract.buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.getTransactionCount(acct.address),
        'gas': 1728712,
        'gasPrice': w3.toWei('21', 'gwei')})
    signed = acct.signTransaction(construct_txn)

    #sending transaction
    tx_hash=w3.eth.sendRawTransaction(signed.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt

def MintNFTForContract(contractjsonpath,contract_instance,contractAddress,JsonURL,acct):
    #converting contractAddress into uint256 
    #uContractAddress=int(contractAddress,16)

    #getting contract Instance with contractAddress and contractJsonFile
    contract_instance=GetContractInstance(contractjsonpath,contractAddress)
    

    #constructing transaction mintNFT function from smartcontract and passing gas Limit, gas 
    construct_txn=contract_instance.functions.mintNFT(acct.address,JsonURL).buildTransaction(getTxnFilter(acct.address,w3,1728712,'21'))
    signed_tx = acct.signTransaction(construct_txn)

    #sending transaction
    tx_hash= w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    
    return tx_receipt


#getting contract Instance of smart contract
def GetContractInstance(path,contract_address):
    contract=getContract(path)
    contract_instance = w3.eth.contract(abi=contract.abi, address=contract_address)
    return contract_instance

#getting contract from json file
def getContract(path):
    jsonFile = json.load(open(path))
    abi = jsonFile['abi']
    bytecode = jsonFile['bytecode']
    contract= w3.eth.contract(bytecode=bytecode, abi=abi)
    return contract

#passing gas limit and gas pice 
def getTxnFilter(accountAddress,w3,gas=1728712,gasPrice='21'):   
    return {
        'from': accountAddress,
        'nonce': w3.eth.getTransactionCount(accountAddress),
        'gas': gas,
        'gasPrice': w3.toWei(gasPrice, 'gwei')}


def compareDictObject(Object,value):
    result = []
    try:
        for v in value:
            x = Object(**v)
            result.append(x)
    except TypeError:
        raise ValueError("Invalid object")
    except:
        raise ValueError
    return result

def CompileContract(contract_source_file, contractName=None):
    #with open(contract_source_file, "r") as f:
    #    contract_source_code = f.read()
    #compiled_sol = compile_source(contract_source_code,True) # Compiled source code
    compiled_sol = compile_files(contract_source_file) # Compiled source code
    if not contractName:
        contractName = list(compiled_sol.keys())[0]
        contract_interface = compiled_sol[contractName]
    else:
        contract_interface = compiled_sol['<stdin>:' + contractName]        
    return contractName, contract_interface

def ReadFile(file):
    f = open(file, "r")
    return f.read()
 

    