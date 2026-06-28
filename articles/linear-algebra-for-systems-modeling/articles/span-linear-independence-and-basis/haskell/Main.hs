module Main where

data SpanBasisAudit = SpanBasisAudit
  { vectorSetName :: String
  , ambientDimension :: Int
  , vectorCount :: Int
  , rankValue :: Int
  , spansAmbientSpace :: Bool
  , linearlyIndependent :: Bool
  , isBasisForAmbientSpace :: Bool
  , modelingRole :: String
  , interpretationWarning :: String
  } deriving (Show)

determinant3x3 :: [[Double]] -> Double
determinant3x3 m =
  let a = (m !! 0) !! 0
      b = (m !! 0) !! 1
      c = (m !! 0) !! 2
      d = (m !! 1) !! 0
      e = (m !! 1) !! 1
      f = (m !! 1) !! 2
      g = (m !! 2) !! 0
      h = (m !! 2) !! 1
      i = (m !! 2) !! 2
  in a * (e * i - f * h)
     - b * (d * i - f * g)
     + c * (d * h - e * g)

rank3x3Simple :: [[Double]] -> Int
rank3x3Simple matrix =
  if abs (determinant3x3 matrix) > 1e-10
  then 3
  else 2

buildAudit :: SpanBasisAudit
buildAudit =
  let matrix =
        [ [1.0, 0.0, 0.5]
        , [0.0, 1.0, 0.5]
        , [0.0, 0.0, 1.0]
        ]
      ambient = 3
      count = 3
      rank = rank3x3Simple matrix
      spans = rank == ambient
      independent = rank == count
      basis = spans && independent
  in SpanBasisAudit
      "candidate_system_basis"
      ambient
      count
      rank
      spans
      independent
      basis
      "Candidate basis vectors for a simplified system representation."
      "A mathematical basis claim does not prove real-world representational adequacy."

main :: IO ()
main =
  print buildAudit
