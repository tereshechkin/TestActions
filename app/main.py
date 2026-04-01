from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import FastAPI, HTTPException, Query

from app.loki import log_endpoint_calls

app = FastAPI(
    title="Test Time Backend",
    docs_url="/swagger/",
    openapi_url="/openapi.json",
)
app.middleware("http")(log_endpoint_calls)


def _zone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown IANA timezone: {name!r}. Example: Europe/Moscow",
        ) from e


def _parse_instant_utc(at: str | None) -> datetime:
    if at is None:
        return datetime.now(timezone.utc)
    s = at.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail="Invalid `at`: use ISO 8601, e.g. 2026-03-30T12:00:00Z",
        ) from e
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


@app.get("/time")
def get_server_time() -> dict[str, str]:
    return {"server_time": datetime.now(timezone.utc).isoformat()}


@app.get("/date")
def get_server_date() -> dict[str, str]:
    return {"server_date": datetime.now().date().isoformat()}


@app.get("/date/utc")
def get_server_date_utc() -> dict[str, str]:
    return {"server_date_utc": datetime.now(timezone.utc).date().isoformat()}


@app.get("/time/convert")
def convert_time_between_timezones(
    to_tz: str = Query(..., description="Target IANA timezone, e.g. Asia/Tokyo"),
    from_tz: str = Query("UTC", description="Source IANA timezone for the same instant"),
    at: str | None = Query(
        None,
        description="Optional moment in ISO 8601 (default: current UTC time)",
    ),
) -> dict[str, str]:
    instant_utc = _parse_instant_utc(at)
    z_from = _zone(from_tz)
    z_to = _zone(to_tz)
    return {
        "instant_utc": instant_utc.isoformat(),
        "from_tz": from_tz,
        "time_in_from_tz": instant_utc.astimezone(z_from).isoformat(),
        "to_tz": to_tz,
        "time_in_to_tz": instant_utc.astimezone(z_to).isoformat(),
    }
