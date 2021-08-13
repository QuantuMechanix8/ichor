import json

from ichor.batch_system import BATCH_SYSTEM, JobID
from ichor.menu import Menu


def delete_jobs():
    from ichor.globals import GLOBALS

    jid_file = GLOBALS.FILE_STRUCTURE["jid"]
    if jid_file.exists():
        with open(jid_file, "r") as f:
            try:
                jids = json.load(f)
            except json.JSONDecodeError:
                jids = []
            for jid in jids:
                jid = JobID(
                    script=jid["script"],
                    id=jid["id"],
                    instance=jid["instance"],
                )
                BATCH_SYSTEM.delete(jid)
                print(f"Deleted {jid}")

        with open(jid_file, "w") as f:
            f.write("[]")


def queue_menu():
    with Menu("Queue Meu", space=True, back=True, exit=True) as menu:
        menu.add_option("del", "Delete currently running jobs", delete_jobs)