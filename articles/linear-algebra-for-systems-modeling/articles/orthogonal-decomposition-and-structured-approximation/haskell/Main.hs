module Main where

data OrthogonalApproximationAudit = OrthogonalApproximationAudit
  { modelName :: String
  , rows :: Int
  , columns :: Int
  , numericalRank :: Int
  , conditionNumber :: Double
  , residualNorm :: Double
  , relativeResidualNorm :: Double
  , orthogonalityError :: Double
  , coefficientNorm :: Double
  , method :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: OrthogonalApproximationAudit
buildAudit =
  OrthogonalApproximationAudit
    "synthetic_orthogonal_approximation_audit"
    6
    3
    3
    58.0
    0.346410
    0.032100
    0.000000
    2.513000
    "qr_least_squares"
    "Orthogonal approximation results depend on subspace choice, scaling, rank tolerance, conditioning, solver method, residual interpretation, data provenance, and validation context."

main :: IO ()
main =
  print buildAudit
