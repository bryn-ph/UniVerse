import { useEffect, useState } from "react";
import { useParams, useLocation, Link } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import CreateDiscussionModal from "@/components/CreateDiscussionModal";
import DiscussionCard from "@/components/DiscussionCard";
import { TagList } from "@/components/Tag";
import type { components } from "@/types/api.d";
import api from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";
1
type Class = components["schemas"]["Class"];
type Discussion = components["schemas"]["Discussion"];

export default function ClassDetails() {
  const { classId } = useParams<{ classId: string }>();
  const location = useLocation();
  const [classData, setClassData] = useState<Class | null>(null);
  const [discussions, setDiscussions] = useState<Discussion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const { user } = useAuth();
  // Get navigation state (if coming from a class group)
  const state = location.state as { from?: string; groupId?: string; groupName?: string } | null;

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
    const backLink = state?.from === 'group' && state.groupId 
      ? `/class-groups/${state.groupId}`
      : "/explore";
    const backText = state?.from === 'group' && state.groupName
      ? `← Back to ${state.groupName}`
      : "← Back to Explore";

    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
        <p className="text-destructive">{error || "Class not found"}</p>
        <Link to={backLink}>
          <Button variant="outline">{backText}</Button>
        </Link>
      </div>
    );
  }

  const discussionCount = typeof classData.discussion_count === 'number' 
    ? classData.discussion_count 
    : discussions.length;

  // Determine back button text and link
  const backLink = state?.from === 'group' && state.groupId 
    ? `/class-groups/${state.groupId}`
    : "/explore";
  const backText = state?.from === 'group' && state.groupName
    ? `← Back to ${state.groupName}`
    : "← Back to Explore";

  return (
    <div className="flex flex-col items-center w-full max-w-5xl mx-auto mt-10 px-4 ">
      {/* Back Button */}
      <div className="w-full mb-4">
        <Link to={backLink}>
          <Button variant="ghost" size="sm">{backText}</Button>
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
          <TagList tags={classData.tags || []} variant="primary" />

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
        <Button disabled={!user} onClick={() => setModalOpen(true)}>+ New Discussion</Button>
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
          discussions.map((discussion) => (
            <DiscussionCard
              key={discussion.id}
              discussion={discussion}
            />
          ))
        )}
      </div>

      {/* Create Discussion Modal */}
      {classId && (
        <CreateDiscussionModal
          open={modalOpen}
          onOpenChange={setModalOpen}
          classId={classId}
          onSuccess={() => {
            // Refetch discussions after creation
            window.location.reload();
          }}
        />
      )}
    </div>
  );
}

