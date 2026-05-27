/** User-facing errors for admin.users list (parity with Django _users_list_auth_message). */

export function usersListErrorMessage(err: unknown): string {
  const msg = err instanceof Error ? err.message : String(err);
  if (
    msg === "Authentication required" ||
    msg.includes("Authentication required")
  ) {
    return (
      "The API did not accept any signed-in user (missing or invalid JWT). " +
      "Sign out and sign in with your Contact360 email and password. " +
      "Listing users requires a Super Admin account on the gateway."
    );
  }
  if (
    msg.includes("Insufficient permissions") ||
    msg === "SuperAdmin role required"
  ) {
    return (
      "Listing users requires Super Admin on the gateway. " +
      "Ask a Super Admin to promote your account, or use a Super Admin login."
    );
  }
  if (
    msg.includes("Name or service not known") ||
    msg.includes("Network error") ||
    msg.includes("Connection refused") ||
    msg.includes("timed out") ||
    msg.includes("Timeout") ||
    msg.includes("Failed to fetch")
  ) {
    return `Failed to load users: ${msg}. Check gateway connectivity.`;
  }
  return `Failed to load users: ${msg}`;
}
