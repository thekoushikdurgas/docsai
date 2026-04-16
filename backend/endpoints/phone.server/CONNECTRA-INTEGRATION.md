# Connectra (sync.server) usage

The **email finder** pipeline in this codebase may call Connectra **`POST /contacts/`** via [`internal/clients/connectra_client.go`](../../../../EC2/phone.server/internal/clients/connectra_client.go) when **`CONNECTRA_BASE_URL`** and **`CONNECTRA_API_KEY`** are set.

If you deploy phone.server **without** finder features, you may omit Connectra; document your env accordingly.
