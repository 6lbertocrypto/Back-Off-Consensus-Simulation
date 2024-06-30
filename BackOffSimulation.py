import random
import time
from collections import defaultdict

class BlockchainSimulator:
    def __init__(self, hold_back_period=3, num_blocks=20):
        self.hold_back_period = hold_back_period
        self.chain = []
        self.pending_blocks = []
        self.num_blocks = num_blocks
        self.current_block_number = 0
        self.miner_hold_back = defaultdict(int)  # dict to keep track of miners hold back periods
        self.support_mechanism = {}  # dict to keep track of supported blocks

    def mine_block(self, miner_id):
        
        # check if the miner is in hold back period
        if self.miner_hold_back[miner_id] > self.current_block_number:
            print(f"{miner_id} is in hold back period and cannot mine block {self.current_block_number}")
            return
        
        print(f"{miner_id} is trying to mine block {self.current_block_number}")
        block = {'block_number': self.current_block_number, 'miner_id': miner_id}
        self.pending_blocks.append(block)
        
        # simulate mining time and possibility of a conflicting block
        mining_time = random.uniform(0.1, 0.5)
        time.sleep(mining_time)
        
        # simulating conflicting block
        conflict = random.random() < 0.3  # %30 chance of conflict
        if conflict:
            conflicting_block = {'block_number': self.current_block_number, 'miner_id': f"Conflicting_{miner_id}"}
            self.support_mechanism[self.current_block_number] = conflicting_block
            print(f"Conflicting block detected for block {self.current_block_number}")

        if random.random() > 0.1 and not conflict:  # mining success rate
            self.chain.append(block)
            self.pending_blocks.remove(block)
            self.current_block_number += 1
            
            # set the hold back period for the miner
            self.miner_hold_back[miner_id] = self.current_block_number + self.hold_back_period
            print(f"Block {block['block_number']} successfully mined by {miner_id}")

        elif conflict:

            if self.resolve_conflict(block, conflicting_block):
                self.chain.append(block)
                self.pending_blocks.remove(block)
                self.current_block_number += 1
                self.miner_hold_back[miner_id] = self.current_block_number + self.hold_back_period
                print(f"Block {block['block_number']} successfully mined by {miner_id} after resolving conflict")
    
            else:
                print(f"{miner_id} failed to mine block {self.current_block_number} due to conflict")
                self.pending_blocks.remove(block)

        else:
            print(f"{miner_id} failed to mine block {self.current_block_number}")

    def resolve_conflict(self, block, conflicting_block):

        # simulate pow for both blocks
        block_pow = random.random()
        conflicting_block_pow = random.random()

        if block_pow > conflicting_block_pow:
            print(f"Block {block['block_number']} by {block['miner_id']} won against conflicting block")
            return True
        
        else:
            print(f"Conflicting block won against block {block['block_number']} by {block['miner_id']}")
            return False

    def simulate(self):
        
        miners = [f"Miner {i}" for i in range(1, 6)]

        for _ in range(self.num_blocks):
            
            miner_id = random.choice(miners)
            self.mine_block(miner_id)
            if self.current_block_number % self.hold_back_period == 0:
                print(f"Hold back period for {self.hold_back_period} blocks")
                time.sleep(1)  # hold back period

    def show_chain(self):
        print("Blockchain:")
        for block in self.chain:
            print(block)

# simulator

simulator = BlockchainSimulator()
simulator.simulate()
simulator.show_chain()
