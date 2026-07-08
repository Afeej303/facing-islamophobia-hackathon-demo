import { useEffect, useState } from "react";
import { EyeOff, MessageSquareReply, Radar, ShieldCheck } from "lucide-react";
import { getAccounts, getStats } from "../api/client.js";
import FlaggedAccountCard from "../components/FlaggedAccountCard.jsx";

const statIcons = [Radar, ShieldCheck, MessageSquareReply, EyeOff];

export default function Dashboard({ navigate }) {
  const [accounts, setAccounts] = useState([]);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    getAccounts().then(setAccounts);
    getStats().then(setStats);
  }, []);

  const statItems = stats
    ? [
        ["Total flagged today", stats.total_flagged_today],
        ["Accounts monitored", stats.accounts_monitored],
        ["Responses sent", stats.responses_sent],
        ["Comments hidden", stats.comments_hidden],
      ]
    : [];

  return (
    <section className="page">
      <div className="statGrid">
        {statItems.map(([label, value], index) => {
          const Icon = statIcons[index];
          return (
            <div className="statCard" key={label}>
              <Icon size={21} />
              <span>{label}</span>
              <strong>{value}</strong>
            </div>
          );
        })}
      </div>
      <div className="sectionTitle">
        <h2>Flagged accounts</h2>
        <p>Representative public-page data plus submitted Facebook sources pending account resolution.</p>
      </div>
      <div className="accountGrid">
        {accounts.map((account) => (
          <FlaggedAccountCard key={account.id} account={account} onView={(id) => navigate(`/account/${id}`)} />
        ))}
      </div>
    </section>
  );
}
