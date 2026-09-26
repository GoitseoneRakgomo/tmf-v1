"""Thuli Madonsela Foundation website (mobile-first Flask app).
Run:  pip install -r requirements.txt && flask --app app run --debug
Sample content throughout is placeholder: replace with approved copy / a CMS."""
from flask import Flask, render_template, request, abort

app = Flask(__name__)

NAV = [("About", "/about", "/about"), ("Our work", "/our-work", "/our-work"),
       ("Insights", "/insights", "/insights"), ("Get involved", "/get-involved/events", "/get-involved"),
       ("Contact", "/contact", "/contact")]

# letter, official wording, short label, programmes, link
DARTS = [
    ("D", "Demologues", "Demologues", "Democracy Dialogues & Festivals", "/get-involved/events"),
    ("A", "Advocacy, Access", "Advocacy & Access", "Democracy4You · Law4You · access facilitation", "/our-work#a"),
    ("R", "Research", "Research", "#DGovTrends · Rule of Law Index · Promise Tracker", "/our-work/research/promise-tracker"),
    ("T", "Training and Technical Support", "Training", "EPIC Leadership · Ethics & Governance", "/our-work/training/epic-leadership"),
    ("S", "Sustainable Development Facilitation", "Sustainable Dev.", "Siyazakhela – Enterprising Communities", "/our-work#s"),
]

ARTICLES = [
    dict(slug="local-government-after-the-vote", type="commentary", title="Local government after the vote: what accountability looks like",
         standfirst="A short standfirst sets up the argument in one or two sentences before the reader commits.",
         author="Author name", date="12 September 2026", mins=6, first_published="the Sunday Times",
         body=["Sample paragraph. Set at a comfortable measure with generous line height.", "Second sample paragraph. Replace with the article body from the CMS."]),
    dict(slug="trust-deficit-report", type="research", title="The trust deficit: findings from the latest survey",
         standfirst="Research pieces carry a copy-ready citation.", author="Research team", date="8 September 2026", mins=9,
         cite="Thuli Madonsela Foundation (2026). The trust deficit. Pretoria: TMF.", body=["Sample research summary."]),
    dict(slug="dialogue-announced", type="news", title="Democracy Dialogue announced for September",
         standfirst="Registration is free and open.", author="Communications", date="5 September 2026", mins=2, body=["Sample news item."]),
    dict(slug="festival-teaser", type="multimedia", title="Festival highlights: a short film",
         standfirst="Recordings and photographs feed the archive later.", author="Media team", date="1 September 2026", mins=5, body=["Sample multimedia description."]),
]
for a in ARTICLES:
    a["url"] = f"/insights/{a['type']}/{a['slug']}"

SESSIONS = [dict(dates="23–24 Sep", place="Pretoria", seats=4), dict(dates="12–13 Nov", place="Online", seats=None)]

EVENTS = [
    dict(day="23", mon="SEP", title="Democracy Dialogue: local government after the vote", place="Pretoria · in person and streamed",
         note="Free · registration required", cta="Register", href="#", ext=False),
    dict(day="12", mon="NOV", title="EPIC Leadership two-day course", place="Pretoria · 2 days · R000 per delegate",
         note="Booking via our partner (leaves this site)", cta="Book now", href="https://booking.example.org", ext=True),
    dict(day="04", mon="DEC", title="International Democracy Festival", place="Three days · programme to be announced",
         note="Save the date", cta="Notify me", href="#", ext=False),
]

PROMISES = [
    dict(id=1, promise="Sample promise one", source="Manifesto, p. 4", sphere="National", status="Delivered"),
    dict(id=2, promise="Sample promise two", source="Manifesto, p. 9", sphere="Provincial", status="In progress"),
    dict(id=3, promise="Sample promise three", source="Speech, 2024", sphere="Local", status="Not delivered"),
    dict(id=4, promise="Sample promise four", source="Manifesto, p. 12", sphere="National", status="Delivered"),
    dict(id=5, promise="Sample promise five", source="Manifesto, p. 15", sphere="National", status="In progress"),
]

