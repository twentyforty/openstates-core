from slugify.slugify import slugify
from openstates.metadata.data import STATES_BY_JID


def cmd_args_and_job_id_for_os_udpate(jurisdiction_id, scrapers=["bills"], session_identifier=None, active_only=True):
    state = STATES_BY_JID[jurisdiction_id]
    state = state.abbr.lower()
    if state == "us":
        state = "usa"

    cmd_args = [state]
    job_id_parts = [state, "os-update"]
    
    if session_identifier:
        job_id_parts.append(session_identifier)

    for scraper in scrapers:
        job_id_parts.append(scraper)
        cmd_args.append(scraper)
        if session_identifier:
            cmd_args.append(f"session='{session_identifier}'")

    if session_identifier is None and active_only:
        cmd_args.append("--active-only")

    job_id = slugify("-".join(job_id_parts).lower())
    return cmd_args, job_id