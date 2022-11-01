import re
import os
from NekPy.FieldUtils import Field, InputModule, ProcessModule

#--------------------------------------------------------------------------------------------------
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
#--------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------
def read_fields(fpath, config_fpaths, *args, derived_fields={}, compute_gradients=False, mode='equispacedoutput', **kwargs):
    """Read chk/fld files/dirs using NekPy"""
    if not os.path.exists(fpath):
        raise RuntimeError(__name__+f": No nektar output found at {fpath}")
    # Define new field
    field = Field([], forceoutput=True)

    try:
        if mode=='equispacedoutput':
            run_equispacedoutput_modules(field, fpath, config_fpaths, *args, derived_fields=derived_fields, compute_gradients=compute_gradients, mode=mode, **kwargs)
        elif mode=='interppoints':
            # Interpolation mode can't be combined with adding fields or gradients yet; warn the user if they're trying to do that. 
            if derived_fields:
                print(f"WARNING: Ignoring extra fields added to Nektar source - doesn't work in {mode} mode.")
            if compute_gradients:
                print(f"WARNING: compute_gradients for Nektar sources doesn't work in {mode} mode; ignoring.")
            # Interpolation mode requires a string to define the interpolation; bail out if it's missing
            interp_str = kwargs.pop('interp_str',None)
            if interp_str is None:
                raise RuntimeError(f"WARNING: 'interp_str' is a required kw arg when getting Nektar data in {mode} mode.")
            # Interpolation mode doesn't work with more than one config file; bail out if multiple were supplied
            Nconfig = len(config_fpaths)
            if Nconfig != 1:
                raise ValueError(__name__+": Exactly one xml config file must be supplied in 'interppoints' mode; received {}".format(Nconfig))
            run_interppoints_modules(field, fpath, config_fpaths, interp_str, *args, **kwargs)
        return field
    except Exception as ex:
        print(f"Failed to load data from {fpath} using Nekpy; exception follows") 
        print(ex)
        return None
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def run_equispacedoutput_modules(field, fpath, config_fpaths, *args, derived_fields={}, compute_gradients=False, mode='equispacedoutput', **kwargs):
    # Read config
    InputModule.Create("xml", field, *config_fpaths).Run()

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
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def run_interppoints_modules(field, fpath, config_fpaths, interp_str, *args, **kwargs):
    interp_kwargs=dict(fromxml=config_fpaths[0], fromfld=fpath)
    if interp_str.startswith('line='):
        interp_kwargs.update(line=interp_str[5:])
    else:
        raise RuntimeError("Reading nektar fields in 'equispacedoutput' mode: Only set up for line interpolation (interp string starting with line=) so far.")
    # Interpolate fields
    ProcessModule.Create("interppoints", field, **interp_kwargs).Run()
#--------------------------------------------------------------------------------------------------