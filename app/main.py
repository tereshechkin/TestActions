from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="Test Time Backend")


@app.get("/time")
def get_server_time() -> dict[str, str]:
    return {"server_time": datetime.now(timezone.utc).isoformat()}
