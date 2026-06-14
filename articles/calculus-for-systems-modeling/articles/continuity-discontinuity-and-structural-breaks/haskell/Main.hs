{-# OPTIONS_GHC -Wall #-}

module Main where

newtype Input = Input Double deriving (Show)
newtype Output = Output Double deriving (Show)
newtype Slope = Slope Double deriving (Show)
newtype Jump = Jump Double deriving (Show)

data BreakFlag
  = OK
  | PossibleJump
  | PossibleSlopeBreak
  | LevelAndSlopeBreak
  deriving (Show)

data Diagnostic = Diagnostic
  { input :: Input
  , output :: Output
  , leftSlope :: Maybe Slope
  , rightSlope :: Maybe Slope
  , levelJump :: Maybe Jump
  , flag :: BreakFlag
  } deriving (Show)

piecewiseSystem :: Input -> Output
piecewiseSystem (Input x)
  | x < 5 = Output (2.0 + 0.5 * x)
  | otherwise = Output (6.0 + 1.4 * (x - 5.0))

classify :: Double -> Double -> BreakFlag
classify jump slopeChange
  | jump > 1.0 && slopeChange > 0.5 = LevelAndSlopeBreak
  | jump > 1.0 = PossibleJump
  | slopeChange > 0.5 = PossibleSlopeBreak
  | otherwise = OK

main :: IO ()
main = do
  let xs = map (\n -> Input (fromIntegral n * 0.25)) [0..40]
  let ys = map piecewiseSystem xs
  print "Synthetic typed continuity diagnostics generated."
  print (take 5 (zip xs ys))
  print (classify 1.2 0.8)
  print "Use Python/R workflows for full tabular diagnostics."
