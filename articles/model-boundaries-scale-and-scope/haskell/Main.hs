{-# OPTIONS_GHC -Wall #-}

module Main where

data BoundaryType
  = PhysicalBoundary
  | TemporalBoundary
  | SpatialBoundary
  | PopulationBoundary
  | MechanismBoundary
  | DataBoundary
  | DecisionBoundary
  deriving (Eq, Show)

data ScopeStatus
  = SupportedUse
  | ExploratoryUse
  | RequiresValidation
  | ProhibitedUse
  deriving (Eq, Show)

data ScaleLevel
  = FineScale
  | IntermediateScale
  | AggregateScale
  | MultiScale
  deriving (Eq, Show)

data BoundaryRecord = BoundaryRecord
  { boundaryType :: BoundaryType
  , included :: String
  , excluded :: String
  , scaleLevel :: ScaleLevel
  , scopeStatus :: ScopeStatus
  , reviewQuestion :: String
  } deriving (Eq, Show)

records :: [BoundaryRecord]
records =
  [ BoundaryRecord
      PhysicalBoundary
      "Storage, inflow, demand, losses, capacity."
      "Spatial variation, quality, local access."
      AggregateScale
      SupportedUse
      "Does aggregate storage match the intended modeling question?"
  , BoundaryRecord
      TemporalBoundary
      "Sixty-period planning horizon."
      "Long-term infrastructure change and regime shifts."
      IntermediateScale
      RequiresValidation
      "Does the model horizon match the decision horizon?"
  , BoundaryRecord
      DecisionBoundary
      "Policy savings as a demand reduction."
      "Implementation capacity, compliance, enforcement, equity."
      AggregateScale
      ExploratoryUse
      "Can policy behavior be treated as an input rather than an internal mechanism?"
  , BoundaryRecord
      PopulationBoundary
      "Aggregate users."
      "User groups, access differences, vulnerable populations."
      AggregateScale
      RequiresValidation
      "Are distributional claims prohibited unless subgroup outputs are added?"
  ]

needsScopeWarning :: BoundaryRecord -> Bool
needsScopeWarning record =
  case scopeStatus record of
    SupportedUse -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed boundary, scale, and scope records:"
  mapM_ print records
  putStrLn "\nRecords requiring scope warning:"
  mapM_ print (filter needsScopeWarning records)
