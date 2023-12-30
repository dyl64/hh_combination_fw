from typing import Union, List, Tuple

from quickstats import DescriptiveEnum

class TaskType(DescriptiveEnum):
    LIMIT        = (0, "Upper limit", "limit", True)
    LIKELIHOOD   = (1, "Likelihood fit", "likelihood", True)
    SIGNIFICANCE = (2, "Significance and pvalue", "significance", True)
    RANKING      = (3, "Nuisance parameter ranking", "ranking", False)
    MODIFICATION = (10, "Modify workspaces", "workspace", False)
    COMBINATION  = (11, "Combine workspaces", ("cfg", "workspace"), False)

    def __new__(cls, value:int, description:str, output_type:Union[str, Tuple], has_runner:bool):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        obj.output_type = output_type
        obj.has_runner = has_runner
        return obj
        
kDefaultCombPOI         = 'xsec_br'
kDefaultBlindDataset    = 'asimovData'
kDefaultUnblindDataset  = 'obsData'
kDefaultCombDataset     = 'combData'
kCombLimitFileName      = 'limits.json'
kModificationOptionList = ["rescale_poi",
                           "define_parameters", "define_constraints",
                           "redefine_parameters", "rename_parameters",
                           "add_product_terms", "gen_asimov",
                           "fix_parameters", "profile_parameters", "set_parameters"]
kRescaledOldPOIName     = "mu_old"
kCombWSName             = "combWS"