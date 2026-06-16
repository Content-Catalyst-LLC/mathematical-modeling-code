package main

import "fmt"

type Record struct {
	RecordType        string
	Name              string
	PatternOrElement  string
	ResponseOrWarning string
	Status            string
}

func main() {
	records := []Record{
		{"continuity_assumption", "smooth_state_change", "state_trajectory_x_t", "smooth_output_does_not_prove_smooth_system_behavior", "review"},
		{"continuity_assumption", "continuous_rate_function", "dxdt_equals_f", "rate_continuity_should_be_justified", "review"},
		{"risk_record", "false_smoothness", "smooth_curve_hides_structural_breaks", "test_for_breaks_and_document_discontinuities", "review"},
		{"risk_record", "equilibrium_bias", "steady_state_overinterpreted", "analyze_trajectories_and_stability", "review"},
		{"solver_diagnostic", "convergence_check", "numerical_solution_converged", "a_plotted_output_can_hide_convergence_failure", "review"},
	}
	fmt.Println("record_type,name,pattern_or_element,response_or_warning,status")
	for _, r := range records {
		fmt.Printf("%s,%s,%s,%s,%s\n", r.RecordType, r.Name, r.PatternOrElement, r.ResponseOrWarning, r.Status)
	}
}
