module Main where

data OrthogonalityAudit = OrthogonalityAudit
  { systemName :: String
  , vectorA :: String
  , vectorB :: String
  , dotProduct :: Double
  , orthogonalUnderTolerance :: Bool
  , unitA :: String
  , unitB :: String
  , projectionOfAOntoB :: String
  , residualVector :: String
  , residualNorm :: Double
  , orthonormalityError :: Double
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: OrthogonalityAudit
buildAudit =
  OrthogonalityAudit
    "three_component_orthogonality_audit"
    "3.000000,1.000000,2.000000"
    "1.000000,-1.000000,-1.000000"
    0.0
    True
    "0.801784,0.267261,0.534522"
    "0.577350,-0.577350,-0.577350"
    "0.000000,0.000000,0.000000"
    "3.000000,1.000000,2.000000"
    3.741657
    0.0
    "Orthogonality depends on geometry, scaling, units, and tolerance; residuals require substantive interpretation."

main :: IO ()
main =
  print buildAudit
