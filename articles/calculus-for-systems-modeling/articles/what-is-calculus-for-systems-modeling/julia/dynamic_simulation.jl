# What Is Calculus for Systems Modeling?
# Dependency-light Julia dynamic simulation.

struct Scenario
    name::String
    initial_state::Float64
    rate::Float64
    capacity::Float64
    dt::Float64
    steps::Int
end

function simulate(s::Scenario)
    state = s.initial_state
    for _ in 1:s.steps
        derivative = s.rate * state * (1.0 - state / s.capacity)
        state = max(0.0, state + derivative * s.dt)
    end
    return state
end

scenarios = [
    Scenario("baseline", 10.0, 0.20, 100.0, 0.1, 300),
    Scenario("slow_adjustment", 10.0, 0.10, 100.0, 0.1, 300),
    Scenario("high_capacity", 10.0, 0.20, 140.0, 0.1, 300)
]

println("scenario,final_state")
for s in scenarios
    println("$(s.name),$(round(simulate(s), digits=6))")
end
