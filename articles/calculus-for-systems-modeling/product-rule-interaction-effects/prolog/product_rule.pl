product_rule(A, B, DA, DB, ContributionA, ContributionB, Total) :-
    ContributionA is DA * B,
    ContributionB is A * DB,
    Total is ContributionA + ContributionB.