PRESETS = {"once": [100, 250, 500, 1000], "monthly": [100, 250, 500], "yearly": [500, 1000, 2500]}

ROUTES = [("general", "General enquiries", "info"), ("media", "Media and interviews", "media"),
          ("training", "Training", "training"), ("donations", "Donations and 18A", "donations")]


@app.context_processor
def shared():
    return dict(nav=NAV, darts=DARTS)


@app.route("/")
def home():
    return render_template("home.html", lead=ARTICLES[0], event=EVENTS[0])


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/about/governance")
def governance():
    return render_template("governance.html")


@app.route("/our-work")
def our_work():
    return render_template("our_work.html")


@app.route("/our-work/training/epic-leadership")
def epic():
    return render_template("epic.html", sessions=SESSIONS)


@app.route("/insights")
def insights():
    kind = request.args.get("type", "all")
    items = [a for a in ARTICLES if kind in ("all", a["type"])]
    return render_template("insights.html", items=items, kind=kind)


@app.route("/insights/<kind>/<slug>")
def article(kind, slug):
    a = next((x for x in ARTICLES if x["slug"] == slug and x["type"] == kind), None) or abort(404)
    return render_template("article.html", a=a)


@app.route("/our-work/research/promise-tracker")
def tracker():
    sphere, status = request.args.get("sphere", ""), request.args.get("status", "")
    rows = [p for p in PROMISES if (not sphere or p["sphere"] == sphere) and (not status or p["status"] == status)]
    n = len(PROMISES)
    stats = {s: round(100 * sum(p["status"] == s for p in PROMISES) / n) for s in ("Delivered", "In progress", "Not delivered")}
    return render_template("tracker.html", rows=rows, total=n, stats=stats, sphere=sphere, status=status,
                           spheres=sorted({p["sphere"] for p in PROMISES}))


@app.route("/our-work/research/promise-tracker/<int:pid>")
def promise(pid):
    p = next((x for x in PROMISES if x["id"] == pid), None) or abort(404)
    return render_template("promise.html", p=p)


@app.route("/get-involved/events")
def events():
    return render_template("events.html", events=EVENTS)


@app.route("/get-involved/donate", methods=["GET", "POST"])
def donate():
    errors, done, f = {}, None, request.form
    if request.method == "POST":
        raw = f.get("other_amount") if f.get("amount") == "other" else f.get("amount")
        try:
            amt = int(raw)
            assert amt >= 20
        except (TypeError, ValueError, AssertionError):
            amt = None
            errors["amount"] = "Enter an amount of R20 or more."
        if not f.get("email", "").strip():
            errors["email"] = "Enter your email address."
        if f.get("cert"):  # tax fields are only required, and only asked for, when a certificate is wanted
            for k in ("donor_type", "id_number", "tax_ref", "address"):
                if not f.get(k, "").strip():
                    errors[k] = "Required for a Section 18A certificate."
        if not errors:
            # TODO: hand off to the payment gateway. Never log or echo ID / tax numbers (POPIA).
            done = dict(freq=f.get("freq", "once"), amount=amt, cert=bool(f.get("cert")))
    return render_template("donate.html", presets=PRESETS, errors=errors, done=done, f=f)


@app.route("/contact")
def contact():
    return render_template("contact.html", routes=ROUTES, route=request.args.get("route", ""))

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/paia")
def paia():
    return render_template("paia.html")


@app.route("/accessibility")
def accessibility():
    return render_template("accessibility.html")

@app.route("/admin")
def admin_dashboard():
    return render_template("admin/index.html", articles_count=len(ARTICLES))


@app.route("/admin/articles")
def admin_articles():
    return render_template("admin/articles.html", articles=ARTICLES)


@app.route("/admin/donations")
def admin_donations():
    return render_template("admin/donations.html")

if __name__ == "__main__":
    app.run(debug=True)
