import { Alert } from "../../components/primitives";

export type SafetyNoticesProps = {
  notices: string[];
};

export function SafetyNotices({ notices }: SafetyNoticesProps) {
  return (
    <Alert
      tone="attention"
      title="Avisos de segurança científica"
      data-testid="evidence-safety-notices"
    >
      <ul className="wick-evidence-notice-list">
        {notices.map((notice) => (
          <li key={notice}>{notice}</li>
        ))}
      </ul>
    </Alert>
  );
}
