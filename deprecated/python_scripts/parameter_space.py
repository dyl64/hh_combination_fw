#!/usr/bin/env python

models = {
           'hMSSM' : {'search_particle' : 'H', 'parameters' : ['mA', 'tanb'],        'xsec_to_be_compared': 'xs_ggFH_br_H_hh'},
           'EWS'   : {'search_particle' : 'H', 'parameters' : ['mH', 'cba', 'tanb'], 'xsec_to_be_compared': 'xs_ggFH_br_H_hh'}
         }


class parameter_point:

    def __init__(self, *args, **kwargs):
        self.parameters = {}

        for key, value in kwargs.items():
            if key == 'model':
                self.model = value
                continue
            self.parameters[key] = value


    @classmethod
    def from_dict(cls, model, param_dict):
        return cls(model=model, **param_dict)

    def print_all_parameters(self):
        for par, value in self.parameters.items():
            print("{}: {}".format(par, value))

    def model_parameters(self):

        str = ''
        for par in models[self.model]['parameters']:
            value = self.parameters[par]
            str += "{0}_{1}_".format(par, value)
        str = str[:-1]
        return str

    def __str__(self):
        return self.model_parameters()

    def __repr__(self):
        return self.model_parameters()

    def __getitem__(self, key):
        return self.parameters[key]

    def __setitem__(self, key, item):
        self.parameters[key] = item

    def __contains__(self, key):
        return key in self.parameters

    def __iter__(self):
        return iter(self.parameters)

    def keys(self):
        return self.parameters.keys()

    def items(self):
        return self.parameters.items()

    def values(self):
        return self.parameters.values()
