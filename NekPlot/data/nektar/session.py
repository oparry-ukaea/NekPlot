import os.path

from NekPy.LibUtilities import SessionReader
from NekPy.SpatialDomains import MeshGraph

#==================================================================================================
def read_session_and_mesh(run_root, session_fname, *other_args):
    # Try session filename as-is first, then append '.xml' if it's not found 
    session = None
    graph   = None
    for postfix in ["",".xml"]:
        session_fpath = os.path.join(run_root,session_fname+postfix)
        if os.path.exists(session_fpath):
            args = ["NekPlot", session_fpath]
            args.extend(other_args[1:])
            session = SessionReader.CreateInstance(args)
            graph = MeshGraph.Read(session)
            break
    if session is None:
        raise ValueError(f"Failed to find either {session_fname} or {session_fname}.xml in {run_root}")
    return session, graph
#==================================================================================================