"""Thuli Madonsela Foundation website (mobile-first Flask app).
Run:  pip install -r requirements.txt && flask --app app run --debug
Sample content throughout is placeholder: replace with approved copy / a CMS."""
from datetime import date
from flask import Flask, render_template, request, abort, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-string"

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

for a in ARTICLES:
    a.setdefault("status", "published")
    a.setdefault("colour", "teal")
    a.setdefault("image_url", "")
    a.setdefault("link_url", "")

# ------------------------------------------------------------------
# PROGRAMMES — events and courses combined
# kind = "event" | "course"
# ------------------------------------------------------------------
PROGRAMMES = [
    # ---------- EVENTS ----------
    dict(
        id=1, slug="democracy-dialogue-local-government",
        kind="event",
        category="talk",
        title="Democracy Dialogue: local government after the vote",
        standfirst="A discussion on accountability and service delivery after the municipal elections.",
        body="Full description of the event goes here. Replace with approved copy from the CMS.",
        date="2026-09-23", end_date="2026-09-23",
        time="09:00 – 12:30",
        place="Pretoria · in person and streamed",
        venue="TMF Offices, Waterkloof Glen",
        price=0, price_label="Free",
        capacity=120, registered=87,
        register_url="#",
        image_url="",
        colour="teal",
        status="published",
        featured=True,
        facilitator="", format="", duration="", outline="", outcomes="", sessions=[],
    ),
    dict(
        id=2, slug="epic-leadership-november",
        kind="course",
        category="educational",
        title="EPIC Leadership two-day course",
        standfirst="Ethical, Purpose-Driven, Impact-Conscious, Committed to Serve leadership training.",
        body="Full description of the course goes here.",
        date="2026-11-12", end_date="2026-11-13",
        time="08:30 – 16:30 both days",
        place="Pretoria · in person",
        venue="TMF Offices, Waterkloof Glen",
        price=4500, price_label="R4,500 per delegate",
        capacity=30, registered=12,
        register_url="https://booking.example.org",
        image_url="",
        colour="deep",
        status="published",
        featured=False,
        facilitator="Prof. Thuli Madonsela",
        format="In-person",
        duration="2 days",
        outline="Module 1: Ethics. Module 2: Purpose. Module 3: Impact. Module 4: Service.",
        outcomes="By the end of this course, participants will be able to...",
        sessions=[
            dict(dates="23–24 Sep 2026", place="Pretoria", seats=4),
            dict(dates="12–13 Nov 2026", place="Online", seats=None),
        ],
    ),
    dict(
        id=3, slug="international-democracy-festival",
        kind="event",
        category="summit",
        title="International Democracy Festival",
        standfirst="Three days of dialogue, art, and civic action.",
        body="Full description of the festival goes here.",
        date="2026-12-04", end_date="2026-12-06",
        time="All day",
        place="Three days · programme to be announced",
        venue="To be confirmed",
        price=0, price_label="Free entry",
        capacity=500, registered=134,
        register_url="#",
        image_url="",
        colour="burg",
        status="published",
        featured=True,
        facilitator="", format="", duration="", outline="", outcomes="", sessions=[],
    ),
    dict(
        id=4, slug="annual-fundraising-gala",
        kind="event",
        category="fundraising",
        title="Annual Fundraising Gala",
        standfirst="An evening of giving in support of civic education programmes.",
        body="Full description of the gala goes here.",
        date="2026-10-18", end_date="2026-10-18",
        time="18:30 – 22:30",
        place="Johannesburg · black tie",
        venue="Sandton Convention Centre",
        price=2500, price_label="R2,500 per seat",
        capacity=200, registered=45,
        register_url="#",
        image_url="",
        colour="gold",
        status="published",
        featured=False,
        facilitator="", format="", duration="", outline="", outcomes="", sessions=[],
    ),
    dict(
        id=5, slug="ethics-governance",
        kind="course",
        category="educational",
        title="Ethics and Governance",
        standfirst="A short course for public servants and civic leaders.",
        body="Full course description.",
        date="2026-10-01", end_date="2026-10-30",
        time="Part-time",
        place="Online",
        venue="",
        price=2500, price_label="R2,500 per delegate",
        capacity=50, registered=18,
        register_url="https://booking.example.org",
        image_url="",
        colour="forest",
        status="published",
        featured=False,
        facilitator="TMF Faculty",
        format="Online",
        duration="4 weeks, part-time",
        outline="",
        outcomes="",
        sessions=[
            dict(dates="1 Oct – 30 Oct 2026", place="Online", seats=None),
        ],
    ),
    dict(
        id=6, slug="community-organising",
        kind="course",
        category="educational",
        title="Community Organising for Democracy",
        standfirst="Practical skills for civic movements.",
        body="Full course description.",
        date="2026-11-01", end_date="2026-12-15",
        time="Part-time",
        place="Hybrid",
        venue="",
        price=0, price_label="Free",
        capacity=40, registered=0,
        register_url="#",
        image_url="",
        colour="teal",
        status="draft",
        featured=False,
        facilitator="TMF Faculty",
        format="Hybrid",
        duration="6 weeks",
        outline="",
        outcomes="",
        sessions=[],
    ),
]

