package main

import "fmt"

type Artifact struct {
	Name string
	Type string
	Path string
	Origin string
	Role string
	Warning string
}

func main() {
	artifacts := []Artifact{
		{"parameter_records", "csv", "data/parameter_records.csv", "source", "documents parameter names values units sources and ranges", "Parameter records do not prove empirical correctness."},
		{"model_outputs", "csv", "outputs/tables/model_outputs.csv", "generated", "stores computed trajectory or summary outputs", "Generated outputs require diagnostics and interpretation limits."},
		{"diagnostics", "json", "outputs/json/diagnostics.json", "generated", "records validation convergence and warning status", "Diagnostics should remain attached to interpretation."},
		{"governance_queue", "markdown", "outputs/reports/governance_queue.md", "generated", "collects warnings requiring human review", "Governance queues support judgment but do not replace it."},
	}
	fmt.Println("artifact_name,artifact_type,path,source_or_generated,review_role,warning")
	for _, a := range artifacts {
		fmt.Printf("%s,%s,%s,%s,%s,%s\n", a.Name, a.Type, a.Path, a.Origin, a.Role, a.Warning)
	}
}
