package cells

var world [10][10]bool

func resetWorld() {
	// world = [10][10]bool  # doesn't work
	for row := 0; row < len(world); row++ {
		for col := 0; col < len(world[row]); col++ {
			world[row][col] = false
		}
	}
}

func resurrectCell(row int, col int) {
	world[row][col] = true
}

func killCell(row int, col int) {
	world[row][col] = false
}

func getCell(row int, col int) bool {
	return world[row][col]
}

func getAliveNeighbours(row int, col int) int {
	count := 0
	// count += int(getCell(row-1, col-1))  # does not work
	if getCell(row-1, col-1) {
		count++
	}
	if getCell(row-1, col) {
		count++
	}
	if getCell(row-1, col+1) {
		count++
	}
	if getCell(row, col-1) {
		count++
	}
	if getCell(row, col+1) {
		count++
	}
	if getCell(row+1, col-1) {
		count++
	}
	if getCell(row+1, col) {
		count++
	}
	if getCell(row+1, col+1) {
		count++
	}
	return count
}

func getNextGenState(row int, col int) bool {
	alive := getCell(row, col)
	alive_neighbours := getAliveNeighbours(row, col)

	if alive && alive_neighbours < 2 {
		return false
	}
	if alive && alive_neighbours >= 2 && alive_neighbours <= 3 {
		return true
	}
	if alive && alive_neighbours > 3 {
		return false
	}
	if !(alive) && alive_neighbours == 3 {
		return true
	}

	// should not happen
	return false
}
