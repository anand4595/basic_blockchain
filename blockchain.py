from hashlib import sha256
import json

class Block:
    """Individual blocks in the blockchain"""
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