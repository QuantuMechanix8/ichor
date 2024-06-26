from pathlib import Path

from ichor.core.files import IntDirectory

from tests.path import get_cwd
from tests.test_files import _assert_val_optional

example_dir = (
    get_cwd(__file__)
    / ".."
    / ".."
    / ".."
    / "example_files"
    / "example_points_directory"
    / "WATER_MONOMER.pointsdir"
    / "WATER_MONOMER0000.pointdir"
    / "WATER_MONOMER0000_atomicfiles"
)


def _test_ints(
    int_dir_path: Path,
):

    """Test function for INTs directory. Non eed to have tests for individual
    Int files because these are already tested separately."""

    int_dir_instance = IntDirectory(int_dir_path)

    expected_raw_data = {
        "O1": {
            "iqa": -75.446714709,
            "integration_error": -2.8725236559e-05,
            "q00": -1.051921199,
            "q10": -0.020042356378,
            "q11c": 0.0018273275449,
            "q11s": -0.20706556929,
            "q20": -0.037266216811,
            "q21c": -0.79780613831,
            "q21s": 0.013146921148,
            "q22c": -0.19595266005,
            "q22s": 0.078488472227,
            "q30": 0.043015515207,
            "q31c": -0.053621704828,
            "q31s": 0.21644282193,
            "q32c": -0.029607236961,
            "q32s": -0.89197505111,
            "q33c": -0.053969314597,
            "q33s": 0.16211677693,
            "q40": -1.4545843935,
            "q41c": 0.91783517331,
            "q41s": 0.17650015949,
            "q42c": -0.73112185714,
            "q42s": -0.3293114897,
            "q43c": 2.8344280941,
            "q43s": -0.16267842746,
            "q44c": -1.3853362266,
            "q44s": 0.089771195512,
            "q50": -0.24411738335,
            "q51c": 0.48960856702,
            "q51s": -1.5472642317,
            "q52c": -0.040094542612,
            "q52s": 0.98097072569,
            "q53c": 0.72718022845,
            "q53s": -1.1988409017,
            "q54c": -0.47766441277,
            "q54s": 2.0753064137,
            "q55c": -0.29405113415,
            "q55s": -1.6430303594,
        },
        "H2": {
            "iqa": -0.48880091691,
            "integration_error": 1.8741005824e-05,
            "q00": 0.55107276527,
            "q10": -0.10046776424,
            "q11c": 0.082404094273,
            "q11s": -0.12293368007,
            "q20": 0.0036460292977,
            "q21c": 0.00029619225829,
            "q21s": -0.0074877731368,
            "q22c": 0.0074481701736,
            "q22s": 0.0056874730269,
            "q30": -0.05956450163,
            "q31c": -0.039733101597,
            "q31s": 0.041495598451,
            "q32c": -0.028165432797,
            "q32s": -0.11949807302,
            "q33c": 0.058162645861,
            "q33s": 0.018335018802,
            "q40": -0.12002978326,
            "q41c": 0.040444633273,
            "q41s": -0.069505346729,
            "q42c": -0.019427525486,
            "q42s": -0.15727748843,
            "q43c": 0.1932877549,
            "q43s": 0.062934026281,
            "q44c": -0.057209327496,
            "q44s": 0.059969789986,
            "q50": -0.011914817313,
            "q51c": 0.062065103525,
            "q51s": -0.076563819972,
            "q52c": 0.048593580786,
            "q52s": 0.026776257085,
            "q53c": 0.072780829944,
            "q53s": 0.028736420893,
            "q54c": -0.04279361242,
            "q54s": 0.10697549721,
            "q55c": -0.031070190556,
            "q55s": -0.026095070495,
        },
        "H3": {
            "iqa": -0.48619221042,
            "integration_error": 1.7274446651e-05,
            "q00": 0.50085300856,
            "q10": 0.085197944712,
            "q11c": -0.087841616442,
            "q11s": -0.12029023455,
            "q20": 0.00023993899792,
            "q21c": -0.023661428009,
            "q21s": -0.021391961736,
            "q22c": -1.9131859436e-05,
            "q22s": 0.02151432195,
            "q30": 0.087599091989,
            "q31c": 0.031324229347,
            "q31s": 0.026427482381,
            "q32c": 0.023804975755,
            "q32s": -0.15674955727,
            "q33c": -0.088059760394,
            "q33s": 0.037288453803,
            "q40": -0.07444947707,
            "q41c": 0.05887992764,
            "q41s": 0.081114651822,
            "q42c": 0.0088380735081,
            "q42s": 0.083371237428,
            "q43c": 0.15535798009,
            "q43s": -0.069909915593,
            "q44c": -0.064026374739,
            "q44s": -0.057177316644,
            "q50": 0.0082484388953,
            "q51c": 0.099441485367,
            "q51s": 0.11360202978,
            "q52c": -0.01832368283,
            "q52s": -0.0010932889664,
            "q53c": 0.15341606275,
            "q53s": -0.10054868004,
            "q54c": -0.17440062253,
            "q54s": -0.0001046247894,
            "q55c": 0.045251112263,
            "q55s": 0.071037518757,
        },
    }

    _assert_val_optional(int_dir_instance.raw_data, expected_raw_data)


def test_water_ints_dir():

    _test_ints(example_dir)
