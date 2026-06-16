<?php
function cc_energy_equilibrium_temperature($forcing, $feedback) {
    return $feedback > 0 ? $forcing / $feedback : null;
}
function cc_energy_adjustment_time($heat_capacity, $feedback) {
    return $feedback > 0 ? $heat_capacity / $feedback : null;
}
function cc_energy_absorbed_solar($solar_constant, $albedo) {
    return $solar_constant * (1 - $albedo) / 4;
}
?>
