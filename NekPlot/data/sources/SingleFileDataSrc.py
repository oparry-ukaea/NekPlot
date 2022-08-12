
from .DiskDataSrc import DiskDataSrc
import os.path

class SingleFileDataSrc(DiskDataSrc):
    def __init__(self, path, **kwargs) -> None:
        super().__init__(**kwargs)
        self.path = path

    def _exists(self):
        return os.path.isfile(self.path)

    def __str__(self):
        s = DiskDataSrc.__str__(self)
        s += f"\n path={self.path}"
        return s