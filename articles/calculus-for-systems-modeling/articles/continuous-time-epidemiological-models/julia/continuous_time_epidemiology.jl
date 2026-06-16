basic_reproduction_number(beta, gamma) = beta / gamma
doubling_time(r) = r <= 0 ? Inf : log(2) / r

function simulate_sir(population, s0, i0, r0, beta, gamma, dt, steps)
    s = s0
    i = i0
    r = r0
    peak_i = i
    for _ in 1:steps
        incidence = beta * s * i / population
        recovery = gamma * i
        s = max(0.0, s - incidence * dt)
        i = max(0.0, i + (incidence - recovery) * dt)
        r = min(population, r + recovery * dt)
        peak_i = max(peak_i, i)
    end
    return s, i, r, peak_i
end

baseline = simulate_sir(100000.0, 99900.0, 100.0, 0.0, 0.32, 0.10, 0.1, 1600)
reduced = simulate_sir(100000.0, 99900.0, 100.0, 0.0, 0.22, 0.10, 0.1, 1600)

println("scenario_name,model_type,peak_infectious,final_recovered,reproduction_number,warning")
println("baseline_sir,SIR,$(baseline[4]),$(baseline[3]),$(basic_reproduction_number(0.32,0.10)),baseline scenario")
println("reduced_transmission_sir,SIR,$(reduced[4]),$(reduced[3]),$(basic_reproduction_number(0.22,0.10)),reduced transmission")
