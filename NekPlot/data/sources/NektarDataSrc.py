import os.path

from .DiskDataSrc import DiskDataSrc
from ..nektar import detect_filebase, read_fields, read_session_and_mesh

class NektarDataSrc(DiskDataSrc):
    def __init__(self,run_root,session_fnames=None,chk_num=None,file_base=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.chk_num = chk_num
        self.compute_gradients=False
        self.derived_fields = {}
        self.fd = {} # Field data cache
        self.file_base = file_base
        self.mesh = None
        self.run_root = run_root
        self.session = None
        self.session_fnames = session_fnames
        self.type = "NEKTAR"

        # Allowed data retrieval modes
        self.valid_modes = ['equispacedoutput','interppoints']

        # Allow more args to be passed through to read_session_and_mesh here?
        self.session,self.session_fpaths,self.mesh = read_session_and_mesh(self.run_root, session_fnames=self.session_fnames)

        self._init_var_idx_map()


    def add_field(self, field_name,field_def_in):
        field_def = self._sub_param_vals(field_def_in)
        self.derived_fields[field_name] = field_def
        self._var_idx_map[field_name] = len(self._var_idx_map)

    def add_gradients(self):
        # Not sure about the effects of calling this twice yet, explicitly disable it for now.
        if not self.compute_gradients:
            self.compute_gradients=True
            nDims = self.mesh.GetMeshDimension()
            current_fields = list(self._var_idx_map.keys())[nDims:]
            grad_field_names = []
            for field_name in current_fields:
                coord_labels = 'xyz'
                for dim in range(nDims):
                    grad_field_name = field_name + "_" + coord_labels[dim]
                    grad_field_names.append(grad_field_name)
                    self._var_idx_map[grad_field_name] = len(self._var_idx_map)
            return grad_field_names
        else:
            print("Ignoring repeat call to add_gradients()")
            return []

    def get_session(self):
        return self.session


    def _exists(self):
        return True


    def _get(self, var_name, *args, **kwargs):
        use_cache = kwargs.get('use-cache',True)

        var_idx = self._get_var_idx(var_name)

        file_base = self.file_base if self.file_base is not None else detect_filebase(self.run_root)
        # By default, cache field data in self.fs dict
        #   Allow data retrieval in multiple 'modes' by storing them under different keys in the cache
        mode = kwargs.pop('mode','equispacedoutput')
        if not mode in self.fd or not use_cache:
            path_end = f"{file_base}.fld" if self.chk_num is None else f"{file_base}_{self.chk_num}.chk"
            field_fpath = os.path.join(self.run_root,path_end)
            # Read field data. For now this just gets equally spaced points
            if mode in self.valid_modes:
                self.fd[mode] = read_fields(field_fpath, self.session_fpaths, *args, derived_fields=self.derived_fields, compute_gradients=self.compute_gradients, mode=mode, **kwargs)
            else:
                raise ValueError(f"{mode} is not a valid mode for getting Nektar fields.  Allowed values are: ["+",".join(self.valid_modes)+"]")

        return self.fd[mode].GetPts(var_idx)


    def _get_var_idx(self,var_name):
        try:
            return self._var_idx_map[var_name]
        except KeyError as ex:
            print(f"Variable {var_name} not recognised in nektar data. Valid names are: ["+",".join(list(self._var_idx_map.keys()))+"]")
            raise ex


    def _init_var_idx_map(self):
        self._var_idx_map = {}
        nDims = self.mesh.GetMeshDimension()

        # Coords are read as fields from leading indices
        coord_labels = 'xyz'
        for coord_idx in range(nDims):
            self._var_idx_map[coord_labels[coord_idx]] = coord_idx

        for var_idx,var_name in enumerate(self.session.GetVariables()):
            self._var_idx_map[var_name] = var_idx + nDims


    def __str__(self):
        s = DiskDataSrc.__str__(self)
        s += "\n root_dir = "+self.run_root
        return s


    def _sub_param_vals(self, s_in):
        import re

        s = s_in
        for pname,pval in self.session.GetParameters().items():
            compiled = re.compile(re.escape(pname), re.IGNORECASE)
            s = compiled.sub(str(pval), s)
        return s