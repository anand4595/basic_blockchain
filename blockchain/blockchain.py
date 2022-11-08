# libraries
from hashlib import sha256
from flask import Flask, request
import json
import time

class Block:
    """
    Individual blocks in the blockchain
    
    Attributes
    ----------
    index : str
        index of block in the chain automatically set 
    transactions : str
        data in the block.gernal format sender-reciver-ammount. 
        !Note their not compulsion or checking of ammount this is basic blockchain
    timestamp :
        store the time the block war mined
    previous_hash
        stores the hash of previous the node
    nounce :
        used of meeting diffculty criteria. here we set it to 4("0000")   
    
    Methods
    -------
    compute_hash(self):
        computes the hash of the block 
    """
    def __init__(self, index:int, transactions, timestamp, previous_hash, nonce=0):
        """
        initialise the block

        Parameters
        ----------
        index : str
            index of block in the chain automatically set 
        transactions : str
            data in the block.gernal format sender-reciver-ammount. 
            !Note their not compulsion or checking of ammount this is basic blockchain
        timestamp :
            store the time the block war mined
        previous_hash
            stores the hash of previous the node
        nounce :
            used of meeting diffculty criteria. here we set it to 4("0000")
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        """
        computes the hash of the block

        returns  
        ------
        hexadecimal value of hash of block 
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class Blockchain: 
    """
    Main blockchain. In oder to maintain the immutability of the entire chain  
    we hash current block with the previous block

    Attributes
    ----------

    unconfimed_transaction: list
        acts as the basic mineing pool for blockchain
    chain: list
        contains bocks in the chain in odered manner 
    last_block:
        returns the last block of the chain 
    difficulty:
        sets the time taken to mine the block 

    Methods
    -------
    last_block(self):
        returns the last block of the blockchain 
    proof_of_work(self,block):
        returns the hash of block as per required difficulty 
    """
    def __init__(self):
        """
        initialise the blockchain and create the first block 

        Parameters
        ----------
        unconfimed_transaction: list
            acts as the basic mineing pool for blockchain
        chain: list
            contains bocks in the chain in odered manner  
        """
        self.unconfirmed_transactions= []
        self.chain = []
        self.create_genesis_block()
 
    def create_genesis_block(self)->None:
        """
        creates the genesis(first) block of the blockchain and adds it to chain
        ! dont use. automatically used for creating for the first block
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
    
    @property
    def last_block(self):
        """
        gets the last block of the blockchain

        returns
        -------
        last block of the chain
        """
        return self.chain[-1]
    
    # proof work 
    # to increase the diffculty in mineing of a block of that blockchain becomes
    # safe it will be practically impossible the recompute all the hashes in the 
    # blockchain. It is implimented by making it compulsory for the hash to have certain 
    # numbers of zero. We keep on changing the value of the nounce till we get required hash  
    difficulty = 2
    def proof_of_work(self,block:Block):
        """
        calculate the hash of block as per required difficulty 

        Parameters
        ----------
        block:
            single block that is to be addded in the blockchain 
        
        returns:
        -------
            computed hash
        """ 
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0'*Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
            previous_hash = self.last_block.hash
            if previous_hash != block.previous_hash:
                return False
            if not self.is_valid_proof(block, proof):
                return False
            block.hash = proof
            self.chain.append(block)
            return True
    
    def is_valid_proof(self, block, block_hash):
            return (block_hash.startswith('0' * Blockchain.difficulty) and
                    block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
                self.unconfirmed_transactions.append(transaction)
    
    def mine(self):
            if not self.unconfirmed_transactions:
                return False
    
            last_block = self.last_block
    
            new_block = Block(index=last_block.index + 1,
                            transactions=self.unconfirmed_transactions,
                            timestamp=time.time(),
                            previous_hash=last_block.hash)
    
            proof = self.proof_of_work(new_block)
            self.add_block(new_block, proof)
            self.unconfirmed_transactions = []
            return new_block.index

app =  Flask(__name__)

blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})



app.run(debug=True, port=5000)