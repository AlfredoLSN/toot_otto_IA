from toot_otto import OttoTootIA

game = OttoTootIA()

# Test 1: Empty board
print(f"Empty board score: {game.evaluate_state()}")

# Test 2: TO.. pattern
game.make_move(0, 'T')
game.make_move(1, 'O')
print(f"Board with TO.. at bottom: {game.evaluate_state()}")
# Expected: some positive score for TO..

# Test 3: OT.. pattern
game = OttoTootIA()
game.make_move(0, 'O')
game.make_move(1, 'T')
print(f"Board with OT.. at bottom: {game.evaluate_state()}")
# Expected: some negative score for OT..

# Test 4: TOOT pattern
game = OttoTootIA()
game.make_move(0, 'T')
game.make_move(1, 'O')
game.make_move(2, 'O')
game.make_move(3, 'T')
print(f"Board with TOOT at bottom: {game.evaluate_state()}")
