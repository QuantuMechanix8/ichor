from pathlib import Path
from typing import List

from ichor.core.atoms import Atoms, Atom
from ichor.core.common.units import AtomicDistance
from ichor.core.files import WFN
from ichor.core.files.gaussian.wfn import MolecularOrbital
from ichor.core.common.types.itypes import T
from tests.test_atoms import _test_atoms_coords
from tests.path import get_cwd
from tests.test_files import _assert_val_optional

import pytest
import numpy as np

example_dir = get_cwd(__file__) / "example_gjfs"


def _test_molecular_orbitals(
        wfn_file_molecular_orbitals: List[MolecularOrbital],
        reference_molecular_orbitals: List[MolecularOrbital]
    ):
        for mo, ref_mo in zip(wfn_file_molecular_orbitals, reference_molecular_orbitals):
            assert mo.index == ref_mo.index
            assert mo.eigen_value == pytest.approx(ref_mo.eigen_value)
            assert mo.occupation_number == pytest.approx(ref_mo.occupation_number)
            assert mo.energy == pytest.approx(ref_mo.energy)
            assert mo.primitives ==  ref_mo.primitives


def _test_read_wfn(
    wfn_file: Path,
    method: str = None,
    atoms: Atoms = None,
    title: str = None,
    program: str = None,
    n_orbitals: int = None,
    n_primitives: int = None,
    n_nuclei: int = None,
    centre_assignments: List[int] = None,
    type_assignments: List[int] = None,
    primitive_exponents: np.ndarray = None,
    molecular_orbitals: List[MolecularOrbital] = None,
    total_energy: float = None,
    virial_ratio: float = None,
):
    
    wfn_file = WFN(wfn_file)
    
    _assert_val_optional(wfn_file.method, method)
    _test_atoms_coords(wfn_file.atoms, atoms, AtomicDistance.Bohr)
    _assert_val_optional(wfn_file.title, title)
    _assert_val_optional(wfn_file.program, program)
    _assert_val_optional(wfn_file.n_orbitals, n_orbitals)
    _assert_val_optional(wfn_file.n_primitives, n_primitives)
    _assert_val_optional(wfn_file.n_nuclei, n_nuclei)
    _assert_val_optional(wfn_file.centre_assignments, centre_assignments)
    _assert_val_optional(wfn_file.type_assignments, type_assignments)
    _assert_val_optional(wfn_file.primitive_exponents, primitive_exponents)
    _test_molecular_orbitals(wfn_file.molecular_orbitals, molecular_orbitals)
    _assert_val_optional(wfn_file.total_energy, total_energy)
    _assert_val_optional(wfn_file.virial_ratio, virial_ratio)
    
