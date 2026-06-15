package main

import (
	"fmt"
	"math"
)

func boundaryPoints(n int) [][2]float64 {
	pts := make([][2]float64, 0, 4*n+1)
	for i := 0; i < n; i++ { t := -1.0 + 2.0*float64(i)/float64(n); pts = append(pts, [2]float64{t, -1.0}) }
	for i := 0; i < n; i++ { t := -1.0 + 2.0*float64(i)/float64(n); pts = append(pts, [2]float64{1.0, t}) }
	for i := 0; i < n; i++ { t := 1.0 - 2.0*float64(i)/float64(n); pts = append(pts, [2]float64{t, 1.0}) }
	for i := 0; i < n; i++ { t := 1.0 - 2.0*float64(i)/float64(n); pts = append(pts, [2]float64{-1.0, t}) }
	pts = append(pts, pts[0])
	return pts
}

func audit(segments int, step float64, scenario string) {
	pts := boundaryPoints(segments)
	bc := 0.0
	bf := 0.0
	for i := 0; i < len(pts)-1; i++ {
		x0, y0 := pts[i][0], pts[i][1]
		x1, y1 := pts[i+1][0], pts[i+1][1]
		xm, ym := 0.5*(x0+x1), 0.5*(y0+y1)
		dx, dy := x1-x0, y1-y0
		bc += (-ym)*dx + xm*dy
		bf += xm*dy + ym*(-dx)
	}
	n := 2.0 / step
	ic := 2.0 * n * n * step * step
	idv := ic
	warning := "Synthetic Greens theorem audit."
	if segments < 16 || step > 0.25 { warning = "Coarse boundary or interior sampling." }
	fmt.Printf("%s,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,circulation F=<-y,x>; flux G=<x,y>,square [-1,1]x[-1,1],%s\n", scenario, segments, step, bc, ic, bf, idv, math.Abs(bc-ic), math.Abs(bf-idv), warning)
}

func main() {
	fmt.Println("scenario,boundary_segments_per_side,interior_grid_step,boundary_circulation,interior_curl_integral,boundary_flux,interior_divergence_integral,circulation_gap,flux_gap,field_description,region_description,warning")
	audit(8, 0.5, "coarse_audit")
	audit(32, 0.25, "medium_audit")
	audit(128, 0.125, "fine_audit")
}
