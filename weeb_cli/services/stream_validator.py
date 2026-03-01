import requests
from typing import Optional, Tuple, List, Dict, Any
from weeb_cli.services.logger import debug

class StreamValidator:
    
    @staticmethod
    def validate_url(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 5) -> Tuple[bool, Optional[str]]:
        if not url:
            return False, "Empty URL"
        
        if not url.startswith(('http://', 'https://')):
            return False, "Invalid protocol"
        
        try:
            response = requests.head(
                url,
                headers=headers or {},
                timeout=timeout,
                allow_redirects=True
            )
            
            if response.status_code == 405:
                response = requests.get(
                    url,
                    headers=headers or {},
                    timeout=timeout,
                    stream=True
                )
                response.close()
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '').lower()
                
                valid_types = ['video/', 'application/x-mpegurl', 'application/vnd.apple.mpegurl', 'application/octet-stream']
                if any(t in content_type for t in valid_types) or not content_type:
                    return True, None
                else:
                    return False, f"Invalid content type: {content_type}"
            
            return False, f"HTTP {response.status_code}"
            
        except requests.Timeout:
            return False, "Connection timeout"
        except requests.ConnectionError:
            return False, "Connection failed"
        except Exception as e:
            debug(f"[VALIDATOR] Validation error: {e}")
            return False, str(e)
    
    @staticmethod
    def validate_streams(streams: List[Any], headers: Optional[Dict[str, str]] = None) -> List[Any]:
        validated = []
        
        for stream in streams:
            url = stream.url if hasattr(stream, 'url') else stream.get('url')
            stream_headers = stream.headers if hasattr(stream, 'headers') else stream.get('headers', {})
            
            if headers:
                stream_headers.update(headers)
            
            is_valid, error = StreamValidator.validate_url(url, stream_headers, timeout=3)
            
            if is_valid:
                validated.append(stream)
                debug(f"[VALIDATOR] Valid stream: {url[:50]}...")
            else:
                debug(f"[VALIDATOR] Invalid stream: {url[:50]}... - {error}")
        
        return validated

stream_validator: StreamValidator = StreamValidator()
