<?php
function cc_economic_exponential_output($y0, $g, $t) {
    return $y0 * exp($g * $t);
}
function cc_economic_doubling_time($g) {
    return $g > 0 ? log(2) / $g : INF;
}
?>
