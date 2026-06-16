mechanism_records <- data.frame(
  mechanism_name = c("stock_flow_accumulation", "balancing_feedback", "threshold_transition"),
  represented_process = c(
    "stock changes through inflow and outflow",
    "state-dependent adjustment limits growth or change",
    "behavior changes after a critical value is crossed"
  ),
  evidence_status = c("synthetic teaching example", "formal teaching example", "scenario-based example"),
  warning = c(
    "A stock-flow equation is mechanistic only when flows represent real processes.",
    "Feedback parameters require process interpretation and evidence.",
    "Threshold claims require careful scope and uncertainty notes."
  )
)

claim_records <- data.frame(
  claim_type = c("mechanistic", "predictive", "exploratory"),
  supported_use = c(
    "explains how an organized process can produce behavior",
    "forecasts output under specified conditions",
    "investigates possible system behavior"
  ),
  evidence_need = c(
    "process evidence and structural plausibility",
    "validation data and uncertainty assessment",
    "clear scenario assumptions and limitation notes"
  ),
  scope_limit = c(
    "applies only where mechanism and assumptions hold",
    "limited to validated domain and time horizon",
    "not a confirmed mechanism or forecast"
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(mechanism_records, "outputs/tables/r_mechanism_records.csv", row.names = FALSE)
write.csv(claim_records, "outputs/tables/r_explanation_claim_records.csv", row.names = FALSE)

print(mechanism_records)
print(claim_records)
