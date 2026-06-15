fn main(){
    let duration = [1.0,1.0,1.0,1.0,1.0];
    let inflow = [12.0,10.0,9.0,8.0,7.0];
    let outflow = [6.0,7.0,8.0,9.0,9.0];
    let exposure = [20.0,18.0,15.0,13.0,11.0];
    let population = [1000.0,1100.0,1050.0,980.0,960.0];
    let initial_stock = 50.0;

    let mut cumulative_in = 0.0;
    let mut cumulative_out = 0.0;
    let mut cumulative_exposure = 0.0;
    let mut pop_exposure = 0.0;

    for i in 0..duration.len() {
        cumulative_in += inflow[i]*duration[i];
        cumulative_out += outflow[i]*duration[i];
        cumulative_exposure += exposure[i]*duration[i];
        pop_exposure += exposure[i]*population[i]*duration[i];
    }

    let net = cumulative_in - cumulative_out;
    let ending_stock = initial_stock + net;
    let gross = cumulative_in + cumulative_out;

    println!("initial_stock,cumulative_inflow,cumulative_outflow,net_accumulation,ending_stock,cumulative_exposure,population_weighted_exposure,gross_activity");
    println!("{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6}",initial_stock,cumulative_in,cumulative_out,net,ending_stock,cumulative_exposure,pop_exposure,gross);
}
