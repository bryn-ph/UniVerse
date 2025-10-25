import { useEffect, useState } from "react";
import { api, type University } from "@/lib/api";
import { Card } from "@/components/ui/card";

export function UniversityList() {
  const [universities, setUniversities] = useState<University[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadUniversities();
  }, []);

  const loadUniversities = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.universities.getAll();
      setUniversities(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load universities");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-4">Loading universities...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Universities</h2>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {universities.map((university) => (
          <Card key={university.id} className="p-4">
            <h3 className="text-lg font-semibold">{university.name}</h3>
            <div className="text-sm text-gray-600 mt-2">
              <p>{university.user_count || 0} users</p>
              <p>{university.class_count || 0} classes</p>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

