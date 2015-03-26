for %%i in (..\project3\data\t-parsed-files\*.*) do (
chunklink_2-2-2000_for_conll.pl -B BeginEndCombined -t -p -f %%i > %%~ni.chunk
)