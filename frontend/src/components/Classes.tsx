import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { components } from "@/types/api.d";
import api from "@/lib/api";

type Class = components["schemas"]["Class"];

export default function Classes() {
  const [classes, setClasses] = useState<Class[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchClasses = async () => {
      const { data, error: fetchError } = await api.GET("/api/classes/");
      
      if (fetchError) {
        setError("Failed to fetch classes");
        console.error("Error fetching classes:", fetchError);
      } else if (data) {
        setClasses(data);
      }
      
      setLoading(false);
    };

    fetchClasses();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <div className="animate-pulse text-muted-foreground">Loading classes...</div>
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

  if (classes.length === 0) {
    return (
      <Card className="border-dashed border-2 border-muted">
        <CardContent className="py-12 text-center text-muted-foreground">
          <p className="text-sm">No classes found — check back later!</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {classes.map((classItem) => {
        const discussionCount = typeof classItem.discussion_count === 'number' 
          ? classItem.discussion_count 
          : 0;
        
        return (
          <Link key={classItem.id} to={`/classes/${classItem.id}`}>
            <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
              <CardHeader>
                <CardTitle className="text-xl">{classItem.name}</CardTitle>
                <CardDescription className="text-sm">
                  {classItem.university || "Unknown University"}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {/* Discussion Count */}
                <div className="flex items-center text-sm text-muted-foreground">
                  <svg
                    className="w-4 h-4 mr-2"
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
                  {discussionCount} {discussionCount === 1 ? "discussion" : "discussions"}
                </div>

                {/* Tags */}
                {classItem.tags && classItem.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {classItem.tags.map((tag) => (
                      <span
                        key={tag.id}
                        className="px-2 py-1 text-xs font-medium bg-primary/10 text-primary rounded-full"
                      >
                        {tag.name}
                      </span>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </Link>
        );
      })}
    </div>
  );
}

