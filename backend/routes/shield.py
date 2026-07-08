from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ShieldAction(BaseModel):
    comment_id: str
    action: str


LOG = [
    {
        "id": "del_001",
        "comment_text": "Go back to Pakistan you Muslim dogs",
        "action": "hidden",
        "timestamp": "Today 9:14 AM",
        "post": "Eid Mubarak post",
    },
    {
        "id": "del_002",
        "comment_text": "Love jihad agent spotted",
        "action": "hidden",
        "timestamp": "Today 8:52 AM",
        "post": "Family photo",
    },
    {
        "id": "del_003",
        "comment_text": "Terrorist supporter",
        "action": "deleted",
        "timestamp": "Yesterday 11:30 PM",
        "post": "Community event",
    },
]


@router.get("/shield/log")
def get_shield_log():
    return LOG


@router.post("/shield/hide")
def hide_comment(payload: ShieldAction):
    print(f"Demo shield action: {payload.action} comment {payload.comment_id}")
    return {"success": True}
