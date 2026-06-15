emissions(t) = 50.0 * exp(0.015 * t)
emissions_rate(t) = 0.015 * emissions(t)
concentration(e) = 0.5 * e
d_concentration_d_emissions(e) = 0.5
forcing(c) = log(1.0 + c)
d_forcing_d_concentration(c) = 1.0 / (1.0 + c)
temperature_response(f) = 1.2 * f
d_temperature_d_forcing(f) = 1.2

println("t,emissions,concentration,forcing,temperature,emissions_rate,d_concentration_d_emissions,d_forcing_d_concentration,d_temperature_d_forcing,total_derivative")
for t in [0.0, 5.0, 10.0, 20.0, 40.0]
    e = emissions(t)
    c = concentration(e)
    f = forcing(c)
    temp = temperature_response(f)
    s1 = emissions_rate(t)
    s2 = d_concentration_d_emissions(e)
    s3 = d_forcing_d_concentration(c)
    s4 = d_temperature_d_forcing(f)
    total = s4 * s3 * s2 * s1
    println("$t,$e,$c,$f,$temp,$s1,$s2,$s3,$s4,$total")
end
