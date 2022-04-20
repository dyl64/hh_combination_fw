from typing import Optional, Union, List, Dict
import json
from string import Formatter
import quickstats

from quickstats.utils.xml_tools import TXMLTree

def create_channel_node(root_node, channel:str, fname:str, poi_name:str, rename_map:Dict=None,
                        ws_name:Optional[str]=None, mc_name:Optional[str]=None, data_name:str='combData',
                        ignore_missing_keys=False):
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 86f6fa86281c7ec55a34010bb03b1fa8a4af8a40
    from quickstats.components import ExtendedModel
    model = ExtendedModel(fname, verbosity="ERROR", ws_name=ws_name,
                          mc_name=mc_name, data_name=data_name)
    ws_name   = model.workspace.GetName()
    mc_name   = model.model_config.GetName()
    data_name = model.data.GetName()
    
    channel_node = root_node.add_node('Channel', Name=channel,
                                      InputFile=fname,
                                      WorkspaceName=ws_name,
                                      ModelConfigName=mc_name,
                                      DataName=data_name)
                                                      
    POI_node = channel_node.add_node('POIList', Input=poi_name)
                             
    rename_node = channel_node.add_node('RenameMap')
    
    if rename_map is not None:
        constraints = model.pair_constraints(to_str=True)
        np_list = [i.GetName() for i in model.nuisance_parameters]
        for (pdf_name, np_name, glob_name) in constraints: 
            if np_name not in np_list:
                continue
            if (np_name not in rename_map) and (not ignore_missing_keys):
                raise ValueError(f'missing mapping for the nuisance parameter "{np_name}" '
                                 f'in the workspace "{fname}"')
            new_name = rename_map[np_name]
            # new nuisance parameter name not specified
            if new_name is None:
                print(f'WARNING: Mapping for the nuisance parameter "{np_name}" is null. Skipped.')
                continue
            old_name_full = f'{pdf_name}( {np_name}, {glob_name})'
            rename_node.add_node('Syst', OldName=old_name_full, NewName=new_name)
    
def create_combination_xml(channel_attributes:Dict, output_ws:str, poi_name:str, rename_map:Dict=None,
                           ws_name:str='combWS', mc_name:str='ModelConfig',
                           data_name:str='combData', ignore_missing_keys:bool=False):
<<<<<<< HEAD
=======
    channel_node = root_node.add_node('Channel', Name=channel, 
                                      InputFile=fname,
                                      WorkspaceName=ws_name,
                                      ModelConfigName=mc_name,
                                      DataName=data_name,
                                      )
    POI_node = channel_node.add_node('POIList', Input=poi_name)
    rename_node = channel_node.add_node('RenameMap')
    from quickstats.components import ExtendedModel
    if rename_map is not None:
        model = ExtendedModel(fname, verbosity="ERROR", binned_likelihood=False,
                                tag_as_measurement=None, data_name=data_name)
        constraints = model.pair_constraints(to_str=True)
        np_list = [i.GetName() for i in model.nuisance_parameters]
        for (pdf_name, np_name, glob_name) in constraints:   
            if np_name not in np_list:
                continue
            if (np_name not in rename_map) and (not ignore_missing_keys):
                raise ValueError('missing mapping for the nuisance parameter "{}" '
                                'in the workspace "{}"'.format(np_name, fname))
            new_name = rename_map[np_name]
            # new nuisance parameter name not specified
            if new_name is None:
                print('WARNING: Mapping for the nuisance parameter "{}" is null. '
                      'Skipped.'.format(np_name))
                continue
            old_name_full = '{}( {}, {})'.format(pdf_name, np_name, glob_name)
            rename_node.add_node('Syst', OldName=old_name_full, NewName=new_name)
    
def create_combination_xml(input_ws, output_ws, poi_name, rename_map=None, wd_name=None,
                           ws_name='combWS', mc_name='ModelConfig', data_name='combData',
                           ignore_missing_keys=False):
>>>>>>> 6fadbd486b2e9a2f7d52d4cf3d5e24d923ce0b88
=======
>>>>>>> 86f6fa86281c7ec55a34010bb03b1fa8a4af8a40
    quickstats.set_verbosity("WARNING")
    rename_map = {} if rename_map is None else rename_map
    xml = TXMLTree(doctype='Combination', system='Combination.dtd')
    xml.new_root('Combination', WorkspaceName=ws_name, ModelConfigName=mc_name, DataName=data_name, OutputFile=output_ws)
    xml.add_node('POIList', Combined=formate_poi_name(poi_name))
    xml.add_node('Asimov', Name='fit')
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 86f6fa86281c7ec55a34010bb03b1fa8a4af8a40
    for channel in channel_attributes:
        channel_rename_map = rename_map.get(channel, None)
        channel_filename  = channel_attributes[channel]["filename"]
        channel_ws_name   = channel_attributes[channel].get("ws_name", None)
        channel_mc_name   = channel_attributes[channel].get("mc_name", None)
        channel_data_name = channel_attributes[channel].get("data_name", data_name)
        create_channel_node(xml, channel, channel_filename, poi_name, rename_map=channel_rename_map,
                            ws_name=channel_ws_name, mc_name=channel_mc_name, data_name=channel_data_name,
<<<<<<< HEAD
=======
    for channel in input_ws:
        channel_rename_map = rename_map.get(channel, None)
        create_channel_node(xml, channel, input_ws[channel], poi_name, rename_map=channel_rename_map,
                            ws_name=wd_name[channel]['ws_name'], mc_name=mc_name, data_name=wd_name[channel]['data_name'],
>>>>>>> 6fadbd486b2e9a2f7d52d4cf3d5e24d923ce0b88
=======
>>>>>>> 86f6fa86281c7ec55a34010bb03b1fa8a4af8a40
                            ignore_missing_keys=ignore_missing_keys)
    quickstats.set_verbosity("INFO")
    return xml

<<<<<<< HEAD
<<<<<<< HEAD
def formate_poi_name(poi_name:str):
    new_poi = [f"{p}[1~1]" for p in poi_name.split(',') if p]
    new_poi = ','.join(new_poi)
    return new_poi
=======
def formate_poi_name(poi_name):
    new_poi=poi_name.split(',')
    new_poi = [ ( p + '[1~1]') for p in new_poi ]
    new_poi = ','.join(new_poi)
    print(new_poi)
    
    return new_poi
>>>>>>> 6fadbd486b2e9a2f7d52d4cf3d5e24d923ce0b88
=======
def formate_poi_name(poi_name:str):
    new_poi = [f"{p}[1~1]" for p in poi_name.split(',') if p]
    new_poi = ','.join(new_poi)
    return new_poi
>>>>>>> 86f6fa86281c7ec55a34010bb03b1fa8a4af8a40
