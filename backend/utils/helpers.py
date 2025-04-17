from datetime import datetime
from zoneinfo import ZoneInfo

SGT = ZoneInfo("Asia/Singapore")

def format_price(price: float) -> str:
    return f"{price:.2f}"

def get_sgt_time() -> str:
    return datetime.now(SGT).isoformat()

def parse_datetime(dt_str: str) -> datetime:
    dt_str = dt_str.strip()
    
    try:
        if dt_str.endswith('Z'):
            dt_str = dt_str[:-1] + '+00:00'
        dt = datetime.fromisoformat(dt_str)
        
        if dt.tzinfo is None:
            return dt.replace(tzinfo=SGT) 
        return dt.astimezone(SGT)
    except ValueError:
        try:
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            return dt.replace(tzinfo=SGT)
        except ValueError:
            try:
                dt = datetime.strptime(dt_str, "%Y-%m-%d")
                return dt.replace(tzinfo=SGT)
            except ValueError as e:
                raise ValueError(f"Invalid datetime format: {dt_str}") from e