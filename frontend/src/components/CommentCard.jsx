import { Loader2, MessageCircle, ThumbsUp } from "lucide-react";

export default function CommentCard({ comment, loading, onAnalyze }) {
  const truncated = comment.text.length > 120 ? `${comment.text.slice(0, 120)}...` : comment.text;
  return (
    <article className="card commentCard">
      <div className="commentTop">
        <div>
          <h3>{comment.author}</h3>
          <p>{truncated}</p>
        </div>
        <span className={`severity ${comment.severity}`}>{comment.severity}</span>
      </div>
      <div className="commentMeta">
        <span><ThumbsUp size={15} /> {comment.likes}</span>
        <span><MessageCircle size={15} /> {comment.timestamp}</span>
      </div>
      <button className="primaryButton" disabled={loading} onClick={() => onAnalyze(comment)}>
        {loading ? <Loader2 className="spin" size={17} /> : null}
        Generate counter-response
      </button>
    </article>
  );
}
