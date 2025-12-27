from toot_otto import OttoTootIA
import time

def run_test(depth):
    print(f"Testing depth {depth}...")
    start = time.time()
    game = OttoTootIA()
    score = game.minimax_alpha_beta(depth, -float('inf'), float('inf'), True)
    end = time.time()
    print(f"Depth {depth}: Score = {score}, Time = {end - start:.2f}s, Nodes = {game.nos_visitados}")

if __name__ == "__main__":
    # run_test(5) # Commented out to avoid long wait if 5 is too slow, but let's try 5.
    pass
