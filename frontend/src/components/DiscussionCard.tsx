import { Link } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { components } from "@/types/api.d";

type Discussion = components["schemas"]["Discussion"];

interface DiscussionCardProps {
  discussion: Discussion;
  linkTo?: string;
}

export default function DiscussionCard({ 
  discussion, 
  linkTo 
}: DiscussionCardProps) {
  const replyCount = typeof discussion.reply_count === 'number' 
    ? discussion.reply_count 
    : (discussion.replies ? discussion.replies.length : 0);

  const discussionLink = linkTo || `/discussions/${discussion.id}`;

  // Format date consistently
  const formatDate = (dateString: string) => {
    return new Intl.DateTimeFormat("en-GB", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false,
    }).format(new Date(dateString));
  };

  return (
    <Link
      key={String(discussion.id)}
      to={discussionLink}
      className="block no-underline text-inherit"
      aria-label={`Open discussion ${discussion.title}`}
    >
      <Card className="w-full hover:shadow-sm transition-shadow">
        <CardHeader>
          <div>
            <CardTitle className="text-base font-medium">{discussion.title}</CardTitle>
            <CardDescription className="text-sm text-muted-foreground">
              {discussion.author || "Unknown User"} • {discussion.created_at
                ? formatDate(discussion.created_at)
                : "Unknown date"}
            </CardDescription>
          </div>
        </CardHeader>

        <CardContent>
          <div className="space-y-3">
            <p className="text-sm text-muted-foreground">{discussion.body}</p>
            
            {/* Bottom row with class tag and reply count */}
            <div className="flex items-center justify-between">
              {/* Course tag / badge */}
              {discussion.class_name && (
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-muted/40 text-muted-foreground">
                  {discussion.class_name}
                </span>
              )}
              
              {/* Reply count badge */}
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3v3l4-3h6a2 2 0 0 0 2-2V6z"
                  />
                </svg>
                <span>
                  {replyCount} {replyCount === 1 ? "reply" : "replies"}
                </span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
