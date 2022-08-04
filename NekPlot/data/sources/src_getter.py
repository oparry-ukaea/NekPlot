from NekPlot.data.sources.DSVDataSrc import DSVDataSrc
from .NektarDataSrc import NektarDataSrc
from .DSVDataSrc import DSVDataSrc

src_map = dict(nektar=NektarDataSrc,dsv=DSVDataSrc)

def Get_source(type, *args, **kw_args):
    try:
        return src_map[type](*args, **kw_args)
    except ValueError as ex:
        print(f"'{type}' is not a recognised data source type")
        raise(ex)