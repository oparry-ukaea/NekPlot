import re
import os
from NekPy.FieldUtils import Field, InputModule, ProcessModule

def detect_filebase(root_dir,exts=["chk","fld"]):
    matcher = re.compile("(.*?)_?[0-9]*\.(?:"+"|".join(exts)+")$")
    fbases = set([match.groups()[0] for match in [matcher.match(os.path.basename(p)) for p in os.listdir(root_dir)] if match])
    if len(fbases)==0:
        raise RuntimeError("No files of type "+" or ".join(exts)+f" found in {root_dir}")
    else:
        first_fbase = list(fbases)[0]
        if len(fbases)>1:
            print(__name__+f": WARNING: found >1 possible file base in {root_dir}...using {first_fbase}.")
        return first_fbase


def read_fields(fpath, config_fpaths, *args, derived_fields={}, compute_gradients=False, **kwargs):
    """Read chk/fld files/dirs using NekPy"""
    if not os.path.exists(fpath):
        raise RuntimeError(__name__+f": No nektar output found at {fpath}")
    # Read config
    field = Field([], forceoutput=True) 
    InputModule.Create("xml", field, *config_fpaths).Run()

    try:
        # Read fld/chk file (type is 'fld', regardless of whether output format is default or hdf5)
        InputModule.Create("fld", field, fpath).Run()        

        # Add any derived fields that have been requested
        for new_field_name,new_field_def in derived_fields.items():
            ProcessModule.Create("fieldfromstring", field, fieldstr=new_field_def, fieldname=new_field_name).Run()

        # Compute gradients for all fields, if requested
        if compute_gradients:
            ProcessModule.Create("gradient",field).Run()

        # Return equi-spaced points for now
        ProcessModule.Create("equispacedoutput", field).Run()

        return field
    except Exception as ex:                
        print(f"Failed to load data from {fpath} using Nekpy; exception follows") 
        print(ex)
        return None       