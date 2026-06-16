package main

import "fmt"

type Record struct {
	RecordType     string
	Name           string
	Value          string
	Unit           string
	Interpretation string
	Warning        string
}

func main() {
	records := []Record{
		{"unit_record", "population_stock", "40", "state units", "synthetic teaching value", "synthetic value do not treat as empirical measurement"},
		{"unit_record", "carrying_capacity", "100", "state units", "synthetic teaching capacity", "capacity scale controls normalized interpretation"},
		{"unit_record", "growth_rate", "0.35", "per time unit", "synthetic teaching rate", "rate units must match the time variable"},
		{"scale_record", "stock_scale", "100", "state units", "carrying capacity used to normalize population stock", "changing the scale changes dimensionless stock"},
		{"nondimensional_record", "scaled_stock", "0.4", "dimensionless", "population stock as fraction of carrying capacity", "dimensionless form depends on documented scale"},
	}
	fmt.Println("record_type,name,value,unit,interpretation,warning")
	for _, r := range records {
		fmt.Printf("%s,%s,%s,%s,%s,%s\n", r.RecordType, r.Name, r.Value, r.Unit, r.Interpretation, r.Warning)
	}
}