def test_water_monomer_wfn():
    
    wfn_file_path = get_cwd(__file__) / "example_points_directory" / "water_monomer_points_dir" / "WATER_MONOMER0001" / "WATER_MONOMER0001.wfn"
    
    expected_atoms =   Atoms([Atom("O", -0.06328188, -0.88230871, -0.00802954, units = AtomicDistance.Bohr),
                             Atom("H", -0.95295537,  0.38291891,  1.07137738, units = AtomicDistance.Bohr),
                             Atom("H", 1.01623725,  0.49938980, -1.06334784, units = AtomicDistance.Bohr)])
    
    expected_molecular_orbitals = [
        
        MolecularOrbital(1, 0.0, 2.0, -19.154182, [0.49669426, 0.92575644, 1.5697501, 2.3756499, 2.963436, 2.543069, 0.97386032, 3.5843855e-05, 0.00038458104, 0.0014176381, 0.0041450907, 0.0049950359, -0.0060170501, 0.055564088, -4.03979e-05, -0.00012364374, 0.00053080754, 0.00051470476, 0.00034721679, 0.0074891282, 0.0072619352, 
0.0048988586, 7.5052246e-05, 7.2775432e-05, 4.9093877e-05, -0.00072771178, -0.00076146816, 0.00072621562, -0.00030466521, -0.00037314629, 0.00029929949, -1.0974244e-05, -5.2155588e-06, 1.149832e-05, -0.0004049188, 0.0004919329, -8.7014098e-05, -0.00031387801, -0.0031862954, 0.0007512178, 4.6711379e-05, -7.5787556e-05, 2.9076177e-05, -0.00066251538, 0.00083657467, 0.00062864363, 1.2829503e-05, -2.0106943e-05, 7.2774406e-06, -7.4705395e-05, 0.00013270782, 6.4474751e-05, 0.00026561335, -0.00010236276, -0.00024245916, -0.00058934746, 9.3219056e-06, 2.9797914e-05, -0.0002074926, 0.00029776638, 0.00069757957, -0.001223812, 3.8822578e-06, 8.3669458e-05, -1.4025414e-05, -3.6218188e-05, -9.1828363e-05, 3.3924706e-05, 2.4571415e-05, -0.00015918001, 8.1515372e-06, 0.00085355854, 0.00017231581, 0.00031077865, 0.00045824294, -0.00011492119, -0.00028645356, -6.2492059e-06, 2.6454351e-05, -0.00012503814, -3.9724128e-05, -0.00022800946, 0.00020695578, 0.00026640426, -4.6291049e-05, 4.2369526e-05, 5.4116838e-05, 0.00018803338, -0.00015599909, -3.2034295e-05, 0.001340348, 0.0011287606, -0.0016009731, -5.4060485e-06, 1.6384663e-05, -1.0978615e-05, 1.9015956e-05, 4.5805872e-05, -2.0446424e-05, 8.0188639e-05, 0.00014462351, 0.00021324729, 0.0013831988, 0.0003270961, 1.4980556e-05, -0.0005125854, -0.00077665514, 0.00049057516, -0.00045437844, -0.00060409094, 0.00044223154, -3.5639775e-05, -3.067183e-05, 3.6144561e-05, -3.7252232e-05, 6.8969239e-05, -3.1717007e-05, 0.00010388175, -0.00015483464, -8.1498041e-05, -6.8556676e-06, 1.4122111e-05, -7.266443e-06, 4.1521315e-05, -3.4261392e-05, -3.853334e-05]),
        MolecularOrbital(2, 0.0, 2.0, -0.996981, [-0.10560755, -0.19683511, -0.33376158, -0.50511266, -0.63008823, -0.54070945, -0.20706299, -0.001640198, -0.017598248, -0.064870455, -0.18967741, -0.2285705, 0.27533738, 0.15615859, 0.073647452, 0.0034072834, -0.01834959, -0.01779293, -0.012003006, 0.29148507, 0.28264247, 0.19066894, 0.045412179, 0.044034538, 0.029705439, -0.002046197, 0.070451497, 0.0083738396, 0.00040357462, 0.0054919929, 3.9027127e-05, -1.2703256e-06, 0.00012652028, 1.2375888e-05, -0.0081544755, 0.012481801, -0.0043273251, -0.0031385919, -0.038132938, 0.010051027, -0.0026132879, 0.0043806164, -0.0017673285, 0.0017041335, -0.010572908, 0.00022258483, -6.3656373e-05, 0.00015580875, -9.215238e-05, 0.00025668679, 8.703928e-05, -0.00024670341, -3.6141016e-05, -0.0010958287, 0.00017080213, 0.00096108015, 0.00068245871, -0.00092957396, -0.0008526571, 0.0026050275, 0.00041716759, -0.023092346, -0.0001457759, 0.00021805406, 0.00011818876, 0.00047792749, -0.00032352298, -4.2821168e-05, -4.0599786e-05, -0.00033063921, -0.0003117451, -0.0010656986, 0.023750114, 0.042834309, 0.063159164, 0.023884032, -0.0011687185, -7.9089539e-05, 0.014318736, -0.017879314, -0.01715598, 0.0025575411, -0.0031489416, -0.0030597217, -0.0001710597, 0.00023430421, 0.00020688467, -0.00084469629, 0.00073048617, 0.00011421012, -0.0056133942, -0.0051385534, 0.0067612022, 8.5325022e-06, -2.0263723e-05, 1.1731221e-05, 1.2567027e-05, -5.4067756e-05, -1.3947825e-05, 0.018766469, 0.033846099, 0.049906053, 0.018098847, -0.00078260356, -4.322687e-05, -0.011984024, -0.01315612, 0.011905548, -0.0021873161, -0.0024949538, 0.002165596, 0.00011453074, 0.00014990723, -0.0001115987, -0.00019405214, 0.0003973352, -0.00020328306, 0.0034280977, -0.0031996384, -0.0033506365, -2.8512305e-05, 5.5955541e-05, -2.7443236e-05, 0.00016213018, -0.00016106568, -0.00014760206]),
        MolecularOrbital(3, 0.0, 2.0, -0.494315, [0.0049777445, 0.0092776973, 0.01573164, 0.023808164, 0.029698807, 0.025485995, 0.0097597822, 9.0278366e-05, 0.00096862762, 0.0035705438, 0.010440061, 0.012580781, -0.015154884, -0.007432128, -0.013487826, -0.0013599314, -0.98681099, -0.95687471, -0.64550203, 0.1027757, 0.099657857, 0.067228602, 1.0838147, 1.0509357, 0.70895502, -0.21472322, 0.017487143, 0.23540532, -0.026752436, 0.00025823135, 0.029161969, -0.00044967704, 9.0099281e-06, 0.00049061414, -0.0045187299, 0.00082546727, 0.0036932626, -0.087402212, -0.0061353495, 0.096012348, -0.00075816477, 0.00014904744, 0.00060911732, -0.017359926, 0.0017287175, 0.018807598, 5.8677436e-05, -0.00010309986, 4.4422423e-05, -0.00037445431, 0.00051180986, 0.00033627623, 0.0052766077, 0.00041925137, -0.0043452796, -0.0028248729, -0.0018784994, 0.0099169406, -0.01300495, 0.00062074533, 0.0031188982, 0.0022529255, 0.00053520519, 0.00016262331, -0.00050487352, -0.00093536991, -0.00036389508, 0.00051414341, -0.00067024565, -0.00012397484, 0.0010004771, 0.0012117218, 0.036111652, 0.065128851, 0.096032453, 0.065657156, 0.008191008, -0.00017886164, 0.0077385905, -0.025809185, 
-0.010679957, 0.0033187913, -0.011063693, -0.004579657, -0.00026968425, -0.00026102765, 0.0002708626, -0.0034881743, 0.0054518001, -0.0019636258, -0.010233695, -0.0063319213, 0.013142272, -0.00016347722, 0.00030032566, -0.00013684843, -0.00041932318, 0.00015032844, 0.00052305275, -0.032870422, -0.059283159, -0.087412984, -0.054932325, -0.0075825906, 0.00021126276, 0.0068225402, 0.020609735, -0.0056336192, 0.0023892465, 
0.0089005918, -0.0018277968, -0.00017098057, 0.00034660061, 0.00021645383, 0.0021322149, -0.0046432152, 0.0025110003, -0.008252086, 0.0032361612, 0.0074894949, 0.00013279753, -0.00031413729, 0.00018133976, -0.00074591166, 0.00014577358, 0.00071735346]),
        MolecularOrbital(4, 0.0, 2.0, -0.413209, [0.037978667, 0.070785991, 0.1200276, 0.181649, 0.22659281, 0.19445034, 0.074464152, 0.00063391986, 0.0068015441, 0.025071772, 0.073308391, 0.088340176, -0.1064151, -0.063247858, -0.073634294, -0.011454607, 0.11537788, 0.11187773, 0.075472056, 1.5256706, 1.4793873, 0.99798594, 0.0074353994, 0.0072098363, 0.004863713, 0.027752383, 0.33247628, -0.0012214373, 0.0046837308, 0.045554597, -0.001128402, 8.6120462e-05, 0.00096901264, -9.5393121e-06, -0.020887921, 0.039617078, -0.018729156, 0.0075846139, -0.026505313, 0.0044730474, -0.0057204894, 0.011737944, -0.0060174542, 0.0032747996, 0.0016194092, -0.00062892936, -0.00011040063, 0.00032686804, -0.00021646741, 0.00040757628, 0.00082994676, -0.0004321772, -0.00090507084, 0.0032535025, 0.00037804171, 0.0024213243, -0.0057713098, -0.0024088941, 0.00029388819, -0.0039891976, 0.001274769, -0.024805085, -0.00016668145, 0.00069186245, 8.2680151e-05, 0.00055621766, -0.00098358696, 7.4149341e-06, -5.6173314e-05, -0.0010920004, -0.00025545539, 0.00015044422, 0.022008124, 0.039692559, 0.058526654, 0.048578695, 0.009784151, 0.00017014943, 0.012924857, 0.0030401609, -0.013812818, 0.0079305736, -0.00057537587, -0.0086869602, 0.00036465419, 0.00034333001, -0.00036641848, 0.00073562467, -0.0026741512, 0.0019385265, -0.004816781, -0.0090859131, 0.0053452576, 6.6338414e-05, -0.00018405616, 0.00011771774, -0.00011112896, -0.00049931694, 0.00011750396, 0.025545768, 0.046072845, 0.067934383, 0.05173125, 0.011858316, 0.00015664081, -0.0105704, 0.0010252089, 0.011602894, -0.0074233863, -0.0015257443, 0.0079547553, -0.00046809192, 0.00011720964, 0.00052082973, 0.00084258516, -0.0019922298, 0.0011496446, 0.003909221, -0.0075123494, -0.0041242671, 1.2341427e-05, -4.683084e-05, 3.4489413e-05, 0.00051248735, -0.00074520265, -0.00050444019]),
        MolecularOrbital(5, 0.0, 2.0, -0.323897, [-4.9573078e-07, -9.2396067e-07, -1.5667052e-06, -2.3710417e-06, -2.9576876e-06, -2.538136e-06, -9.7197124e-07, -4.7592968e-09, -5.1064132e-08, -1.88232e-07, -5.5037934e-07, -6.6323387e-07, 7.9893548e-07, 4.9013225e-07, 4.8900032e-06, -2.7749943e-07, 1.3187806, 1.2787736, 0.8626531, -0.10563696, -0.10243231, -0.069100234, 1.2107629, 1.1740327, 0.79199552, 0.29695076, -0.023785257, 0.27262907, 0.051912095, -0.0041559418, 0.047662079, 0.0020162263, -0.00016160841, 0.0018512568, -0.00092031565, -0.0037260186, 0.0046463343, 0.04659864, 0.004216792, 0.042307861, 
0.00040538728, -0.0011505339, 0.0007451466, 0.014333452, 0.0011830597, 0.013125284, 0.00013127732, -5.4610338e-05, -7.6666985e-05, 0.0006795092, 3.7287788e-05, 0.00064117531, 0.0019247304, -0.00074760585, 0.0034533362, 0.0092884686, 0.00036937401, -0.018736235, -0.01506266, 0.0018734435, 0.0083762266, 0.004490453, 9.2383053e-05, -5.9320761e-05, 0.00014655616, 0.00069929444, 0.0005369158, -0.0011525137, -0.0009764436, -0.00035895352, 0.0007128452, 0.000221971, -2.3915669e-07, -4.3132894e-07, -6.3599426e-07, -6.2829501e-06, 1.8964402e-06, 8.3724006e-10, 0.017103516, -0.0013692626, 0.015704172, 0.0085650858, -0.00068552466, 0.0078655465, 0.0010649959, -8.4852521e-05, 0.00097657123, 0.0049884686, 0.00054563671, -0.0055341053, -0.0072134755, -0.0014467624, -0.0057730897, 0.00047275682, 4.5155307e-05, -0.00051791213, -0.00060422903, -0.00013069904, -0.00047528094, -4.2086509e-07, -7.5904752e-07, -1.1192151e-06, -2.5100693e-06, -1.0334872e-06, 5.7045764e-09, 0.014183236, -0.0011354608, 0.013021715, 0.0072332084, -0.00057945081, 0.0066381132, 0.00088918263, -7.1094634e-05, 0.00081570384, -0.0049621795, 0.00047940724, 0.0044827722, -0.0055894235, 0.00032838963, -0.0058879042, -0.00038392027, 3.0630065e-05, 0.00035329021, -0.00035137257, 3.2662389e-05, -0.00038117806]) 
    ]
    
    _test_read_wfn(wfn_file_path,
                   method = "B3LYP",
                   atoms = expected_atoms,
                   title="WATER_MONOMER0001",
                   program="GAUSSIAN",
                   n_orbitals=5,
                   n_primitives=126,
                   n_nuclei=3,
                   centre_assignments=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
                   type_assignments=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,3,3,3,4,4,4,2,3,4,2,3,4,2,3,4,5,6,7,8,9,10,5,6,7,8,9,10,5,6,7,8,9,10,11,12,13,17,14,15,18,19,16,20,11,12,13,17,14,15,18,19,16,20,1,1,1,1,1,1,2,3,4,2,3,4,2,3,4,5,6,7,8,9,10,5,6,7,8,9,10,1,1,1,1,1,1,2,3,4,2,3,4,2,3,4,5,6,7,8,9,10,5,6,7,8,9,10],
                   primitive_exponents=[15330.0, 2299.0, 522.4, 147.3, 47.55, 16.76, 6.207, 522.4, 147.3, 47.55, 16.76, 6.207, 0.6882, 1.752, 0.2384, 0.07376, 34.46, 7.749, 2.28, 34.46, 7.749, 2.28, 34.46, 7.749, 2.28, 0.7156, 0.7156, 0.7156, 0.214, 0.214, 0.214, 0.05974, 0.05974, 0.05974, 2.314, 2.314, 2.314, 2.314, 2.314, 2.314, 0.645, 0.645, 0.645, 0.645, 0.645, 0.645, 0.214, 0.214, 0.214, 0.214, 0.214, 0.214, 1.428, 1.428, 1.428, 1.428, 1.428, 1.428, 1.428, 1.428, 1.428, 1.428, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 33.87, 5.095, 1.159, 0.3258, 0.1027, 0.02526, 1.407, 1.407, 1.407, 0.388, 0.388, 0.388, 0.102, 0.102, 0.102, 1.057, 1.057, 1.057, 1.057, 1.057, 1.057, 0.247, 0.247, 0.247, 0.247, 0.247, 0.247, 33.87, 5.095, 
1.159, 0.3258, 0.1027, 0.02526, 1.407, 1.407, 1.407, 0.388, 0.388, 0.388, 0.102, 0.102, 0.102, 1.057, 1.057, 1.057, 1.057, 1.057, 1.057, 0.247, 0.247, 0.247, 0.247, 0.247, 0.247],
                   molecular_orbitals=expected_molecular_orbitals,
                   total_energy=-76.460540818734,
                   virial_ratio=2.00902678
    )
    
