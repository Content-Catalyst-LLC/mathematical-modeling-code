<?php
function cc_urban_traffic_flow($density, $free_flow_speed, $jam_density) {
    return max(0, $free_flow_speed * $density * (1 - $density / $jam_density));
}
function cc_urban_bpr_travel_time($free_flow_time, $volume, $capacity, $alpha = 0.15, $beta = 4) {
    return $capacity > 0 ? $free_flow_time * (1 + $alpha * pow($volume / $capacity, $beta)) : null;
}
function cc_urban_queue_step($queue, $arrival_rate, $service_rate, $dt) {
    return max(0, $queue + ($arrival_rate - $service_rate) * $dt);
}
?>
