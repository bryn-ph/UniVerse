import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import type { components } from "@/types/api.d";
import api from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";

type Discussion = components["schemas"]["Discussion"];
type Reply = components["schemas"]["Reply"];

function formatDateTime(dateString?: string) {
  if (!dateString) return "Unknown date";
  const d = new Date(dateString);
  return `${d.getDate().toString().padStart(2, "0")}/${(d.getMonth() + 1)
    .toString()
    .padStart(2, "0")}/${d.getFullYear()} • ${d.getHours().toString().padStart(2, "0")}:${d
    .getMinutes()
    .toString()
    .padStart(2, "0")}`;
}

export default function DiscussionPage() {
  const params = useParams();
  const discussionId = (params as { id?: string }).id ?? "";
  const navigate = useNavigate();

  const { user, isLoading: authLoading } = useAuth();

  const [discussion, setDiscussion] = useState<Discussion | null>(null);
  const [replies, setReplies] = useState<Reply[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [replyText, setReplyText] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      if (!discussionId) {
        setError("No discussion id provided.");
        setLoading(false);
        return;
      }

      try {
        const { data: discData, error: discErr } = await api.GET("/api/discussions/{discussion_id}", {
          params: { path: { discussion_id: discussionId } },
        });
        if (discErr) throw discErr;
        setDiscussion(discData as Discussion);

        // Fetch replies by query (typed client)
        const { data: repliesData, error: repliesErr } = await api.GET("/api/replies/", {
          params: { query: { discussion_id: discussionId } },
        });
        if (repliesErr) throw repliesErr;
        setReplies((repliesData as Reply[]) || []);
      } catch (e) {
        console.error(e);
        setError("Failed to load discussion.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [discussionId]);

  const handleReplySubmit = async () => {
    if (!user) return setError("You must be logged in to reply.");
    if (!replyText.trim()) return;
    setSubmitting(true);
    try {
      const { data, error: postErr } = await api.POST("/api/replies/", {
        body: {
          body: replyText,
          user_id: user.id,
          discussion_id: discussionId,
        },
      });
      if (postErr) throw postErr;
      if (data) {
        setReplies((prev) => [...prev, data as Reply]);
        setReplyText("");
      }
    } catch (e) {
      console.error(e);
      setError("Failed to post reply.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p className="animate-pulse text-muted-foreground">Loading discussion...</p>
      </div>
    );
  }

  if (error || !discussion) {
    return (
      <Card className="border-destructive w-full max-w-4xl mx-auto mt-10">
        <CardContent className="py-12 text-center">
          <p className="text-destructive">{error || "Discussion not found."}</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="flex flex-col items-center w-full max-w-5xl mx-auto mt-10 px-4 space-y-6">
      <div className="w-full">
        <Button
          variant="default"
          onClick={() => navigate('/')}
          className="bg-[#234E70] text-white hover:bg-[#1d3f56]"
        >
          ← Back
        </Button>
      </div>
      <Card className="w-full">
        <CardHeader>
          <div className="space-y-2">
            <CardTitle className="text-3xl">{discussion.title}</CardTitle>
            <div className="flex items-center gap-3">
              <div className="text-sm text-muted-foreground">{discussion.author || "Unknown User"}</div>
              <div className="text-xs text-muted-foreground">•</div>
              <div className="text-xs text-muted-foreground">{formatDateTime(discussion.created_at)}</div>
              <div className="ml-4">
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-muted/40 text-muted-foreground">
                  {discussion.class_name || "Unknown Class"}
                </span>
              </div>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-base leading-relaxed text-muted-foreground">{discussion.body}</p>
        </CardContent>
      </Card>

      <Separator />

      <div className="w-full">
        <h2 className="text-2xl font-semibold mb-4">Replies</h2>

        {replies.length === 0 ? (
          <Card className="border-dashed border-2 border-muted w-full">
            <CardContent className="py-6 text-center text-muted-foreground">
              <p className="text-sm">No replies yet — be the first to reply!</p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {replies.map((r) => (
              <Card key={r.id} className="w-full">
                <CardContent>
                  <div className="flex items-start gap-4">
                    <Avatar className="h-10 w-10">
                      <AvatarImage src="" alt={r.author || "User"} />
                      <AvatarFallback>{(r.author || "U").slice(0, 2)}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <div className="text-sm font-medium">{r.author || "Unknown User"}</div>
                        <div className="text-xs text-muted-foreground">{formatDateTime(r.created_at)}</div>
                      </div>
                      <p className="mt-2 text-sm text-muted-foreground">{r.body}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Reply form */}
        <div className="mt-6">
          {authLoading ? (
            <div className="text-sm text-muted-foreground">Checking authentication...</div>
          ) : user ? (
            <Card className="w-full">
              <CardContent>
                <div className="flex items-start gap-4">
                  <Avatar className="h-10 w-10">
                    <AvatarImage src="" alt={user.name} />
                    <AvatarFallback>{user.name.slice(0, 2)}</AvatarFallback>
                  </Avatar>
                  <div className="flex-1">
                    <Textarea value={replyText} onChange={(e) => setReplyText(e.target.value)} placeholder="Write a reply..." className="mb-2" />
                    <div className="flex justify-end">
                      <Button onClick={handleReplySubmit} disabled={submitting}>
                        {submitting ? "Replying..." : "Reply"}
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card className="w-full">
              <CardContent>
                <div className="flex items-center justify-between">
                  <div className="text-sm text-muted-foreground">Please log in to reply.</div>
                  <div>
                    <Button variant="default" className="bg-[#234E70] text-white hover:bg-[#1d3f56]" onClick={() => navigate('/login')}>
                      Log in
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
