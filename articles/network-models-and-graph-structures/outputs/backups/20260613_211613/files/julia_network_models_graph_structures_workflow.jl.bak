# Julia workflow for network models and graph structures.
using Printf

struct Edge
    source::String
    target::String
    weight::Float64
end

function nodes(edges)
    return sort(unique(vcat([e.source for e in edges], [e.target for e in edges])))
end

function degree_diagnostics(edges)
    node_list = nodes(edges)
    incoming = Dict(n => 0 for n in node_list)
    outgoing = Dict(n => 0 for n in node_list)
    weighted_out = Dict(n => 0.0 for n in node_list)

    for edge in edges
        outgoing[edge.source] += 1
        incoming[edge.target] += 1
        weighted_out[edge.source] += edge.weight
    end

    for node in node_list
        @printf("%s in_degree=%d out_degree=%d weighted_out=%.2f\n", node, incoming[node], outgoing[node], weighted_out[node])
    end
end

function main()
    edges = [
        Edge("power_substation", "hospital", 0.95),
        Edge("power_substation", "water_treatment", 0.90),
        Edge("communications_hub", "hospital", 0.70),
        Edge("fuel_depot", "power_substation", 0.60),
        Edge("transport_hub", "hospital", 0.50),
        Edge("transport_hub", "fuel_depot", 0.65),
        Edge("water_treatment", "hospital", 0.80),
        Edge("emergency_depot", "hospital", 0.75),
        Edge("communications_hub", "emergency_depot", 0.55),
        Edge("power_substation", "communications_hub", 0.85)
    ]

    @printf("julia node_count=%d edge_count=%d\n", length(nodes(edges)), length(edges))
    degree_diagnostics(edges)
end

main()
