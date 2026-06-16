# Urban Dynamics and Congestion Audit

## Scenario Records
- **below_capacity_corridor** (queue_and_bpr): demand=1800.0, capacity=2000.0, final queue=0.00, total delay=0.00, travel time=21.97. demand below capacity produces limited queue accumulation.
- **over_capacity_bottleneck** (queue_and_bpr): demand=2300.0, capacity=2000.0, final queue=900.00, total delay=1354.50, travel time=25.25. demand above capacity produces persistent queue and delay.
- **capacity_expansion_with_induced_demand** (capacity_adjustment): demand=2540.9, capacity=2600.0, final queue=0.00, total delay=0.00, travel time=22.74. capacity expansion may reduce delay while long-run demand adjusts upward.
- **transit_priority_case** (multimodal_capacity): demand=1200.0, capacity=1600.0, final queue=0.00, total delay=0.00, travel time=20.95. transit priority can reduce person-delay when person throughput is considered.

## Diagnostic Records
- **critical_density_example**: 70.000 vehicles per kilometer. Critical density depends on the selected flow-density relation.
- **flow_at_density_example**: 1575.000 vehicles per hour. Fundamental diagrams are context-specific, not universal laws.
- **accessibility_example**: 523.828 weighted opportunities. Accessibility depends on opportunity definition and travel-cost assumptions.
- **distributional_delay_burden_example**: 110.000 weighted minutes. Average delay can hide unequal burden.
- **curb_occupancy_step_example**: 19.000 occupied spaces. Curb dynamics can reduce effective road and transit capacity.

Urban congestion model outputs depend on system boundaries, flow definitions, capacity assumptions, behavioral response, mode options, land-use feedback, equity outputs, uncertainty, and claim boundaries.
