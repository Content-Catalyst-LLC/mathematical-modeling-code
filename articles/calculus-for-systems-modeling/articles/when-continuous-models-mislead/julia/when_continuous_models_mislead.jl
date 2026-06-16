records = [
    ("continuity_assumption", "smooth_state_change", "state trajectory x(t)", "smooth output does not prove smooth system behavior", "review"),
    ("continuity_assumption", "continuous_rate_function", "dx/dt=f(x,t,theta)", "rate continuity should be justified at modeled scale", "review"),
    ("risk_record", "false_smoothness", "smooth curve hides structural breaks", "test for breaks and document discontinuities", "review"),
    ("risk_record", "equilibrium_bias", "steady-state result is overinterpreted", "analyze trajectories and stability", "review"),
    ("solver_diagnostic", "convergence_check", "records whether numerical solution converged", "a plotted output can hide convergence failure", "review")
]

println("record_type,name,model_element_or_pattern,warning_or_response,status")
for row in records
    println(join(row, ","))
end
