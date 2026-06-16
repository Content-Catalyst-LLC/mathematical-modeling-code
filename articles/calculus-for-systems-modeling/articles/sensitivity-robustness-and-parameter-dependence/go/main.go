package main

import "fmt"

type Record struct {
	Parameter string
	Baseline  float64
	Lower     float64
	Upper     float64
	Status    string
	Warning   string
}

func main() {
	records := []Record{
		{"growth_rate", 0.35, 0.20, 0.50, "sensitive", "conclusion may depend on growth-rate assumptions"},
		{"carrying_capacity", 100.0, 75.0, 125.0, "sensitive", "capacity scale affects final stock interpretation"},
		{"initial_stock", 10.0, 5.0, 20.0, "stable", "output variation is limited across this synthetic range"},
	}
	fmt.Println("parameter_name,baseline_value,lower_bound,upper_bound,status,warning")
	for _, r := range records {
		fmt.Printf("%s,%.6f,%.6f,%.6f,%s,%s\n", r.Parameter, r.Baseline, r.Lower, r.Upper, r.Status, r.Warning)
	}
}
