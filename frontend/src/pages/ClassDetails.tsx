import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import type { components } from "@/types/api.d";
import api from "@/lib/api";

type Class = components["schemas"]["Class"];
type Discussion = components["schemas"]["Discussion"];

export default function ClassDetails() {
  const { classId } = useParams<{ classId: string }>();
  const [classData, setClassData] = useState<Class | null>(null);
  const [discussions, setDiscussions] = useState<Discussion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!classId) {
        setError("No class ID provided");
        setLoading(false);
        return;
      }

      // Fetch class details
      const classResponse = await api.GET("/api/classes/{class_id}", {
        params: { path: { class_id: classId } },
      });

      if (classResponse.error) {
        setError("Failed to load class");
        setLoading(false);
        return;
      }

      setClassData(classResponse.data || null);

      // Fetch discussions for this class
      const discussionsResponse = await api.GET("/api/discussions/", {
        params: {
          query: {
            class_id: classId,
          },
        },
      });

      if (discussionsResponse.error) {
        console.error("Failed to load discussions");
      } else if (discussionsResponse.data) {
        setDiscussions(discussionsResponse.data);
      }

      setLoading(false);
    };

    fetchData();
  }, [classId]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="animate-pulse text-muted-foreground">Loading class...</div>
      </div>
    );
  }

  if (error || !classData) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
        <p className="text-destructive">{error || "Class not found"}</p>
        <Link to="/explore">
          <Button variant="outline">← Back to Explore</Button>
        </Link>
      </div>
    );
  }

  const discussionCount = typeof classData.discussion_count === 'number' 
    ? classData.discussion_count 
    : discussions.length;

  return (
    <div className="flex flex-col items-center w-full max-w-5xl mx-auto mt-10 px-4">
      {/* Back Button */}
      <div className="w-full mb-4">
        <Link to="/explore">
          <Button variant="ghost" size="sm">← Back to Explore</Button>
        </Link>
      </div>

      {/* Class Header */}
      <Card className="w-full mb-8">
        <CardHeader>
          <CardTitle className="text-3xl">{classData.name}</CardTitle>
          <CardDescription className="text-lg">
            {classData.university || "Unknown University"}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Tags */}
          {classData.tags && classData.tags.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {classData.tags.map((tag) => (
                <span
                  key={tag.id}
                  className="px-3 py-1 text-sm font-medium bg-primary/10 text-primary rounded-full"
                >
                  {tag.name}
                </span>
              ))}
            </div>
          )}

          {/* Stats */}
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                />
              </svg>
              <span>{discussionCount} {discussionCount === 1 ? "discussion" : "discussions"}</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Create Discussion Button */}
      <div className="w-full mb-6 flex justify-between items-center">
        <h2 className="text-2xl font-bold">Discussions</h2>
        <Button>+ New Discussion</Button>
      </div>

      {/* Discussions List */}
      <div className="w-full space-y-4">
        {discussions.length === 0 ? (
          <Card className="border-dashed border-2 border-muted">
            <CardContent className="py-12 text-center text-muted-foreground">
              <p className="text-sm">No discussions yet — be the first to start one!</p>
            </CardContent>
          </Card>
        ) : (
          discussions.map((discussion) => {
            const replyCount = typeof discussion.reply_count === 'number' 
              ? discussion.reply_count 
              : 0;

            return (
              <Card key={discussion.id} className="hover:shadow-md transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <CardTitle className="text-xl mb-2">{discussion.title}</CardTitle>
                      <CardDescription className="line-clamp-2">
                        {discussion.body}
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between text-sm text-muted-foreground">
                    <div className="flex items-center gap-4">
                      <span>By {discussion.author || "Unknown"}</span>
                      {discussion.created_at && (
                        <span>
                          {new Date(discussion.created_at).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                        />
                      </svg>
                      <span>{replyCount} {replyCount === 1 ? "reply" : "replies"}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })
        )}
      </div>
    </div>
  );
}

