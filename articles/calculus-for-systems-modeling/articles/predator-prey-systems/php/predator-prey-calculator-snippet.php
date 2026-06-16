<?php
function cc_predator_prey_lotka_volterra_step($x, $y, $alpha, $beta, $gamma, $delta, $dt) {
    $dx = $alpha * $x - $beta * $x * $y;
    $dy = $delta * $x * $y - $gamma * $y;
    return array(max(0.0, $x + $dt * $dx), max(0.0, $y + $dt * $dy));
}
?>
