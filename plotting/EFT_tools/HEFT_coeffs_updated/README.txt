     ## Instructions for the data files ##
Contact information: Tom Ingebretsen Carlson <tom.ingebretsen-carlson@fysik.su.se>.


The folder contain the following sub folders:
muR_muF_0p5 muR_muF_1  muR_muF_2
Which contain the inclusive A-coefficients and differential dA-coefficients for the renormalization and factorization scales muR = muF = {0.5*c,1*c,2*c}, where c = m_hh/2. They also contain the covariance matrices for the A-coefficients and dA-coefficients.

The sub folders contain the following files
HEFT_dA_and_A_with_Binning_250_1050_41_Variable_Bins_1200_1400_muR_muF_*.txt
HEFT_CovMat_for_A_muR_muF_*.txt 
HEFT_CovMat_for_dA_muR_muF_*.txt 


Explanation of the files:

HEFT_dA_and_A_with_Binning_250_1050_41_Variable_Bins_1200_1400_muR_muF_*.txt - contain the inclusive A-coefficients and differential dA-coefficients.
The inclusive A-coefficients are on the last row, while the differential dA-coefficients are divided bin by bin where the first value is the central mhh value of that bin.

HEFT_CovMat_for_dA_muR_muF_*.txt - contain the covariance matrices for the differential dA-coefficients. The covariance matrices are 23x23 and are unique for every bin. The bin is given by the first number in the covariance matrix, which is the central mhh value of that bin. Thereby, a covariance matrix starting with a specific mhh value corresponds to the covariance matrix of the dA coefficients with the same mhh value in the file HEFT_dA_and_A_with_Binning_250_1050_41_Variable_Bins_1200_1400_muR_muF_*.txt. 

HEFT_CovMat_for_A_muR_muF_*.txt - contain the covariance matrix for the inclusive A-coefficients. Corresponds to the covariance matrix of A-coefficients found in the last row in the file HEFT_dA_and_A_with_Binning_250_1050_41_Variable_Bins_1200_1400_muR_muF_*.txt. 
