from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="Test Time Backend")


@app.get("/time")
def get_server_time() -> dict[str, str]:
    return {"server_time": datetime.now(timezone.utc).isoformat()}


@app.get("/date")
def get_server_date() -> dict[str, str]:
    return {"server_date": datetime.now().date().isoformat()}


@app.get("/date/utc")
def get_server_date_utc() -> dict[str, str]:
    return {"server_date_utc": datetime.now(timezone.utc).date().isoformat()}
