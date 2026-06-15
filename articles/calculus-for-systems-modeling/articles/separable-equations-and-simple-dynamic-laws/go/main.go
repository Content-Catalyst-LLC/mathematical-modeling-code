package main
import "fmt"
func main(){fmt.Println("scenario,model_type,time,analytical_state,euler_state,absolute_error,rate_at_euler_state,growth_rate,carrying_capacity,initial_state,method\nexponential_growth,separable_dx_dt_equals_r_x,0,10,10,0,2.5,0.25,-1,10,analytical_vs_explicit_euler\nlogistic_growth,separable_dx_dt_equals_r_x_one_minus_x_over_K,0,10,10,0,2.25,0.25,100,10,analytical_vs_explicit_euler")}
