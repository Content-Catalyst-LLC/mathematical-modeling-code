# Scaling and Unit Audit

## Unit Records
- **population_stock** = 40.0 state units; dimension: stock. Synthetic value; do not treat as empirical measurement.
- **carrying_capacity** = 100.0 state units; dimension: stock. Capacity scale controls normalized interpretation.
- **growth_rate** = 0.35 per time unit; dimension: inverse time. Rate units must match the time variable.

## Scale Records
- **stock_scale** = 100.000000 state units; carrying capacity used to normalize population stock. Changing the capacity scale changes dimensionless stock.
- **time_scale** = 2.857143 time units; inverse growth rate used as characteristic response time. Changing the growth-rate scale changes dimensionless time.

## Nondimensional Records
- **scaled_stock** = 0.400000; population stock as fraction of carrying capacity
- **scaled_time** = 7.000000; time measured in characteristic growth-time units

Scaling improves comparability but does not prove empirical validity.
