#!/usr/bin/env node
/**
 * Example RESTful API client for weeb-cli (Node.js/JavaScript)
 * 
 * This script demonstrates how to interact with the weeb-cli RESTful API server.
 * 
 * Usage:
 *   node restful_api_client.js
 */

const BASE_URL = process.env.WEEB_CLI_URL || 'http://localhost:8080';

/**
 * WeebCLI API Client
 */
class WeebCLIClient {
  constructor(baseUrl = BASE_URL) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  /**
   * Make HTTP GET request
   */
  async get(endpoint, params = {}) {
    const url = new URL(`${this.baseUrl}${endpoint}`);
    Object.keys(params).forEach(key => {
      if (params[key] !== null && params[key] !== undefined) {
        url.searchParams.append(key, params[key]);
      }
    });

    const response = await fetch(url.toString());
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Health check
   */
  async healthCheck() {
    return this.get('/health');
  }

  /**
   * List all providers
   */
  async listProviders() {
    return this.get('/api/providers');
  }

  /**
   * Search anime
   */
  async search(query, provider = null) {
    const data = await this.get('/api/search', { q: query, provider });
    return data.results || [];
  }

  /**
   * Get anime details
   */
  async getAnimeDetails(animeId, provider = null) {
    const data = await this.get(`/api/anime/${animeId}`, { provider });
    return data.anime || {};
  }

  /**
   * Get episodes
   */
  async getEpisodes(animeId, season = null, provider = null) {
    const data = await this.get(`/api/anime/${animeId}/episodes`, { season, provider });
    return data.episodes || [];
  }

  /**
   * Get streams
   */
  async getStreams(animeId, episodeId, provider = null, sort = 'desc') {
    const data = await this.get(
      `/api/anime/${animeId}/episodes/${episodeId}/streams`,
      { provider, sort }
    );
    return data.streams || [];
  }
}

/**
 * Main example function
 */
async function main() {
  const client = new WeebCLIClient();

  try {
    // Health check
    console.log('=== Health Check ===');
    const health = await client.healthCheck();
    console.log(`Status: ${health.status}`);
    console.log(`Providers: ${health.providers.join(', ')}`);
    console.log();

    // List providers
    console.log('=== Available Providers ===');
    const providersData = await client.listProviders();
    providersData.providers.forEach(provider => {
      console.log(`- ${provider.name} (${provider.lang}/${provider.region})`);
    });
    console.log();

    // Search anime
    console.log('=== Search Results ===');
    const query = 'naruto';
    const results = await client.search(query, 'animecix');
    console.log(`Found ${results.length} results for '${query}':`);
    results.slice(0, 5).forEach((anime, i) => {
      console.log(`${i + 1}. ${anime.title} (${anime.year}) - ID: ${anime.id}`);
    });
    console.log();

    if (results.length === 0) {
      console.log('No results found. Exiting.');
      return;
    }

    // Get anime details
    console.log('=== Anime Details ===');
    const animeId = results[0].id;
    const details = await client.getAnimeDetails(animeId, 'animecix');
    console.log(`Title: ${details.title}`);
    console.log(`Type: ${details.type}`);
    console.log(`Year: ${details.year}`);
    console.log(`Status: ${details.status || 'N/A'}`);
    if (details.genres && details.genres.length > 0) {
      console.log(`Genres: ${details.genres.join(', ')}`);
    }
    console.log();

    // Get episodes
    console.log('=== Episodes (Season 1) ===');
    const episodes = await client.getEpisodes(animeId, 1, 'animecix');
    console.log(`Found ${episodes.length} episodes:`);
    episodes.slice(0, 5).forEach(ep => {
      const title = ep.title || `Episode ${ep.number}`;
      const season = String(ep.season).padStart(2, '0');
      const number = String(ep.number).padStart(2, '0');
      console.log(`- S${season}E${number}: ${title}`);
    });
    console.log();

    if (episodes.length === 0) {
      console.log('No episodes found. Exiting.');
      return;
    }

    // Get streams for first episode
    console.log('=== Streams (First Episode) ===');
    const episodeId = episodes[0].id;
    const streams = await client.getStreams(animeId, episodeId, 'animecix');
    console.log(`Found ${streams.length} streams:`);
    streams.forEach(stream => {
      console.log(`- Quality: ${stream.quality}`);
      console.log(`  Server: ${stream.server}`);
      console.log(`  URL: ${stream.url.substring(0, 60)}...`);
      if (stream.subtitles) {
        console.log(`  Subtitles: ${stream.subtitles}`);
      }
    });
    console.log();

  } catch (error) {
    if (error.code === 'ECONNREFUSED') {
      console.error('Error: Could not connect to weeb-cli RESTful API server.');
      console.error('Make sure the server is running: weeb-cli serve restful');
    } else {
      console.error(`Error: ${error.message}`);
    }
    process.exit(1);
  }
}

// Run main function
if (require.main === module) {
  main().catch(error => {
    console.error('Unhandled error:', error);
    process.exit(1);
  });
}

module.exports = { WeebCLIClient };
