package cells

import "testing"

func TestResurrectAndKillCell(t *testing.T) {
	resetWorld() // there is no builtin `setup` and `teardown`
	resurrectCell(1, 5)
	if getCell(1, 5) == false {
		t.Errorf("Should be alive")
	}
	killCell(1, 5)
	if getCell(1, 5) == true {
		t.Errorf("Should be dead")
	}
}

func TestGetAliveNeighbours(t *testing.T) {
	resetWorld()
	resurrectCell(3, 4)
	count := getAliveNeighbours(3, 4)
	if count != 0 {
		t.Errorf("Should be exactly 0")
	}
	resurrectCell(3, 3)
	count = getAliveNeighbours(3, 4)
	if count != 1 {
		t.Errorf("Should be exactly 1")
	}
}

func TestGetNextGenStateUnderPopulation(t *testing.T) {
	resetWorld()
	resurrectCell(3, 7)
	alive := getNextGenState(3, 7)
	if alive {
		t.Errorf("3,7 Should be dead because of under population")
	}
	resurrectCell(4, 7)
	alive = getNextGenState(3, 7)
	if alive {
		t.Errorf("3,7 Should be dead because of under population")
	}
}

func TestGetNextGenStateOkayPopulation(t *testing.T) {
	resetWorld()
	resurrectCell(3, 7)
	resurrectCell(4, 7)
	resurrectCell(5, 7)
	alive := getNextGenState(4, 7)
	if !(alive) {
		t.Errorf("4,7 Should be alive")
	}
}

func TestGetNextGenStateOverPopulation(t *testing.T) {
	resetWorld()
	resurrectCell(3, 6)
	resurrectCell(4, 6)
	resurrectCell(5, 6)
	resurrectCell(4, 7)
	resurrectCell(5, 7)
	alive := getNextGenState(4, 7)
	if alive {
		t.Errorf("4,7 Should be dead")
	}
}

func TestGetNextGenStateReproduction(t *testing.T) {
	resetWorld()
	resurrectCell(3, 6)
	resurrectCell(4, 6)
	resurrectCell(5, 6)
	alive := getNextGenState(4, 7)
	if !(alive) {
		t.Errorf("4,7 Should be alive")
	}
}
