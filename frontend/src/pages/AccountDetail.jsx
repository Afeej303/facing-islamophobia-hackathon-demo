import { useEffect, useState } from "react";
import { analyzeComment, getComments } from "../api/client.js";
import CommentCard from "../components/CommentCard.jsx";
import ResponseDrawer from "../components/ResponseDrawer.jsx";

export default function AccountDetail({ accountId }) {
  const [comments, setComments] = useState([]);
  const [selectedComment, setSelectedComment] = useState(null);
  const [response, setResponse] = useState(null);
  const [loadingId, setLoadingId] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    getComments(accountId).then(setComments);
  }, [accountId]);

  const handleAnalyze = async (comment) => {
    setLoadingId(comment.id);
    setSelectedComment(comment);
    setError("");
    try {
      const result = await analyzeComment({
        comment_text: comment.text,
        claim_key: comment.claim_key,
        language: "english",
      });
      setResponse(result);
    } catch (exception) {
      setError("Could not generate a response. Make sure the backend is running, then try again.");
    } finally {
      setLoadingId("");
    }
  };

  return (
    <section className="page">
      <div className="sectionTitle">
        <h2>Flagged comments</h2>
        <p>Select a comment to generate a calm, sourced counter-response.</p>
      </div>
      {error && <div className="errorBanner">{error}</div>}
      <div className="commentList">
        {comments.map((comment) => (
          <CommentCard
            key={comment.id}
            comment={comment}
            loading={loadingId === comment.id}
            onAnalyze={handleAnalyze}
          />
        ))}
      </div>
      <ResponseDrawer response={response} comment={selectedComment || {}} onClose={() => setResponse(null)} />
    </section>
  );
}
