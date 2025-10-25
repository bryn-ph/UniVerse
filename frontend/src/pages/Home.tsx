import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import api from "@/lib/api";
import ShareMenu from "@/components/ShareMenu";
import type { components } from "@/types/api.d";

// Infer Discussion type from your OpenAPI schema
type Discussion = components["schemas"]["Discussion"];

export default function Home() {
  const [discussions, setDiscussions] = useState<Discussion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  // Share handled by reusable ShareMenu component

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
            <div key={String(post.id)} className="block no-underline text-inherit">
              <Card
                onClick={() => navigate(`/discussions/${post.id}`)}
                className="w-full hover:shadow-sm transition-shadow cursor-pointer relative"
              >
                <CardHeader className="flex items-start justify-between">
                  <div>
                    <CardTitle className="text-base font-medium">{post.title}</CardTitle>
                    <CardDescription className="text-sm text-muted-foreground">
                      {post.author || "Unknown User"} • {post.created_at
                        ? new Intl.DateTimeFormat("en-GB", {
                          day: "2-digit",
                          month: "2-digit",
                          year: "numeric",
                          hour: "2-digit",
                          minute: "2-digit",
                          hour12: false,
                        }).format(new Date(post.created_at))
                        : "Unknown date"}
                    </CardDescription>
                  </div>

                  {/* Reply count badge (top-right) */}
                  <div className="flex items-center gap-2 text-sm text-muted-foreground pl-4">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="h-5 w-5">
                      <path d="M21 6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3v3l4-3h6a2 2 0 0 0 2-2V6z" />
                    </svg>
                    <span>
                      {((post as any).reply_count ?? (post.replies ? post.replies.length : 0))}{" "}
                      {(((post as any).reply_count ?? (post.replies ? post.replies.length : 0)) === 1) ? "reply" : "replies"}
                    </span>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-start gap-4">
                    <div className="flex-1">
                      <p className="text-sm text-muted-foreground">{post.body}</p>
                      {/* Course tag / badge below the body */}
                      {post.class_name ? (
                        <div className="mt-3">
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-muted/40 text-muted-foreground">
                            {post.class_name}
                          </span>
                        </div>
                      ) : null}
                    </div>
                  </div>
                </CardContent>

                {/* Bottom-right actions (three dots menu) */}
                <div className="absolute bottom-3 right-3 flex items-end">
                  <ShareMenu path={`/discussions/${post.id}`} />
                </div>
              </Card>
            </div>
          ))
        )}
      </div>
    </div>
  );
}