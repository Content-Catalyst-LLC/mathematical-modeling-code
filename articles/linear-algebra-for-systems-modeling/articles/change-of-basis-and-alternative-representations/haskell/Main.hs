module Main where

data ChangeOfBasisAudit = ChangeOfBasisAudit
  { systemName :: String
  , basisShape :: String
  , basisRank :: Int
  , basisDeterminant :: Double
  , basisConditionWarning :: String
  , originalVector :: String
  , basisCoordinates :: String
  , reconstructedVector :: String
  , reconstructionError :: Double
  , transformedMatrix :: String
  , invariantWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: ChangeOfBasisAudit
buildAudit =
  ChangeOfBasisAudit
    "two_mode_representation_audit"
    "2x2"
    2
    3.0
    "basis is valid in this teaching example; serious workflows should compute a numerical condition number"
    "5.000000,4.000000"
    "2.000000,1.500000"
    "5.000000,4.000000"
    0.0
    "1.133333,0.033333;0.333333,0.966667"
    "Similarity preserves structural invariants but changes individual entries."
    "Changing basis requires basis meaning, units, scaling, conditioning, and translation back to system terms."

main :: IO ()
main =
  print buildAudit
