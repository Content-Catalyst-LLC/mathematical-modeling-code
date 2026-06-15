package main
import "fmt"
func systemResponse(x float64, y float64) float64 { return 3.0*x + 2.0*y + 0.5*x*y }
func isFeasible(x float64, y float64) bool { return x >= 0.0 && y >= 0.0 && x+y <= 10.0 }
func main() {
	cases := [][2]float64{{2.0, 4.0}, {8.0, 4.0}, {6.0, 3.0}}
	fmt.Println("x,y,output,feasible,warning")
	for _, pair := range cases {
		x := pair[0]; y := pair[1]
		feasible := isFeasible(x, y)
		warning := ""
		if !feasible { warning = "Input combination is outside the feasible region." }
		fmt.Printf("%.12f,%.12f,%.12f,%t,%s\n", x, y, systemResponse(x, y), feasible, warning)
	}
}
