import math
from dataclasses import dataclass
from pathlib import Path
from typing import Union

import ichor.cli.global_menu_variables
import ichor.hpc.global_variables
from consolemenu.items import FunctionItem, SubmenuItem
from ichor.cli.console_menu import add_items_to_menu, ConsoleMenu
from ichor.cli.main_menu_submenus.points_directory_menu.points_directory_submenus import (
    submit_aimall_menu,
    SUBMIT_AIMALL_MENU_DESCRIPTION,
    submit_database_menu,
    SUBMIT_DATABASE_MENU_DESCRIPTION,
    submit_gaussian_menu,
    SUBMIT_GAUSSIAN_MENU_DESCRIPTION,
)
from ichor.cli.menu_description import MenuDescription
from ichor.cli.menu_options import MenuOptions
from ichor.cli.script_names import SCRIPT_NAMES
from ichor.cli.useful_functions import (
    bool_to_str,
    compile_strings_to_python_code,
    user_input_bool,
    user_input_float,
    user_input_int,
    user_input_path,
)
from ichor.core.sql.query_database import (
    get_alf_from_first_db_geometry,
    write_processed_data_for_atoms_parallel,
)
from ichor.hpc.submission_commands.free_flow_python_command import FreeFlowPythonCommand
from ichor.hpc.submission_script import SubmissionScript

POINTS_DIRECTORY_MENU_DESCRIPTION = MenuDescription(
    "PointsDirectory Menu",
    subtitle="Use this to interact with ichor's PointsDirectory class.\n",
)


# dataclass used to store values for PointsDirectoryMenu
@dataclass
class PointsDirectoryMenuOptions(MenuOptions):
    # defaults to the current working directory
    selected_points_directory_path: Path

    def check_selected_points_directory_path(self) -> Union[str, None]:
        """Checks whether the given PointsDirectory exists or if it is a directory."""
        pd_path = Path(self.selected_points_directory_path)
        if (not pd_path.exists()) or (not pd_path.is_dir()):
            return f"Current path: {pd_path} does not exist or is not a directory."


# initialize dataclass for storing information for menu
points_directory_menu_options = PointsDirectoryMenuOptions(
    ichor.cli.global_menu_variables.SELECTED_POINTS_DIRECTORY_PATH
)


