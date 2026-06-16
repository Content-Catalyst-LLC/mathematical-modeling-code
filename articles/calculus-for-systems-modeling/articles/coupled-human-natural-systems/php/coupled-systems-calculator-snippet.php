<?php
function cc_coupled_regeneration($stock, $growth_rate, $carrying_capacity) {
    return $growth_rate * $stock * (1 - $stock / $carrying_capacity);
}
function cc_coupled_extraction($efficiency, $effort, $stock) {
    return $efficiency * $effort * $stock;
}
function cc_coupled_natural_stock_step($stock, $growth_rate, $carrying_capacity, $harvest, $stress, $dt) {
    return max(0, $stock + (cc_coupled_regeneration($stock, $growth_rate, $carrying_capacity) - $harvest - $stress) * $dt);
}
?>
