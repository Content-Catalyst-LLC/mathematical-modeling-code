<?php
function cc_financial_continuous_future_value($v0, $r, $t) {
    return $v0 * exp($r * $t);
}
function cc_financial_continuous_present_value($fv, $r, $t) {
    return $fv * exp(-$r * $t);
}
function cc_financial_real_rate($nominal_rate, $inflation_rate) {
    return (1 + $nominal_rate) / (1 + $inflation_rate) - 1;
}
?>
