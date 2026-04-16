# Optional: align `go.mod` with GitHub `emailapis`

- **Current module:** `github.com/ayan/emailapigo` ([`EC2/email.server/go.mod`](../../../../EC2/email.server/go.mod))
- **Example remote:** `https://github.com/thekoushikdurgas/emailapis.git`

Renaming the module only affects `import` strings and tooling (`go get`). Deployed binaries are unaffected if built from the local tree. Perform a repo-wide find/replace in **`EC2/email.server`** and run `go test ./...` before merging.
