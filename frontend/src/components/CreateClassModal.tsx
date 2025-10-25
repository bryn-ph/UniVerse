import { useState, useEffect } from "react";
import Modal from "./Modal";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import api from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";
import type { components } from "@/types/api.d";

type University = components["schemas"]["University"];
type ClassGroup = components["schemas"]["ClassGroup"];
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
  const [universityId, setUniversityId] = useState("");
  const [classGroupId, setClassGroupId] = useState("");
  const [tagIds, setTagIds] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [universities, setUniversities] = useState<University[]>([]);
  const [classGroups, setClassGroups] = useState<ClassGroup[]>([]);
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
      // Fetch universities
      const universitiesResponse = await api.GET("/api/universities/");
      if (universitiesResponse.data) {
        setUniversities(universitiesResponse.data);
      }

      // Fetch class groups
      const classGroupsResponse = await api.GET("/api/class-groups/");
      if (classGroupsResponse.data) {
        setClassGroups(classGroupsResponse.data);
      }

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
    if (!name.trim() || !universityId || !classGroupId || !user) return;

    setLoading(true);
    
    const { data, error } = await api.POST("/api/classes/", {
      body: { 
        name: name.trim(),
        university_id: universityId,
        class_group_id: classGroupId,
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
    setUniversityId("");
    setClassGroupId("");
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
            disabled={loading || !name.trim() || !universityId || !classGroupId || isLoadingData}
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
          <Select value={universityId} onValueChange={setUniversityId} disabled={isLoadingData}>
            <SelectTrigger>
              <SelectValue placeholder={isLoadingData ? "Loading..." : "Select university"} />
            </SelectTrigger>
            <SelectContent>
              {universities.map((uni) => (
                <SelectItem key={uni.id} value={uni.id as string}>
                  {uni.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="classGroup">Class Group</Label>
          <Select value={classGroupId} onValueChange={setClassGroupId} disabled={isLoadingData}>
            <SelectTrigger>
              <SelectValue placeholder={isLoadingData ? "Loading..." : "Select class group"} />
            </SelectTrigger>
            <SelectContent>
              {classGroups.map((group) => (
                <SelectItem key={group.id} value={group.id as string}>
                  {group.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
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
