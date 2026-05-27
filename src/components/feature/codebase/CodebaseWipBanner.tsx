export function CodebaseWipBanner({ message }: { message?: string }) {
  return (
    <div
      className="c360-card"
      style={{
        padding: 16,
        marginBottom: 20,
        fontSize: "0.875rem",
        borderLeft: "4px solid var(--c360-warning, #f59e0b)",
      }}
    >
      <strong>WIP:</strong>{" "}
      {message ??
        "Scanner microservice not connected — triggers are stubs. Track in admin/TODO.md (Phase 0)."}
    </div>
  );
}
