fn rates(prey: f64, predator: f64, alpha: f64, beta: f64, delta: f64, gamma: f64) -> (f64, f64) {
    (alpha*prey - beta*prey*predator, delta*prey*predator - gamma*predator)
}
fn main() {
    let mut prey = 40.0;
    let mut predator = 9.0;
    let alpha = 0.7;
    let beta = 0.05;
    let delta = 0.02;
    let gamma = 0.5;
    let dt = 0.01;
    println!("scenario,time,prey,predator,prey_rate,predator_rate,alpha,beta,delta,gamma,method,warning");
    for n in 0..=2000 {
        let t = n as f64 * dt;
        let (prey_rate, predator_rate) = rates(prey, predator, alpha, beta, delta, gamma);
        println!("predator_prey_coupled_system,{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},explicit_euler,Predator-prey terms are illustrative and assume continuous well-mixed interaction.", t, prey, predator, prey_rate, predator_rate, alpha, beta, delta, gamma);
        prey = (prey + dt*prey_rate).max(0.0);
        predator = (predator + dt*predator_rate).max(0.0);
    }
}