def test_water_monomer_wfn_no_method():
    
    wfn_file_path = get_cwd(__file__) / "example_wfns" / "WATER_MONOMER0001.wfn"
    
    expected_atoms =   Atoms([Atom("O", -0.06328188, -0.88230871, -0.00802954, units = AtomicDistance.Bohr),
                             Atom("H", -0.95295537,  0.38291891,  1.07137738, units = AtomicDistance.Bohr),
                             Atom("H", 1.01623725,  0.49938980, -1.06334784, units = AtomicDistance.Bohr)])
    
    expected_molecular_orbitals = [
        
        MolecularOrbital(1, 0.0, 2.0, -19.154182, [0.49669426, 0.92575644, 1.5697501, 2.3756499, 2.963436, 2.543069, 0.97386032, 3.5843855e-05, 0.00038458104, 0.0014176381, 0.0041450907, 0.0049950359, -0.0060170501, 0.055564088, -4.03979e-05, -0.00012364374, 0.00053080754, 0.00051470476, 0.00034721679, 0.0074891282, 0.0072619352, 
0.0048988586, 7.5052246e-05, 7.2775432e-05, 4.9093877e-05, -0.00072771178, -0.00076146816, 0.00072621562, -0.00030466521, -0.00037314629, 0.00029929949, -1.0974244e-05, -5.2155588e-06, 1.149832e-05, -0.0004049188, 0.0004919329, -8.7014098e-05, -0.00031387801, -0.0031862954, 0.0007512178, 4.6711379e-05, -7.5787556e-05, 2.9076177e-05, -0.00066251538, 0.00083657467, 0.00062864363, 1.2829503e-05, -2.0106943e-05, 7.2774406e-06, -7.4705395e-05, 0.00013270782, 6.4474751e-05, 0.00026561335, -0.00010236276, -0.00024245916, -0.00058934746, 9.3219056e-06, 2.9797914e-05, -0.0002074926, 0.00029776638, 0.00069757957, -0.001223812, 3.8822578e-06, 8.3669458e-05, -1.4025414e-05, -3.6218188e-05, -9.1828363e-05, 3.3924706e-05, 2.4571415e-05, -0.00015918001, 8.1515372e-06, 0.00085355854, 0.00017231581, 0.00031077865, 0.00045824294, -0.00011492119, -0.00028645356, -6.2492059e-06, 2.6454351e-05, -0.00012503814, -3.9724128e-05, -0.00022800946, 0.00020695578, 0.00026640426, -4.6291049e-05, 4.2369526e-05, 5.4116838e-05, 0.00018803338, -0.00015599909, -3.2034295e-05, 0.001340348, 0.0011287606, -0.0016009731, -5.4060485e-06, 1.6384663e-05, -1.0978615e-05, 1.9015956e-05, 4.5805872e-05, -2.0446424e-05, 8.0188639e-05, 0.00014462351, 0.00021324729, 0.0013831988, 0.0003270961, 1.4980556e-05, -0.0005125854, -0.00077665514, 0.00049057516, -0.00045437844, -0.00060409094, 0.00044223154, -3.5639775e-05, -3.067183e-05, 3.6144561e-05, -3.7252232e-05, 6.8969239e-05, -3.1717007e-05, 0.00010388175, -0.00015483464, -8.1498041e-05, -6.8556676e-06, 1.4122111e-05, -7.266443e-06, 4.1521315e-05, -3.4261392e-05, -3.853334e-05]),
        MolecularOrbital(2, 0.0, 2.0, -0.996981, [-0.10560755, -0.19683511, -0.33376158, -0.50511266, -0.63008823, -0.54070945, -0.20706299, -0.001640198, -0.017598248, -0.064870455, -0.18967741, -0.2285705, 0.27533738, 0.15615859, 0.073647452, 0.0034072834, -0.01834959, -0.01779293, -0.012003006, 0.29148507, 0.28264247, 0.19066894, 0.045412179, 0.044034538, 0.029705439, -0.002046197, 0.070451497, 0.0083738396, 0.00040357462, 0.0054919929, 3.9027127e-05, -1.2703256e-06, 0.00012652028, 1.2375888e-05, -0.0081544755, 0.012481801, -0.0043273251, -0.0031385919, -0.038132938, 0.010051027, -0.0026132879, 0.0043806164, -0.0017673285, 0.0017041335, -0.010572908, 0.00022258483, -6.3656373e-05, 0.00015580875, -9.215238e-05, 0.00025668679, 8.703928e-05, -0.00024670341, -3.6141016e-05, -0.0010958287, 0.00017080213, 0.00096108015, 0.00068245871, -0.00092957396, -0.0008526571, 0.0026050275, 0.00041716759, -0.023092346, -0.0001457759, 0.00021805406, 0.00011818876, 0.00047792749, -0.00032352298, -4.2821168e-05, -4.0599786e-05, -0.00033063921, -0.0003117451, -0.0010656986, 0.023750114, 0.042834309, 0.063159164, 0.023884032, -0.0011687185, -7.9089539e-05, 0.014318736, -0.017879314, -0.01715598, 0.0025575411, -0.0031489416, -0.0030597217, -0.0001710597, 0.00023430421, 0.00020688467, -0.00084469629, 0.00073048617, 0.00011421012, -0.0056133942, -0.0051385534, 0.0067612022, 8.5325022e-06, -2.0263723e-05, 1.1731221e-05, 1.2567027e-05, -5.4067756e-05, -1.3947825e-05, 0.018766469, 0.033846099, 0.049906053, 0.018098847, -0.00078260356, -4.322687e-05, -0.011984024, -0.01315612, 0.011905548, -0.0021873161, -0.0024949538, 0.002165596, 0.00011453074, 0.00014990723, -0.0001115987, -0.00019405214, 0.0003973352, -0.00020328306, 0.0034280977, -0.0031996384, -0.0033506365, -2.8512305e-05, 5.5955541e-05, -2.7443236e-05, 0.00016213018, -0.00016106568, -0.00014760206]),
        MolecularOrbital(3, 0.0, 2.0, -0.494315, [0.0049777445, 0.0092776973, 0.01573164, 0.023808164, 0.029698807, 0.025485995, 0.0097597822, 9.0278366e-05, 0.00096862762, 0.0035705438, 0.010440061, 0.012580781, -0.015154884, -0.007432128, -0.013487826, -0.0013599314, -0.98681099, -0.95687471, -0.64550203, 0.1027757, 0.099657857, 0.067228602, 1.0838147, 1.0509357, 0.70895502, -0.21472322, 0.017487143, 0.23540532, -0.026752436, 0.00025823135, 0.029161969, -0.00044967704, 9.0099281e-06, 0.00049061414, -0.0045187299, 0.00082546727, 0.0036932626, -0.087402212, -0.0061353495, 0.096012348, -0.00075816477, 0.00014904744, 0.00060911732, -0.017359926, 0.0017287175, 0.018807598, 5.8677436e-05, -0.00010309986, 4.4422423e-05, -0.00037445431, 0.00051180986, 0.00033627623, 0.0052766077, 0.00041925137, -0.0043452796, -0.0028248729, -0.0018784994, 0.0099169406, -0.01300495, 0.00062074533, 0.0031188982, 0.0022529255, 0.00053520519, 0.00016262331, -0.00050487352, -0.00093536991, -0.00036389508, 0.00051414341, -0.00067024565, -0.00012397484, 0.0010004771, 0.0012117218, 0.036111652, 0.065128851, 0.096032453, 0.065657156, 0.008191008, -0.00017886164, 0.0077385905, -0.025809185, 
-0.010679957, 0.0033187913, -0.011063693, -0.004579657, -0.00026968425, -0.00026102765, 0.0002708626, -0.0034881743, 0.0054518001, -0.0019636258, -0.010233695, -0.0063319213, 0.013142272, -0.00016347722, 0.00030032566, -0.00013684843, -0.00041932318, 0.00015032844, 0.00052305275, -0.032870422, -0.059283159, -0.087412984, -0.054932325, -0.0075825906, 0.00021126276, 0.0068225402, 0.020609735, -0.0056336192, 0.0023892465, 
0.0089005918, -0.0018277968, -0.00017098057, 0.00034660061, 0.00021645383, 0.0021322149, -0.0046432152, 0.0025110003, -0.008252086, 0.0032361612, 0.0074894949, 0.00013279753, -0.00031413729, 0.00018133976, -0.00074591166, 0.00014577358, 0.00071735346]),
        MolecularOrbital(4, 0.0, 2.0, -0.413209, [0.037978667, 0.070785991, 0.1200276, 0.181649, 0.22659281, 0.19445034, 0.074464152, 0.00063391986, 0.0068015441, 0.025071772, 0.073308391, 0.088340176, -0.1064151, -0.063247858, -0.073634294, -0.011454607, 0.11537788, 0.11187773, 0.075472056, 1.5256706, 1.4793873, 0.99798594, 0.0074353994, 0.0072098363, 0.004863713, 0.027752383, 0.33247628, -0.0012214373, 0.0046837308, 0.045554597, -0.001128402, 8.6120462e-05, 0.00096901264, -9.5393121e-06, -0.020887921, 0.039617078, -0.018729156, 0.0075846139, -0.026505313, 0.0044730474, -0.0057204894, 0.011737944, -0.0060174542, 0.0032747996, 0.0016194092, -0.00062892936, -0.00011040063, 0.00032686804, -0.00021646741, 0.00040757628, 0.00082994676, -0.0004321772, -0.00090507084, 0.0032535025, 0.00037804171, 0.0024213243, -0.0057713098, -0.0024088941, 0.00029388819, -0.0039891976, 0.001274769, -0.024805085, -0.00016668145, 0.00069186245, 8.2680151e-05, 0.00055621766, -0.00098358696, 7.4149341e-06, -5.6173314e-05, -0.0010920004, -0.00025545539, 0.00015044422, 0.022008124, 0.039692559, 0.058526654, 0.048578695, 0.009784151, 0.00017014943, 0.012924857, 0.0030401609, -0.013812818, 0.0079305736, -0.00057537587, -0.0086869602, 0.00036465419, 0.00034333001, -0.00036641848, 0.00073562467, -0.0026741512, 0.0019385265, -0.004816781, -0.0090859131, 0.0053452576, 6.6338414e-05, -0.00018405616, 0.00011771774, -0.00011112896, -0.00049931694, 0.00011750396, 0.025545768, 0.046072845, 0.067934383, 0.05173125, 0.011858316, 0.00015664081, -0.0105704, 0.0010252089, 0.011602894, -0.0074233863, -0.0015257443, 0.0079547553, -0.00046809192, 0.00011720964, 0.00052082973, 0.00084258516, -0.0019922298, 0.0011496446, 0.003909221, -0.0075123494, -0.0041242671, 1.2341427e-05, -4.683084e-05, 3.4489413e-05, 0.00051248735, -0.00074520265, -0.00050444019]),
        MolecularOrbital(5, 0.0, 2.0, -0.323897, [-4.9573078e-07, -9.2396067e-07, -1.5667052e-06, -2.3710417e-06, -2.9576876e-06, -2.538136e-06, -9.7197124e-07, -4.7592968e-09, -5.1064132e-08, -1.88232e-07, -5.5037934e-07, -6.6323387e-07, 7.9893548e-07, 4.9013225e-07, 4.8900032e-06, -2.7749943e-07, 1.3187806, 1.2787736, 0.8626531, -0.10563696, -0.10243231, -0.069100234, 1.2107629, 1.1740327, 0.79199552, 0.29695076, -0.023785257, 0.27262907, 0.051912095, -0.0041559418, 0.047662079, 0.0020162263, -0.00016160841, 0.0018512568, -0.00092031565, -0.0037260186, 0.0046463343, 0.04659864, 0.004216792, 0.042307861, 
0.00040538728, -0.0011505339, 0.0007451466, 0.014333452, 0.0011830597, 0.013125284, 0.00013127732, -5.4610338e-05, -7.6666985e-05, 0.0006795092, 3.7287788e-05, 0.00064117531, 0.0019247304, -0.00074760585, 0.0034533362, 0.0092884686, 0.00036937401, -0.018736235, -0.01506266, 0.0018734435, 0.0083762266, 0.004490453, 9.2383053e-05, -5.9320761e-05, 0.00014655616, 0.00069929444, 0.0005369158, -0.0011525137, -0.0009764436, -0.00035895352, 0.0007128452, 0.000221971, -2.3915669e-07, -4.3132894e-07, -6.3599426e-07, -6.2829501e-06, 1.8964402e-06, 8.3724006e-10, 0.017103516, -0.0013692626, 0.015704172, 0.0085650858, -0.00068552466, 0.0078655465, 0.0010649959, -8.4852521e-05, 0.00097657123, 0.0049884686, 0.00054563671, -0.0055341053, -0.0072134755, -0.0014467624, -0.0057730897, 0.00047275682, 4.5155307e-05, -0.00051791213, -0.00060422903, -0.00013069904, -0.00047528094, -4.2086509e-07, -7.5904752e-07, -1.1192151e-06, -2.5100693e-06, -1.0334872e-06, 5.7045764e-09, 0.014183236, -0.0011354608, 0.013021715, 0.0072332084, -0.00057945081, 0.0066381132, 0.00088918263, -7.1094634e-05, 0.00081570384, -0.0049621795, 0.00047940724, 0.0044827722, -0.0055894235, 0.00032838963, -0.0058879042, -0.00038392027, 3.0630065e-05, 0.00035329021, -0.00035137257, 3.2662389e-05, -0.00038117806]) 
    ]
    
    _test_read_wfn(wfn_file_path,
                   method = None,
                   atoms = expected_atoms,
                   title="WATER_MONOMER0001",
                   program="GAUSSIAN",
                   n_orbitals=5,
                   n_primitives=126,
                   n_nuclei=3,
                   centre_assignments=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
                   type_assignments=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,3,3,3,4,4,4,2,3,4,2,3,4,2,3,4,5,6,7,8,9,10,5,6,7,8,9,10,5,6,7,8,9,10,11,12,13,17,14,15,18,19,16,20,11,12,13,17,14,15,18,19,16,20,1,1,1,1,1,1,2,3,4,2,3,4,2,3,4,5,6,7,8,9,10,5,6,7,8,9,10,1,1,1,1,1,1,2,3,4,2,3,4,2,3,4,5,6,7,8,9,10,5,6,7,8,9,10],
                   primitive_exponents=[15330.0, 2299.0, 522.4, 147.3, 47.55, 16.76, 6.207, 522.4, 147.3, 47.55, 16.76, 6.207, 0.6882, 1.752, 0.2384, 0.07376, 34.46, 7.749, 2.28, 34.46, 7.749, 2.28, 34.46, 7.749, 2.28, 0.7156, 0.7156, 0.7156, 0.214, 0.214, 0.214, 0.05974, 0.05974, 0.05974, 2.314, 2.314, 2.314, 2.314, 2.314, 2.314, 0.645, 0.645, 0.645, 0.645, 0.645, 0.645, 0.214, 0.214, 0.214, 0.214, 0.214, 0.214, 1.428, 1.428, 1.428, 1.428, 1.428, 1.428, 1.428, 1.428, 1.428, 1.428, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 33.87, 5.095, 1.159, 0.3258, 0.1027, 0.02526, 1.407, 1.407, 1.407, 0.388, 0.388, 0.388, 0.102, 0.102, 0.102, 1.057, 1.057, 1.057, 1.057, 1.057, 1.057, 0.247, 0.247, 0.247, 0.247, 0.247, 0.247, 33.87, 5.095, 
1.159, 0.3258, 0.1027, 0.02526, 1.407, 1.407, 1.407, 0.388, 0.388, 0.388, 0.102, 0.102, 0.102, 1.057, 1.057, 1.057, 1.057, 1.057, 1.057, 0.247, 0.247, 0.247, 0.247, 0.247, 0.247],
                   molecular_orbitals=expected_molecular_orbitals,
                   total_energy=-76.460540818734,
                   virial_ratio=2.00902678
    )