# Defaults loop for programmes
for p in PROGRAMMES:
    p.setdefault("status", "published")
    p.setdefault("colour", "teal")
    p.setdefault("image_url", "")
    p.setdefault("featured", False)
    p.setdefault("sessions", [])

# Categories for filtering (events only)
EVENT_CATEGORIES = [
    ("talk", "Talks & Dialogues"),
    ("summit", "Summits"),
    ("educational", "Educational Events"),
    ("fundraising", "Fundraising"),
]

SUBSCRIBERS = [
    dict(id=1, email="thabo@example.com", name="Thabo Mokoena", source="homepage",
         status="active", subscribed_at="2026-09-20", interests="insights,events"),
    dict(id=2, email="nomsa@example.com", name="Nomsa Dlamini", source="insights",
         status="active", subscribed_at="2026-09-18", interests="insights"),
    dict(id=3, email="info@acme.co.za", name="Acme Corporation", source="donate",
         status="active", subscribed_at="2026-09-15", interests="insights,events,courses"),
    dict(id=4, email="old@example.com", name="Former Subscriber", source="homepage",
         status="unsubscribed", subscribed_at="2026-08-01", interests="insights"),
    dict(id=5, email="bounce@example.com", name="Bounced Email", source="events",
         status="bounced", subscribed_at="2026-07-12", interests="events"),
]

PROMISES = [
    dict(id=1, promise="Sample promise one", source="Manifesto, p. 4", sphere="National", status="Delivered"),
    dict(id=2, promise="Sample promise two", source="Manifesto, p. 9", sphere="Provincial", status="In progress"),
    dict(id=3, promise="Sample promise three", source="Speech, 2024", sphere="Local", status="Not delivered"),
    dict(id=4, promise="Sample promise four", source="Manifesto, p. 12", sphere="National", status="Delivered"),
    dict(id=5, promise="Sample promise five", source="Manifesto, p. 15", sphere="National", status="In progress"),
]

DONATIONS = [
    dict(id=1, donor_name="Thabo Mokoena", donor_email="thabo@example.com", category="individual",
         amount=500, frequency="once", date="2026-09-20", certificate=False),
    dict(id=2, donor_name="Department of Justice", donor_email="finance@justice.gov.za", category="government",
         amount=25000, frequency="once", date="2026-09-18", certificate=True),
    dict(id=3, donor_name="Acme Corporation", donor_email="csi@acme.co.za", category="corporate",
         amount=10000, frequency="yearly", date="2026-09-15", certificate=True),
    dict(id=4, donor_name="Anonymous", donor_email="", category="anonymous",
         amount=250, frequency="monthly", date="2026-09-12", certificate=False),
    dict(id=5, donor_name="Nomsa Dlamini", donor_email="nomsa@example.com", category="individual",
         amount=100, frequency="monthly", date="2026-09-10", certificate=False),
    dict(id=6, donor_name="Open Society Foundation", donor_email="grants@osf.org", category="ngo",
         amount=50000, frequency="once", date="2026-09-05", certificate=True),
]


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text


PRESETS = {"once": [100, 250, 500, 1000], "monthly": [100, 250, 500], "yearly": [500, 1000, 2500]}

ROUTES = [("general", "General enquiries", "info"), ("media", "Media and interviews", "media"),
          ("training", "Training", "training"), ("donations", "Donations and 18A", "donations")]


@app.context_processor
def shared():
    return dict(nav=NAV, darts=DARTS)


# ---------- Public routes ----------

