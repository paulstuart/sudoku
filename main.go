package main

// a brute force Sudoku problem solver

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"
)

// Sudoku is the puzzle data
type Sudoku [9][9]int

// String allows printing the puzzle
func (s Sudoku) String() string {
	var b bytes.Buffer
	for _, row := range s {
		var strs [9]string
		for i, value := range row {
			if value > 0 {
				strs[i] = fmt.Sprint(value)
			} else {
				strs[i] = " "
			}
		}
		fmt.Fprintf(&b, "%s\n", strings.Join(strs[:], " "))
	}
	return b.String()
}

// Count returns the count of valid cells
func (s *Sudoku) Count() int {
	count := 0
	for _, row := range s {
		for _, n := range row {
			if n > 0 {
				count++
			}
		}
	}
	return count
}

// Status prints the Sudoku puzzle and it's completion status
func (s Sudoku) Status(msg string) {
	fmt.Println()
	fmt.Printf("completed: %d/81 (%s)\n", s.Count(), msg)
	fmt.Println(s)
	if x, y := s.Valid(); x >= 0 || y >= 0 {
		log.Fatalf("invalid cell: %d, %d\n\n", x, y)
	}
}

// Valid returns the coordinates of the first invalid cell (if any)
func (s *Sudoku) Valid() (int, int) {
	for y, row := range s {
		for x, n := range row {
			if s.Conflicted(x, y, n) {
				return x, y
			}
		}
	}
	return -1, -1
}

// Conflicted returns true if 'n' has a conflict
func (s *Sudoku) Conflicted(x, y, n int) bool {
	if n == 0 {
		return false
	}
	// any dupes in the row?
	for i, col := range s[y] {
		if col == n && i != x {
			return true
		}
	}

	// any dupes in the column?
	for j, row := range s {
		if row[x] == n && j != y {
			return true
		}
	}

	// any dupes in our square?
	x2 := (x / 3) * 3
	y2 := (y / 3) * 3
	for i, row := range s[y2 : y2+3] {
		for k, col := range row[x2 : x2+3] {
			if x != x2+k && y != y2+i && n == col {
				return true
			}
		}
	}

	// all good!
	return false
}

// TODO: make random -- so solutions vary
func random() []int {
	return []int{1, 2, 3, 4, 5, 6, 7, 8, 9}
}

// Solve does recursive guesses at cell numbers
// by working with copies of the puzzle
// it can "backtrack" with a good copy at any point
func Solve(so Sudoku, col, row int) (Sudoku, bool) {
	if col > 8 {
		col = 0
		row++
	}
	if row > 8 {
		// done, no more recursion
		return so, true
	}
	// already set?
	if so[row][col] > 0 {
		return Solve(so, col+1, row)
	}
	try := random()
	for _, n := range try {
		//if okay(so, col, row, n) {
		if !so.Conflicted(col, row, n) {
			so[row][col] = n
			solved, ok := Solve(so, col+1, row)
			if ok {
				return solved, true
			}
		}
	}
	// this is a dead end, retry up the call stack
	return so, false
}

// Loadfile loads an ascii representation of the Sudoku puzzle
func Loadfile(filename string) Sudoku {
	text, err := ioutil.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}
	var so Sudoku
	for y, line := range strings.Split(string(text), "\n") {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		cols := strings.Fields(line)
		if len(cols) != 9 {
			log.Fatalf("expected 9 columns but got %d for %q\n", len(cols), line)
		}
		for x, col := range cols {
			switch col {
			case "_", "-":
			default:
				n, err := strconv.Atoi(col)
				if err != nil {
					log.Fatal(err)
				}
				if n > 9 {
					log.Fatalf("too big: %d", n)
				}
				so[y][x] = n
			}
		}
	}
	return so
}

func main() {
	args := os.Args
	if len(args) < 2 {
		log.Fatal("missing filename")
	}
	so := Loadfile(args[1])
	so.Status("starting")
	solved, ok := Solve(so, 0, 0)
	if !ok {
		fmt.Println("failed...")
	}
	solved.Status("finished")

}
