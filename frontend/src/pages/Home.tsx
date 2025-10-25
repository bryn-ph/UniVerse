import { useState, useEffect, useRef } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import DiscussionCard from "@/components/DiscussionCard";
import api from "@/lib/api";
import type { components } from "@/types/api.d";

// Infer Discussion type from your OpenAPI schema
type Discussion = components["schemas"]["Discussion"];

export default function Home() {
  const [discussions, setDiscussions] = useState<Discussion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const debounceRef = useRef<number | null>(null);
  
  // Fetch discussions from backend (optionally with search q)
  const fetchDiscussions = async (q?: string) => {
    setLoading(true);
    setError(null);
    try {
      const params = q ? { params: { query: { q } } } : { params: {} };
      const res = await api.GET("/api/discussions/", params as any);
      // openapi-fetch returns { data, error }
      if ((res as any).error) {
        console.error("api client error:", (res as any).error);
        setError("Failed to fetch posts");
      } else if ((res as any).data) {
        setDiscussions((res as any).data);
      } else if (Array.isArray(res)) {
        setDiscussions(res as any);
      } else {
        console.warn("Unexpected api.GET response shape", res);
        setError("Failed to fetch posts (unexpected response)");
      }
    } catch (err) {
      console.error("Error fetching discussions with api client:", err);
      // fallback to native fetch
      try {
        const url = q ? `/api/discussions/?q=${encodeURIComponent(q)}` : "/api/discussions/";
        const r = await fetch(url);
        if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
        const data = await r.json();
        setDiscussions(data);
      } catch (err2) {
        console.error("Fetch fallback failed:", err2);
        setError("Failed to fetch posts");
      }
    } finally {
      setLoading(false);
    }
  };

  // initial load
  useEffect(() => {
    fetchDiscussions();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // watch query and fetch with debounce
  useEffect(() => {
    if (debounceRef.current) window.clearTimeout(debounceRef.current);
    // small debounce to avoid spamming backend
    debounceRef.current = window.setTimeout(() => {
      fetchDiscussions(query.trim() ? query.trim() : undefined);
    }, 300) as unknown as number;
    return () => {
      if (debounceRef.current) window.clearTimeout(debounceRef.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [query]);


  return (
  <div className="flex flex-col items-center w-full max-w-7xl mx-auto mt-10 px-4">
      {/* Hero/Header */}
      <div className="w-full mb-6">
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#234E70] via-[#1f6b8a] to-[#0ea5a4] text-white shadow-2xl p-6 sm:p-10">
          <div className="max-w-5xl mx-auto flex flex-col sm:flex-row items-center gap-6">
            <div className="flex-1 text-center sm:text-left">
              <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight">UniVerse Feed</h1>
              <p className="mt-2 text-sm sm:text-lg text-white/90">Connect, share, and learn with fellow university students.</p>
            </div>

            <div className="w-full sm:w-auto">
              <div className="flex items-center gap-2 bg-white rounded-full p-1 shadow-sm">
                <Input
                  placeholder="Search discussions..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="bg-transparent pr-2 pl-4 py-2 rounded-full w-56 sm:w-80 placeholder:text-muted-foreground text-slate-800 dark:text-slate-100"
                />
                <Button className="rounded-full" onClick={() => setQuery("")}>Clear</Button>
              </div>
            </div>
          </div>

          {/* decorative accent */}
          <div className="absolute -top-10 -right-10 w-40 h-40 bg-white/10 rounded-full blur-3xl pointer-events-none" />
        </div>
      </div>
      {query && (
        <div className="w-full text-sm text-muted-foreground mb-4 text-center">
          Showing results for "{query}"
        </div>
      )}

      {/* Recent Posts Section */}
      <div className="w-full space-y-4">
        {loading ? (
          <div className="flex justify-center items-center min-h-[200px]">
            <div className="animate-pulse text-muted-foreground">
              Loading posts...
            </div>
          </div>
        ) : error ? (
          <Card className="border-destructive">
            <CardContent className="py-12 text-center">
              <p className="text-destructive">{error}</p>
            </CardContent>
          </Card>
        ) : discussions.length === 0 ? (
          <Card className="w-full border-dashed border-2 border-muted">
            <CardContent className="py-12 text-center text-muted-foreground">
              <p className="text-sm">
                No posts yet — be the first to share something!
              </p>
            </CardContent>
          </Card>
        ) : (
          discussions.map((post) => (
            <DiscussionCard
              key={String(post.id)}
              discussion={post}
              groupId={undefined}
              groupName={undefined}
            />
          ))
        )}
      </div>
    </div>
  );
}