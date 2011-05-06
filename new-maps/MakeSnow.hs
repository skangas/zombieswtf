
main = mapM_ putStrLn 
        [ "\t\t\t<i y=\"" ++ show y ++ "\" x=\"" ++ show x ++ 
          "\" r=\"0\" z=\"0.0\" o=\"snow02\" stackpos=\"0\"></i>"
        | y <- [-60..(60 :: Double)]
        , x <- [-60..(60 :: Double)]
        ]

