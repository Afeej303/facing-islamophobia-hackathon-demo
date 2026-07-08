import { ArrowDown, ArrowRight, ArrowUp, ExternalLink, MessageSquare } from "lucide-react";
import ThreatBadge from "./ThreatBadge.jsx";

const trendIcon = {
  rising: <ArrowUp size={16} />,
  stable: <ArrowRight size={16} />,
  falling: <ArrowDown size={16} />,
};

export default function FlaggedAccountCard({ account, onView }) {
  const followerText =
    typeof account.followers === "number" ? `${account.followers.toLocaleString()} followers` : "Account pending";

  return (
    <article className="card accountCard">
      <div className="cardHeader">
        <div>
          <h3>{account.name}</h3>
          <span className="platformBadge">{account.platform}</span>
          {account.source_status && <span className="sourceStatus">{account.source_status}</span>}
        </div>
        <a className="iconButton" title="Open page" href={account.page_url} target="_blank" rel="noreferrer">
          <ExternalLink size={17} />
        </a>
      </div>
      <div className="accountMeta">
        <span>{followerText}</span>
        <span><MessageSquare size={15} /> {account.flagged_comments} flagged</span>
      </div>
      <ThreatBadge score={account.threat_score} />
      <div className="chips">
        {account.primary_narratives.map((item) => (
          <span key={item}>{item}</span>
        ))}
      </div>
      <div className="cardFooter">
        <span className={`trend ${account.trend}`}>{trendIcon[account.trend]} {account.trend}</span>
        <span>{account.last_active}</span>
      </div>
      <button className="primaryButton" onClick={() => onView(account.id)}>
        {account.source_status ? "Review source" : "View comments"}
      </button>
    </article>
  );
}
