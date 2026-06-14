{-# OPTIONS_GHC -Wall #-}

module Main where

data PublicHealthDomain
  = InfectiousDisease
  | PublicHealthSurveillance
  | HealthSystemPlanning
  | HealthEquity
  | PublicCommunication
  deriving (Eq, Show)

data PublicHealthModelRole
  = TransmissionAnalysis
  | DataInterpretation
  | CapacityReview
  | DistributionalReview
  | UncertaintyCommunication
  deriving (Eq, Show)

data PublicHealthModelFamily
  = SIRCompartmentalModel
  | NowcastingAndReportingDelayModel
  | HospitalDemandModel
  | SubgroupRiskModel
  | ScenarioSummaryModel
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresEquityReview
  | RequiresSurveillanceReview
  | RequiresCommunicationReview
  deriving (Eq, Show)

data PublicHealthModelRecord = PublicHealthModelRecord
  { key :: String
  , domain :: PublicHealthDomain
  , role :: PublicHealthModelRole
  , family :: PublicHealthModelFamily
  , publicHealthQuestion :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

publicHealthRegister :: [PublicHealthModelRecord]
publicHealthRegister =
  [ PublicHealthModelRecord
      "transmission_model"
      InfectiousDisease
      TransmissionAnalysis
      SIRCompartmentalModel
      "How does transmission change under different intervention assumptions?"
      Active
  , PublicHealthModelRecord
      "surveillance_model"
      PublicHealthSurveillance
      DataInterpretation
      NowcastingAndReportingDelayModel
      "How should reported data be interpreted under delay and undercounting?"
      RequiresSurveillanceReview
  , PublicHealthModelRecord
      "capacity_model"
      HealthSystemPlanning
      CapacityReview
      HospitalDemandModel
      "Could projected severe cases exceed healthcare capacity?"
      RequiresReview
  , PublicHealthModelRecord
      "equity_model"
      HealthEquity
      DistributionalReview
      SubgroupRiskModel
      "Which populations face unequal exposure, severity, or access?"
      RequiresEquityReview
  , PublicHealthModelRecord
      "communication_model"
      PublicCommunication
      UncertaintyCommunication
      ScenarioSummaryModel
      "How should model uncertainty and use limits be communicated?"
      RequiresCommunicationReview
  ]

needsReview :: PublicHealthModelRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed public health model records:"
  mapM_ print publicHealthRegister

  putStrLn "\nPublic health records requiring review:"
  mapM_ print (filter needsReview publicHealthRegister)
