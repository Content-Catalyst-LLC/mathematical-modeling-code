{-# OPTIONS_GHC -Wall #-}

module Main where

data Dimension
  = Volume
  | Time
  | VolumePerTime
  | InverseTime
  | Dimensionless
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | Revise
  deriving (Eq, Show)

data UnitRecord = UnitRecord
  { key :: String
  , dimension :: Dimension
  , unitLabel :: String
  , interpretation :: String
  , reviewQuestion :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

unitRegister :: [UnitRecord]
unitRegister =
  [ UnitRecord
      "storage"
      Volume
      "m^3"
      "Storage stock."
      "Does storage remain within physical bounds?"
      Active
  , UnitRecord
      "inflow"
      VolumePerTime
      "m^3/day"
      "Inflow rate."
      "Is inflow multiplied by the model time step?"
      RequiresReview
  , UnitRecord
      "demand"
      VolumePerTime
      "m^3/day"
      "Demand rate."
      "Is demand multiplied by the model time step?"
      RequiresReview
  , UnitRecord
      "loss_rate"
      InverseTime
      "1/day"
      "Proportional loss rate."
      "Does the loss-rate unit match the model time step?"
      RequiresValidation
  , UnitRecord
      "storage_fraction"
      Dimensionless
      "1"
      "Storage divided by capacity."
      "Is dimensionless comparison used responsibly?"
      Active
  ]

needsReview :: UnitRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed unit and dimension records:"
  mapM_ print unitRegister

  putStrLn "\nUnit records requiring review:"
  mapM_ print (filter needsReview unitRegister)
