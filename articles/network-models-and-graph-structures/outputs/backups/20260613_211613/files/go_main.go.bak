package main

import "fmt"

type Edge struct {
	Source string
	Target string
	Weight float64
}

func main() {
	edges := []Edge{
		{"power_substation", "hospital", 0.95},
		{"power_substation", "water_treatment", 0.90},
		{"communications_hub", "hospital", 0.70},
		{"fuel_depot", "power_substation", 0.60},
		{"transport_hub", "hospital", 0.50},
		{"transport_hub", "fuel_depot", 0.65},
		{"water_treatment", "hospital", 0.80},
		{"emergency_depot", "hospital", 0.75},
		{"communications_hub", "emergency_depot", 0.55},
		{"power_substation", "communications_hub", 0.85},
	}

	inDegree := map[string]int{}
	outDegree := map[string]int{}
	weightedOut := map[string]float64{}
	nodes := map[string]bool{}

	for _, edge := range edges {
		nodes[edge.Source] = true
		nodes[edge.Target] = true
		outDegree[edge.Source]++
		inDegree[edge.Target]++
		weightedOut[edge.Source] += edge.Weight
	}

	fmt.Printf("go edge_count=%d node_count=%d\n", len(edges), len(nodes))
	for node := range nodes {
		fmt.Printf("%s in_degree=%d out_degree=%d weighted_out=%.2f\n", node, inDegree[node], outDegree[node], weightedOut[node])
	}
}
