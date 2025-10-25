import { useState } from "react";
import Modal from "./Modal";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import api from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";

interface CreateDiscussionModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  classId: string;
  onSuccess?: () => void;
}

export default function CreateDiscussionModal({
  open,
  onOpenChange,
  classId,
  onSuccess,
}: CreateDiscussionModalProps) {
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();

  if (!user) {
    return null;
  }

  const handleSubmit = async () => {
    if (!title.trim() || !body.trim() || !user) return;

    setLoading(true);
    
    const { data, error } = await api.POST("/api/discussions/", {
      body: { 
        title, 
        body, 
        user_id: user.id,
        class_id: classId 
      },
    });

    setLoading(false);

    if (error) {
      console.error("Failed to create discussion", error);
      return;
    }

    // Success - clear form and close modal
    setTitle("");
    setBody("");
    onOpenChange(false);
    onSuccess?.();
  };

  return (
    <Modal
      open={open}
      onOpenChange={onOpenChange}
      title="Create New Discussion"
      description="Start a new discussion in this class"
      footer={
        <>
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={loading}
          >
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={loading || !title.trim() || !body.trim()}>
            {loading ? "Creating..." : "Create Discussion"}
          </Button>
        </>
      }
    >
      <div className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="title">Title</Label>
          <Input
            id="title"
            placeholder="Enter discussion title..."
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="body">Description</Label>
          <Textarea
            id="body"
            placeholder="What do you want to discuss?"
            value={body}
            onChange={(e) => setBody(e.target.value)}
            rows={6}
          />
        </div>
      </div>
    </Modal>
  );
}

