import os.path
from glob import glob
from NekPy.LibUtilities import NekError, SessionReader
from NekPy.SpatialDomains import MeshGraph

from xml.dom.minidom import parse

#--------------------------------------------------------------------------------------------------
def _is_valid_xml(fpath):
    """Valid if the 'nektar' node can be read from XML"""
    if not os.path.exists(fpath):
        return False
    else:
        dom = parse(fpath)
        for root_node_name in ["nektar","NEKTAR"]:
            if dom.getElementsByTagName(root_node_name):
                return True
        return False
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def _filter_out_invalid_xml(fpaths_in):
    fpaths = [fp for fp in fpaths_in if _is_valid_xml(fp) ]
    if len(fpaths)==0:
        raise RuntimeError("No valid XML session files found")
    return fpaths
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def _gen_session_paths(run_root, session_fnames):
    ex = TypeError("session_fnames must be a string or a list of strings")
    if type(session_fnames)==list:
        session_paths = [os.path.join(run_root,f) if (type(f)==str) else None for f in session_fnames]
        if None in session_paths:
            raise ex
    elif type(session_fnames)==str:
        session_paths = [os.path.join(run_root,session_fnames)]
    else:
        raise ex
    return session_paths
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def _find_and_read_session_and_mesh(run_root, *other_args):
    """Helper function to automatically find XML session file(s) in [run_root].
    """
    xml_paths = _filter_out_invalid_xml(glob(f"{run_root}/*.xml"))
    session_and_mesh = _read_session_and_mesh(xml_paths, *other_args)
    return session_and_mesh,xml_paths
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def _read_session_and_mesh(fpaths, *other_args):
        args = ["NekPlot"]
        args.extend(fpaths)
        args.extend(other_args[1:])
        try:
            session = SessionReader.CreateInstance(args)
            mesh = MeshGraph.Read(session)
            return session,mesh
        except NekError:
            # Silently ignore invalid input files and return None
            return None,None
#--------------------------------------------------------------------------------------------------


#==================================================================================================
def read_session_and_mesh(run_root, session_fnames=None, *other_args):
    session = None
    mesh    = None
    if session_fnames is None:
        # If session_fname wasn't specified, try and find it automatically in run_root
        # Throws an exception if no valid input files are found
        (session,mesh), session_paths = _find_and_read_session_and_mesh(run_root, *other_args)
    else:
        session_paths = _filter_out_invalid_xml(_gen_session_paths(run_root, session_fnames))
        session,mesh  = _read_session_and_mesh(session_paths, *other_args)
        if session is None:
            raise FileNotFoundError("Unable to read session from file(s) "+",".join(session_paths)+" in "+run_root)

    return session, session_paths, mesh
#==================================================================================================