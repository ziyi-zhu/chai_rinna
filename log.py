from chai_py import display_logs, get_logs
from chai_py.auth import set_auth

from credentials import DEVELOPER_UID, DEVELOPER_KEY


if DEVELOPER_KEY is None or DEVELOPER_UID is None:
    raise RuntimeError("Please fetch your UID and KEY from the bottom of the Chai Developer Platform. https://chai.ml/dev")

set_auth(DEVELOPER_UID, DEVELOPER_KEY)
display_logs(get_logs(bot_uid="_bot_5599ef8b-ee37-4a5d-a1ce-3267aad0181c"))