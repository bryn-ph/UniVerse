import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import DiscussionCard from "@/components/DiscussionCard";
import api from "@/lib/api";
import type { components } from "@/types/api.d";

// Infer Discussion type from your OpenAPI schema
type Discussion = components["schemas"]["Discussion"];

export default function Home() {
  const [discussions, setDiscussions] = useState<Discussion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Fetch discussions from backend
  useEffect(() => {
    const fetchDiscussions = async () => {
      try {
        const res = await api.GET("/api/discussions/", { params: {} });
        console.log("api.GET /api/discussions/ =>", res);

        // openapi-fetch returns { data, error }
        if ((res as any).error) {
          console.error("api client error:", (res as any).error);
          setError("Failed to fetch recent posts");
        } else if ((res as any).data) {
          setDiscussions((res as any).data);
        } else if (Array.isArray(res)) {
          // some clients may return raw array
          setDiscussions(res as any);
        } else {
          console.warn("Unexpected api.GET response shape", res);
          setError("Failed to fetch recent posts (unexpected response)");
        }
      } catch (err) {
        console.error("Error fetching discussions with api client:", err);
        // fallback to native fetch
        try {
          const r = await fetch("/api/discussions/");
          if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
          const data = await r.json();
          console.log("fetch fallback /api/discussions/ =>", data);
          setDiscussions(data);
        } catch (err2) {
          console.error("Fetch fallback failed:", err2);
          setError("Failed to fetch recent posts");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchDiscussions();
  }, []);


  return (
  <div className="flex flex-col items-center w-full max-w-5xl mx-auto mt-10 px-4">
      {/* Header */}
      <h1 className="text-4xl font-bold mb-2 text-center">UniVerse Feed</h1>
      <p className="text-primary/70 mb-8 text-center">
        Connect, share, and learn with fellow university students.
      </p>

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
            />
          ))
        )}
      </div>
    </div>
  );
}