@app.route("/")
def home():
    published_events = [p for p in PROGRAMMES if p["kind"] == "event" and p.get("status") == "published"]
    event = sorted(published_events, key=lambda e: e["date"])[0] if published_events else None
    return render_template("home.html", lead=ARTICLES[0], event=event)


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
    # Find the EPIC Leadership course in PROGRAMMES
    course = next((p for p in PROGRAMMES if p["slug"] == "epic-leadership"), None)
    sessions = course["sessions"] if course else []
    return render_template("epic.html", sessions=sessions)


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
    kind = request.args.get("kind", "event")
    cat = request.args.get("cat", "")
    items = [p for p in PROGRAMMES if p["kind"] == kind and p.get("status") == "published"]
    if cat:
        items = [p for p in items if p.get("category") == cat]
    return render_template("events.html", events=sorted(items, key=lambda p: p["date"]),
                           categories=EVENT_CATEGORIES, kind=kind, cat=cat)


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
        if f.get("cert"):
            for k in ("donor_type", "id_number", "tax_ref", "address"):
                if not f.get(k, "").strip():
                    errors[k] = "Required for a Section 18A certificate."
        if not errors:
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


# ---------- Admin: Dashboard ----------

@app.route("/admin")
def admin_dashboard():
    total_revenue = sum(d["amount"] for d in DONATIONS)
    donor_count = len({d["donor_email"] for d in DONATIONS if d["donor_email"]})
    by_cat = {}
    for d in DONATIONS:
        c = d["category"]
        by_cat.setdefault(c, {"count": 0, "total": 0})
        by_cat[c]["count"] += 1
        by_cat[c]["total"] += d["amount"]
    top_cat = max(by_cat, key=lambda k: by_cat[k]["count"]) if by_cat else None
    top_cat_count = by_cat[top_cat]["count"] if top_cat else 0

    published_insights = [a for a in ARTICLES if a.get("status") == "published"]
    draft_insights = [a for a in ARTICLES if a.get("status") == "draft"]

    published_programmes = [p for p in PROGRAMMES if p.get("status") == "published"]
    draft_programmes = [p for p in PROGRAMMES if p.get("status") == "draft"]
    published_events = [p for p in published_programmes if p["kind"] == "event"]
    published_courses = [p for p in published_programmes if p["kind"] == "course"]
    draft_events = [p for p in draft_programmes if p["kind"] == "event"]
    draft_courses = [p for p in draft_programmes if p["kind"] == "course"]
    today_str = date.today().isoformat()
    upcoming_events = [p for p in published_events if p["date"] >= today_str]

    active_subscribers = [s for s in SUBSCRIBERS if s["status"] == "active"]

    attention_items = []
    if draft_insights:
        attention_items.append({
            "text": f"{len(draft_insights)} draft insight{'s' if len(draft_insights) != 1 else ''} to publish",
            "url": "/admin/insights",
        })
    if draft_programmes:
        attention_items.append({
            "text": f"{len(draft_programmes)} draft programme{'s' if len(draft_programmes) != 1 else ''} to publish",
            "url": "/admin/programmes",
        })
    large_gifts = [d for d in DONATIONS if d["amount"] >= 25000]
    if large_gifts:
        attention_items.append({
            "text": f"{len(large_gifts)} large gift{'s' if len(large_gifts) != 1 else ''} to review",
            "url": "/admin/donations",
        })
    soon = [e for e in upcoming_events if e["date"] <= "2026-10-01"]
    if soon:
        attention_items.append({
            "text": f"{len(soon)} event{'s' if len(soon) != 1 else ''} within 7 days",
            "url": "/admin/programmes",
        })

    return render_template(
        "admin/index.html",
        today=date.today().strftime("%A, %d %B %Y"),
        total_donations_count=len(DONATIONS),
        total_revenue=total_revenue,
        donor_count=donor_count,
        top_category=top_cat,
        top_category_count=top_cat_count,
        recent_donations=sorted(DONATIONS, key=lambda d: d["date"], reverse=True)[:5],
        published_insights_count=len(published_insights),
        draft_insights_count=len(draft_insights),
        recent_insights=sorted(ARTICLES, key=lambda a: a.get("date", ""), reverse=True)[:5],
        published_events_count=len(published_events),
        upcoming_events_count=len(upcoming_events),
        recent_events=sorted(upcoming_events, key=lambda e: e["date"])[:3],
        published_courses_count=len(published_courses),
        draft_courses_count=len(draft_courses),
        total_subscribers_count=len(SUBSCRIBERS),
        active_subscribers_count=len(active_subscribers),
        attention_items=attention_items,
    )


# ---------- Admin: Donations ----------

