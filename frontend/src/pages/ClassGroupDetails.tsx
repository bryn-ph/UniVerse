import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import BackButton from "@/components/BackButton";
import ClassCard from "@/components/ClassCard";
import type { components } from "@/types/api.d";
import api from "@/lib/api";

type ClassGroup = components["schemas"]["ClassGroup"];
type Class = components["schemas"]["Class"];

export default function ClassGroupDetails() {
  const { groupId } = useParams<{ groupId: string }>();
  const [groupData, setGroupData] = useState<ClassGroup | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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

      if (groupResponse.error) {
        setError("Failed to load class group");
        setLoading(false);
        return;
      }

      setGroupData(groupResponse.data || null);
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
  const classCount = typeof groupData.class_count === 'number' 
    ? groupData.class_count 
    : classes.length;

  return (
    <div className="flex flex-col items-center w-full max-w-5xl mx-auto mt-10 px-4">
      {/* Back Button */}
      <div className="w-full mb-4">
        <BackButton to="/explore" size="sm">← Back to Explore</BackButton>
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
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                />
              </svg>
              <span>{classCount} {classCount === 1 ? "class" : "classes"}</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Classes Section */}
      <div className="w-full mb-6">
        <h2 className="text-2xl font-bold">Classes in this Group</h2>
      </div>

      {/* Classes List */}
      <div className="w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {classes.length === 0 ? (
          <Card className="border-dashed border-2 border-muted col-span-full">
            <CardContent className="py-12 text-center text-muted-foreground">
              <p className="text-sm">No classes in this group yet.</p>
            </CardContent>
          </Card>
        ) : (
          classes.map((classItem) => (
            <ClassCard
              key={classItem.id}
              id={classItem.id!}
              title={classItem.name!}
              subtitle={classItem.university || "Unknown University"}
              count={typeof classItem.discussion_count === 'number' ? classItem.discussion_count : 0}
              countLabel="discussion"
              tags={classItem.tags}
              linkTo={`/classes/${classItem.id}`}
              linkState={{ 
                from: 'group',
                groupId: groupData.id,
                groupName: groupData.name 
              }}
            />
          ))
        )}
      </div>
    </div>
  );
}

