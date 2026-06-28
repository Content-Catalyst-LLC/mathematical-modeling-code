module Main where

data RankNullityAudit = RankNullityAudit
  { systemName :: String
  , rowCount :: Int
  , columnCount :: Int
  , rankValue :: Int
  , nullityValue :: Int
  , rankDeficient :: Bool
  , pivotColumns :: String
  , freeColumns :: String
  , tolerance :: Double
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: RankNullityAudit
buildAudit =
  RankNullityAudit
    "three_constraint_resource_balance_matrix"
    3
    3
    3
    0
    False
    "0,1,2"
    "none"
    1.0e-10
    "Rank and nullity reveal structure, but model meaning requires row and column interpretation."

main :: IO ()
main =
  print buildAudit
