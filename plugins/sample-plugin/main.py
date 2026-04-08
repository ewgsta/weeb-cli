def register():
    """Register the sample provider with the Weeb CLI registry."""
    from weeb_cli.providers.registry import register_provider
    from weeb_cli.providers.base import BaseProvider
    
    @register_provider("sample_provider", lang="en", region="US")
    class SampleProvider(BaseProvider):
        def __init__(self):
            super().__init__()
            self.name = "sample_provider"
            
        def search(self, query: str):
            return [{"title": f"Sample Result for {query}", "id": "1"}]
            
        def get_episodes(self, anime_id: str):
            return [{"id": "1", "title": "Episode 1"}]
            
        def get_streams(self, ep_id: str):
            return [{"url": "https://example.com/video.mp4", "quality": "720p"}]

    print("Sample Plugin Registered!")
