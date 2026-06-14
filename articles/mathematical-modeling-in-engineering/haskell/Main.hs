{-# OPTIONS_GHC -Wall #-}

module Main where

data EngineeringDomain
  = StructuralEngineering
  | MechanicalEngineering
  | ElectricalEngineering
  | ChemicalEngineering
  | SystemsEngineering
  | ReliabilityEngineering
  deriving (Eq, Show)

data EngineeringModelRole
  = InitialDesign
  | PerformanceAnalysis
  | SafetyReview
  | Optimization
  | Validation
  | LifecycleMonitoring
  deriving (Eq, Show)

data EngineeringModelFamily
  = AlgebraicDesignModel
  | DifferentialEquationModel
  | FiniteElementModel
  | ControlModel
  | ReliabilityModel
  | SimulationModel
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSafetyReview
  | Revise
  deriving (Eq, Show)

data EngineeringModelRecord = EngineeringModelRecord
  { key :: String
  , domain :: EngineeringDomain
  , role :: EngineeringModelRole
  , family :: EngineeringModelFamily
  , designQuestion :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

engineeringRegister :: [EngineeringModelRecord]
engineeringRegister =
  [ EngineeringModelRecord
      "sizing_model"
      StructuralEngineering
      InitialDesign
      AlgebraicDesignModel
      "What beam dimensions are feasible under baseline load?"
      Active
  , EngineeringModelRecord
      "safety_model"
      StructuralEngineering
      SafetyReview
      AlgebraicDesignModel
      "Does the design maintain positive stress margin?"
      RequiresSafetyReview
  , EngineeringModelRecord
      "optimization_model"
      SystemsEngineering
      Optimization
      SimulationModel
      "Which design balances weight and safety margin?"
      RequiresReview
  , EngineeringModelRecord
      "validation_model"
      ReliabilityEngineering
      Validation
      ReliabilityModel
      "What test evidence is needed before use?"
      RequiresValidation
  ]

needsReview :: EngineeringModelRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed engineering model records:"
  mapM_ print engineeringRegister

  putStrLn "\nEngineering model records requiring review:"
  mapM_ print (filter needsReview engineeringRegister)
