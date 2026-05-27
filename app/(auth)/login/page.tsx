"use client";

import { useAuth } from "@/context/AuthContext";
import { useAuthRedirect } from "@/hooks/useAuthRedirect";
import { useLoginForm } from "@/hooks/useLoginForm";
import { AuthBrandHeader } from "@/components/feature/auth/AuthBrandHeader";
import { AuthLoginForm } from "@/components/feature/auth/AuthLoginForm";

export default function LoginPage() {
  useAuthRedirect();

  const { login } = useAuth();
  const loginForm = useLoginForm({ login });

  return (
    <div className="c360-auth-card" suppressHydrationWarning>
      <AuthBrandHeader subtitle="Admin Console — Sign in to your account" />
      <AuthLoginForm form={loginForm} />
    </div>
  );
}
