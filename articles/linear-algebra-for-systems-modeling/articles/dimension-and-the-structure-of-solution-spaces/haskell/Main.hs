module Main where

data SolutionSpaceAudit = SolutionSpaceAudit
  { systemName :: String
  , variableCount :: Int
  , equationCount :: Int
  , rankValue :: Int
  , nullityValue :: Int
  , likelySolutionStructure :: String
  , modelingRole :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: SolutionSpaceAudit
buildAudit =
  let variableCount' = 4
      equationCount' = 3
      rank' = 3
      nullity' = variableCount' - rank'
      structure =
        if nullity' == 0
        then "No free variables if the system is consistent; a unique solution may exist."
        else "Positive-dimensional solution space if the system is consistent."
  in SolutionSpaceAudit
      "four_variable_three_constraint_system"
      variableCount'
      equationCount'
      rank'
      nullity'
      structure
      "Audit degrees of freedom in a constrained system representation."
      "Rank and nullity describe mathematical freedom, not full real-world adequacy."

main :: IO ()
main =
  print buildAudit
