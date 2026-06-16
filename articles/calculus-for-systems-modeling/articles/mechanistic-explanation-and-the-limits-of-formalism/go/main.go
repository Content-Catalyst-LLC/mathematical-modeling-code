package main

import "fmt"

type Record struct {
	RecordType            string
	Name                  string
	RoleOrProcess         string
	EvidenceOrRequirement string
	Status                string
	Warning               string
}

func main() {
	records := []Record{
		{"mechanism_record", "stock_flow_accumulation", "stock changes through inflow and outflow", "synthetic teaching example", "review", "flows must represent real processes"},
		{"mechanism_record", "balancing_feedback", "state-dependent adjustment limits growth", "formal teaching example", "review", "feedback parameters require evidence"},
		{"formal_record", "differential_equation", "dxdt=f", "process interpretation required", "review", "rate equation needs mechanism meaning"},
		{"claim_record", "mechanistic", "organized process produces behavior", "process evidence required", "review", "scope depends on assumptions"},
		{"claim_record", "exploratory", "investigates possible behavior", "scenario assumptions required", "active", "not a confirmed mechanism or forecast"},
	}
	fmt.Println("record_type,name,role_or_process,evidence_or_requirement,status,warning")
	for _, r := range records {
		fmt.Printf("%s,%s,%s,%s,%s,%s\n", r.RecordType, r.Name, r.RoleOrProcess, r.EvidenceOrRequirement, r.Status, r.Warning)
	}
}
