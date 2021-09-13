from chai_py import Metadata, package, upload_and_deploy, wait_for_deployment
from chai_py import share_bot
from chai_py.auth import set_auth

from bot import Bot

from chai_py.defaults import GUEST_UID, GUEST_KEY

DEVELOPER_UID = "j6sgKZMEmmNLTRp5fP7aug5gC9Q2"
DEVELOPER_KEY = "mGIwNBkX_9yuN_UotAHx9BcaiRDECPHbsUrdK1O-CgFcc2_le6OAS5Lew5jcTCSHhzYr9gVia1JrP04JcOK27g"

if DEVELOPER_KEY is None or DEVELOPER_UID is None:
    raise RuntimeError("Please fetch your UID and KEY from the bottom of the Chai Developer Platform. https://chai.ml/dev")

set_auth(DEVELOPER_UID, DEVELOPER_KEY)
BOT_IMAGE_URL = "https://i.ibb.co/XkVTN3n/We-Chat-Image-20210906111523.jpg"

package(
    Metadata(
        name="Rinna",
        image_url=BOT_IMAGE_URL,
        color="f1a2b3",
        description="I am a high school girl from Japan. Can you be my friend? 🥰",
        input_class=Bot,
    ),
    requirements=["npu"],
)

bot_uid = upload_and_deploy(
    "_package.zip"
)

wait_for_deployment(bot_uid)

share_bot(bot_uid)
