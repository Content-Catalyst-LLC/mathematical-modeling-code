<?php
function cc_infrastructure_utilization($arrival, $capacity) {
    return $capacity > 0 ? $arrival / $capacity : null;
}
function cc_infrastructure_delay($utilization, $base_delay = 1.0, $alpha = 0.8) {
    if ($utilization >= 1.0) return INF;
    return $base_delay * (1.0 + $alpha * ($utilization / (1.0 - $utilization)));
}
?>
