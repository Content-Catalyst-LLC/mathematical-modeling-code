struct Scenario
    name::String
    initial_state::Float64
    rate::Float64
    capacity::Float64
    time_horizon::Float64
end

function validate_domain(s::Scenario)
    issues = String[]
    if s.initial_state < 0 push!(issues, "initial_state must be nonnegative") end
    if s.rate < 0 push!(issues, "rate must be nonnegative") end
    if s.capacity <= 0 push!(issues, "capacity must be positive") end
    if s.time_horizon < 0 push!(issues, "time_horizon must be nonnegative") end
    if s.capacity > 0 && s.initial_state > s.capacity push!(issues, "initial_state exceeds capacity") end
    return issues
end

bounded_growth(s::Scenario) = s.capacity / (1 + ((s.capacity - s.initial_state) / s.initial_state) * exp(-s.rate * s.time_horizon))

scenarios = [
    Scenario("baseline", 10.0, 0.20, 100.0, 20.0),
    Scenario("near_capacity", 95.0, 0.20, 100.0, 20.0),
    Scenario("invalid_negative_state", -5.0, 0.20, 100.0, 20.0)
]

println("scenario,status,value_or_issue")
for s in scenarios
    issues = validate_domain(s)
    if length(issues) > 0
        println("$(s.name),domain_review,$(join(issues, "; "))")
    else
        println("$(s.name),ok,$(round(bounded_growth(s), digits=6))")
    end
end
