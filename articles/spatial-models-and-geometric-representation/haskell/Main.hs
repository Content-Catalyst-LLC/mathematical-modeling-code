{-# OPTIONS_GHC -Wall #-}

module Main where

data SpatialComponent
  = GeometryDefinition
  | CoordinateSystem
  | DistanceMetric
  | NeighborhoodRule
  | AccessibilityMetric
  | SpatialField
  | ValidationDiagnostic
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSensitivityTest
  | Revise
  deriving (Eq, Show)

data SpatialRecord = SpatialRecord
  { key :: String
  , component :: SpatialComponent
  , geometryOrStructure :: String
  , interpretation :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

spatialRegister :: [SpatialRecord]
spatialRegister =
  [ SpatialRecord
      "point_geometry"
      GeometryDefinition
      "p=(x,y)"
      "Facilities and observations are represented as point coordinates."
      "Geometry simplification."
      RequiresReview
  , SpatialRecord
      "euclidean_distance"
      DistanceMetric
      "sqrt((x_i-x_j)^2+(y_i-y_j)^2)"
      "Straight-line distance is used as a transparent baseline."
      "Distance validity."
      RequiresReview
  , SpatialRecord
      "service_access"
      AccessibilityMetric
      "capacity / (1 + distance)"
      "Service capacity is discounted by distance."
      "Decision relevance."
      RequiresValidation
  , SpatialRecord
      "spatial_uncertainty"
      ValidationDiagnostic
      "distance and boundary sensitivity"
      "Spatial results require sensitivity checks."
      "Uncertainty communication."
      Active
  ]

needsReview :: SpatialRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed spatial model records:"
  mapM_ print spatialRegister

  putStrLn "\nSpatial records requiring review:"
  mapM_ print (filter needsReview spatialRegister)
