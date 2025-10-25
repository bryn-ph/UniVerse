import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import ClassCard from "./ClassCard";
import type { components } from "@/types/api.d";
import api from "@/lib/api";

type ClassGroup = components["schemas"]["ClassGroup"];
type ClassGroupWithDiscussions = ClassGroup & { discussionCount?: number };

export default function ClassGroups() {
  const [groups, setGroups] = useState<ClassGroupWithDiscussions[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchGroupsWithDiscussions = async () => {
      const { data: groupsData, error: groupsError } = await api.GET("/api/class-groups/");
      
      if (groupsError) {
        setError("Failed to fetch class groups");
        console.error("Error fetching class groups:", groupsError);
        setLoading(false);
        return;
      }
  
      if (groupsData) {
        // Fetch discussion counts for each group
        const groupsWithCounts = await Promise.all(
          groupsData.map(async (group) => {
            const { data: discussionsData } = await api.GET("/api/discussions/", {
              params: { query: { class_group_id: group.id } },
            });
            return {
              ...group,
              discussionCount: discussionsData?.length || 0
            } as ClassGroupWithDiscussions;
          })
        );
        setGroups(groupsWithCounts);
      }
      
      setLoading(false);
    };
  
    fetchGroupsWithDiscussions();
  }, []);
  
  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="animate-pulse text-muted-foreground">Loading class groups...</div>
      </div>
    );
  }

  if (error) {
    return (
      <Card className="border-destructive">
        <CardContent className="py-12 text-center">
          <p className="text-destructive">{error}</p>
        </CardContent>
      </Card>
    );
  }

  if (groups.length === 0) {
    return (
      <Card className="border-dashed border-2 border-muted">
        <CardContent className="py-12 text-center text-muted-foreground">
          <p className="text-sm">No class groups found — check back later!</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {groups.map((group) => (
        <ClassCard
          key={group.id}
          id={group.id!}
          title={group.name!}
          subtitle={group.label || group.description || "Class Group"}
          count={group.discussionCount || 0}
          countLabel="discussion"
          linkTo={`/class-groups/${group.id}`}
        />
      ))}
    </div>
  );
}
