# Mathematical Deepening Notes

## Required distinctions

- compression versus explanation
- retained signal versus discarded residual
- noise as measurement error versus noise as modeling judgment
- low-rank approximation versus faithful system representation
- reconstruction error versus decision relevance
- aggregate error versus localized loss
- dominant components versus meaningful components
- weak signals versus noise
- sparse zeros as structure versus missing data
- compression ratio versus acceptable loss

## Review checklist

- Define the original representation, rows, columns, units, and missing-data handling.
- Document preprocessing, scaling, centering, normalization, transformation, and weighting.
- State the compression method and the preserved structure.
- Report retained rank, retained energy, discarded energy, compression ratio, and reconstruction error.
- Review row, column, temporal, spatial, and subgroup residuals where relevant.
- Examine weak signals and rare events before treating discarded structure as noise.
- Validate compressed representations against the system question and downstream use.
