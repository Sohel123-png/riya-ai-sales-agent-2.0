"""Webhook server: Vapi yahan tool calls aur call reports bhejta hai."""
import csv, os, json
from datetime import datetime
from fastapi import FastAPI, Request

app = FastAPI()
LEADS = "leads.csv"
DNC = "do_not_call.txt"
REPORTS = "call_reports.jsonl"

def append_lead(row: dict):
    new = not os.path.exists(LEADS)
    fields = ["time", "phone", "name", "need", "budget", "callback_time", "status"]
    with open(LEADS, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in fields})

@app.post("/vapi")
async def vapi(req: Request):
    data = await req.json()
    msg = data.get("message", {})
    mtype = msg.get("type")
    phone = msg.get("call", {}).get("customer", {}).get("number", "")

    if mtype == "tool-calls":
        results = []
        for tc in msg.get("toolCallList", []):
            name = tc.get("name") or tc.get("function", {}).get("name")
            args = tc.get("arguments") or tc.get("function", {}).get("arguments") or {}
            if isinstance(args, str):
                args = json.loads(args or "{}")
            if name == "save_lead":
                append_lead({**args, "phone": phone, "time": datetime.now().isoformat(timespec="seconds")})
                out = "Lead saved."
            elif name == "mark_do_not_call":
                open(DNC, "a").write(phone + "\n")
                out = "Number DNC list mein add ho gaya."
            else:
                out = "Unknown tool."
            results.append({"toolCallId": tc.get("id"), "result": out})
        return {"results": results}

    if mtype == "end-of-call-report":
        with open(REPORTS, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "time": datetime.now().isoformat(timespec="seconds"),
                "phone": phone,
                "summary": msg.get("summary"),
                "ended_reason": msg.get("endedReason"),
                "transcript": msg.get("transcript"),
            }, ensure_ascii=False) + "\n")
    return {"ok": True}

@app.get("/")
def health():
    return {"status": "running"}
