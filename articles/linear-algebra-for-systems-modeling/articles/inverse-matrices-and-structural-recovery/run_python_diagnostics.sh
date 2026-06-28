#!/usr/bin/env bash
set -euo pipefail

python3 python/engineering_grade_recovery.py
python3 python/near_singular_instability.py
python3 python/pseudoinverse_and_least_squares.py
python3 python/sensor_state_recovery.py
python3 python/residual_error_checks.py
python3 python/generate_outputs.py
python3 tests/test_recovery_diagnostics.py
