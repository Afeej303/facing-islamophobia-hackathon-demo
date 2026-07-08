import { Copy, ExternalLink, X } from "lucide-react";
import { useState } from "react";

export default function ResponseDrawer({ response, comment, onClose }) {
  const [suggestedReply, setSuggestedReply] = useState(response?.suggested_reply || "");
  const [toast, setToast] = useState("");

  if (!response) return null;

  const handleOpenFacebook = async () => {
    await navigator.clipboard.writeText(suggestedReply);
    window.open(comment.post_url || response.facebook_url || "https://www.facebook.com", "_blank");
    setToast("Response copied to clipboard. Paste it as your comment on Facebook.");
  };

  return (
    <div className="drawerWrap">
      <div className="drawerScrim" onClick={onClose} />
      <aside className="drawer" aria-label="Generated counter-response">
        <button className="iconButton drawerClose" title="Close" onClick={onClose}>
          <X size={18} />
        </button>
        <div className="drawerSection">
          <span className="eyebrow">Claim identified</span>
          <div className="claimBox">{response.claim_identified}</div>
        </div>
        <div className="drawerSection">
          <span className={`verdict ${response.verdict?.toLowerCase().replace(" ", "-")}`}>{response.verdict}</span>
        </div>
        <div className="drawerSection">
          <h3>Counter narrative</h3>
          <p>{response.counter_narrative}</p>
        </div>
        <div className="drawerSection">
          <h3>Sources</h3>
          <ul className="sourceList">
            {(response.sources || []).map((source) => (
              <li key={source}>{source}</li>
            ))}
          </ul>
        </div>
        <div className="drawerSection">
          <h3>Suggested reply</h3>
          <textarea value={suggestedReply} onChange={(event) => setSuggestedReply(event.target.value)} />
        </div>
        <button className="primaryButton wide" onClick={handleOpenFacebook}>
          <Copy size={17} /> Open Facebook & copy response <ExternalLink size={17} />
        </button>
        {toast && <div className="toast">{toast}</div>}
      </aside>
    </div>
  );
}
