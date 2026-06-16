struct Record {
    record_type: &'static str,
    name: &'static str,
    pattern_or_element: &'static str,
    response_or_warning: &'static str,
    status: &'static str,
}

fn main() {
    let records = [
        Record { record_type: "continuity_assumption", name: "smooth_state_change", pattern_or_element: "state_trajectory_x_t", response_or_warning: "smooth_output_does_not_prove_smooth_system_behavior", status: "review" },
        Record { record_type: "continuity_assumption", name: "continuous_rate_function", pattern_or_element: "dxdt_equals_f", response_or_warning: "rate_continuity_should_be_justified", status: "review" },
        Record { record_type: "risk_record", name: "false_smoothness", pattern_or_element: "smooth_curve_hides_structural_breaks", response_or_warning: "test_for_breaks_and_document_discontinuities", status: "review" },
        Record { record_type: "risk_record", name: "equilibrium_bias", pattern_or_element: "steady_state_overinterpreted", response_or_warning: "analyze_trajectories_and_stability", status: "review" },
        Record { record_type: "solver_diagnostic", name: "convergence_check", pattern_or_element: "numerical_solution_converged", response_or_warning: "a_plotted_output_can_hide_convergence_failure", status: "review" },
    ];
    println!("record_type,name,pattern_or_element,response_or_warning,status");
    for r in records {
        println!("{},{},{},{},{}", r.record_type, r.name, r.pattern_or_element, r.response_or_warning, r.status);
    }
}
