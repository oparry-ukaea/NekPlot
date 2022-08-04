from ..dsv import ReadDSV
from .SingleFileDataSrc import SingleFileDataSrc

class DSVDataSrc(SingleFileDataSrc):
    def __init__(self,path,delimiter=",", **kwargs):
        super().__init__(path,**kwargs)
        self.data = None       
        self.delimiter = delimiter
        self.type      = "DSV"

    def _read(self, var_name, *args, **kwargs):
        if self.data is None:
            self.data = ReadDSV(self.path,**kwargs)
        return self.data[var_name]

    def __str__(self):
        s = SingleFileDataSrc.__str__(self)
        s += f"\n delimiter={self.delimiter}"
        return s