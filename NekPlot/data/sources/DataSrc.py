from abc import ABC, abstractmethod

class DataSrc(ABC):
    def __init__(self,label='Unlabelled data source') -> None:
        self.label        = label
        self.plot_kws     = {}
        self.type         = None
        self.var_name_map = {}

    def add_var_name_mappings(self,mappings):
        self.var_name_map.update(mappings)

    def get(self, var_name_in, *args, **kwargs):
        var_name = self.var_name_map.get(var_name_in, var_name_in)
        if self._exists():
            if self._is_valid():
                return self._get(var_name, *args, **kwargs)
            else:
                raise RuntimeError("Read failed; data source seems to be invalid.\n"+self.__str__())
        else:
            print(self)
            raise RuntimeError("Read failed; data source not detected.\n"+self.__str__())

    def get_plot_kws(self):
        return self.plot_kws

    def set_plot_kws(self, plot_kws):
        self.plot_kws.update(plot_kws)

    # Subclasses MUST define what existence of a source means
    @abstractmethod
    def _exists(self):
        pass

    # Subclasses MUST define a method to retrieve data from a source
    @abstractmethod
    def _get(self, var_name, *args, **kwargs):
        pass

    # Subclasses CAN define what validity of a source means
    def _is_valid(self):
        return True
    
    def __str__(self):
        return f"Source (type = {self.type}) has params:"