# Hunters, busybodies, and the knowledge network building associated with curiosity

Code for the paper, [*Hunters, busybodies, and the knowledge network building associated with curiosity*](https://psyarxiv.com/undy4).

## Setup

```
platform       x86_64-pc-linux-gnu         
arch           x86_64                      
os             linux-gnu                   
system         x86_64, linux-gnu           

R:             3.5.1 (2018-07-02)
MATLAB:        9.6.0.1174912 (R2019a)
Python:        2.7.15
```

See `environment_root.yml` for Python libraries and packages used.

## Author

Dale Zhou (dalezhou [at] pennmedicine.upenn.edu)

## Project Organization

```

    ├── data                                    <- Data goes here.
    │      |
    │      ├── subjectLevel
    │      ├── kFolds
    │
    ├── scripts                                 <- Downloaded functions go here
    │      |
    │      ├── copyScripts.sh                   <- prepare code to fit each individual
    │      ├── editScripts.sh                   <- prepare code to fit each individual
    │      ├── entropySimulated.py              <- function for entropy
    │      ├── errwLevyFunction.py              <- function for growth model
    │      ├── errwLevyFunction.m               <- MATLAB version of growth model
    │      ├── heapsSimulated.py                <- function for Heaps' law
    │      ├── intervalsSimulated.py            <- function for inter-event time
    │      ├── launchAnalysis.sh                <- launch training on cluster
    │      ├── launchTest.sh                    <- launch test on cluster
    │      ├── nsga.py                          <- main script running evolutionary optimization
    │      ├── testFit.py                       <- main script testing fit
    │      ├── wikiWrangler.R                   <- prepare code to fit each individual
    │      ├── zipfsSimulated.py                <- function for Zipf's law
    │
    │
    ├── environment_root.yml                    <- Python environment packages
    │
    ├── README.md

```

## Order of scripts

1. Run `wikiWrangler.R` to get train and test folds
2. `copyScripts.sh` if `copyCommands` does not exist. Then source `copyCommands`
3. `editScripts.sh` if `editCommands` does not exist. Then source `editCommands`
4. qsub `launchAnalysis.sh` to launch the `nsga.py` scripts
5. qsub `launchTest.sh` to launch the `testFit.py` scripts

### Notes
The growth model itself is `errwLevyFunction.py` or `errwLevyFunction.m` for equivalent Python and MATLAB versions. All other code is to fit individual data to that growth model. 

Scripts were run on a high-performance computing cluster.