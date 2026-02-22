PLAYER_PRIORITY = [
    "ALUCARD", "AMATERASU", "SIBNET", "MP4UPLOAD", "UQLOAD",
    "MAIL", "DAILYMOTION", "SENDVID", "ODNOKLASSNIKI", "VK",
    "VIDMOLY", "YOURUPLOAD", "MYVI", "GDRIVE", "PIXELDRAIN", "HDVID", "YADISK"
]

def get_player_priority(server_name: str) -> int:
    server_upper = server_name.upper()
    for i, p in enumerate(PLAYER_PRIORITY):
        if p in server_upper:
            return i
    return 999

def sort_streams(streams: list) -> list:
    return sorted(streams, key=lambda s: get_player_priority(s.get("server", "")))

def extract_streams_from_response(stream_resp):
    if not stream_resp or not isinstance(stream_resp, dict):
        return []
    
    data_node = stream_resp
    for _ in range(3):
        if "data" in data_node and isinstance(data_node["data"], (dict, list)):
            data_node = data_node["data"]
        else:
            break
    
    sources = None
    if isinstance(data_node, list):
        sources = data_node
    elif isinstance(data_node, dict):
        sources = data_node.get("links") or data_node.get("sources")
    
    return sources if sources and isinstance(sources, list) else []
