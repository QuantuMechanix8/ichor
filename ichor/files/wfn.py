import re

from ichor.common.functools import buildermethod, classproperty
from ichor.files.file import File
from ichor.geometry import Geometry, GeometryData
from ichor.globals import GLOBALS


class WFN(Geometry, GeometryData, File):
    def __init__(self, path):
        File.__init__(self, path)
        Geometry.__init__(self)
        GeometryData.__init__(self)

        self.header: str = ""

        self.mol_orbitals: int = 0
        self.primitives: int = 0
        self.nuclei: int = 0
        self.method: str = "HF"

    @buildermethod
    def _read_file(self, only_header=False):
        with open(self.path, "r") as f:
            next(f)
            self.header = next(f)
            self.read_header()
            if only_header:
                return
            for line in f:
                if "CHARGE" in line:
                    self.atoms.add(line)
                if "CENTRE ASSIGNMENTS" in line:
                    self.atoms.finish()
                    self.atoms.to_angstroms()
                if "TOTAL ENERGY" in line:
                    self.data.energy = float(line.split()[3])
                    self.data.virial = float(line.split()[-1])

    @classproperty
    def filetype(cls) -> str:
        return ".wfn"

    def read_header(self):
        data = re.findall(r"\s\d+\s", self.header)

        self.mol_orbitals = int(data[0])
        self.primitives = int(data[1])
        self.nuclei = int(data[2])

        split_header = self.header.split()
        if split_header[-1] != "NUCLEI":
            self.method = split_header[-1]
        else:
            self.method = GLOBALS.METHOD

    @property
    def title(self):
        return self.path.stem

    def check_functional(self):
        data = []
        with open(self.path, "r") as f:
            for i, line in enumerate(f):
                if i == 1:
                    if GLOBALS.METHOD.upper() not in line.upper():
                        f.seek(0)
                        data = f.readlines()
                    break

        if data:
            data[1] = data[1].strip() + "   " + str(GLOBALS.METHOD) + "\n"
            with open(self.path, "w") as f:
                f.writelines(data)