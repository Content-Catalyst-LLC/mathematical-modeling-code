package main

import (
	"fmt"
	"math"
)

func position(t float64) (float64, float64) {
	return t, math.Sin(t)
}

func distanceBetween(x1 float64, y1 float64, x2 float64, y2 float64) float64 {
	return math.Sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
}

func audit(step float64, scenario string) {
	count := int((2.0*math.Pi)/step) + 1
	firstX, firstY := position(0.0)
	prevX, prevY := firstX, firstY
	arc := 0.0
	speedSum := 0.0
	speedMax := 0.0

	for i := 1; i < count; i++ {
		x, y := position(float64(i) * step)
		seg := distanceBetween(prevX, prevY, x, y)
		speed := seg / step
		arc += seg
		speedSum += speed
		speedMax = math.Max(speedMax, speed)
		prevX, prevY = x, y
	}

	disp := distanceBetween(firstX, firstY, prevX, prevY)
	eff := disp / math.Max(arc, 1e-12)
	warning := "Synthetic trajectory audit; document units parameter meaning and sampling."
	if step > 0.5 { warning = "Time step is coarse; turns and speed variation may be undersampled." }
	fmt.Printf("%s,%.12f,%d,%.12f,%.12f,%.12f,%.12f,%.12f,trajectory r(t)=<t,sin(t)>,%s\n", scenario, step, count, arc, disp, eff, speedSum/float64(count-1), speedMax, warning)
}

func main() {
	fmt.Println("scenario,time_step,point_count,approximate_arc_length,displacement_magnitude,path_efficiency,average_speed,maximum_speed,domain_description,warning")
	audit(1.0, "coarse_time_step")
	audit(0.5, "medium_time_step")
	audit(0.25, "fine_time_step")
}
