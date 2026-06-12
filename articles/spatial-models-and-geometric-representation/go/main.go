package main

import (
	"fmt"
	"math"
)

type Location struct {
	Key   string
	Kind  string
	X     float64
	Y     float64
	Value float64
}

func distance(a Location, b Location) float64 {
	return math.Sqrt(math.Pow(a.X-b.X, 2) + math.Pow(a.Y-b.Y, 2))
}

func main() {
	locations := []Location{
		{"neighborhood_a", "demand", 0.0, 0.0, 1200},
		{"neighborhood_b", "demand", 2.0, 1.0, 900},
		{"neighborhood_c", "demand", 4.0, 2.5, 1400},
		{"neighborhood_d", "demand", 6.0, 1.5, 700},
		{"clinic_1", "service", 1.0, 0.5, 500},
		{"clinic_2", "service", 5.5, 2.0, 650},
		{"clinic_3", "service", 3.0, 4.0, 400},
	}

	for _, demand := range locations {
		if demand.Kind != "demand" {
			continue
		}
		nearest := ""
		nearestDistance := math.Inf(1)
		accessibility := 0.0
		for _, service := range locations {
			if service.Kind != "service" {
				continue
			}
			d := distance(demand, service)
			accessibility += service.Value / (1.0 + d)
			if d < nearestDistance {
				nearestDistance = d
				nearest = service.Key
			}
		}
		fmt.Printf("%s nearest=%s distance=%.3f accessibility=%.3f\n", demand.Key, nearest, nearestDistance, accessibility)
	}
}
