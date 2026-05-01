#!/usr/bin/env python3
"""Example usage of Weeb CLI SDK.

This script demonstrates various SDK features including:
- Provider listing and selection
- Anime search
- Episode listing
- Stream URL extraction
- Episode downloading

Run this script to see the SDK in action.
"""

from weeb_cli import WeebSDK, list_providers


def example_list_providers():
    """Example: List all available providers."""
    print("=" * 60)
    print("Example 1: List Available Providers")
    print("=" * 60)
    
    providers = list_providers()
    
    print(f"\nFound {len(providers)} providers:\n")
    for p in providers:
        status = "✓" if not p.get('disabled', False) else "✗"
        print(f"  {status} {p['name']:15} - {p['lang'].upper()} ({p['region']})")
    
    print()


def example_search():
    """Example: Search for anime."""
    print("=" * 60)
    print("Example 2: Search for Anime")
    print("=" * 60)
    
    sdk = WeebSDK(default_provider="hianime")
    
    query = "One Piece"
    print(f"\nSearching for '{query}' on HiAnime...\n")
    
    results = sdk.search(query)
    
    print(f"Found {len(results)} results:\n")
    for i, anime in enumerate(results[:5], 1):
        print(f"  {i}. {anime.title}")
        print(f"     Type: {anime.type} | Year: {anime.year}")
        print(f"     ID: {anime.id}")
        if anime.cover:
            print(f"     Cover: {anime.cover[:50]}...")
        print()


def example_get_details():
    """Example: Get anime details."""
    print("=" * 60)
    print("Example 3: Get Anime Details")
    print("=" * 60)
    
    sdk = WeebSDK(default_provider="hianime")
    
    # First search to get an ID
    results = sdk.search("Naruto")
    if not results:
        print("No results found")
        return
    
    anime_id = results[0].id
    print(f"\nFetching details for '{results[0].title}'...\n")
    
    details = sdk.get_details(anime_id)
    
    if details:
        print(f"Title: {details.title}")
        print(f"Status: {details.status}")
        print(f"Year: {details.year}")
        print(f"Genres: {', '.join(details.genres)}")
        print(f"\nDescription:")
        print(f"  {details.description[:200]}..." if details.description else "  N/A")
        print(f"\nTotal Episodes: {details.total_episodes or 'Unknown'}")
        print(f"Available Episodes: {len(details.episodes)}")
    print()


def example_get_episodes():
    """Example: Get episode list."""
    print("=" * 60)
    print("Example 4: Get Episode List")
    print("=" * 60)
    
    sdk = WeebSDK(default_provider="hianime")
    
    # Search and get first result
    results = sdk.search("Death Note")
    if not results:
        print("No results found")
        return
    
    anime_id = results[0].id
    print(f"\nFetching episodes for '{results[0].title}'...\n")
    
    episodes = sdk.get_episodes(anime_id, season=1)
    
    print(f"Season 1 has {len(episodes)} episodes:\n")
    for ep in episodes[:10]:  # Show first 10
        title = ep.title or "No title"
        print(f"  S{ep.season:02d}E{ep.number:02d}: {title}")
    
    if len(episodes) > 10:
        print(f"  ... and {len(episodes) - 10} more episodes")
    print()


def example_get_streams():
    """Example: Get stream URLs."""
    print("=" * 60)
    print("Example 5: Get Stream URLs")
    print("=" * 60)
    
    sdk = WeebSDK(default_provider="hianime")
    
    # Search and get episodes
    results = sdk.search("Demon Slayer")
    if not results:
        print("No results found")
        return
    
    anime_id = results[0].id
    episodes = sdk.get_episodes(anime_id)
    
    if not episodes:
        print("No episodes found")
        return
    
    episode_id = episodes[0].id
    print(f"\nFetching streams for '{results[0].title}' Episode 1...\n")
    
    streams = sdk.get_streams(anime_id, episode_id)
    
    print(f"Found {len(streams)} stream(s):\n")
    for i, stream in enumerate(streams, 1):
        print(f"  {i}. Quality: {stream.quality}")
        print(f"     Server: {stream.server}")
        print(f"     URL: {stream.url[:60]}...")
        if stream.headers:
            print(f"     Headers: {len(stream.headers)} header(s)")
        print()


def example_multi_provider_search():
    """Example: Search across multiple providers."""
    print("=" * 60)
    print("Example 6: Multi-Provider Search")
    print("=" * 60)
    
    sdk = WeebSDK()
    query = "Attack on Titan"
    
    # Try multiple providers
    providers_to_try = ["hianime", "animecix", "aniworld"]
    
    print(f"\nSearching for '{query}' across multiple providers...\n")
    
    for provider in providers_to_try:
        try:
            results = sdk.search(query, provider=provider)
            print(f"  {provider:15} - {len(results)} result(s)")
        except Exception as e:
            print(f"  {provider:15} - Error: {e}")
    
    print()


def example_download_episode():
    """Example: Download an episode (commented out for safety)."""
    print("=" * 60)
    print("Example 7: Download Episode (Demonstration)")
    print("=" * 60)
    
    print("\nThis example shows how to download an episode.")
    print("Actual download is commented out to prevent accidental downloads.\n")
    
    print("Code example:")
    print("""
    sdk = WeebSDK(default_provider="hianime")
    
    # Search for anime
    results = sdk.search("My Anime")
    anime_id = results[0].id
    
    # Download episode
    path = sdk.download_episode(
        anime_id=anime_id,
        season=1,
        episode=1,
        output_dir="./downloads"
    )
    
    print(f"Downloaded to: {path}")
    """)
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Weeb CLI SDK Examples")
    print("=" * 60 + "\n")
    
    try:
        example_list_providers()
        example_search()
        example_get_details()
        example_get_episodes()
        example_get_streams()
        example_multi_provider_search()
        example_download_episode()
        
        print("=" * 60)
        print("All examples completed!")
        print("=" * 60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\n\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
