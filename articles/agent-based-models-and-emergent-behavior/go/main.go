package main

import "fmt"

func neighbors(i int, n int) []int {
	return []int{(i - 2 + n) % n, (i - 1 + n) % n, (i + 1) % n, (i + 2) % n}
}

func main() {
	n := 20
	steps := 10
	threshold := 0.35
	adopted := make([]bool, n)

	for _, idx := range []int{0, 1, 2} {
		adopted[idx] = true
	}

	for t := 0; t <= steps; t++ {
		count := 0
		for _, state := range adopted {
			if state {
				count++
			}
		}
		fmt.Printf("go step=%d adopted=%d share=%.3f\n", t, count, float64(count)/float64(n))

		next := make([]bool, n)
		copy(next, adopted)

		for i := 0; i < n; i++ {
			if adopted[i] {
				continue
			}
			local := neighbors(i, n)
			adoptedNeighbors := 0
			for _, j := range local {
				if adopted[j] {
					adoptedNeighbors++
				}
			}
			if float64(adoptedNeighbors)/float64(len(local)) >= threshold {
				next[i] = true
			}
		}
		adopted = next
	}
}
