"use client";

import { useState } from "react";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { opsService } from "@/services/opsService";

export function OpsCampaignCqlClient() {
  const [query, setQuery] = useState("");
  const [target, setTarget] = useState("");
  const [parseResult, setParseResult] = useState<string>("");
  const [loading, setLoading] = useState(false);

  async function parse() {
    setLoading(true);
    try {
      const res = await opsService.cqlParse(query, target || undefined);
      const json =
        (res as { campaignSatellite?: { cqlParse?: unknown } })?.campaignSatellite
          ?.cqlParse ?? res;
      setParseResult(JSON.stringify(json, null, 2));
    } catch (e) {
      setParseResult(e instanceof Error ? e.message : "Parse failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AdminPageLayout title="Campaign CQL lab" subtitle="Parse CQL via campaign satellite">
      <div className="c360-flex c360-flex--col c360-flex--gap-4" style={{ maxWidth: 720 }}>
        <Input
          label="CQL query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <Input
          label="Target (optional)"
          value={target}
          onChange={(e) => setTarget(e.target.value)}
        />
        <Button onClick={() => void parse()} loading={loading}>
          Parse
        </Button>
        {parseResult ? (
          <pre className="c360-code-block" style={{ whiteSpace: "pre-wrap" }}>
            {parseResult}
          </pre>
        ) : null}
      </div>
    </AdminPageLayout>
  );
}
