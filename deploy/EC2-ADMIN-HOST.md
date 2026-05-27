# Admin EC2 — dedicated host (`18.207.217.168`)

Production operator UI at **`https://admin.contact360.io`**. Next.js listens on **`127.0.0.1:3000`**; nginx terminates TLS on **443**.

## Prerequisites

- Ubuntu EC2 with security group: **22**, **80**, **443** inbound
- DNS: `admin.contact360.io` → `18.207.217.168` (**proxied** in Cloudflare)
- Cloudflare SSL: **Full (strict)**; Origin CA installed (see [`contact360.io/cloundflare/ssl/README.md`](../../cloundflare/ssl/README.md))

## One-time server setup

```bash
# On 18.207.217.168 as ubuntu
git clone <your-repo-url> ~/contact360-admin
cd ~/contact360-admin/contact360.io/admin   # monorepo layout — or admin-only repo root

sudo bash deploy/ec2-setup.sh

sudo mkdir -p /etc/nginx/ssl/cloudflare
sudo chmod 700 /etc/nginx/ssl/cloudflare
# Install contact360.io-origin.pem and contact360.io-origin.key (scp or install-cloudflare-origin-cert.sh)

cp .env.production.example .env.production
# Edit: NEXT_PUBLIC_API_URL, NEXT_PUBLIC_GRAPHQL_URL, PORT=3000

bash deploy/ec2-deploy.sh

sudo cp deploy/ec2-nginx-admin.conf /etc/nginx/sites-available/admin
sudo ln -sf /etc/nginx/sites-available/admin /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

pm2 save
```

## Cloudflare DNS

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| A | `admin` | `18.207.217.168` | Proxied (orange) |

Verify: `nslookup admin.contact360.io` returns Cloudflare anycast IPs, not the origin IP.

## GitHub Actions secrets

| Secret / variable | Value |
|-------------------|-------|
| `EC2_ADMIN_HOST` (preferred) or `EC2_HOST` | `18.207.217.168` |
| `EC2_USER` | `ubuntu` |
| `EC2_SSH_KEY` | Deploy private key |
| `NEXT_PUBLIC_API_URL` | `https://api.contact360.io` |
| `NEXT_PUBLIC_GRAPHQL_URL` | `https://api.contact360.io/graphql` |
| `vars.EC2_ADMIN_PATH` | `/home/ubuntu/contact360-admin/contact360.io/admin` (adjust to clone layout) |

Workflow: `.github/workflows/deploy-contact360-admin.yml` uses `EC2_ADMIN_HOST` when set, else `EC2_HOST`.

## Verify

```bash
pm2 list
curl -sf http://127.0.0.1:3000/login
curl -I https://admin.contact360.io/login
```

## Updates

```bash
cd ~/contact360-admin/contact360.io/admin
bash deploy/ec2-update.sh
# or push to main → GitHub Actions runs ec2-github-deploy.sh
```

## Decommission old admin origin

If `admin.contact360.io` previously pointed at Django (`contact360.io/1`, legacy EC2 e.g. `34.201.10.84`) or another host:

1. Smoke-test this host (`curl -sf http://127.0.0.1:3000/login`, `curl -I https://admin.contact360.io/login`).
2. Point Cloudflare A record to `18.207.217.168` (proxied).
3. On the old host: disable nginx vhost for `admin.contact360.io`, stop `gunicorn` / PM2 for Django admin.
4. See [`docs/runbooks/decommission-django-docsai.md`](../../../docs/runbooks/decommission-django-docsai.md).
