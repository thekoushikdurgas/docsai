export function Spinner({ label = "Loading" }: { label?: string }) {
  return (
    <div className="c360-spinner-wrap" role="status" aria-label={label}>
      <span className="c360-spinner" aria-hidden />
    </div>
  );
}
