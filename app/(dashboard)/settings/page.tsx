"use client";

import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";
import Button from "@/components/ui/Button";
import { GRAPHQL_URL } from "@/lib/config";

export default function SettingsPage() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <AdminPageLayout title="Settings" subtitle="Admin console preferences">
      <dl className="c360-dl">
        <dt>GraphQL endpoint</dt>
        <dd>
          <code>{GRAPHQL_URL}</code>
        </dd>
        <dt>Signed in as</dt>
        <dd>{user?.email}</dd>
        <dt>Role</dt>
        <dd>{user?.profile?.role ?? user?.role ?? "—"}</dd>
        <dt>Theme</dt>
        <dd>{theme}</dd>
      </dl>
      <div className="c360-flex c360-flex--gap-2" style={{ marginTop: 24 }}>
        <Button variant="secondary" onClick={toggleTheme}>
          Toggle theme
        </Button>
        <Button variant="outline" onClick={() => logout()}>
          Sign out
        </Button>
      </div>
    </AdminPageLayout>
  );
}
