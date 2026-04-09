# Weeb CLI Examples

This directory contains example scripts demonstrating how to use weeb-cli's various features.

## RESTful API Client Examples

### Python Client

**File:** `restful_api_client.py`

A comprehensive Python client demonstrating all RESTful API endpoints.

**Requirements:**
```bash
pip install requests
```

**Usage:**
```bash
# Start the RESTful API server first
weeb-cli serve restful --port 8080

# Run the example client
python examples/restful_api_client.py
```

**Features:**
- Health check
- List providers
- Search anime
- Get anime details
- List episodes
- Get stream URLs

### JavaScript/Node.js Client

**File:** `restful_api_client.js`

A Node.js client demonstrating RESTful API usage in JavaScript.

**Requirements:**
- Node.js 18+ (for native fetch support)

**Usage:**
```bash
# Start the RESTful API server first
weeb-cli serve restful --port 8080

# Run the example client
node examples/restful_api_client.js
```

**Environment Variables:**
```bash
# Custom server URL
WEEB_CLI_URL=http://localhost:9000 node examples/restful_api_client.js
```

## Creating Your Own Client

### Basic Structure

```python
import requests

class WeebCLIClient:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
    
    def search(self, query, provider=None):
        params = {"q": query}
        if provider:
            params["provider"] = provider
        response = requests.get(f"{self.base_url}/api/search", params=params)
        return response.json()

# Usage
client = WeebCLIClient()
results = client.search("naruto", provider="animecix")
```

### Error Handling

```python
try:
    results = client.search("naruto")
except requests.exceptions.ConnectionError:
    print("Server not running")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
```

### Async Support (Python)

```python
import aiohttp

class AsyncWeebCLIClient:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
    
    async def search(self, query, provider=None):
        params = {"q": query}
        if provider:
            params["provider"] = provider
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/api/search",
                params=params
            ) as response:
                return await response.json()

# Usage
import asyncio
client = AsyncWeebCLIClient()
results = asyncio.run(client.search("naruto"))
```

## API Endpoints Reference

### Health Check
```http
GET /health
```

### List Providers
```http
GET /api/providers
```

### Search Anime
```http
GET /api/search?q=naruto&provider=animecix
```

### Get Anime Details
```http
GET /api/anime/{anime_id}?provider=animecix
```

### List Episodes
```http
GET /api/anime/{anime_id}/episodes?season=1&provider=animecix
```

### Get Streams
```http
GET /api/anime/{anime_id}/episodes/{episode_id}/streams?provider=animecix&sort=desc
```

## Integration Examples

### Web Application (React)

```javascript
// api/weebcli.js
export class WeebCLIAPI {
  constructor(baseUrl = 'http://localhost:8080') {
    this.baseUrl = baseUrl;
  }

  async search(query, provider) {
    const params = new URLSearchParams({ q: query });
    if (provider) params.append('provider', provider);
    
    const response = await fetch(`${this.baseUrl}/api/search?${params}`);
    const data = await response.json();
    return data.results;
  }
}

// Component usage
import { WeebCLIAPI } from './api/weebcli';

function SearchComponent() {
  const [results, setResults] = useState([]);
  const api = new WeebCLIAPI();

  const handleSearch = async (query) => {
    const data = await api.search(query, 'animecix');
    setResults(data);
  };

  return (
    <div>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {results.map(anime => (
        <div key={anime.id}>{anime.title}</div>
      ))}
    </div>
  );
}
```

### Mobile App (React Native)

```javascript
// services/weebcli.js
export const searchAnime = async (query, provider = 'animecix') => {
  const response = await fetch(
    `http://your-server:8080/api/search?q=${encodeURIComponent(query)}&provider=${provider}`
  );
  const data = await response.json();
  return data.results;
};

// Usage in component
import { searchAnime } from './services/weebcli';

const SearchScreen = () => {
  const [results, setResults] = useState([]);

  useEffect(() => {
    searchAnime('naruto').then(setResults);
  }, []);

  return (
    <FlatList
      data={results}
      renderItem={({ item }) => <Text>{item.title}</Text>}
    />
  );
};
```

### CLI Tool (Bash)

```bash
#!/bin/bash
# weeb-search.sh

API_URL="http://localhost:8080"
QUERY="$1"
PROVIDER="${2:-animecix}"

# Search anime
curl -s "${API_URL}/api/search?q=${QUERY}&provider=${PROVIDER}" | jq '.results[] | "\(.title) (\(.year))"'
```

## Docker Deployment

### docker-compose.yml

```yaml
version: '3.8'

services:
  weeb-cli-api:
    image: weeb-cli-restful
    ports:
      - "8080:8080"
    environment:
      - RESTFUL_PROVIDERS=animecix,hianime,aniworld
      - RESTFUL_CORS=true
    restart: unless-stopped

  web-app:
    image: your-web-app
    depends_on:
      - weeb-cli-api
    environment:
      - WEEB_CLI_API_URL=http://weeb-cli-api:8080
```

## Testing

### Unit Tests (Python)

```python
import pytest
from restful_api_client import WeebCLIClient

@pytest.fixture
def client():
    return WeebCLIClient("http://localhost:8080")

def test_health_check(client):
    health = client.health_check()
    assert health["status"] == "ok"

def test_search(client):
    results = client.search("naruto", provider="animecix")
    assert len(results) > 0
    assert "id" in results[0]
    assert "title" in results[0]
```

### Integration Tests (JavaScript)

```javascript
const { WeebCLIClient } = require('./restful_api_client');

describe('WeebCLI API', () => {
  let client;

  beforeAll(() => {
    client = new WeebCLIClient('http://localhost:8080');
  });

  test('health check returns ok', async () => {
    const health = await client.healthCheck();
    expect(health.status).toBe('ok');
  });

  test('search returns results', async () => {
    const results = await client.search('naruto', 'animecix');
    expect(results.length).toBeGreaterThan(0);
    expect(results[0]).toHaveProperty('id');
    expect(results[0]).toHaveProperty('title');
  });
});
```

## Contributing

Feel free to contribute more examples! Submit a pull request with:
- Clear documentation
- Working code
- Usage instructions
- Error handling

## License

These examples are part of weeb-cli and are licensed under GPL-3.0.
