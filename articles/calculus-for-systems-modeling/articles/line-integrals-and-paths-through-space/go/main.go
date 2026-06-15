package main

import (
	"fmt"
	"math"
)

func pathPoint(t float64) (float64, float64) { return t, math.Sin(t) }
func scalarField(x float64, y float64) float64 { _ = x; return 1.0 + y*y }
func vectorField(x float64, y float64) (float64, float64) { _ = y; return 1.0, x }
func distance(x1 float64, y1 float64, x2 float64, y2 float64) float64 {
	return math.Sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))
}
func dot(ax float64, ay float64, bx float64, by float64) float64 { return ax*bx + ay*by }

func audit(step float64, scenario string) {
	count := int((2.0*math.Pi)/step) + 1
	pathLen := 0.0
	scalarTotal := 0.0
	vectorTotal := 0.0
	alignSum := 0.0
	maxSeg := 0.0

	for i := 0; i < count-1; i++ {
		x1, y1 := pathPoint(float64(i)*step)
		x2, y2 := pathPoint(float64(i+1)*step)
		dx := x2 - x1
		dy := y2 - y1
		seg := distance(x1,y1,x2,y2)
		vx, vy := vectorField(x1,y1)
		term := dot(vx,vy,dx,dy)
		pathLen += seg
		scalarTotal += scalarField(x1,y1) * seg
		vectorTotal += term
		alignSum += term / math.Max(seg, 1e-12)
		maxSeg = math.Max(maxSeg, seg)
	}

	warning := "Synthetic line-integral audit; document path field units and interpolation."
	if step > 0.5 { warning = "Time step is coarse; path turns and field variation may be undersampled." }
	fmt.Printf("%s,%.12f,%d,%.12f,%.12f,%.12f,%.12f,%.12f,path r(t)=<t,sin(t)>,%s\n", scenario, step, count, pathLen, scalarTotal, vectorTotal, alignSum/float64(count-1), maxSeg, warning)
}

func main() {
	fmt.Println("scenario,time_step,point_count,path_length,scalar_line_integral,vector_line_integral,average_alignment,maximum_segment_length,path_description,warning")
	audit(1.0, "coarse_path")
	audit(0.5, "medium_path")
	audit(0.25, "fine_path")
}