@app.route("/admin/donations")
def admin_donations():
    total_revenue = sum(d["amount"] for d in DONATIONS)
    avg = round(total_revenue / len(DONATIONS)) if DONATIONS else 0
    by_cat = {}
    for d in DONATIONS:
        c = d["category"]
        by_cat.setdefault(c, {"count": 0, "total": 0})
        by_cat[c]["count"] += 1
        by_cat[c]["total"] += d["amount"]
    return render_template(
        "admin/donations.html",
        donations=sorted(DONATIONS, key=lambda d: d["date"], reverse=True),
        total_revenue=total_revenue,
        avg_donation=avg,
        by_category=by_cat,
    )


# ---------- Admin: Insights ----------

@app.route("/admin/insights")
def admin_insights():
    return render_template("admin/insights.html", insights=ARTICLES)


@app.route("/admin/insights/new", methods=["GET", "POST"])
def admin_insight_new():
    errors = {}
    f = request.form
    if request.method == "POST":
        if not f.get("title", "").strip():
            errors["title"] = "Title is required."
        if not f.get("body", "").strip():
            errors["body"] = "Story is required."
        if not errors:
            slug = slugify(f.get("title", ""))
            existing = {a["slug"] for a in ARTICLES}
            base, n = slug, 2
            while slug in existing:
                slug = f"{base}-{n}"
                n += 1
            ARTICLES.append(dict(
                slug=slug,
                type=f.get("type", "commentary"),
                title=f.get("title", ""),
                standfirst=f.get("standfirst", ""),
                author="Admin",
                date="—",
                mins=5,
                body=[f.get("body", "")],
                image_url=f.get("image_url", ""),
                link_url=f.get("link_url", ""),
                colour=f.get("colour", "teal"),
                status="published" if f.get("action") == "publish" else "draft",
                url=f"/insights/{f.get('type', 'commentary')}/{slug}",
            ))
            flash("Insight saved.", "success")
            return redirect(url_for("admin_insights"))
    return render_template("admin/insight_new.html", errors=errors, f=f)


@app.route("/admin/insights/<slug>/edit", methods=["GET", "POST"])
def admin_insight_edit(slug):
    a = next((x for x in ARTICLES if x["slug"] == slug), None) or abort(404)
    errors = {}
    f = request.form
    if request.method == "POST":
        if not f.get("title", "").strip():
            errors["title"] = "Title is required."
        if not f.get("body", "").strip():
            errors["body"] = "Story is required."
        if not errors:
            a["title"] = f.get("title", "")
            a["type"] = f.get("type", a["type"])
            a["standfirst"] = f.get("standfirst", "")
            a["body"] = [f.get("body", "")]
            a["image_url"] = f.get("image_url", "")
            a["link_url"] = f.get("link_url", "")
            a["colour"] = f.get("colour", "teal")
            a["url"] = f"/insights/{a['type']}/{a['slug']}"
            flash("Insight updated.", "success")
            return redirect(url_for("admin_insights"))
    return render_template("admin/insight_edit.html", a=a, errors=errors, f=f)


@app.route("/admin/insights/<slug>/publish", methods=["POST", "GET"])
def admin_insight_publish(slug):
    a = next((x for x in ARTICLES if x["slug"] == slug), None) or abort(404)
    a["status"] = "published"
    flash(f"Published: {a['title']}", "success")
    return redirect(url_for("admin_insights"))


# ---------- Admin: Programmes (Events + Courses) ----------

@app.route("/admin/programmes")
def admin_programmes():
    kind_filter = request.args.get("kind", "all")
    items = PROGRAMMES
    if kind_filter == "event":
        items = [p for p in PROGRAMMES if p["kind"] == "event"]
    elif kind_filter == "course":
        items = [p for p in PROGRAMMES if p["kind"] == "course"]
    return render_template(
        "admin/programmes.html",
        programmes=sorted(items, key=lambda p: p["date"]),
        kind_filter=kind_filter,
        counts={
            "all": len(PROGRAMMES),
            "event": sum(1 for p in PROGRAMMES if p["kind"] == "event"),
            "course": sum(1 for p in PROGRAMMES if p["kind"] == "course"),
        },
    )


