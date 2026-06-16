<?php
function cc_population_logistic($n0, $r, $k, $t) {
    return $k / (1.0 + (($k - $n0) / $n0) * exp(-$r * $t));
}
?>
