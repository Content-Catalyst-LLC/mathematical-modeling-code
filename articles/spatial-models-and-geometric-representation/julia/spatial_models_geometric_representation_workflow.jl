# Julia workflow for spatial models and geometric representation.
# Dependency-light: Base only.

using Printf

struct Location
    key::String
    kind::String
    x::Float64
    y::Float64
    value::Float64
end

function distance(a::Location, b::Location)
    return sqrt((a.x - b.x)^2 + (a.y - b.y)^2)
end

function main()
    locations = [
        Location("neighborhood_a", "demand", 0.0, 0.0, 1200.0),
        Location("neighborhood_b", "demand", 2.0, 1.0, 900.0),
        Location("neighborhood_c", "demand", 4.0, 2.5, 1400.0),
        Location("neighborhood_d", "demand", 6.0, 1.5, 700.0),
        Location("clinic_1", "service", 1.0, 0.5, 500.0),
        Location("clinic_2", "service", 5.5, 2.0, 650.0),
        Location("clinic_3", "service", 3.0, 4.0, 400.0)
    ]

    demand = filter(l -> l.kind == "demand", locations)
    services = filter(l -> l.kind == "service", locations)

    for area in demand
        distances = [(service.key, distance(area, service)) for service in services]
        nearest = reduce((a, b) -> a[2] <= b[2] ? a : b, distances)
        accessibility = sum(service.value / (1.0 + distance(area, service)) for service in services)
        @printf("%s nearest=%s distance=%.3f accessibility=%.3f\n", area.key, nearest[1], nearest[2], accessibility)
    end
end

main()
