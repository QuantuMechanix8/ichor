from ichor.modules.modules import Modules
from ichor.globals import Machine


FerebusModules = Modules()

FerebusModules[Machine.csf3] = [
    "compilers/intel/18.0.3"
]

FerebusModules[Machine.ffluxlab] = [
    "compilers/intel/20.0.1"
]