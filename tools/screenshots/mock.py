#!/usr/bin/env python3
"""A stand-in for the WordPress REST API, for the integration test.

    python3 Scripts/mock_wordpress.py 8881 requests.json

Speaks just enough of wp/v2 — the index, users/me, media, posts, pages, categories,
tags — to take a document from AutoPress end to end over real HTTP, checks the Basic
authentication the way WordPress does, and writes every request it got to the log file
so the test can look at what actually went over the wire.

User: tester, application password: abcd EFGH 1234 ijkl (spaces optional, as in WordPress).
"""
import base64
import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8881
LOG = sys.argv[2] if len(sys.argv) > 2 else "requests.json"
USER, PASSWORD = "tester", "abcdEFGH1234ijkl"
# As WordPress stores them: with HTML entities. One category is there from the start.
requests, next_id = [], [100]
terms = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else {"categories": {}, "tags": {}}


def new_id():
    next_id[0] += 1
    return next_id[0]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def reply(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=UTF-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def authorized(self):
        header = self.headers.get("Authorization", "")
        if not header.startswith("Basic "):
            self.reply(401, {"code": "rest_not_logged_in", "message": "You are not currently logged in.", "data": {"status": 401}})
            return False
        user, _, password = base64.b64decode(header[6:]).decode().partition(":")
        if user != USER:
            self.reply(401, {"code": "invalid_username", "message": "<strong>Error:</strong> Unknown username.", "data": {"status": 401}})
            return False
        if password.replace(" ", "") != PASSWORD:
            self.reply(401, {"code": "incorrect_password", "message": "<strong>Error:</strong> The provided password is an invalid application password.", "data": {"status": 401}})
            return False
        return True

    def handle_any(self):
        url = urlparse(self.path)
        query = parse_qs(url.query)
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        route = url.path
        entry = {"method": self.command, "path": route, "query": query,
                 "contentType": self.headers.get("Content-Type"),
                 "disposition": self.headers.get("Content-Disposition"), "bytes": len(body)}
        if (self.headers.get("Content-Type") or "").startswith("application/json") and body:
            entry["json"] = json.loads(body)
        requests.append(entry)
        with open(LOG, "w") as handle:
            json.dump(requests, handle, indent=1)

        base = f"http://localhost:{PORT}"
        if route == "/wp-json/":
            return self.reply(200, {
                "name": "Coastline Journal", "home": "https://coastline-journal.example", "url": "https://coastline-journal.example", "namespaces": ["oembed/1.0", "wp/v2"],
                "authentication": {"application-passwords": {"endpoints": {"authorization": base + "/wp-admin/authorize-application.php"}}}})
        if not route.startswith("/wp-json/wp/v2/"):
            return self.reply(404, {"code": "rest_no_route", "message": "No route was found matching the URL and request method.", "data": {"status": 404}})
        if not self.authorized():
            return
        rest = route[len("/wp-json/wp/v2/"):].strip("/")
        if rest == "users/me":
            return self.reply(200, {"id": 1, "name": "Maria Santos", "slug": "maria"})
        if rest == "users":
            return self.reply(200, [{"id": 1, "name": "Maria Santos"}, {"id": 2, "name": "João Ferreira"}, {"id": 3, "name": "Guest authors"}])
        if rest in ("posts", "pages") and self.command == "OPTIONS":
            # What a site with Yoast SEO and one plugin-registered field answers.
            return self.reply(200, {"namespace": "wp/v2", "schema": {"properties": {"meta": {"type": "object", "properties": {
                "_yoast_wpseo_title": {"type": "string"}, "_yoast_wpseo_metadesc": {"type": "string"},
                "_yoast_wpseo_focuskw": {"type": "string"}, "_internal_flag": {"type": "boolean"},
                "footnotes": {"type": "string"},
                "newspack_post_subtitle": {"type": "string", "description": "A line under the headline."}, "jetpack_publicize_message": {"type": "string", "description": "Custom message for social sharing."}}}}}})
        if rest == "media" and self.command == "POST":
            name = (self.headers.get("Content-Disposition") or "").split('filename="')[-1].rstrip('"')
            media_id = new_id()
            # Kept next to the log, so a test can look at what the picture became.
            with open(os.path.join(os.path.dirname(os.path.abspath(LOG)), f"upload-{media_id}-{name}"), "wb") as handle:
                handle.write(body)
            return self.reply(201, {"id": media_id, "source_url": f"{base}/wp-content/uploads/2026/09/{name}"})
        if rest.startswith("media/") and self.command == "POST":
            return self.reply(200, {"id": int(rest.split("/")[1]), "source_url": base + "/wp-content/uploads/x"})
        if rest in ("categories", "tags"):
            if self.command == "GET":
                wanted = (query.get("search") or query.get("slug") or [""])[0].lower()
                return self.reply(200, [{"id": i, "name": n, "count": 40 - (i % 20)} for n, i in terms[rest].items() if wanted in n.lower()])
            name = entry["json"]["name"].replace("&", "&amp;")
            if name in terms[rest]:
                return self.reply(400, {"code": "term_exists", "message": "A term with the name provided already exists with this parent.",
                                        "data": {"status": 400, "term_id": terms[rest][name]}})
            terms[rest][name] = new_id()
            return self.reply(201, {"id": terms[rest][name], "name": name})
        if rest in ("posts", "pages") and self.command == "POST":
            time.sleep(1.2)
            post_id = new_id()
            return self.reply(201, {"id": post_id, "link": f"{base}/?p={post_id}", "status": entry["json"]["status"]})
        self.reply(404, {"code": "rest_no_route", "message": "No route.", "data": {"status": 404}})

    do_GET = do_POST = do_OPTIONS = handle_any


HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
