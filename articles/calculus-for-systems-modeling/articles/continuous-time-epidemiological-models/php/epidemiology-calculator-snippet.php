<?php
function cc_epidemiology_r0($beta, $gamma) {
    return $gamma > 0 ? $beta / $gamma : null;
}
function cc_epidemiology_rt($beta, $gamma, $susceptible, $population) {
    return ($gamma > 0 && $population > 0) ? ($beta / $gamma) * ($susceptible / $population) : null;
}
function cc_epidemiology_doubling_time($growth_rate) {
    return $growth_rate > 0 ? log(2) / $growth_rate : INF;
}
?>
