function saddle_node_equilibria(mu)
    if mu < 0
        return Float64[]
    elseif abs(mu) < 1e-12
        return [0.0]
    else
        root = sqrt(mu)
        return [-root, root]
    end
end

saddle_node_derivative(x) = -2.0 * x

function classify_scalar_stability(d; tolerance=1e-8)
    if d < -tolerance
        return "locally_stable"
    elseif d > tolerance
        return "locally_unstable"
    else
        return "inconclusive_at_critical_value"
    end
end

println("model,parameter_mu,equilibrium,derivative_value,stability,branch_status,warning")
for step in -20:40
    mu = step / 10
    equilibria = saddle_node_equilibria(mu)
    if isempty(equilibria)
        println(join(("saddle_node_normal_form", mu, "", "", "no_real_equilibrium", "equilibrium_absent", "For mu below zero the saddle-node normal form has no real equilibrium."), ","))
    else
        for eq in equilibria
            d = saddle_node_derivative(eq)
            status = abs(mu) < 1e-12 ? "critical_branch" : "equilibrium_present"
            println(join(("saddle_node_normal_form", mu, eq, d, classify_scalar_stability(d), status, "Bifurcation interpretation depends on model form parameter meaning and domain validity."), ","))
        end
    end
end
