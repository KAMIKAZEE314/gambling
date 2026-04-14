from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Middleware hinzufuegen
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

num2symbol = {
    0: "L",
    1: "C",
    2: "K",
    3: "B",
    4: "D",
    5: "T",
    6: "7"
}

num2value = {
    0: 2,
    1: 2,
    2: 3,
    3: 3,
    4: 5,
    5: 5,
    6: 7,
}

patterns = [
    ([(0, 0),(0, 1),(0, 2),(0, 3),(0, 4),(1, 0),(1, 1),(1, 2),(1, 3),(1, 4),(2, 0),(2, 1),(2, 2),(2, 3),(2, 4)], 10, []),
    ([(0, 1),(0, 2),(0, 3),(1, 0),(1, 1),(1, 3),(1, 4),(2, 1),(2, 2),(2, 3)], 8, []),
    ([(0, 0),(0, 1),(0, 2),(0, 3),(0, 4),(1, 1),(1, 3),(2, 2)], 7, []),
    ([(0, 2),(1, 1),(1, 3),(0, 0),(0, 1),(0, 2),(0, 3),(0, 4)], 7, []),
    ([(0, 0),(0, 4),(1, 1),(1, 3),(2, 2)], 4, []),
    ([(0, 2),(1, 1),(1, 3),(2, 0),(2, 4)], 4, []),
    ([(0, 0),(0, 1),(0, 2),(0, 3),(0, 4)], 3, [7, 11]),
    ([(0, 0),(0, 1),(0, 2),(0, 3)], 2, [11]),
    ([(0, 2),(1, 1),(2, 0)], 1, []),
    ([(0, 0),(1, 1),(2, 2)], 1, []),
    ([(0, 0),(1, 0),(2, 0)], 1, []),
    ([(0, 0),(0, 1),(0, 2)], 1, [])
]

@app.get("/spin")
def spin():
	roll = []
	for row in range(3):
		roll.append([])
		for column in range(5):
			random_num = int.from_bytes(os.urandom(5), "big") % 1000
			symbol = None
			if random_num in range(194):
				symbol = 0
			elif random_num in range(194, 388):
				symbol = 1
			elif random_num in range(388, 537):
				symbol = 2
			elif random_num in range(537, 686):
				symbol = 3
			elif random_num in range(686, 805):
				symbol = 4
			elif random_num in range(805, 924):
				symbol = 5
			elif random_num in range(924, 1000):
				symbol = 6
			roll[-1].append((int.from_bytes(os.urandom(1), "big") % 7, []))

	value = 0
	for y, row in enumerate(patterns):
		for x, column in enumerate(row):
			for pattern in patterns:
				selected_tiles, multiplier, conflicting_patterns = pattern

				was_canceled = False
				check_symbol = None
				for tile in selected_tiles:
					tile_y, tile_x = tile
					if tile_x >= 0 and tile_x + x < 5 and tile_y >= 0 and tile_y + y < 3:
						if not patterns.index(pattern) in roll[tile_y + y][tile_x + x][1]:
							if not check_symbol:
								check_symbol = roll[tile_y + y][tile_x + x][0]
							else:
								if check_symbol != roll[tile_y + y][tile_x + x][0]:
									was_canceled = True
									break
						else:
							was_canceled = True
							break
					else:
						was_canceled = True
						break

				if not was_canceled:
					for tile_y, tile_x in selected_tiles:
						symbol, excluded_patterns = roll[tile_y + y][tile_x + x]

						excluded_patterns += conflicting_patterns

					value += num2value[check_symbol] * len(selected_tiles) * multiplier

	display_roll = []
	for row in roll:
		for column in row:
			display_roll.append(num2symbol[column[0]])

	return {"roll": display_roll, "value": value}
