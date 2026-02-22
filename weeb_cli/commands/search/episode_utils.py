def get_episodes_safe(details):
    episodes = None
    for k in ["episodes", "episodes_list", "episode_list", "results", "chapters"]:
        if k in details and isinstance(details[k], list):
            episodes = details[k]
            break
            
    if not episodes:
        for v in details.values():
            if isinstance(v, list) and v and isinstance(v[0], dict) and ("number" in v[0] or "ep_num" in v[0] or "url" in v[0]):
                episodes = v
                break
    return episodes

def group_episodes_by_season(episodes):
    seasons = {}
    for ep in episodes:
        season = ep.get('season', 1)
        if season not in seasons:
            seasons[season] = []
        seasons[season].append(ep)
    
    for season in seasons:
        seasons[season] = sorted(seasons[season], key=lambda x: int(x.get('number') or x.get('ep_num') or 0))
    
    return seasons

def make_season_episode_id(season, ep_num):
    return season * 1000 + ep_num

def normalize_search_results(data):
    if not isinstance(data, dict):
        return data
    
    if "results" in data and isinstance(data["results"], list):
        return data["results"]
    
    if "data" in data:
        inner = data["data"]
        if isinstance(inner, list):
            return inner
        if isinstance(inner, dict):
            if "results" in inner and isinstance(inner["results"], list):
                return inner["results"]
            if "animes" in inner and isinstance(inner["animes"], list):
                return inner["animes"]
            if "items" in inner and isinstance(inner["items"], list):
                return inner["items"]
    
    return data

def normalize_details(details):
    if not isinstance(details, dict):
        return details
    
    source = details.get("source")
    
    if "data" in details and isinstance(details["data"], dict):
        details = details["data"]
    
    if "details" in details and isinstance(details["details"], dict):
        details = details["details"]
        if source:
            details["source"] = source
    
    return details
