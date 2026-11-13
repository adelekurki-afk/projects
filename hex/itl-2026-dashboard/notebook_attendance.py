from IPython.display import display, HTML

# Self-contained. Do not reference Hex dataframes defined later in the notebook.

ITL_CSS = """
.itl { font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color:#111827; max-width: 920px; }
.itl h2 { font-size: 18px; font-weight: 700; margin: 28px 0 8px; letter-spacing: -0.01em; }
.itl h2:first-child { margin-top: 4px; }
.itl p { font-size: 14px; line-height: 1.55; color: #4B5563; margin: 0 0 12px; }
.itl table { width: 100%; border-collapse: collapse; font-size: 13px; margin: 0 0 4px; }
.itl th { text-align: left; font-weight: 600; color: #6B7280; padding: 8px 12px 8px 0; border-bottom: 1px solid #E5E7EB; }
.itl td { padding: 8px 12px 8px 0; border-bottom: 1px solid #F3F4F6; }
.itl th.n, .itl td.n { text-align: right; font-variant-numeric: tabular-nums; padding-right: 0; }
.itl .cap { font-size: 13px; color: #6B7280; margin: 4px 0 20px; }
"""


def _c(tag):
    return "<" + "/" + tag + ">"


def _table(headers, rows, caption=""):
    head = []
    for i, h in enumerate(headers):
        head.append(f'<th class="n">{h}{_c("th")}' if i else f"<th>{h}{_c('th')}")
    body = []
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            cls = ' class="n"' if i else ""
            cells.append(f"<td{cls}>{cell}{_c('td')}")
        body.append("<tr>" + "".join(cells) + _c("tr"))
    cap = f'<p class="cap">{caption}{_c("p")}' if caption else ""
    return "<table><tr>" + "".join(head) + _c("tr") + "".join(body) + _c("table") + cap


body = f"""
<div class="itl">
  <h2>People per day{_c("h2")}
  {_table(
      ["Day", "Came", "How built"],
      [
          ("Partner Day · 13 Oct", "426", "391 door + 35 badge"),
          ("Ecosystem Day · 14 Oct", "916", "878 door + 38 green YES"),
          ("Unique people", "1,018", "324 both days · 102 Partner only · 592 Eco only"),
      ],
      "Fliplet visits. Salesforce Attended is a different clock.",
  )}
  <h2>Region per day · Salesforce Attended{_c("h2")}
  {_table(
      ["Region", "Partner Day", "Ecosystem Day"],
      [
          ("EMEA", "194", "415"),
          ("Unknown", "154", "358"),
          ("NA", "48", "80"),
          ("LATAM", "5", "4"),
          ("APAC", "1", "8"),
          ("ANZ", "1", "—"),
      ],
      "Not Fliplet 426 / 916.",
  )}
  <h2>Sales segment per day · Salesforce Attended{_c("h2")}
  {_table(
      ["Segment", "Partner Day", "Ecosystem Day"],
      [
          ("Unknown", "149", "343"),
          ("MM", "138", "304"),
          ("ENT", "64", "158"),
          ("SMB", "52", "60"),
      ],
  )}
  <h2>Seniority · title on Salesforce Attended{_c("h2")}
  {_table(
      ["Seniority", "Partner Day", "Ecosystem Day"],
      [
          ("Exec / founder", "87", "130"),
          ("Manager / lead", "83", "187"),
          ("IC / practitioner", "69", "206"),
          ("Other", "61", "145"),
          ("Director / head of", "42", "90"),
          ("Unknown title", "28", "45"),
          ("Partner / consultant", "28", "56"),
          ("VP", "4", "6"),
      ],
  )}
  <h2>Attendance to sessions · Fliplet{_c("h2")}
  {_table(
      ["Zone or signal", "Scans"],
      [
          ("Community Lounge", "484"),
          ("Cardputer Station", "425"),
          ("Solution Zone n8n", "377"),
          ("Candy Station", "350"),
          ("Coffee Station", "335"),
          ("Solution Zone Exhibitors", "293"),
          ("Connection Zone", "252"),
          ("Session ratings 4.8/5 (n=66)", "66"),
      ],
      "No named session-scan column in the workbook.",
  )}
  <h2>Attendance to meetings{_c("h2")}
  {_table(
      ["Clock", "Count"],
      [
          ("Fliplet booked", "1,076"),
          ("Meeting arrivals", "425"),
          ("Sales meetings sheet", "23"),
          ("Salesforce meeting booked", "20"),
      ],
  )}
  <h2>Feedback · Ecosystem and Partner Day survey tabs{_c("h2")}
  {_table(
      ["Survey", "Score"],
      [
          ("Ecosystem recommend (n=43, NPS 72)", "9.1 / 10"),
          ("Partner Day overall (n=23)", "8.8 / 10"),
          ("Session rating (n=66)", "4.8 / 5"),
      ],
  )}
  {_table(
      ["Ecosystem Day · more of next year (n=43, pick up to 3)", "Mentions"],
      [
          ("Business value and ROI", "21"),
          ("Features and roadmap", "21"),
          ("Running n8n at scale", "19"),
          ("Workshops and build-alongs", "19"),
          ("Agents for production", "19"),
          ("Customer case studies", "16"),
      ],
  )}
{_c("div")}
"""
display(HTML("<style>" + ITL_CSS + _c("style") + body))
