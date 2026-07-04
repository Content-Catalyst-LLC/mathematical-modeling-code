module Main where

data DecompositionWorkflowAudit = DecompositionWorkflowAudit
  { modelName :: String
  , matrixShape :: String
  , matrixClass :: String
  , recommendedWorkflow :: String
  , conditionProxy :: Double
  , estimatedRank :: Int
  , singularValue1 :: Double
  , singularValue2 :: Double
  , singularValue3 :: Double
  , lowRankReconstructionError :: Double
  , solveResidualNorm :: Double
  , decompositionWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: DecompositionWorkflowAudit
buildAudit =
  DecompositionWorkflowAudit
    "decomposition_workflow_audit"
    "4x3"
    "rectangular_overdetermined_dense_demo_matrix"
    "QR_or_SVD_for_least_squares_and_rank_diagnostics"
    4.20
    3
    5.12
    2.35
    1.02
    1.02
    0.0
    "Rectangular systems should generally use QR or SVD rather than normal equations when stability and rank diagnostics matter."
    "Decomposition factors should be interpreted through matrix construction, scaling, rank tolerance, conditioning, residuals, and system meaning."

main :: IO ()
main =
  print buildAudit
