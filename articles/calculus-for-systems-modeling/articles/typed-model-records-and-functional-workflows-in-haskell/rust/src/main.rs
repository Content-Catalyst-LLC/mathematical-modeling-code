struct ModelParameters {
    growth_rate: f64,
    carrying_capacity: f64,
    initial_stock: f64,
    time_step: f64,
    horizon: f64,
}

struct ModelState {
    model_time: f64,
    stock: f64,
}

fn step_logistic(params: &ModelParameters, state: &ModelState) -> ModelState {
    let dx = params.growth_rate * state.stock * (1.0 - state.stock / params.carrying_capacity);
    ModelState {
        model_time: state.model_time + params.time_step,
        stock: state.stock + params.time_step * dx,
    }
}

fn main() {
    let params = ModelParameters { growth_rate: 0.35, carrying_capacity: 100.0, initial_stock: 10.0, time_step: 0.25, horizon: 20.0 };
    let mut state = ModelState { model_time: 0.0, stock: params.initial_stock };
    while state.model_time < params.horizon {
        state = step_logistic(&params, &state);
    }
    println!("model_use,growth_rate,carrying_capacity,initial_stock,time_step,horizon,final_time,final_stock,warning");
    println!("governance_review,{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.12},Typed records improve structural review but do not prove empirical validity.",
        params.growth_rate, params.carrying_capacity, params.initial_stock, params.time_step, params.horizon, state.model_time, state.stock);
}
