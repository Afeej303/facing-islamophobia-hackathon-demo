import { ArrowLeft, LayoutDashboard, ShieldCheck } from "lucide-react";

export default function Navbar({ route, navigate }) {
  const isDetail = route.startsWith("/account/");
  return (
    <header className="topbar">
      <div className="topbarLeft">
        {isDetail && (
          <button className="iconButton" title="Back to dashboard" onClick={() => navigate("/")}>
            <ArrowLeft size={18} />
          </button>
        )}
        <div>
          <div className="eyebrow">Facebook monitoring demo</div>
          <h2>{route === "/shield" ? "Shield panel" : isDetail ? "Flagged comments" : "Dashboard"}</h2>
        </div>
      </div>
      <div className="topbarActions">
        <button className={route === "/" ? "navPill active" : "navPill"} onClick={() => navigate("/")}>
          <LayoutDashboard size={16} /> Dashboard
        </button>
        <button className={route === "/shield" ? "navPill active" : "navPill"} onClick={() => navigate("/shield")}>
          <ShieldCheck size={16} /> Shield
        </button>
      </div>
    </header>
  );
}
