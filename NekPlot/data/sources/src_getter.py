from .DSVDataSrc import DSVDataSrc
from .NektarDataSrc import NektarDataSrc

src_map = dict(nektar=NektarDataSrc,dsv=DSVDataSrc)

def get_source(type, *args, **kw_args):
    try:
        return src_map[type](*args, **kw_args)
    except ValueError as ex:
        print(f"'{type}' is not a recognised data source type")
        raise(ex)