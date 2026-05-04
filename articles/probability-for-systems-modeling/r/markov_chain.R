# Probability for Systems Modeling:
# Markov chain transition simulation in R.
# Educational example only.

library(tidyverse)

set.seed(42)

transitions <- read_csv("../data/markov_transition_matrix.csv", show_col_types = FALSE)

states <- sort(unique(c(transitions$from_state, transitions$to_state)))

transition_matrix <- matrix(0, nrow = length(states), ncol = length(states))
rownames(transition_matrix) <- states
colnames(transition_matrix) <- states

for (i in seq_len(nrow(transitions))) {
  transition_matrix[transitions$from_state[i], transitions$to_state[i]] <- transitions$probability[i]
}

steps <- 500
state_sequence <- character(steps)
state_sequence[1] <- "stable"

for (t in 2:steps) {
  current_state <- state_sequence[t - 1]
  state_sequence[t] <- sample(states, size = 1, prob = transition_matrix[current_state, ])
}

simulation <- tibble(
  time = 1:steps,
  state = state_sequence
)

summary_results <- simulation |>
  count(state) |>
  mutate(proportion = n / sum(n))

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(simulation, "../outputs/r_markov_chain_simulation.csv")
write_csv(summary_results, "../outputs/r_markov_chain_state_summary.csv")

print(summary_results)
