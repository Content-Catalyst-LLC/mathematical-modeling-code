package main
import "fmt"
type Scenario struct{ Name string; InitialStock, Capacity, Inflow, Demand, LossRate float64; Periods int }
func bounded(raw, cap float64) float64 { if raw < 0 { return 0 }; if raw > cap { return cap }; return raw }
func simulate(s Scenario) (float64,float64,float64) { stock:=s.InitialStock; shortage:=0.0; overflow:=0.0; for p:=0; p<=s.Periods; p++ { losses:=s.LossRate*stock; raw:=stock+s.Inflow-s.Demand-losses; if -raw>0 { shortage += -raw }; if raw-s.Capacity>0 { overflow += raw-s.Capacity }; stock=bounded(raw,s.Capacity) }; return stock,shortage,overflow }
func main(){ for _,s:= range []Scenario{{"go_baseline",80,100,8,6,0.015,60},{"go_constraint_stress",40,60,3,7,0.050,60}} { f,sh,ov:=simulate(s); fmt.Printf("%s final_stock=%.3f total_shortage=%.3f total_overflow=%.3f\n",s.Name,f,sh,ov) } }
