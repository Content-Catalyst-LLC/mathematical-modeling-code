println("scenario,model_type,time,analytical_state,euler_state,absolute_error,rate_at_euler_state,growth_rate,carrying_capacity,initial_state,method")
for kind in ["exponential", "logistic"]
    x0=10.0; x=10.0; r=0.25; k=100.0; dt=0.1
    for n in 0:100
        t=n*dt
        analytical = kind == "exponential" ? x0*exp(r*t) : k/(1+((k-x0)/x0)*exp(-r*t))
        rate = kind == "exponential" ? r*x : r*x*(1-x/k)
        println(join((kind*"_growth",kind,t,analytical,x,abs(analytical-x),rate,r,kind=="exponential" ? "NA" : k,x0,"analytical_vs_explicit_euler"), ","))
        x += dt*rate
    end
end
