"""
SPIF parameter documentation formatter

"""


# ----------------------------------------------------------------------
class ncParam():

    def __init__(self, param):
        self.dtype = None
        self.group = None
        self.name = None
        self.path = None
        self.dims = []
        self.attrs = {}

        # Identify type of parameter
        nctypes = [(k1,k2) for k1,v1 in param.items()
                           for k2,v2 in ALLOWED_TYPES.items()
                           if k1 in v2 and v1==None]
        if len(nctypes) > 1:
            raise KeyError(
                       f"More than one parameter type given for {param.name}.")
        try:
            typekey, self.nctype = nctypes[0]
        except IndexError as err:
            raise err(f"No parameter type given for {param.name}. Must be one of ",
                      ', '.join(ALLOWED_TYPES.keys()))

        _ = param.pop(typekey)

        if self.nctype == 'grp':
            self.set_ncgrp(param)
        elif self.nctype == 'attr':
            self.set_ncattr(param)
        elif self.nctype == 'dim':
            self.set_ncdim(param)
        elif self.nctype == 'coord':
            self.set_ncvar(param)
        elif self.nctype == 'var':
            self.set_ncvar(param)
            if [self.name] == self.dims:
                self.nctype = 'coord'

    def _grprst(self):
        if self.group == '/':
            return "~~~~\nroot\n~~~~\n"
        else:
            return f"\n{self.group}\n{'~'*max(3, len(self.group))}\n"

    def _dimrst(self):
        """ Print attribute string block in rst format
        """
        return f" :dimension: \"{self.name}\" ;\n"

    def _attrrst(self):
        """ Print attribute string block in rst format
        """
        block = f" :{self.esc(self.name)}: "
        for attr, astr in self.attrs.items():
            block += f"\"{self.esc(astr)}\" ;\n "
        return block

    def _varrst(self):
        """ Print variable string block in rst format
        """
        try:
            block = f" | *{self.dtype}* **{self.esc(self.name)}** ({', '.join(self.dims)})\n"
        except TypeError as err:
            # dims are None
            block = f" | *{self.dtype}* **{self.esc(self.name)}**\n"
        for attr, astr in self.attrs.items():
            block += f" |  **{self.esc(self.name)}**:{self.esc(attr)} = \"{self.esc(astr)}\" ;\n"
        return block

    @staticmethod
    def esc(s):
        """ Include \ in strings to escape rst special characters
        """
        specials = '*_:'
        return re.sub(r'([\*\_\:])', r'\\\1', s)

    @staticmethod
    def root_path(path):
        return os.path.join('/', path)

    def set_ncgrp(self, param):
        self.path = self.root_path(param.name)
        self.group = self.path

    def set_ncattr(self, param):
        self.path = self.root_path(param.name)
        self.group, self.name = os.path.split(self.path)
        self.attrs = {k: v for k,v in param.items()}

    def set_ncdim(self, param):
        self.path = self.root_path(param.name)
        self.group, self.name = os.path.split(self.path)

    def set_ncvar(self, param):
        # May be variable or coordinate (name is same as dimension)
        self.path = self.root_path(param.name)
        self.group, self.name = os.path.split(self.path)
        try:
            self.dtype = param.pop('dtype')
        except KeyError as err:
            raise KeyError(f"'dtype' is required for a {param.name} declaration")
        self.dims = param.getlist('dimensions')
        _ = param.pop('dimensions', None)
        self.attrs = {k: v for k,v in param.items()}

    @property
    def rst(self):
        if self.nctype == 'grp':
            return self._grprst()
        elif self.nctype == 'attr':
            return self._attrrst()
        elif self.nctype == 'dim':
            return self._dimrst()
        elif self.nctype == 'coord':
            return self._varrst()
        elif self.nctype == 'var':
            return self._varrst()
