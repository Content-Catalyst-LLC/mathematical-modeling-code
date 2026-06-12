using Printf, Statistics
struct ComponentScenario
    name::String; initial_stock::Float64; capacity::Float64; inflow::Float64; demand::Float64; loss_rate::Float64; periods::Int
end
bounded_update(raw_next, capacity) = min(capacity, max(0.0, raw_next))
function simulate(s::ComponentScenario)
    stock=s.initial_stock; rows=[]
    for period in 0:s.periods
        losses=s.loss_rate*stock; raw_next=stock+s.inflow-s.demand-losses
        push!(rows,(stock=stock,shortage=max(0.0,-raw_next),overflow=max(0.0,raw_next-s.capacity)))
        stock=bounded_update(raw_next,s.capacity)
    end
    rows
end
for s in [ComponentScenario("julia_baseline",80,100,8,6,0.015,60), ComponentScenario("julia_constraint_stress",40,60,3,7,0.050,60)]
    rows=simulate(s); stocks=[r.stock for r in rows]; shortages=[r.shortage for r in rows]; overflows=[r.overflow for r in rows]
    @printf("%s final_stock=%.3f mean_stock=%.3f total_shortage=%.3f total_overflow=%.3f\n", s.name, stocks[end], mean(stocks), sum(shortages), sum(overflows))
end
