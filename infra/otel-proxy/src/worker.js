const OTLP_PATHS = new Set([
  "/v1/traces",
  "/v1/metrics",
  "/v1/logs",
]);

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return corsResponse(env, 204);
    }

    const url = new URL(request.url);

    if (url.pathname === "/health") {
      return corsResponse(env, 200, { status: "ok" });
    }

    if (request.method !== "POST" || !OTLP_PATHS.has(url.pathname)) {
      return corsResponse(env, 404, { error: "not found" });
    }

    if (!env.GRAFANA_INSTANCE_ID || !env.GRAFANA_API_KEY) {
      return corsResponse(env, 500, { error: "proxy not configured" });
    }

    const target = `${env.GRAFANA_OTLP_ENDPOINT}${url.pathname}`;
    const credentials = btoa(`${env.GRAFANA_INSTANCE_ID}:${env.GRAFANA_API_KEY}`);

    const headers = new Headers();
    headers.set("Authorization", `Basic ${credentials}`);
    headers.set("Content-Type", request.headers.get("Content-Type") || "application/x-protobuf");

    const encoding = request.headers.get("Content-Encoding");
    if (encoding) {
      headers.set("Content-Encoding", encoding);
    }

    try {
      const upstream = await fetch(target, {
        method: "POST",
        headers,
        body: request.body,
      });

      const response = new Response(upstream.body, {
        status: upstream.status,
        headers: { "Content-Type": upstream.headers.get("Content-Type") || "application/json" },
      });

      setCors(response, env);
      return response;
    } catch (err) {
      return corsResponse(env, 502, { error: "upstream failed" });
    }
  },
};

function corsResponse(env, status, body) {
  const response = new Response(
    body ? JSON.stringify(body) : null,
    { status, headers: body ? { "Content-Type": "application/json" } : {} },
  );
  setCors(response, env);
  return response;
}

function setCors(response, env) {
  const origin = env.ALLOWED_ORIGINS || "*";
  response.headers.set("Access-Control-Allow-Origin", origin);
  response.headers.set("Access-Control-Allow-Methods", "POST, OPTIONS");
  response.headers.set("Access-Control-Allow-Headers", "Content-Type, Content-Encoding");
  response.headers.set("Access-Control-Max-Age", "86400");
}
