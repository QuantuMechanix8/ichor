from ichor.hpc.global_variables import FILE_STRUCTURE
from ichor.hpc.submission_script.script_names import ScriptNames

SCRIPT_NAMES = ScriptNames(
    {
        "pd_to_database": "pd_to_database.sh",
        "calculate_features": "calculate_features.sh",
        "center_trajectory": "center_trajectory.sh",
    },
    parent=FILE_STRUCTURE["scripts"],
)
