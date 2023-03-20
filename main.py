import datetime as dt
import hashlib
import json
from file import *
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['college']
collection = db['blockTest']


class Blockchain:
    def __init__(self) -> None:
        self.chain = list()
        start_block = self.create_block("This is the Genesis block", 1, "0", 1)
        collection.insert_one(start_block)
        self.chain.append(start_block)

    def mine_block(self, data) -> dict:
        previous_block = self.get_previous_block()
        previous_proof = previous_block["proof"]
        index = len(self.chain) + 1
        proof = self.proof_of_work(previous_proof, index, data["id"])
        previous_hash = self.hash(previous_block)
        # previous_hash = "Hash value"
        block = self.create_block(data, proof, previous_hash, index)
        collection.insert_one(block)
        self.chain.append(block)
        return block

    def hash(self, block: dict) -> str:
        """
        hash a block and return the cryptographic hash value
        """
        encoded_block = json.dumps(block, sort_keys=True, default=str).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    # A mathematical computation
    def to_digest(self, new_proof: int, previous_proof: int, index: int, data: str) -> bytes:
        toDigest = str(new_proof ** 2 - previous_proof ** 2 + index) + data

        return toDigest.encode()

    # a number that meet some requirement (0 to some value)
    def proof_of_work(self, previous_proof: str, index: int, data: str) -> int:
        new_proof = 1
        check_proof = False

        while not check_proof:
            # print(new_proof)
            digest = self.to_digest(new_proof, previous_proof, index, data)

            hash_value = hashlib.sha256(digest).hexdigest()

            if hash_value[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def get_previous_block(self) -> dict:
        return self.chain[-1]

    def create_block(self, data: str, proof: int, prev_hash: str, index: int) -> dict:
        block = {
            "index": index,
            "timestamp": str(dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": prev_hash,
        }

        return block
