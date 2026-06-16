<?php
function cc_resource_logistic_regeneration($stock, $r, $k) {
    return max(0.0, $r * $stock * (1.0 - $stock / $k));
}
function cc_resource_msy($r, $k) {
    return $r * $k / 4.0;
}
?>
