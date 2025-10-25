import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import BackButton from "@/components/BackButton";
import type { components } from "@/types/api.d";
import api from "@/lib/api";
import DiscussionCard from "@/components/DiscussionCard";
import CreateDiscussionModal from "@/components/CreateDiscussionModal";

type ClassGroup = components["schemas"]["ClassGroup"];
type Class = components["schemas"]["Class"];
type Discussion = components["schemas"]["Discussion"];

export default function ClassGroupDetails() {
  const { groupId } = useParams<{ groupId: string }>();
  const [groupData, setGroupData] = useState<ClassGroup | null>(null);
  const [discussions, setDiscussions] = useState<Discussion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [classId, setClassId] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!groupId) {
        setError("No group ID provided");
        setLoading(false);
        return;
      }

      // Fetch class group details (includes classes)
      const groupResponse = await api.GET("/api/class-groups/{group_id}", {
        params: { path: { group_id: groupId } },
      });

      const discussionsResponse = await api.GET("/api/discussions/", {
        params: { query: { class_group_id: groupId } },
      });

      if (groupResponse.error || discussionsResponse.error) {
        setError("Failed to load class group");
        setLoading(false);
        return;
      }

      setGroupData(groupResponse.data || null);
      setDiscussions(discussionsResponse.data || []);
      setLoading(false);
    };

    fetchData();
  }, [groupId]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="animate-pulse text-muted-foreground">Loading class group...</div>
      </div>
    );
  }

  if (error || !groupData) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
        <p className="text-destructive">{error || "Class group not found"}</p>
        <BackButton to="/explore" size="sm">← Back to Explore</BackButton>
      </div>
    );
  }

  const classes = (groupData.classes || []) as Class[];
  const discussionCount = discussions.length; 

  return (
    <div className="flex flex-col items-center w-full max-w-5xl mx-auto mt-10 px-4">
      {/* Back Button */}
      <div className="w-full mb-4">
        <BackButton autoBack size="sm" />
      </div>

      {/* Class Group Header */}
      <Card className="w-full mb-8">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <CardTitle className="text-3xl">{groupData.name}</CardTitle>
              {groupData.label && (
                <CardDescription className="text-lg mt-2">
                  {groupData.label}
                </CardDescription>
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Description */}
          {groupData.description && (
            <p className="text-muted-foreground">{groupData.description}</p>
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

      {/* Classes Section */}
      <div className="w-full mb-6 flex items-center justify-between">
        <h2 className="text-2xl font-bold">Discussions</h2>
        <Button onClick={() => setModalOpen(true)}>
          + Create Discussion
        </Button>
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
              groupId={groupId}
              groupName={groupData.name}
            />
          ))
        )}
      </div>

      {/* Create Discussion Modal */}
      <CreateDiscussionModal
        open={modalOpen}
        onOpenChange={setModalOpen}
        groupId={groupId!}
        onSuccess={() => {
          // Refetch discussions after creation
          window.location.reload();
        }}
      />
    </div>
  );
}

