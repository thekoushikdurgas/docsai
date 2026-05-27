"use client";

import Link from "next/link";
import { ExternalLink } from "lucide-react";
import { LEGACY_DOCSAI_URL } from "@/lib/config";

export function LegacyDocsaiLink({ className }: { className?: string }) {
  return (
    <Link
      href={LEGACY_DOCSAI_URL}
      target="_blank"
      rel="noopener noreferrer"
      className={className}
      title="Open full Django DocsAI console"
    >
      <ExternalLink size={14} aria-hidden />
      <span>Legacy DocsAI</span>
    </Link>
  );
}
