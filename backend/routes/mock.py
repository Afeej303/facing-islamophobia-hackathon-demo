from fastapi import APIRouter, HTTPException

router = APIRouter()

SUBMITTED_SOURCE_TEXT = "ഉപയോക്താവ് സമർപ്പിച്ച മലയാളത്തിലുള്ള ഫേസ്ബുക്ക് പോസ്റ്റ്/റീൽ ഇസ്‌ലാം വിരുദ്ധ ഉള്ളടക്കമായി ഫ്ലാഗ് ചെയ്തിരിക്കുന്നു. കൃത്യമായ ഉള്ളടക്കം പരിശോധിക്കാൻ ഒറിജിനൽ ലിങ്ക് തുറക്കുക."

ACCOUNTS = [
    {
        "id": "acc_001",
        "name": "Hindu Rashtra Voice",
        "platform": "Facebook",
        "page_url": "https://facebook.com",
        "followers": 87400,
        "flagged_comments": 34,
        "threat_score": 91,
        "primary_narratives": ["love jihad", "demographic replacement"],
        "last_active": "2 hours ago",
        "trend": "rising",
    },
    {
        "id": "acc_002",
        "name": "Bharat Mata Seva",
        "platform": "Facebook",
        "page_url": "https://facebook.com",
        "followers": 45200,
        "flagged_comments": 18,
        "threat_score": 74,
        "primary_narratives": ["madrasa radicalization", "waqf land grab"],
        "last_active": "5 hours ago",
        "trend": "stable",
    },
    {
        "id": "acc_003",
        "name": "Sanatan Dharma Raksha",
        "platform": "Facebook",
        "page_url": "https://facebook.com",
        "followers": 112000,
        "flagged_comments": 51,
        "threat_score": 95,
        "primary_narratives": ["population replacement", "cow slaughter"],
        "last_active": "30 minutes ago",
        "trend": "rising",
    },
    {
        "id": "acc_004",
        "name": "Kerala Hindu Front",
        "platform": "Facebook",
        "page_url": "https://facebook.com",
        "followers": 23800,
        "flagged_comments": 12,
        "threat_score": 61,
        "primary_narratives": ["love jihad", "waqf land grab"],
        "last_active": "1 day ago",
        "trend": "falling",
    },
    {
        "id": "src_001",
        "name": "Submitted Facebook post 17f4pREHtH",
        "platform": "Facebook",
        "page_url": "https://www.facebook.com/share/p/17f4pREHtH/",
        "followers": None,
        "flagged_comments": 1,
        "threat_score": 88,
        "primary_narratives": ["user submitted", "pending review"],
        "last_active": "Submitted Jul 10, 2:37 PM",
        "trend": "rising",
        "source_status": "pending account resolution",
    },
    {
        "id": "src_002",
        "name": "Submitted Facebook post 18rwTG8eks",
        "platform": "Facebook",
        "page_url": "https://www.facebook.com/share/p/18rwTG8eks/",
        "followers": None,
        "flagged_comments": 1,
        "threat_score": 88,
        "primary_narratives": ["user submitted", "pending review"],
        "last_active": "Submitted Jul 10, 2:38 PM",
        "trend": "rising",
        "source_status": "pending account resolution",
    },
    {
        "id": "src_003",
        "name": "Submitted Facebook reel 1H4GzR4Zn3",
        "platform": "Facebook",
        "page_url": "https://www.facebook.com/share/r/1H4GzR4Zn3/",
        "followers": None,
        "flagged_comments": 1,
        "threat_score": 88,
        "primary_narratives": ["user submitted", "pending review"],
        "last_active": "Submitted Jul 10, 2:40 PM",
        "trend": "rising",
        "source_status": "pending account resolution",
    },
    {
        "id": "src_004",
        "name": "Submitted Facebook video 18JKkX5EW8",
        "platform": "Facebook",
        "page_url": "https://www.facebook.com/share/v/18JKkX5EW8/",
        "followers": None,
        "flagged_comments": 1,
        "threat_score": 88,
        "primary_narratives": ["user submitted", "pending review"],
        "last_active": "Submitted Jul 10, 2:43 PM",
        "trend": "rising",
        "source_status": "pending account resolution",
    },
    {
        "id": "src_005",
        "name": "Submitted Facebook video 1GHMJmXj6z",
        "platform": "Facebook",
        "page_url": "https://www.facebook.com/share/v/1GHMJmXj6z/",
        "followers": None,
        "flagged_comments": 1,
        "threat_score": 88,
        "primary_narratives": ["user submitted", "pending review"],
        "last_active": "Submitted Jul 10, 2:44 PM",
        "trend": "rising",
        "source_status": "pending account resolution",
    },
]

