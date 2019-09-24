# Workspace versions


## bbbb

| **Version** |  **Date**  | **Comment** |
| ----------- | ---------- | ----------------------------- |
|    v00      | 2017.07.27 |                               |
|    v01      | 2017.08.27 |                               |
|    v02      | 2017.10.19 |                               |
|    v03      | 2017.10.19 | Non-resonant not yet updated! |

## bb&tau;&tau;

| **Version** |  **Date**  | **Comment** |
| ----------- | ---------- | ----------- |
|    v00      | 2017.07.31 |             |

## bb&gamma;&gamma;

| **Version** |  **Date**  | **Comment** |
| ----------- | ---------- | ----------- |
|    v00      | 2017.07.27 |             |
|    v01      | 2017.10.19 |             |

## bbWW

| **Version** |  **Date**  | **Comment** |
| ----------- | ---------- | ----------- |
|    v00      | 2017.10.17 |             |
|    v01      | 2017.11.16 |             |

- v1
    
    Received on 16/11/2017 from Gabriel Palacino.
    
    Source:
    `palacino/public/forCombination/workspaces`
    
    Accompanying messages:
    
    - 16 November 2017 at 11:09:
        One important thing. For getting the graviton limits you should use the scalar cross section and not
        the graviton cross sections. There are
        
        600 GeV - 1800 GeV: 0.044 pb
        2000 GeV - 3000 GeV: 0.041 pb
        
        This is due to the method we used for the interpolation using the scalar samples.
        
        Also, I have updated the non-resonant workspace as well. The new one uses the signal with the new
        reweighting. You should see an improvement in the expected/observed limit of about 37% with respect
        to the previous workspace.
    
    - 16 November 2017 at 12:53:
        There was a bug in the previous non-resonant workspace. I have updated it my public area. The change
        now is only 16%.


## WW&gamma;&gamma;

| **Version** |  **Date**  | **Comment** |
| ----------- | ---------- | ----------- |
|    v00      | 2017.07.31 |             |
|    v01      | 2017.10.22 |             |
|    v02      | 2017.10.24 |             |
|    v03      | 2017.11.01 |             |

- v3
    solved the issue `Error in <RooFormula::Compile>: Bad numerical expression : "d_Lumi"`
