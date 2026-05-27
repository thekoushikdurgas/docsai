import { Alert } from "@/components/ui/Alert";
import Button from "@/components/ui/Button";

export function AdminEmptyState({
  title = "No data",
  message,
  onRetry,
}: {
  title?: string;
  message?: string;
  onRetry?: () => void;
}) {
  return (
    <div className="c360-flex c360-flex--col c360-flex--gap-3" style={{ padding: 24 }}>
      <Alert variant="info" title={title}>
        {message ?? "Nothing to show yet."}
      </Alert>
      {onRetry ? (
        <Button variant="outline" size="sm" onClick={onRetry}>
          Retry
        </Button>
      ) : null}
    </div>
  );
}
