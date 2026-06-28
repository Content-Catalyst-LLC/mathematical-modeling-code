% Inverse Matrices and Structural Recovery
% Logical conditions for structural recovery in a 2x2 system.

determinant_2x2(A, B, C, D, Det) :-
    Det is A * D - B * C.

singular_2x2(A, B, C, D) :-
    determinant_2x2(A, B, C, D, Det),
    Det =:= 0.

invertible_2x2(A, B, C, D) :-
    determinant_2x2(A, B, C, D, Det),
    Det =\= 0.

structural_recovery_possible(A, B, C, D) :-
    invertible_2x2(A, B, C, D).

structural_recovery_ambiguous(A, B, C, D) :-
    singular_2x2(A, B, C, D).

recover_2x2(A, B, C, D, Y1, Y2, X1, X2) :-
    determinant_2x2(A, B, C, D, Det),
    Det =\= 0,
    X1 is (D * Y1 - B * Y2) / Det,
    X2 is (-C * Y1 + A * Y2) / Det.

% Example queries:
% structural_recovery_possible(3, 1, 2, 4).
% structural_recovery_ambiguous(2, 4, 1, 2).
% recover_2x2(3, 1, 2, 4, 7, 8, X1, X2).
