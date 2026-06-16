<?php
function cc_carbon_linear_decline_cumulative($e0, $years) {
    $cumulative = 0.0;
    for ($y = 0; $y <= $years; $y++) {
        $emission = max(0.0, $e0 * (1.0 - ($y / $years)));
        $cumulative += $emission;
    }
    return $cumulative;
}
?>
