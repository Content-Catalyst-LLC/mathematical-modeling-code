package main

import (
    "fmt"
    "math"
)

func main() {
    a, b, c, d := 0.80, 0.15, 0.20, 0.90
    trace := a + d
    determinant := a*d - b*c
    discriminant := trace*trace - 4.0*determinant
    root := math.Sqrt(discriminant)
    lambda1 := (trace + root) / 2.0
    lambda2 := (trace - root) / 2.0
    dominant := math.Max(math.Abs(lambda1), math.Abs(lambda2))
    fmt.Println("model_name,rank,determinant,dominant_eigenvalue,warning")
    fmt.Printf("two_component_transition_model,2,%.6f,%.6f,Matrix interpretation depends on entry meaning and scale.\n", determinant, dominant)
}
