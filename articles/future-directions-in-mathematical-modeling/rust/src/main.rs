#[derive(Debug)]
struct FutureDirectionRecord {
    key: &'static str,
    direction_name: &'static str,
    complexity_relevance: f64,
    technical_maturity: f64,
    governance_need: f64,
    uncertainty_pressure: f64,
    human_judgment_need: f64,
}

fn priority(item: &FutureDirectionRecord) -> f64 {
    0.25*item.complexity_relevance + 0.20*item.technical_maturity + 0.20*item.governance_need + 0.20*item.uncertainty_pressure + 0.15*item.human_judgment_need
}

fn review_class(item: &FutureDirectionRecord) -> &'static str {
    if item.governance_need >= 0.85 || item.human_judgment_need >= 0.90 { "governance_priority" }
    else if item.uncertainty_pressure >= 0.85 { "uncertainty_priority" }
    else if priority(item) >= 0.78 { "strategic_priority" }
    else { "monitor" }
}

fn main() {
    let records = vec![
        FutureDirectionRecord{key:"hybrid_models",direction_name:"Hybrid modeling and model ensembles",complexity_relevance:0.88,technical_maturity:0.70,governance_need:0.74,uncertainty_pressure:0.72,human_judgment_need:0.80},
        FutureDirectionRecord{key:"ai_assistance",direction_name:"AI-assisted modeling",complexity_relevance:0.82,technical_maturity:0.78,governance_need:0.90,uncertainty_pressure:0.76,human_judgment_need:0.92},
        FutureDirectionRecord{key:"uncertainty_workflows",direction_name:"Uncertainty-aware modeling",complexity_relevance:0.90,technical_maturity:0.72,governance_need:0.82,uncertainty_pressure:0.92,human_judgment_need:0.86},
    ];
    for record in records {
        println!("{} | {} | score={:.4} | {}", record.key, record.direction_name, priority(&record), review_class(&record));
    }
}
