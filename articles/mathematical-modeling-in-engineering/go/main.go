package main

import "fmt"

type BeamDesign struct {
	Key               string
	WidthM            float64
	HeightM           float64
	SpanM             float64
	LoadN             float64
	AllowableStressPa float64
	Density           float64
}

func evaluate(design BeamDesign) (stress float64, margin float64, safetyFactor float64, mass float64) {
	moment := design.LoadN * design.SpanM / 4.0
	inertia := design.WidthM * design.HeightM * design.HeightM * design.HeightM / 12.0
	c := design.HeightM / 2.0
	stress = moment * c / inertia
	margin = design.AllowableStressPa - stress
	safetyFactor = design.AllowableStressPa / stress
	mass = design.WidthM * design.HeightM * design.SpanM * design.Density
	return
}

func main() {
	designs := []BeamDesign{
		{"light_design", 0.08, 0.16, 3.0, 4200.0, 145000000.0, 7850.0},
		{"balanced_design", 0.10, 0.18, 3.0, 4200.0, 145000000.0, 7850.0},
		{"stiff_design", 0.12, 0.22, 3.0, 4200.0, 145000000.0, 7850.0},
		{"overloaded_case", 0.10, 0.18, 3.0, 7000.0, 145000000.0, 7850.0},
	}

	fmt.Println("key,max_stress_pa,stress_margin_pa,safety_factor,estimated_mass_kg,passes_stress_constraint")
	for _, design := range designs {
		stress, margin, safetyFactor, mass := evaluate(design)
		passes := stress <= design.AllowableStressPa
		fmt.Printf("%s,%.6f,%.6f,%.6f,%.6f,%t\n", design.Key, stress, margin, safetyFactor, mass, passes)
	}
}
