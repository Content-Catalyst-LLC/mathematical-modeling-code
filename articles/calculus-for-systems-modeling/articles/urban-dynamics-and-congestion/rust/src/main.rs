fn traffic_flow(density: f64, free_flow_speed: f64, jam_density: f64) -> f64 { (free_flow_speed * density * (1.0 - density / jam_density)).max(0.0) }
fn bpr_travel_time(free_flow_time: f64, volume: f64, capacity: f64) -> f64 { free_flow_time * (1.0 + 0.15 * (volume / capacity).powf(4.0)) }
fn queue_step(queue: f64, arrival: f64, service: f64, dt: f64) -> f64 { (queue + (arrival - service) * dt).max(0.0) }
fn main() {
    println!("scenario_name,model_type,flow,travel_time,queue_step,warning");
    println!("below_capacity_corridor,link_flow,{:.6},{:.6},{:.6},flow_unit_and_boundary_must_be_documented", traffic_flow(35.0,60.0,140.0), bpr_travel_time(20.0,1800.0,2000.0), queue_step(0.0,1800.0,2000.0,0.01));
    println!("over_capacity_bottleneck,queue_and_bpr,{:.6},{:.6},{:.6},over_capacity_delays_can_spill_back_upstream", traffic_flow(70.0,60.0,140.0), bpr_travel_time(20.0,2300.0,2000.0), queue_step(0.0,2300.0,2000.0,0.01));
}