# class with static methods for each menu item that calls a function.
class PointsDirectoryFunctions:
    """Functions that run when menu items are selected"""

    @staticmethod
    def select_points_directory():
        """Asks user to update points directory and then updates PointsDirectoryMenuPrologue instance."""
        pd_path = user_input_path("Enter PointsDirectory Path: ")
        ichor.cli.global_menu_variables.SELECTED_POINTS_DIRECTORY_PATH = Path(
            pd_path
        ).absolute()
        points_directory_menu_options.selected_points_directory_path = (
            ichor.cli.global_menu_variables.SELECTED_POINTS_DIRECTORY_PATH
        )

    @staticmethod
    def make_csvs_from_database():
        """Makes csv files contaning features, iqa energies, and rotated multipole moments given a database"""

        default_submit_on_compute = True
        default_rotate_multipoles = True
        default_calculate_feature_forces = False
        default_filter_by_sum_iqa_compared_to_wfn = True
        default_float_difference_iqa_wfn = 4.184
        default_filter_by_integration_error = True
        default_float_integration_error = 0.001
        default_ncores = 4

        db_path = user_input_path("Enter path to SQLite3 database: ")
        db_path = Path(db_path)

        rotate_multipoles = user_input_bool(
            f"Calculate rotated multipoles (yes/no), default {bool_to_str(default_rotate_multipoles)}: "
        )
        if rotate_multipoles is None:
            rotate_multipoles = default_rotate_multipoles

        calculate_feature_forces = user_input_bool(
            f"Calculate feature forces (yes/no), default {bool_to_str(default_calculate_feature_forces)}: "
        )
        if calculate_feature_forces is None:
            calculate_feature_forces = default_calculate_feature_forces

        # filtering by sum of iqa vs wfn energy
        filter_by_sum_iqa_vs_wfn = user_input_bool(
            f"Filter by comparing sum of IQA to WFN (yes/no), default {bool_to_str(default_filter_by_sum_iqa_compared_to_wfn)}: "  # noqa: E501
        )
        if filter_by_sum_iqa_vs_wfn is None:
            filter_by_sum_iqa_vs_wfn = default_filter_by_sum_iqa_compared_to_wfn

        if filter_by_sum_iqa_vs_wfn:
            float_difference_iqa_wfn = user_input_float(
                f"Enter maximum energy difference (kJ mol-1) between sum of IQA and WFN, default {default_float_difference_iqa_wfn}: "  # noqa: E501
            )
            if float_difference_iqa_wfn is None:
                float_difference_iqa_wfn = default_float_difference_iqa_wfn
        else:
            float_difference_iqa_wfn = math.inf

        # filtering by integration error
        filter_by_integration_error = user_input_bool(
            f"Filter by integration error (yes/no), default {bool_to_str(default_filter_by_integration_error)}: "
        )
        if filter_by_integration_error is None:
            filter_by_integration_error = default_filter_by_integration_error

        # ask for integration error if user has said yes
        if filter_by_integration_error:
            float_integration_error = user_input_float(
                f"Enter integration error threshold, default {default_float_integration_error}: "
            )
            if float_integration_error is None:
                float_integration_error = default_float_integration_error
        # if user has selected do not filter by integration error, then set threshold to infinity
        else:
            float_integration_error = math.inf

        submit_on_compute = user_input_bool(
            f"Submit to compute node (yes/no), default {bool_to_str(default_submit_on_compute)}: "
        )
        if submit_on_compute is None:
            submit_on_compute = default_submit_on_compute

        ncores = user_input_int(
            f"Number of cores to use (one core per atom csv), default {default_ncores}: "
        )
        if ncores is None:
            ncores = default_ncores

        if not submit_on_compute:
            alf = get_alf_from_first_db_geometry(db_path)
            write_processed_data_for_atoms_parallel(
                db_path,
                alf,
                ncores,
                max_diff_iqa_wfn=float_difference_iqa_wfn,
                max_integration_error=float_integration_error,
                calc_multipoles=rotate_multipoles,
                calc_forces=calculate_feature_forces,
            )

        # if running on compute
        else:
            text_list = []
            # make the python command that will be written in the submit script
            # it will get executed as `python -c python_code_to_execute...`
            text_list.append(
                "from ichor.core.sql.query_database import write_processed_data_for_atoms_parallel"
            )
            text_list.append(
                "from ichor.core.sql.query_database import get_alf_from_first_db_geometry"
            )
            text_list.append("from pathlib import Path")
            text_list.append(f"db_path = Path('{db_path.absolute()}')")
            text_list.append("alf = get_alf_from_first_db_geometry(db_path)")
            str_part1 = (
                f"write_processed_data_for_atoms_parallel(db_path, alf, {ncores},"
            )
            str_part2 = f" calc_multipoles={rotate_multipoles}, calc_forces={calculate_feature_forces})"
            text_list.append(str_part1 + str_part2)

            final_cmd = compile_strings_to_python_code(text_list)
            py_cmd = FreeFlowPythonCommand(final_cmd)
            with SubmissionScript(
                SCRIPT_NAMES["calculate_features"], ncores=ncores
            ) as submission_script:
                submission_script.add_command(py_cmd)
            submission_script.submit()


# initialize menu
points_directory_menu = ConsoleMenu(
    this_menu_options=points_directory_menu_options,
    title=POINTS_DIRECTORY_MENU_DESCRIPTION.title,
    subtitle=POINTS_DIRECTORY_MENU_DESCRIPTION.subtitle,
    prologue_text=POINTS_DIRECTORY_MENU_DESCRIPTION.prologue_description_text,
    epilogue_text=POINTS_DIRECTORY_MENU_DESCRIPTION.epilogue_description_text,
    show_exit_option=POINTS_DIRECTORY_MENU_DESCRIPTION.show_exit_option,
)

# make menu items
# can use lambda functions to change text of options as well :)
point_directory_menu_items = [
    FunctionItem(
        "Select PointsDirectory Path or Parent to PointsDirectory",
        PointsDirectoryFunctions.select_points_directory,
    ),
    SubmenuItem(
        SUBMIT_GAUSSIAN_MENU_DESCRIPTION.title,
        submit_gaussian_menu,
        points_directory_menu,
    ),
    SubmenuItem(
        SUBMIT_AIMALL_MENU_DESCRIPTION.title, submit_aimall_menu, points_directory_menu
    ),
    SubmenuItem(
        SUBMIT_DATABASE_MENU_DESCRIPTION.title,
        submit_database_menu,
        points_directory_menu,
    ),
    FunctionItem(
        "Make processed csvs from SQLite3 database",
        PointsDirectoryFunctions.make_csvs_from_database,
    ),
]

add_items_to_menu(points_directory_menu, point_directory_menu_items)
