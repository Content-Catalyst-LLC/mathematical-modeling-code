package main
import ("fmt"; "math")
func rate(t float64) float64 { return 2.0 + math.Sin(t) + 0.1*t }
func trueInt(t float64) float64 { return 2.0*t - math.Cos(t) + 1.0 + 0.05*t*t }
func main(){ h:=0.1; left:=0.0; trap:=0.0; fmt.Println("index,time,rate,left_cumulative,trapezoid_cumulative,true_cumulative,error"); for i:=0;i<=100;i++{ t:=float64(i)*h; r:=rate(t); if i>0{ left += rate(float64(i-1)*h)*h; trap += 0.5*(rate(float64(i-1)*h)+r)*h }; truth:=trueInt(t)-trueInt(0); fmt.Printf("%d,%.6f,%.12f,%.12f,%.12f,%.12f,%.12f\n", i,t,r,left,trap,truth,math.Abs(trap-truth)) } }
