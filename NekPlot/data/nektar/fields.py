import os
from NekPy.FieldUtils import Field, InputModule, ProcessModule

#def add_field(fields, new_field_name, new_field_def):
#    ProcessModule.Create("fieldfromstring", fields, fieldstr=new_field_def, fieldname=new_field_name).Run()

def read_fields(fpath,config_fpath, *args, derived_fields=None, **kwargs):
    """Read chk/fld files/dirs using NekPy"""
    if not os.path.exists(fpath):
        raise RuntimeError(__name__+f": No nektar output found at {fpath}")
    # Read config
    field = Field([], forceoutput=True) 
    InputModule.Create("xml", field, config_fpath).Run()

    try:
        # Read fld/chk file (type is 'fld', regardless)
        InputModule.Create("fld", field, fpath).Run()        

        # Add any derived fields that have been requested
        for new_field_name,new_field_def in derived_fields.items():
            ProcessModule.Create("fieldfromstring", field, fieldstr=new_field_def, fieldname=new_field_name).Run()

        # Return equi-spaced points for now
        ProcessModule.Create("equispacedoutput", field).Run()

        return field
    except Exception as ex:                
        print(f"Failed to load data from {fpath} using Nekpy; exception follows") 
        print(ex)
        return None       