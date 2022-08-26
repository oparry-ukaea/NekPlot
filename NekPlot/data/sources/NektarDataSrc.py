import os.path

from .DiskDataSrc import DiskDataSrc
from ..nektar import detect_filebase, read_fields, read_session_and_mesh

class NektarDataSrc(DiskDataSrc):
    def __init__(self,run_root,session_fnames=None,chk_num=None,file_base=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.chk_num = chk_num
        self.derived_fields = {}
        self.fd = None # Field data cache
        self.file_base = file_base
        self.mesh = None
        self.run_root = run_root
        self.session = None
        self.session_fnames = session_fnames
        self.type = "NEKTAR"

        # Allow more args to be passed through to read_session_and_mesh here?
        self.session,self.session_fpaths,self.mesh = read_session_and_mesh(self.run_root, session_fnames=self.session_fnames)

        self._init_var_idx_map()


    def add_field(self, field_name,field_def_in):
        field_def = self._sub_param_vals(field_def_in)
        self.derived_fields[field_name] = field_def
        self._var_idx_map[field_name] = len(self._var_idx_map)


    def get_session(self):
        return self.session


    def _exists(self):
        return True


    def _get(self, var_name, *args, **kwargs):
        use_cache = kwargs.get('use-cache',True)

        var_idx = self._get_var_idx(var_name)

        file_base = self.file_base if self.file_base is not None else detect_filebase(self.run_root)
        # By default, cache field data in self.fs
        if self.fd is None or not use_cache:
            path_end = f"{file_base}.fld" if self.chk_num is None else f"{file_base}_{self.chk_num}.chk"
            field_fpath = os.path.join(self.run_root,path_end)
            # Read field data. For now this just gets equally spaced points
            self.fd = read_fields(field_fpath, self.session_fpaths, *args, derived_fields=self.derived_fields, **kwargs)

        return self.fd.GetPts(var_idx)


    def _get_var_idx(self,var_name):
        try:
            return self._var_idx_map[var_name]
        except KeyError as ex:
            print(f"Variable {var_name} not recognised in nektar data. Valid names are: ["+",".join(list(self._var_idx_map.keys()))+"]")
            raise ex


    def _init_var_idx_map(self):
        nd = self.mesh.GetMeshDimension()
        if nd != 1:
            raise NotImplementedError(f"Mesh dimension is {nd} but NektarDataSrc is only setup for 1D so far. _init_var_idx_map() and possibly other methods may need to change.")

        self._var_idx_map = {}
        self._var_idx_map['coords'] = 0
        for var_idx,var_name in enumerate(self.session.GetVariables()):
            self._var_idx_map[var_name] = var_idx + nd


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