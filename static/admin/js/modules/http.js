/**
 * Thin fetch helpers for admin pages (optional ES module).
 * Import as a static file from /static/admin/js/modules/http.js when using type="module".
 */
export async function getJson(url, options = {}) {
  const res = await fetch(url, {
    credentials: "same-origin",
    headers: { Accept: "application/json", ...options.headers },
    ...options,
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export async function postJson(url, body, options = {}) {
  const res = await fetch(url, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      ...options.headers,
    },
    body: JSON.stringify(body),
    ...options,
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}
