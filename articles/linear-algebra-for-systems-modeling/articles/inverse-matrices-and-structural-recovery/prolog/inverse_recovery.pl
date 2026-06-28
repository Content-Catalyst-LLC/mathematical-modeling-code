% Inverse Matrices and Structural Recovery

determinant_2x2(A, B, C, D, Det) :-
    Det is A * D - B * C.

invertible_2x2(A, B, C, D) :-
    determinant_2x2(A, B, C, D, Det),
    Det =\= 0.

recover_2x2(A, B, C, D, Y1, Y2, X1, X2) :-
    determinant_2x2(A, B, C, D, Det),
    Det =\= 0,
    X1 is (D * Y1 - B * Y2) / Det,
    X2 is (-C * Y1 + A * Y2) / Det.

% Example query:
% recover_2x2(3, 1, 2, 4, 7, 8, X1, X2).
