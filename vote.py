import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_votes = []
        self.create_block(previous_hash='1', proof=100)

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'votes': self.current_votes,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_votes = []
        self.chain.append(block)
        self.store_results()
        return block

    def add_vote(self, voter_id, candidate):
        vote = {'voter_id': voter_id, 'candidate': candidate}
        self.current_votes.append(vote)

    def proof_of_work(self, previous_proof):
        proof = 0
        while self.valid_proof(previous_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(previous_proof, proof):
        guess = f'{previous_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def get_last_block(self):
        return self.chain[-1]

    def store_results(self):
        with open("voting_results.txt", "w") as file:
            for block in self.chain:
                file.write(json.dumps(block, indent=4))
                file.write("\n")

# Example usage
blockchain = Blockchain()
blockchain.add_vote("Voter1", "Candidate1")
proof = blockchain.proof_of_work(blockchain.get_last_block()['proof'])
previous_hash = blockchain.hash(blockchain.get_last_block())
blockchain.create_block(proof, previous_hash)
import tkinter as tk
from tkinter import messagebox

blockchain = Blockchain()

def cast_vote():
    voter_id = voter_id_entry.get()
    candidate = candidate_var.get()
    if voter_id and candidate:
        blockchain.add_vote(voter_id, candidate)
        proof = blockchain.proof_of_work(blockchain.get_last_block()['proof'])
        previous_hash = blockchain.hash(blockchain.get_last_block())
        blockchain.create_block(proof, previous_hash)
        messagebox.showinfo("Vote Cast", "Your vote has been successfully cast!")
    else:
        messagebox.showerror("Error", "Please enter a valid voter ID and select a candidate.")

# Setting up the main window
window = tk.Tk()
window.title("Blockchain Voting System")

# Voter ID Input
tk.Label(window, text="Enter your Voter ID:").pack()
voter_id_entry = tk.Entry(window)
voter_id_entry.pack()

# Candidate Selection
tk.Label(window, text="Select a Candidate:").pack()
candidate_var = tk.StringVar(value="Candidate1")
tk.Radiobutton(window, text="Candidate 1", variable=candidate_var, value="Candidate1").pack(anchor=tk.W)
tk.Radiobutton(window, text="Candidate 2", variable=candidate_var, value="Candidate2").pack(anchor=tk.W)
tk.Radiobutton(window, text="Candidate 3", variable=candidate_var, value="Candidate3").pack(anchor=tk.W)

# Vote Button
vote_button = tk.Button(window, text="Cast Vote", command=cast_vote)
vote_button.pack()

window.mainloop()
