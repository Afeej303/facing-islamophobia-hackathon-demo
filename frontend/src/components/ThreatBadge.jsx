export default function ThreatBadge({ score }) {
  const tone = score > 80 ? "danger" : score >= 60 ? "warning" : "success";
  return (
    <div className="threatBlock">
      <div className="threatHeader">
        <span>Threat score</span>
        <strong className={tone}>{score}</strong>
      </div>
      <div className="meter">
        <div className={`meterFill ${tone}`} style={{ width: `${score}%` }} />
      </div>
    </div>
  );
}
