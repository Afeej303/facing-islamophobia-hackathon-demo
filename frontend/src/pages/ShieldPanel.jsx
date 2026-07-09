import { useEffect, useMemo, useState } from "react";
import { ExternalLink, EyeOff, Trash2, X } from "lucide-react";
import { API_LOAD_ERROR, getFacebookLoginUrl, getFacebookStatus, getShieldLog } from "../api/client.js";

export default function ShieldPanel() {
  const [log, setLog] = useState([]);
  const [modal, setModal] = useState(false);
  const [facebook, setFacebook] = useState(null);
  const [connectMessage, setConnectMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([getShieldLog(), getFacebookStatus()])
      .then(([logData, facebookData]) => {
        setLog(logData);
        setFacebook(facebookData);
        setError("");
      })
      .catch((exception) => {
        setLog([]);
        setFacebook(null);
        setError(exception.message || API_LOAD_ERROR);
      });
  }, []);

  const totals = useMemo(
    () => ({
      hidden: log.filter((item) => item.action === "hidden").length,
      deleted: log.filter((item) => item.action === "deleted").length,
    }),
    [log]
  );

  const handleConnect = async () => {
    try {
      const result = await getFacebookLoginUrl();
      if (result.configured && result.url) {
        window.open(result.url, "_blank", "noopener,noreferrer");
        setConnectMessage("Facebook opened in a new tab. Return here after approving the requested Page permissions.");
        return;
      }
      setConnectMessage(result.message || "Facebook connection is not configured yet.");
    } catch (error) {
      setConnectMessage(API_LOAD_ERROR);
    }
    setModal(true);
  };

  return (
    <section className="page">
      <div className="sectionTitle">
        <h2>Shield - Protecting Muslim voices on Facebook</h2>
        <p>Moderation actions for hateful comments on owned content.</p>
      </div>
      {error && <div className="errorBanner">{error}</div>}
      <div className="statGrid two">
        <div className="statCard">
          <EyeOff size={21} />
          <span>Comments hidden this week</span>
          <strong>{totals.hidden}</strong>
        </div>
        <div className="statCard">
          <Trash2 size={21} />
          <span>Comments deleted this week</span>
          <strong>{totals.deleted}</strong>
        </div>
      </div>
      <div className="tableWrap">
        <table>
          <thead>
            <tr>
              <th>Comment text</th>
              <th>Action</th>
              <th>Post</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {log.map((item) => (
              <tr key={item.id}>
                <td>{item.comment_text}</td>
                <td><span className={`actionBadge ${item.action}`}>{item.action}</span></td>
                <td>{item.post}</td>
                <td>{item.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="ctaBand">
        <div>
          <h3>Connect your Facebook account to enable auto-shield</h3>
          <p>
            {facebook?.connected
              ? facebook.pages?.length
                ? `${facebook.pages.length} Facebook page${facebook.pages.length === 1 ? "" : "s"} connected.`
                : `Facebook profile connected${facebook.profile?.name ? `: ${facebook.profile.name}` : "."}`
              : "Requires a Meta app with Page permissions and OAuth credentials."}
          </p>
        </div>
        <button className="primaryButton" onClick={handleConnect}>
          Connect account <ExternalLink size={17} />
        </button>
      </div>
      {facebook?.pages?.length ? (
        <div className="connectedPages">
          {facebook.pages.map((page) => (
            <span key={page.id}>{page.name}</span>
          ))}
        </div>
      ) : null}
      {facebook?.connected && facebook?.profile ? (
        <div className="connectedPages">
          <span>{facebook.profile.name || "Facebook profile connected"}</span>
        </div>
      ) : null}
      {modal && (
        <div className="modalLayer">
          <div className="modalBox">
            <button className="iconButton drawerClose" title="Close" onClick={() => setModal(false)}>
              <X size={18} />
            </button>
            <h3>Facebook credentials needed</h3>
            <p>{connectMessage}</p>
            <div className="setupList">
              <span>Add your Meta app ID and secret to the backend environment file.</span>
              <span>Use the local callback URL shown in the README as the OAuth redirect URI.</span>
              <span>Request Page list, engagement read, user content read, and engagement management permissions.</span>
            </div>
          </div>
        </div>
      )}
      {connectMessage && !modal && <div className="toast connectToast">{connectMessage}</div>}
    </section>
  );
}
