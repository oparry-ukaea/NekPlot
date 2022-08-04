from abc import ABC, abstractmethod

class DataSrc(ABC):
    def __init__(self,**kwargs) -> None:
        self.label = kwargs.pop('label','Unlabelled data source')
        self.plot_kws = {}
        self.var_name_map = {}
        self.type = None

    def Add_var_name_mappings(self,mappings):
        self.var_name_map.update(mappings)

    # Must be defined by subclasses
    @abstractmethod
    def exists(self):
        pass

    def Get_plot_kws(self):
        return self.plot_kws

    def Set_plot_kws(self, plot_kws):
        self.plot_kws.update(plot_kws)

    # Can be overridden by subclasses
    def is_valid(self):
        return True

    # Must be defined by subclasses
    @abstractmethod
    def _read(self, var_name, *args, **kwargs):
        pass

    def read(self, var_name_in, *args, **kwargs):
        var_name = self.var_name_map.get(var_name_in, var_name_in)
        if self.exists():
            if self.is_valid():
                return self._read(var_name, *args, **kwargs)
            else:
                raise RuntimeError("Read failed; data source seems to be invalid.\n"+self.__str__())
        else:
            print(self)
            raise RuntimeError("Read failed; data source not detected.\n"+self.__str__())

    def __str__(self):
        return f"Source (type = {self.type}) has params:"