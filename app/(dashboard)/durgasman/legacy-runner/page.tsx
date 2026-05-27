import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { DurgasmanLegacyRunnerFrame } from "@/components/feature/durgasman/DurgasmanLegacyRunnerFrame";
import { DurgasmanSubNav } from "@/components/feature/durgasman/DurgasmanSubNav";

export default function DurgasmanLegacyRunnerPage() {
  return (
    <AdminPageLayout
      title="Legacy API runner"
      subtitle="Full Django Postman UI"
      tabs={<DurgasmanSubNav />}
    >
      <DurgasmanLegacyRunnerFrame />
    </AdminPageLayout>
  );
}
