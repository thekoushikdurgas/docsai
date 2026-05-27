export type StorageBreadcrumb = {
  label: string;
  bucket: string;
  prefix: string;
};

export function buildStorageBreadcrumbs(
  selectedBucket: string,
  prefix: string,
  userLabel: string,
): StorageBreadcrumb[] {
  if (!selectedBucket) return [];
  const crumbs: StorageBreadcrumb[] = [
    { label: "All", bucket: "", prefix: "" },
    { label: userLabel, bucket: selectedBucket, prefix: "" },
  ];
  const segments = prefix.split("/").filter(Boolean);
  for (let i = 0; i < segments.length; i++) {
    crumbs.push({
      label: segments[i]!,
      bucket: selectedBucket,
      prefix: segments.slice(0, i + 1).join("/"),
    });
  }
  return crumbs;
}
