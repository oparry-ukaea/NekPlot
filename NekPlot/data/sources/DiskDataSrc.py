from .DataSrc import DataSrc

class DiskDataSrc(DataSrc):
    def __init__(self,**kwargs) -> None:
        DataSrc().__init__(**kwargs)
        self.Type = None