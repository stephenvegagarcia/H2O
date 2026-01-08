# H2O
Satellite water shield system using orbital hot/cold cycles for radiation protection and power generation

## Routing traffic through a custom domain (qc1.dev)

If you want a friendly domain to land on this project, you can forward traffic through the qc1.dev edge and let it redirect to your deployed H2O instance or repository page.

1. Add a DNS **CNAME** record for your domain (e.g., `h2o.example.com`) that points to `qc1.dev`.
2. On your reverse proxy at qc1.dev, create a route that forwards incoming requests for `h2o.example.com` to the target you want to serve (for example, your deployed H2O service or this repository URL).
   - Example Nginx snippet:
     ```
     server {
       server_name h2o.example.com;
       location / {
         proxy_pass https://your-h2o-target.example.com; # e.g., https://github.com/stephenvegagarcia/H2O
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_set_header X-Forwarded-Proto $scheme;
       }
     }
     ```
3. Verify the forwarding with `curl -I https://h2o.example.com` and check for the expected status (e.g., `200` for a served page or `301/302` if you are intentionally redirecting).
