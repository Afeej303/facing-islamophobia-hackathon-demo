import { ServerCrash } from "lucide-react";

export default function InfrastructureNotice() {
  return (
    <div className="infraNotice">
      <ServerCrash size={22} />
      <div>
        <h3>Vercel cannot run the live crawler stack</h3>
        <p>
          Live Facebook monitoring needs backend services that run continuously on Linux:
          Redis, Celery workers, Celery Beat, Playwright browser workers, Prometheus,
          and Grafana. This Vercel frontend can only call their API when that Linux
          stack is deployed.
        </p>
      </div>
    </div>
  );
}
