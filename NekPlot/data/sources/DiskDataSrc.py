from .DataSrc import DataSrc

class DiskDataSrc(DataSrc):
    def __init__(self,**kwargs) -> None:
        super().__init__(**kwargs)
        self.type = None