from ..dsv import read_dsv
from .SingleFileDataSrc import SingleFileDataSrc

class DSVDataSrc(SingleFileDataSrc):
    def __init__(self,path,delimiter=",", **kwargs) -> None:
        super(SingleFileDataSrc,self).__init__(path,**kwargs)
        self.data      = None       
        self.delimiter = delimiter
        self.type      = "DSV"

    def _get(self, var_name, *args, **kwargs):
        if self.data is None:
            self.data = read_dsv(self.path,**kwargs)
        return self.data[var_name]

    def __str__(self):
        s = SingleFileDataSrc.__str__(self)
        s += f"\n delimiter={self.delimiter}"
        return s