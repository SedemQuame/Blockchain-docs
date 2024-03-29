# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import datetime
import hashlib
import json

from flask import Flask, jsonify

#Part 1 - Building a Blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash
                }
        self.chain.append(block)
        return block
    
    # getting previous block
    def get_previous_block(self):
        return self.chain[-1]
    
    # getting the proof of work. (hard to find solution, but easy to verify)
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True 
            else:
                new_proof += 1
            return new_proof
        
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()   
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            # check if hash operation starts with 4 leading 0000s
            if hash_operation[:4] != '0000':
                return False
            #updating variable indices
            previous_block = block
            block_index += 1
        return True
    

#Part 2 - Mining our Blockchain
#=======================================================
#Creating a Web App using Flask
app = Flask(__name__)
        
#Creating a Blockchain
blockchain = Blockchain()

#Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash()
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

  