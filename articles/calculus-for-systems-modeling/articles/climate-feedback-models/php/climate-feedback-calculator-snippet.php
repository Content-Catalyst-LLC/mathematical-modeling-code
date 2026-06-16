<?php
function cc_climate_one_box_temperature($forcing, $feedback, $heat_capacity, $time) {
    $equilibrium = $forcing / $feedback;
    return $equilibrium * (1.0 - exp(-($feedback / $heat_capacity) * $time));
}
?>
