struct ModelParameters
    growth_rate::Float64
    carrying_capacity::Float64
    initial_stock::Float64
    time_step::Float64
    horizon::Float64
end

struct ModelState
    model_time::Float64
    stock::Float64
end

function step_logistic(params::ModelParameters, state::ModelState)
    dx = params.growth_rate * state.stock * (1 - state.stock / params.carrying_capacity)
    ModelState(state.model_time + params.time_step, state.stock + params.time_step * dx)
end

function simulate(params::ModelParameters)
    states = [ModelState(0.0, params.initial_stock)]
    while states[end].model_time < params.horizon
        push!(states, step_logistic(params, states[end]))
    end
    states
end

params = ModelParameters(0.35, 100.0, 10.0, 0.25, 20.0)
states = simulate(params)
final = states[end]

println("model_use,growth_rate,carrying_capacity,initial_stock,time_step,horizon,final_time,final_stock,warning")
println(join(("governance_review", params.growth_rate, params.carrying_capacity, params.initial_stock, params.time_step, params.horizon, final.model_time, final.stock, "Typed records improve structural review but do not prove empirical validity."), ","))
