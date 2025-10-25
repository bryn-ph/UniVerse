import { useState, useEffect } from "react";
import Modal from "./Modal";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import api from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";
import type { components } from "@/types/api.d";

type Tag = components["schemas"]["TagMini"];

interface CreateClassModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess?: () => void;
}

export default function CreateClassModal({
  open,
  onOpenChange,
  onSuccess,
}: CreateClassModalProps) {
  const [name, setName] = useState("");
  const [tagIds, setTagIds] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [tags, setTags] = useState<Tag[]>([]);
  const [isLoadingData, setIsLoadingData] = useState(false);
  const { user } = useAuth();

  // Fetch universities, class groups, and tags when modal opens
  useEffect(() => {
    if (open) {
      fetchData();
    }
  }, [open]);

  const fetchData = async () => {
    setIsLoadingData(true);
    
    try {
      // Fetch tags
      const tagsResponse = await api.GET("/api/tags/");
      if (tagsResponse.data) {
        setTags(tagsResponse.data);
      }
    } catch (error) {
      console.error("Failed to fetch data:", error);
    } finally {
      setIsLoadingData(false);
    }
  };

  if (!user) {
    return null;
  }

  const handleSubmit = async () => {
    if (!name.trim() || !user || !user.university_id) return;

    setLoading(true);
    
    const { data, error } = await api.POST("/api/classes/", {
      body: { 
        name: name.trim(),
        university_id: user.university_id,
        tag_ids: tagIds.length > 0 ? tagIds : undefined
      },
    });

    setLoading(false);

    if (error) {
      console.error("Failed to create class", error);
      return;
    }

    // Success - clear form and close modal
    setName("");
    setTagIds([]);
    onOpenChange(false);
    onSuccess?.();
  };

  const handleTagToggle = (tagId: string) => {
    setTagIds(prev => 
      prev.includes(tagId) 
        ? prev.filter(id => id !== tagId)
        : [...prev, tagId]
    );
  };

  return (
    <Modal
      open={open}
      onOpenChange={onOpenChange}
      title="Create New Class"
      description="Add a new class to your university"
      footer={
        <>
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={loading}
          >
            Cancel
          </Button>
          <Button 
            onClick={handleSubmit} 
            disabled={loading || !name.trim() || !user?.university_id || isLoadingData}
          >
            {loading ? "Creating..." : "Create Class"}
          </Button>
        </>
      }
    >
      <div className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="name">Class Name</Label>
          <Input
            id="name"
            placeholder="e.g., Introduction to Computer Science"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="university">University</Label>
          <Input
            id="university"
            value={user?.university || "Unknown University"}
            disabled
            className="bg-muted"
          />
        </div>

        <div className="space-y-2">
          <Label>Tags (Optional)</Label>
          <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
            {tags.map((tag) => (
              <Button
                key={tag.id}
                variant={tagIds.includes(tag.id as string) ? "default" : "outline"}
                size="sm"
                onClick={() => handleTagToggle(tag.id as string)}
                className="text-xs"
              >
                {tag.name}
              </Button>
            ))}
          </div>
          {tags.length === 0 && !isLoadingData && (
            <p className="text-sm text-muted-foreground">No tags available</p>
          )}
        </div>
      </div>
    </Modal>
  );
}
