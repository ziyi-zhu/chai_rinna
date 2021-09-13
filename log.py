from chai_py import display_logs, get_logs
from chai_py.auth import set_auth

DEVELOPER_UID = "OY1JRCCpzsViVBIKWCm0042xw4i1"
DEVELOPER_KEY = "_iDHBp83k-G1XHjoJ6IlihEwBqsfoHJbkR_yNrfNmg9-lI-4iACN5RJHEXewCXvdDPo136_XiVtA6T_0tPkNlg"

if DEVELOPER_KEY is None or DEVELOPER_UID is None:
    raise RuntimeError("Please fetch your UID and KEY from the bottom of the Chai Developer Platform. https://chai.ml/dev")

set_auth(DEVELOPER_UID, DEVELOPER_KEY)
display_logs(get_logs(bot_uid="_bot_f8110500-ca89-4f2e-816a-775b8fda265b"))