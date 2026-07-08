import { useEffect, useMemo, useState } from "react";
import { LayoutDashboard, ShieldCheck } from "lucide-react";
import Navbar from "./components/Navbar.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import AccountDetail from "./pages/AccountDetail.jsx";
import ShieldPanel from "./pages/ShieldPanel.jsx";

const getRoute = () => window.location.pathname;

export default function App() {
  const [route, setRoute] = useState(getRoute());

  useEffect(() => {
    const onPop = () => setRoute(getRoute());
    window.addEventListener("popstate", onPop);
    return () => window.removeEventListener("popstate", onPop);
  }, []);

  const navigate = (path) => {
    window.history.pushState({}, "", path);
    setRoute(path);
  };

  const page = useMemo(() => {
    if (route.startsWith("/account/")) {
      return <AccountDetail accountId={route.split("/").pop()} navigate={navigate} />;
    }
    if (route === "/shield") {
      return <ShieldPanel />;
    }
    return <Dashboard navigate={navigate} />;
  }, [route]);

  return (
    <div className="appShell">
      <aside className="sidebar">
        <div className="brandMark">IG</div>
        <div>
          <h1>IslamGuard</h1>
          <p>Counter-hate response desk</p>
        </div>
        <nav className="sideNav" aria-label="Primary">
          <button className={route === "/" ? "active" : ""} onClick={() => navigate("/")}>
            <LayoutDashboard size={18} /> Dashboard
          </button>
          <button className={route === "/shield" ? "active" : ""} onClick={() => navigate("/shield")}>
            <ShieldCheck size={18} /> Shield panel
          </button>
        </nav>
      </aside>
      <main className="mainArea">
        <Navbar route={route} navigate={navigate} />
        {page}
      </main>
    </div>
  );
}
