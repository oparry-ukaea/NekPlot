import os.path
from glob import glob
from NekPy.LibUtilities import NekError, SessionReader
from NekPy.SpatialDomains import MeshGraph


#--------------------------------------------------------------------------------------------------
def _read_session_and_mesh(fpath, *other_args):
    if os.path.exists(fpath):
        args = ["NekPlot", fpath]
        args.extend(other_args[1:])
        try:
            session = SessionReader.CreateInstance(args)
            mesh = MeshGraph.Read(session)
            return session,mesh
        except NekError:
            # Silently ignore invalid input files and return None
            return None,None
    else:
        return None,None
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def _find_and_read_session_and_mesh(run_root, *other_args):
    """Helper function to automatically find an XML session file in [run_root].
       Constructed in a slightly convoluted way in order to give clear error/warning when 0/multiple session files are found.
    """
    xml_paths = glob(f"{run_root}/*.xml")
    sessions_and_meshes = {}
    for xml_path in xml_paths:
        sessions_and_meshes[xml_path] = _read_session_and_mesh(xml_path, *other_args)

    # Filter out invalid paths
    sessions_and_meshes = {path: obj for (path, obj) in sessions_and_meshes.items() if obj is not None}
    if len(sessions_and_meshes) == 0:
        raise RuntimeError(f"No valid session files found in {run_root}")
    else:
        first_path = list(sessions_and_meshes.keys())[0]
        if len(sessions_and_meshes) != 1:
            print("WARNING: "+__name__+f" found multiple valid session files in {run_root}")
            print(f"         Returning session read from {first_path}")
        return sessions_and_meshes[first_path],first_path
#--------------------------------------------------------------------------------------------------

#==================================================================================================
def read_session_and_mesh(run_root, session_fname=None, *other_args):
    session = None
    mesh    = None
    if session_fname is None:
        # If session_fname wasn't specified, try and find it automatically in run_root
        # Throws an exception if no valid input files are found
        (session,mesh), session_path = _find_and_read_session_and_mesh(run_root, *other_args)
    else:
        session_path = os.path.join(run_root,session_fname)
        session,mesh = _read_session_and_mesh(session_path, *other_args)
        if session is None:
            raise FileNotFoundError(f"Failed to find {session_fname}.xml in {run_root}")

    return session, session_path, mesh
#==================================================================================================