@app.route("/admin/programmes/new", methods=["GET", "POST"])
def admin_programme_new():
    errors = {}
    f = request.form
    if request.method == "POST":
        kind = f.get("kind", "event")
        if not f.get("title", "").strip():
            errors["title"] = "Title is required."
        if not f.get("date", "").strip():
            errors["date"] = "Date is required."
        if not errors:
            slug = slugify(f.get("title", ""))
            existing = {p["slug"] for p in PROGRAMMES}
            base, n = slug, 2
            while slug in existing:
                slug = f"{base}-{n}"
                n += 1
            PROGRAMMES.append(dict(
                id=max([p["id"] for p in PROGRAMMES] + [0]) + 1,
                slug=slug,
                kind=kind,
                category=f.get("category", "talk" if kind == "event" else "educational"),
                title=f.get("title", ""),
                standfirst=f.get("standfirst", ""),
                body=f.get("body", ""),
                date=f.get("date", ""),
                end_date=f.get("end_date", "") or f.get("date", ""),
                time=f.get("time", ""),
                place=f.get("place", ""),
                venue=f.get("venue", ""),
                price=int(f.get("price", 0) or 0),
                price_label=f.get("price_label", ""),
                capacity=int(f.get("capacity", 0) or 0),
                registered=0,
                register_url=f.get("register_url", ""),
                image_url=f.get("image_url", ""),
                colour=f.get("colour", "teal"),
                status="published" if f.get("action") == "publish" else "draft",
                featured=f.get("featured") == "on",
                facilitator=f.get("facilitator", ""),
                format=f.get("format", ""),
                duration=f.get("duration", ""),
                outline=f.get("outline", ""),
                outcomes=f.get("outcomes", ""),
                sessions=[],
            ))
            flash("Programme saved.", "success")
            return redirect(url_for("admin_programmes"))
    return render_template(
        "admin/programme_new.html",
        errors=errors, f=f, categories=EVENT_CATEGORIES,
    )


@app.route("/admin/programmes/<slug>/edit", methods=["GET", "POST"])
def admin_programme_edit(slug):
    p = next((x for x in PROGRAMMES if x["slug"] == slug), None) or abort(404)
    errors = {}
    f = request.form
    if request.method == "POST":
        if not f.get("title", "").strip():
            errors["title"] = "Title is required."
        if not f.get("date", "").strip():
            errors["date"] = "Date is required."
        if not errors:
            p["kind"] = f.get("kind", p["kind"])
            p["category"] = f.get("category", p["category"])
            p["title"] = f.get("title", p["title"])
            p["standfirst"] = f.get("standfirst", "")
            p["body"] = f.get("body", "")
            p["date"] = f.get("date", p["date"])
            p["end_date"] = f.get("end_date", "") or p["date"]
            p["time"] = f.get("time", "")
            p["place"] = f.get("place", "")
            p["venue"] = f.get("venue", "")
            p["price"] = int(f.get("price", 0) or 0)
            p["price_label"] = f.get("price_label", "")
            p["capacity"] = int(f.get("capacity", 0) or 0)
            p["register_url"] = f.get("register_url", "")
            p["image_url"] = f.get("image_url", "")
            p["colour"] = f.get("colour", p["colour"])
            p["featured"] = f.get("featured") == "on"
            p["facilitator"] = f.get("facilitator", "")
            p["format"] = f.get("format", "")
            p["duration"] = f.get("duration", "")
            p["outline"] = f.get("outline", "")
            p["outcomes"] = f.get("outcomes", "")
            flash("Programme updated.", "success")
            return redirect(url_for("admin_programmes"))
    return render_template(
        "admin/programme_edit.html",
        p=p, errors=errors, f=f, categories=EVENT_CATEGORIES,
    )


@app.route("/admin/programmes/<slug>/publish", methods=["POST", "GET"])
def admin_programme_publish(slug):
    p = next((x for x in PROGRAMMES if x["slug"] == slug), None) or abort(404)
    p["status"] = "published"
    flash(f"Published: {p['title']}", "success")
    return redirect(url_for("admin_programmes"))


# ---------- Admin: Subscribers ----------

@app.route("/admin/subscribers")
def admin_subscribers():
    status_filter = request.args.get("status", "all")
    subs = SUBSCRIBERS
    if status_filter != "all":
        subs = [s for s in subs if s["status"] == status_filter]
    stats = {
        "total": len(SUBSCRIBERS),
        "active": sum(1 for s in SUBSCRIBERS if s["status"] == "active"),
        "unsubscribed": sum(1 for s in SUBSCRIBERS if s["status"] == "unsubscribed"),
        "bounced": sum(1 for s in SUBSCRIBERS if s["status"] == "bounced"),
    }
    return render_template("admin/subscribers.html",
                           subscribers=sorted(subs, key=lambda s: s["subscribed_at"], reverse=True),
                           stats=stats, status_filter=status_filter)


if __name__ == "__main__":
    app.run(debug=True)