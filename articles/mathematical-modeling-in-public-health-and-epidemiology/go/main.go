package main

import "fmt"

type EpidemicScenario struct {
	Key                 string
	ScenarioName        string
	Population          float64
	InitialInfectious   float64
	InitialRecovered    float64
	Beta                float64
	Gamma               float64
	Days                int
	HospitalCapacity    float64
	HospitalizationRate float64
}

type Evaluation struct {
	R0Simple            float64
	PeakInfectious     float64
	PeakHospitalDemand float64
	CapacityMargin     float64
	CapacityBreach     bool
}

func evaluate(s EpidemicScenario) Evaluation {
	susceptible := s.Population - s.InitialInfectious - s.InitialRecovered
	infectious := s.InitialInfectious
	recovered := s.InitialRecovered
	peakInfectious := infectious
	peakHospitalDemand := infectious * s.HospitalizationRate

	for day := 0; day < s.Days; day++ {
		newInfections := s.Beta * susceptible * infectious / s.Population
		newRecoveries := s.Gamma * infectious
		susceptible -= newInfections
		if susceptible < 0.0 {
			susceptible = 0.0
		}
		infectious = infectious + newInfections - newRecoveries
		if infectious < 0.0 {
			infectious = 0.0
		}
		recovered += newRecoveries
		if recovered > s.Population {
			recovered = s.Population
		}
		if infectious > peakInfectious {
			peakInfectious = infectious
		}
		hospitalDemand := infectious * s.HospitalizationRate
		if hospitalDemand > peakHospitalDemand {
			peakHospitalDemand = hospitalDemand
		}
	}

	return Evaluation{
		R0Simple:            s.Beta / s.Gamma,
		PeakInfectious:     peakInfectious,
		PeakHospitalDemand: peakHospitalDemand,
		CapacityMargin:     s.HospitalCapacity - peakHospitalDemand,
		CapacityBreach:     peakHospitalDemand > s.HospitalCapacity,
	}
}

func main() {
	scenarios := []EpidemicScenario{
		{"baseline", "Baseline transmission", 100000.0, 120.0, 4000.0, 0.32, 0.12, 120, 850.0, 0.045},
		{"moderate_intervention", "Moderate intervention", 100000.0, 120.0, 4000.0, 0.24, 0.12, 120, 850.0, 0.045},
		{"strong_intervention", "Strong intervention", 100000.0, 120.0, 4000.0, 0.18, 0.12, 120, 850.0, 0.045},
		{"vaccination_plus_intervention", "Vaccination plus intervention", 100000.0, 120.0, 22000.0, 0.20, 0.12, 120, 850.0, 0.030},
	}

	fmt.Println("key,r0_simple,peak_infectious,peak_hospital_demand,capacity_margin,capacity_breach")
	for _, scenario := range scenarios {
		eval := evaluate(scenario)
		fmt.Printf("%s,%.6f,%.6f,%.6f,%.6f,%t\n",
			scenario.Key,
			eval.R0Simple,
			eval.PeakInfectious,
			eval.PeakHospitalDemand,
			eval.CapacityMargin,
			eval.CapacityBreach)
	}
}
