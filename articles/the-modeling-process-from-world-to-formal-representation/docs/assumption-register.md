# Assumption Register

| Assumption | Role | Risk if false | Review action |
|---|---|---|---|
| Capacity is fixed within scenario | Defines storage upper bound | Sedimentation, infrastructure, or operations may change capacity | Test capacity scenarios |
| Inflow is deterministic within scenario | Keeps model transparent | Variability and drought risk may be understated | Add stochastic inflow ensemble |
| Demand grows at constant rate | Represents increasing pressure | Seasonality, price response, and conservation may be missed | Add demand scenarios |
| Losses are proportional to storage | Represents evaporation/leakage | Losses may depend on temperature, surface area, infrastructure | Compare loss formulations |
| No water-quality constraint | Simplifies first model | Quantity may appear adequate when quality is not | Add quality threshold if relevant |
| No legal/ecological allocation | Narrows model boundary | Model may ignore rights and ecological flow needs | Add constraint layer |
