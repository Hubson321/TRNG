# TRNG
Random Generator python script based on `I-Te Chen “Random Numbers Generated from Audio and Video Sources”, Mathematical Problems in Engineering (Volume 2013, Article ID 285373`.


Project consists of: 
- [Videos](Videos) folder with video samples for analyzing and generating random numbers
- [OutputsUltimate](OutputsUltimate) folder with output 8-bit strings representing binary 8-bit numbers
- [algorithm.py](algorith.py) file, which is main algorithm for analyzing video inputs and generating random bits
- [hitograms.py](hitograms.py) file fo generating histogram/s of given files with entropy of given numbers

In [algorithm.py](algorith.py) only thing to define is `file` variable with the name of video file input inside [Videos](Videos) folder (`.txt` file in [OutputsUltimate](OutputsUltimate) is generated automatically and also needs to be defined in `file` variable in [hitograms.py](hitograms.py) as a file name withouot extension).
