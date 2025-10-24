import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export default function Home() {
  const [newPost, setNewPost] = useState("");

  const handlePost = () => {
    // TODO: send post to backend
    console.log("Submitting post:", newPost);
    setNewPost("");
  };

  return (
    <div className="flex flex-col items-center w-full max-w-2xl mx-auto mt-10 px-4">
      {/* Header */}
      <h1 className="text-4xl font-bold mb-2 text-center">UniVerse Feed</h1>
      <p className="text-primary/70 mb-8 text-center">
        Connect, share, and learn with fellow university students.
      </p>

      {/* Create Post Section */}
      <Card className="w-full mb-6">
        <CardHeader>
          <CardTitle className="text-lg">Create a post</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Textarea
            placeholder="What's on your mind?"
            value={newPost}
            onChange={(e) => setNewPost(e.target.value)}
          />
          <div className="flex justify-end">
            <Button onClick={handlePost}>Post</Button>
          </div>
        </CardContent>
      </Card>

      {/* Feed Container */}
      <div className="space-y-4 w-full">
        {/* Empty state placeholder */}
        <Card className="w-full border-dashed border-2 border-muted">
          <CardContent className="py-12 text-center text-muted-foreground">
            <p className="text-sm">No posts yet — be the first to share something!</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