COMMENTS = {
    "acc_001": [
        {
            "id": "cmt_001",
            "account_id": "acc_001",
            "author": "Ramesh K.",
            "text": "Muslim population is growing at an alarming rate. By 2050 Hindus will be a minority in their own country. This is a planned conspiracy.",
            "post_url": "https://facebook.com",
            "likes": 312,
            "timestamp": "3 hours ago",
            "claim_key": "demographic_replacement",
            "severity": "high",
        },
        {
            "id": "cmt_002",
            "account_id": "acc_001",
            "author": "Vijay S.",
            "text": "Love jihad is real. Muslim men are systematically targeting Hindu girls to convert them. Wake up Hindus.",
            "post_url": "https://facebook.com",
            "likes": 187,
            "timestamp": "5 hours ago",
            "claim_key": "love_jihad",
            "severity": "high",
        },
        {
            "id": "cmt_003",
            "account_id": "acc_001",
            "author": "Anita P.",
            "text": "These madrasas are nothing but radicalization factories funded by Gulf money. They teach hatred not education.",
            "post_url": "https://facebook.com",
            "likes": 94,
            "timestamp": "8 hours ago",
            "claim_key": "madrasa_radicalization",
            "severity": "medium",
        },
    ],
    "acc_002": [
        {
            "id": "cmt_004",
            "account_id": "acc_002",
            "author": "Deepak M.",
            "text": "Waqf boards are grabbing land everywhere and ordinary citizens cannot fight back.",
            "post_url": "https://facebook.com",
            "likes": 121,
            "timestamp": "7 hours ago",
            "claim_key": "waqf_land_grab",
            "severity": "medium",
        }
    ],
    "acc_003": [
        {
            "id": "cmt_005",
            "account_id": "acc_003",
            "author": "Nitin R.",
            "text": "They will outnumber everyone soon, and that is why every family is part of the same population plot.",
            "post_url": "https://facebook.com",
            "likes": 401,
            "timestamp": "30 minutes ago",
            "claim_key": "demographic_replacement",
            "severity": "high",
        },
        {
            "id": "cmt_006",
            "account_id": "acc_003",
            "author": "Kavita D.",
            "text": "Cow slaughter is done only to insult Hindu beliefs and provoke society.",
            "post_url": "https://facebook.com",
            "likes": 165,
            "timestamp": "1 hour ago",
            "claim_key": "cow_slaughter",
            "severity": "medium",
        },
    ],
    "acc_004": [
        {
            "id": "cmt_007",
            "account_id": "acc_004",
            "author": "Suresh V.",
            "text": "Love jihad networks are running in Kerala and people are hiding the truth.",
            "post_url": "https://facebook.com",
            "likes": 78,
            "timestamp": "1 day ago",
            "claim_key": "love_jihad",
            "severity": "medium",
        }
    ],
    "src_001": [
        {
            "id": "src_cmt_001",
            "account_id": "src_001",
            "author": "സമർപ്പിച്ച ഫേസ്ബുക്ക് ഉറവിടം",
            "text": SUBMITTED_SOURCE_TEXT,
            "post_url": "https://www.facebook.com/share/p/17f4pREHtH/",
            "likes": 0,
            "timestamp": "Jul 10, 2:37 PM",
            "claim_key": "terrorism_association",
            "severity": "high",
        }
    ],
    "src_002": [
        {
            "id": "src_cmt_002",
            "account_id": "src_002",
            "author": "സമർപ്പിച്ച ഫേസ്ബുക്ക് ഉറവിടം",
            "text": SUBMITTED_SOURCE_TEXT,
            "post_url": "https://www.facebook.com/share/p/18rwTG8eks/",
            "likes": 0,
            "timestamp": "Jul 10, 2:38 PM",
            "claim_key": "terrorism_association",
            "severity": "high",
        }
    ],
    "src_003": [
        {
            "id": "src_cmt_003",
            "account_id": "src_003",
            "author": "സമർപ്പിച്ച ഫേസ്ബുക്ക് ഉറവിടം",
            "text": SUBMITTED_SOURCE_TEXT,
            "post_url": "https://www.facebook.com/share/r/1H4GzR4Zn3/",
            "likes": 0,
            "timestamp": "Jul 10, 2:40 PM",
            "claim_key": "terrorism_association",
            "severity": "high",
        }
    ],
    "src_004": [
        {
            "id": "src_cmt_004",
            "account_id": "src_004",
            "author": "സമർപ്പിച്ച ഫേസ്ബുക്ക് ഉറവിടം",
            "text": SUBMITTED_SOURCE_TEXT,
            "post_url": "https://www.facebook.com/share/v/18JKkX5EW8/",
            "likes": 0,
            "timestamp": "Jul 10, 2:43 PM",
            "claim_key": "terrorism_association",
            "severity": "high",
        }
    ],
    "src_005": [
        {
            "id": "src_cmt_005",
            "account_id": "src_005",
            "author": "സമർപ്പിച്ച ഫേസ്ബുക്ക് ഉറവിടം",
            "text": SUBMITTED_SOURCE_TEXT,
            "post_url": "https://www.facebook.com/share/v/1GHMJmXj6z/",
            "likes": 0,
            "timestamp": "Jul 10, 2:44 PM",
            "claim_key": "terrorism_association",
            "severity": "high",
        }
    ],
}


@router.get("/accounts")
def get_accounts():
    return ACCOUNTS


@router.get("/accounts/{account_id}/comments")
def get_comments(account_id: str):
    if account_id not in COMMENTS:
        raise HTTPException(status_code=404, detail="Account not found")
    return COMMENTS[account_id]


@router.get("/stats")
def get_stats():
    return {
        "total_flagged_today": 28,
        "accounts_monitored": len(ACCOUNTS),
        "responses_sent": 7,
        "comments_hidden": 14,
    }
