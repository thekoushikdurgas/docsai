/** ISO window for bulk log delete (Django `time_range_to_iso` parity). */

export function logTimeRangeToIso(
  range: string,
): { startTime: string; endTime: string } {
  const end = new Date();
  const start = new Date(end);
  switch (range) {
    case "1h":
      start.setHours(start.getHours() - 1);
      break;
    case "7d":
      start.setDate(start.getDate() - 7);
      break;
    case "30d":
      start.setDate(start.getDate() - 30);
      break;
    case "24h":
    default:
      start.setDate(start.getDate() - 1);
      break;
  }
  return { startTime: start.toISOString(), endTime: end.toISOString() };
}
