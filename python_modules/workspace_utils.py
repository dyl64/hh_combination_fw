# copied from RooStatTools/python_modules/workspace_utils.py (Rui Zhang)
import os
import ROOT

class WSModel:
    def __init__(self, fname:str, ws_name=None, mc_name:str=None):
        self.initialize(fname, ws_name, mc_name)
        
    def initialize(self, fname, ws_name, mc_name):
        if not os.path.exists(fname):
            raise FileNotFoundError("workspace file {} does not exist".format(fname))
        file = ROOT.TFile(fname) 
        if (not file):
            raise RuntimeError("something went wrong while loading the root file: {}".format(fname))
        if ws_name is None:
            ws_names = [i.GetName() for i in file.GetListOfKeys() if i.GetClassName() == 'RooWorkspace']
            if not ws_names:
                raise RuntimeError("No workspaces found in the root file: {}".format(fname))
            if len(ws_names) > 1:
                print("WARNING: Found multiple workspace instances from the root file: {}. Available workspaces"
                      " are \"{}\". Will choose the first one by default".format(fname, ','.join(ws_names)))
            ws_name = ws_names[0]
        ws = file.Get(ws_name)
        if not ws:
            raise RuntimeError("something went wrong while loading the workspace: {}".format(self.ws_name))
        if mc_name is None:
            mc_names = [i.GetName() for i in ws.allGenericObjects() if 'ModelConfig' in i.ClassName()]
            if not mc_names:
                raise RuntimeError("no ModelConfig object found in the workspace: {}".format(ws_name))
            if len(mc_names) > 1:
                print("WARNING: Found multiple ModelConfig instances from the workspace: {}. "
                      "Available ModelConfigs are \"{}\". "
                      "Will choose the first one by default".format(ws_name, ','.join(mc_names)))
            mc_name = mc_names[0]
        model_config = ws.obj(mc_name)
        if not model_config:
            raise RuntimeError("failed to load model config {}".format(self.model_config_name))
        
        datasets = [i for i in ws.allData()]
        if not datasets:
            raise RuntimeError("failed to load datasets")
        pois = model_config.GetParametersOfInterest()
        if not pois:
            raise RuntimeError("failed to load parameters of interest")
        self.file = file
        self.workspace = ws
        self.model_config = model_config
        self.pois = pois
        self.datasets = datasets
        
    def get_first_poi_name(self):
        return self.pois[0].GetName()
    
    def get_poi_names(self):
        return [p.GetName() for p in self.pois]
    
    def get_nuisance_parameter_names(self):
        return [np.GetName() for np in self.model_config.GetNuisanceParameters()]
    
    def get_first_dataset_name(self):
        return self.datasets[0].GetName()
    
    def get_dataset_names(self):
        return [d.GetName() for d in self.datasets]
    
    def save_summary(self, fname):
        ROOT.gSystem.RedirectOutput(fname)
        self.workspace.Print()
        ROOT.gROOT.ProcessLine('gSystem->RedirectOutput(0);')
    
    def save(self, fname):
        self.workspace.writeToFile(fname)
