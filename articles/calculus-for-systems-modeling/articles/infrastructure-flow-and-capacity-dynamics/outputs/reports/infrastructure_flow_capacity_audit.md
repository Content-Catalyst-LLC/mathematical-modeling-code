# Infrastructure Flow and Capacity Audit

## Scenario Records
- **baseline_spare_capacity** (queue_capacity): final queue=0.00, average utilization=0.750, maximum delay=3.40. spare capacity keeps queues low.
- **near_capacity_operation** (queue_capacity): final queue=0.00, average utilization=0.950, maximum delay=16.20. near-capacity operation creates high delay sensitivity.
- **over_capacity_backlog** (queue_capacity): final queue=360.00, average utilization=1.150, maximum delay=800.20. arrival rate above capacity causes backlog accumulation.
- **series_bottleneck** (network_bottleneck): final queue=120.00, average utilization=1.056, maximum delay=800.20. minimum stage capacity limits effective throughput.
- **capacity_decay_case** (maintenance_capacity): final queue=427.45, average utilization=1.231, maximum delay=800.20. capacity decay can create congestion even if demand is unchanged.
- **peak_load_case** (peak_load_capacity): final queue=0.00, average utilization=0.950, maximum delay=16.20. peak-load scenario tests stress conditions beyond average demand.

## Bottleneck Records
- **series_process_bottleneck**: effective capacity=90.00; bottleneck stage=3. Effective capacity is limited by the smallest stage capacity.

Infrastructure model outputs depend on flow definitions, effective capacity, queues, bottlenecks, buffers, maintenance, failure modes, recovery assumptions, uncertainty, and claim boundaries.
