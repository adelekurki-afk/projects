import "app/app.css";
import { createElement as h, useMemo, useState } from "react";
import { render, useHexData } from "app/_data.js";
import { KpiCard } from "app/components/KpiCard.js";
import { CartesianChart } from "app/components/CartesianChart.js";
import { SEGMENT_COLORS, SEGMENT_ORDER, segLabel, money } from "app/theme.js";

const STAGES = ["Registered", "Attended", "Had n8n Meeting", "Account with Opp", "Closed Won"];
const GROUP_ORDER = ["Both Days", "Partner Day only", "Ecosystem Day only", "Gap (Did Not Attend)"];
const ATTR_TABS = ["Sourced", "Influenced", "Renewals"];
const STATUS_COLORS = { "Open pipeline": "#4f7fb8", "Closed won": "#2e8b57" };
const ATTR_COLORS = { Sourced: "#4f7fb8", Influenced: "#2e8b57", "Renewal touched": "#888888" };
const REGION_ORDER = ["EMEA", "NA", "APAC", "LATAM", "ANZ", "Unknown"];
const muted = { margin: 0, color: "var(--color-text-muted)", fontSize: "var(--text-sm)" };
const grid2 = { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(340px, 1fr))", gap: "var(--space-6)" };
const th = { textAlign: "left", padding: "8px 10px", borderBottom: "1px solid var(--color-border)", whiteSpace: "nowrap" };
const td = { padding: "8px 10px", borderBottom: "1px solid var(--color-border)", verticalAlign: "top" };
const kpiGridStyle = { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(170px, 1fr))", gap: "var(--space-4)" };
const cardGridStyle = { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "var(--space-4)" };
const cardStyle = { border: "1px solid var(--color-border)", borderRadius: "8px", padding: "var(--space-4)", display: "flex", flexDirection: "column", gap: "var(--space-2)" };
const tableStyle = { width: "100%", borderCollapse: "collapse", fontSize: "var(--text-sm)" };

/* Physical attendance: Fliplet Purchases + Scans + CAB sheet. Snapshot 10 Nov 2026.
   Overlapping on purpose: a person on both days counts in Partner AND Eco. */
const DAY_ROWS = [
  { day: "Partner Day", date: "13 Oct", participants: 391, registered: 487, note: "Door scans. People who also came on Eco Day are included here." },
  { day: "Ecosystem Day", date: "14 Oct", participants: 878, registered: 1205, note: "Door scans. People who also came on Partner Day are included here." }
];
const REGISTERED = 1269;
const BOTH_DAYS = 272;

const CAB_ROWS = [
  { attendance_group: "CAB total", on_cab_list: 39, partner_day: 29, eco_day: 39, both_days: 29, redeemed: 39 },
  { attendance_group: "CAB Member", on_cab_list: 11, partner_day: 1, eco_day: 11, both_days: 1, redeemed: 11 },
  { attendance_group: "CAB Guest", on_cab_list: 28, partner_day: 28, eco_day: 28, both_days: 28, redeemed: 28 }
];

const STAFF_KPIS = [
  { label: "Staff tickets", value: 113, note: "Fliplet Ticket family = Staff (crew, not n8n-only)" },
  { label: "n8n on any ticket", value: 168, note: "13 staff tickets, 48 speaker tickets, 107 other" },
  { label: "C2 crew tickets", value: 40, note: "Largest staff bucket" },
  { label: "Speaker tickets", value: 76, note: "Fliplet Ticket family = Speakers" }
];

const STAFF_BUCKETS = [
  { bucket: "C2", registered: 40, partner_day: 0, eco_day: 2 },
  { bucket: "Hospitality / QT Events", registered: 36, partner_day: 8, eco_day: 6 },
  { bucket: "Content / merch / film", registered: 19, partner_day: 1, eco_day: 2 },
  { bucket: "n8n (staff ticket)", registered: 13, partner_day: 6, eco_day: 8 },
  { bucket: "Other crew", registered: 5, partner_day: 3, eco_day: 1 }
];

const SPEAKER_KPIS = [
  { label: "Programme speakers", value: 116, note: "Speakers tab in Fliplet raw workbook" },
  { label: "n8n speakers", value: 62, note: "Company = n8n on the Speakers tab" },
  { label: "External speakers", value: 54, note: "Non-n8n on the Speakers tab" },
  { label: "Speaker tickets", value: 76, note: "Fliplet Ticket family = Speakers" }
];

const SPEAKER_DAYS = [
  { day: "Partner Day", speakers: 62 },
  { day: "Ecosystem Day", speakers: 79 }
];

const PERSONA_ROWS = [
  { persona: "IC / practitioner", registrants: 229, meeting_rate_pct: 1.7, opp_rate_pct: 5.7 },
  { persona: "Manager / lead", registrants: 226, meeting_rate_pct: 1.3, opp_rate_pct: 6.2 },
  { persona: "Exec / founder", registrants: 193, meeting_rate_pct: 1.0, opp_rate_pct: 1.6 },
  { persona: "Other", registrants: 146, meeting_rate_pct: 3.4, opp_rate_pct: 7.5 },
  { persona: "Director / head of", registrants: 124, meeting_rate_pct: 4.0, opp_rate_pct: 4.8 },
  { persona: "Partner / consultant", registrants: 74, meeting_rate_pct: 1.4, opp_rate_pct: 2.7 },
  { persona: "Unknown title", registrants: 62, meeting_rate_pct: 0, opp_rate_pct: 0 },
  { persona: "Sales / GTM", registrants: 24, meeting_rate_pct: 0, opp_rate_pct: 8.3 },
  { persona: "Product / design", registrants: 22, meeting_rate_pct: 0, opp_rate_pct: 0 },
  { persona: "VP", registrants: 11, meeting_rate_pct: 0, opp_rate_pct: 9.1 },
  { persona: "Student / intern", registrants: 8, meeting_rate_pct: 0, opp_rate_pct: 12.5 }
];

const ATTR_KPIS = [
  { bucket: "Sourced", opp_count: 9, amount: 916600, open_count: 9, won_count: 0 },
  { bucket: "Influenced", opp_count: 12, amount: 1043341, open_count: 10, won_count: 2 },
  { bucket: "Renewal touched", opp_count: 10, amount: 756519, open_count: 10, won_count: 0 }
];

const ATTR_OPPS = [
  { opp_id: "s1", account_name: "Kongsberg Satellite Services AS", segment: "MM", opp_name: "Kongsberg Satellite Services AS-Expansion-Enterprise-4-2027", primary_campaign: "Ecosystem Day", opp_type: "Expansion", attribution: "Sourced", StageName: "Value Workshop", status: "Open", amount: 215000, people_associated: "Brynhild Bentsen Saether, Daniel Norum Danielsen" },
  { opp_id: "s2", account_name: "Boston Consulting Group, Inc.", segment: "ENT", opp_name: "Boston Consulting Group, Inc.-Expansion-Enterprise-2-2027", primary_campaign: "Ecosystem Day", opp_type: "Expansion", attribution: "Sourced", StageName: "Value Workshop", status: "Open", amount: 200000, people_associated: "Alexandra Petkova, Andrej Levin, Robin Wagner" },
  { opp_id: "s3", account_name: "TeamViewer GmbH", segment: "MM", opp_name: "TeamViewer GmbH-New Business-Embed-12-2027", primary_campaign: "In The Loop", opp_type: "New Business", attribution: "Sourced", StageName: "Value Workshop", status: "Open", amount: 196700, people_associated: "Hector Castro" },
  { opp_id: "s4", account_name: "N3 Engine Overhaul Services", segment: "MM", opp_name: "N3 Engine Overhaul Services-New Business-Enterprise-12-2026", primary_campaign: "In The Loop", opp_type: "New Business", attribution: "Sourced", StageName: "Value Workshop", status: "Open", amount: 113900, people_associated: "Christoph Petzold" },
  { opp_id: "s5", account_name: "Eleven Labs Inc.", segment: "MM", opp_name: "Eleven Labs Inc.-Expansion-Enterprise-12-2026", primary_campaign: "In The Loop", opp_type: "Expansion", attribution: "Sourced", StageName: "Value Workshop", status: "Open", amount: 80000, people_associated: "Lena Braeuninger" },
  { opp_id: "s6", account_name: "Relex", segment: "MM", opp_name: "Retail Logistics Excellence - Relex Oy-Expansion-12-2026", primary_campaign: "In The Loop", opp_type: "Expansion", attribution: "Sourced", StageName: "Stakeholder Alignment", status: "Open", amount: 56000, people_associated: "Onur Akbal" },
  { opp_id: "s7", account_name: "Next PLC", segment: "ENT", opp_name: "Next PLC-Expansion-Enterprise-2-2027", primary_campaign: "Ecosystem Day", opp_type: "Expansion", attribution: "Sourced", StageName: "Meeting Booked", status: "Open", amount: 55000, people_associated: "Chris Kirt" },
  { opp_id: "s8", account_name: "Moonspring AI", segment: "SMB", opp_name: "Moonspring AI-New Business-12-2026", primary_campaign: "In The Loop", opp_type: "New Business", attribution: "Sourced", StageName: "Meeting Booked", status: "Open", amount: 0, people_associated: "" },
  { opp_id: "s9", account_name: "ECTIVE Automation", segment: "SMB", opp_name: "ECTIVE Automation-New Business-10-2028", primary_campaign: "In The Loop", opp_type: "New Business", attribution: "Sourced", StageName: "Meeting Booked", status: "Open", amount: 0, people_associated: "" },
  { opp_id: "i1", account_name: "NVIDIA", segment: "ENT", opp_name: "NVIDIA-New Business-Enterprise-4-2027", primary_campaign: "", opp_type: "New Business", attribution: "Influenced - new opp", StageName: "Meeting Booked", status: "Open", amount: 700000, people_associated: "Claire Helffer-de Soyres, Soeren Petersen, Zenodia Charpy" },
  { opp_id: "i2", account_name: "Rohde & Schwarz GmbH & Co. KG", segment: "ENT", opp_name: "Rohde & Schwarz-New Business-12-2026", primary_campaign: "", opp_type: "New Business", attribution: "Influenced - new opp", StageName: "Meeting Booked", status: "Open", amount: 55000, people_associated: "Kristian Kunst, Marco Volbracht" },
  { opp_id: "i3", account_name: "EngageTech", segment: "MM", opp_name: "EngageTech-New Business-12-2026", primary_campaign: "Talk to Sales Web Form", opp_type: "New Business", attribution: "Influenced - new opp", StageName: "Meeting Booked", status: "Open", amount: 28000, people_associated: "Max Meinders, Michael Pham" },
  { opp_id: "i4", account_name: "Cornelsen", segment: "MM", opp_name: "damian.lasnia@cornelsen.de-New Business-12-2026", primary_campaign: "Talk to Sales Web Form", opp_type: "New Business", attribution: "Influenced - new opp", StageName: "Meeting Booked", status: "Open", amount: 28000, people_associated: "Damian Lasnia, Lotta Fagel" },
  { opp_id: "i5", account_name: "Graphwise", segment: "MM", opp_name: "Graphwise-Expansion-Embed-12-2026", primary_campaign: "Talk to Sales Web Form", opp_type: "Expansion", attribution: "Influenced - new opp", StageName: "Stakeholder Alignment", status: "Open", amount: 26701, people_associated: "Gary Leicester" },
  { opp_id: "i6", account_name: "HiSolutions AG", segment: "MM", opp_name: "HiSolutions AG-New Business-1-2027", primary_campaign: "Talk to Sales Web Form", opp_type: "New Business", attribution: "Influenced - new opp", StageName: "Value Workshop", status: "Open", amount: 26000, people_associated: "Sandro Grundmann" },
  { opp_id: "i7", account_name: "voize", segment: "MM", opp_name: "voize-New Business-12-2026", primary_campaign: "Talk to Sales Web Form", opp_type: "New Business", attribution: "Influenced - new opp", StageName: "Value Workshop", status: "Open", amount: 26000, people_associated: "Alessio Pellegrini, Charlotte Cheung" },
  { opp_id: "i8", account_name: "C Digital Technologies Limited", segment: "MM", opp_name: "C Digital Technologies Limited-New Business-11-2026", primary_campaign: "Talk to Sales Web Form", opp_type: "New Business", attribution: "Influenced - new opp", StageName: "Value Workshop", status: "Open", amount: 26000, people_associated: "Jasmina Popovikj Zabrchanec" },
  { opp_id: "i9", account_name: "Apaleo", segment: "MM", opp_name: "Apaleo-New Business-12-2026", primary_campaign: "", opp_type: "New Business", attribution: "Influenced - new opp", StageName: "Closed Won Approved", status: "Closed won", amount: 22000, people_associated: "Jan Schwarz, Raphael Daubner" },
  { opp_id: "i10", account_name: "Deutsche Telekom MMS GmbH", segment: "ENT", opp_name: "Deutsche Telekom MMS GmbH-New Business-12-2026", primary_campaign: "Talk to Sales Web Form", opp_type: "New Business", attribution: "Influenced - new opp", StageName: "Meeting Booked", status: "Open", amount: 16000, people_associated: "Askan Schmeisser, Christoph Keller, Hannah Materne, Mirko Golze" },
  { opp_id: "i11", account_name: "Globalization Partners LLC", segment: "MM", opp_name: "Globalization Partners LLC-Expansion-10-2026", primary_campaign: "", opp_type: "Expansion", attribution: "Influenced - new opp", StageName: "Closed Won Approved", status: "Closed won", amount: 3640, people_associated: "Volker Elzner" },
  { opp_id: "i12", account_name: "Solaris SE", segment: "MM", opp_name: "Solaris SE-New Business-12-2026", primary_campaign: "Talk to Sales Web Form", opp_type: "New Business", attribution: "Influenced - existing open", StageName: "Stakeholder Alignment", status: "Open", amount: 86000, people_associated: "Uzair Anwar" },
  { opp_id: "r1", account_name: "Atruvia AG", segment: "ENT", opp_name: "Atruvia AG-Renewal-Enterprise-9-2027", primary_campaign: "", opp_type: "Renewal", attribution: "Renewal touched", StageName: "Not Yet Qualified", status: "Open", amount: 230050, people_associated: "Peter Lorenz" },
  { opp_id: "r2", account_name: "eBay Inc", segment: "ENT", opp_name: "eBay Inc-Renewal-Enterprise-10-2027", primary_campaign: "", opp_type: "Renewal", attribution: "Renewal touched", StageName: "Not Yet Qualified", status: "Open", amount: 188460, people_associated: "Michael Gross" },
  { opp_id: "r3", account_name: "Syngenta", segment: "ENT", opp_name: "Syngenta-Renewal-Enterprise-9-2027", primary_campaign: "", opp_type: "Renewal", attribution: "Renewal touched", StageName: "Auto-Renewal", status: "Open", amount: 109925, people_associated: "Roxana Lupu" },
  { opp_id: "r4", account_name: "Globalization Partners LLC", segment: "MM", opp_name: "Globalization Partners LLC-Renewal-10-2027", primary_campaign: "", opp_type: "Renewal", attribution: "Renewal touched", StageName: "Auto-Renewal", status: "Open", amount: 57395, people_associated: "Volker Elzner" },
  { opp_id: "r5", account_name: "Paddle", segment: "MM", opp_name: "Paddle-Renewal-Enterprise-6-2025", primary_campaign: "", opp_type: "Renewal", attribution: "Renewal touched", StageName: "Not Yet Qualified", status: "Open", amount: 51425, people_associated: "Charlie Sparrow, Matheus Martins, Stephane De Keerle" },
  { opp_id: "r6", account_name: "Aerzteversorgung Westfalen-Lippe", segment: "SMB", opp_name: "Aerzteversorgung Westfalen-Lippe-Renewal-9-2026", primary_campaign: "", opp_type: "Renewal", attribution: "Renewal touched", StageName: "Not Yet Qualified", status: "Open", amount: 40000, people_associated: "Marc-Andre Hoffmeister" },
  { opp_id: "r7", account_name: "Pillsbury Winthrop Shaw Pittman LLP", segment: "MM", opp_name: "Pillsbury-Renewal-Enterprise-5-2027", primary_campaign: "", opp_type: "Renewal", attribution: "Renewal touched", StageName: "Not Yet Qualified", status: "Open", amount: 38604, people_associated: "Michael McCann" },
  { opp_id: "r8", account_name: "Apaleo", segment: "MM", opp_name: "Apaleo-Renewal-Enterprise-10-2027", primary_campaign: "", opp_type: "Renewal", attribution: "Renewal touched", StageName: "Auto-Renewal", status: "Open", amount: 23540, people_associated: "Jan Schwarz, Raphael Daubner" },
  { opp_id: "r9", account_name: "Tiger AI Taiwan", segment: "SMB", opp_name: "Tiger AI Taiwan-Renewal-10-2027", primary_campaign: "", opp_type: "Renewal", attribution: "Renewal touched", StageName: "Auto-Renewal", status: "Open", amount: 8560, people_associated: "TigerAI Tech" },
  { opp_id: "r10", account_name: "Deloitte - Global", segment: "ENT", opp_name: "Deloitte - Global-Renewal-10-2027", primary_campaign: "", opp_type: "Renewal", attribution: "Renewal touched", StageName: "Auto-Renewal", status: "Open", amount: 8560, people_associated: "Christian Maurer, Niklas Kern, Ondrej Michalik" }
];

const TREND_ROWS = [
  { week_label: "5 Oct", berlin_events: 8601, cta_clicks: 80954, trial_starts: 417, youtube_referrer_events: 8100, itl_page_views: 2905 },
  { week_label: "12 Oct", berlin_events: 11428, cta_clicks: 78744, trial_starts: 414, youtube_referrer_events: 6773, itl_page_views: 2005 },
  { week_label: "19 Oct", berlin_events: 6995, cta_clicks: 68808, trial_starts: 286, youtube_referrer_events: 6446, itl_page_views: 246 },
  { week_label: "26 Oct", berlin_events: 5833, cta_clicks: 64839, trial_starts: 239, youtube_referrer_events: 5811, itl_page_views: 100 },
  { week_label: "2 Nov", berlin_events: 5928, cta_clicks: 63252, trial_starts: 169, youtube_referrer_events: 5979, itl_page_views: 101 }
];
const TREND_WEEKS = ["5 Oct", "12 Oct", "19 Oct", "26 Oct", "2 Nov"];

function Section({ title, note, children, testid }) {
  return h("section", { "data-testid": testid, style: { display: "flex", flexDirection: "column", gap: "var(--space-4)", borderTop: "1px solid var(--color-border)", paddingTop: "var(--space-6)" } },
    h("h2", { style: { fontSize: "var(--text-xl)", margin: 0 } }, title),
    note ? h("p", { style: muted }, note) : null,
    children);
}

const pct = (v) => (Number(v) || 0).toFixed(1) + "%";
const dash = (v) => (v == null || v === "" ? "-" : String(v));
const n = (v) => Number(v || 0).toLocaleString();

function breakdownHas(row, needle) {
  return String(row.breakdown || "").toLowerCase().indexOf(needle) !== -1;
}

function HeadRow(labels) {
  return h("thead", null,
    h("tr", null, labels.map(function (c) {
      return h("th", { key: c, style: th }, c);
    })));
}

function OppTable({ rows }) {
  const head = HeadRow(["Account", "Opportunity", "Type", "Stage", "Amount", "Person associated"]);
  const body = h("tbody", null, rows.map(function (r) {
    return h("tr", { key: r.opp_id },
      h("td", { style: td },
        h("div", { style: { fontWeight: 600 } }, dash(r.account_name)),
        h("div", { style: muted }, dash(r.segment))),
      h("td", { style: td },
        dash(r.opp_name),
        h("div", { style: muted }, dash(r.primary_campaign))),
      h("td", { style: td },
        dash(r.opp_type),
        h("div", { style: muted }, dash(r.attribution))),
      h("td", { style: td },
        dash(r.StageName),
        h("div", { style: muted }, dash(r.status))),
      h("td", { style: Object.assign({}, td, { whiteSpace: "nowrap" }) }, money(+r.amount || 0)),
      h("td", { style: td }, dash(r.people_associated)));
  }));
  return h("div", { style: { overflowX: "auto" } },
    h("table", { style: tableStyle }, head, body));
}

function App() {
  const funnel = useHexData("01a1bfe3-9664-7625-8434-41290e76c627");
  const pipe = useHexData("01a1bfe4-17f7-77be-b00d-e14537341ed5");
  const mix = useHexData("01a1c473-53ad-7318-bb55-1e5a6f7647ca");
  const grp = useHexData("01a1c189-bfc0-726f-96b2-634428bd9c3a");
  const grpPipe = useHexData("01a1c189-ebf0-728b-afe0-9e8bc47ad2b6");
  const ga = useHexData("01a1bfe5-4cac-766f-86d7-2325e635fe2d");
  const pages = useHexData("01a1bfe5-702b-7448-a138-15aa30fc8c96");
  const [attrTab, setAttrTab] = useState("Sourced");

  const stage = useMemo(() => {
    const m = {};
    (funnel.rows || []).forEach((r) => { const k = STAGES.find((s) => String(r.stage).startsWith(s)); if (k) m[k] = r; });
    return m;
  }, [funnel.rows]);
  const stageOrder = useMemo(() => STAGES.map((s) => (stage[s] ? stage[s].stage : s)), [stage]);
  const pipeRows = useMemo(() => (pipe.rows || []).map((r) => Object.assign({}, r, { segment_label: segLabel(r.segment) })), [pipe.rows]);
  const tot = useMemo(() => {
    const t = { opps: 0, amt: 0, won: 0, wonAmt: 0, open: 0, openAmt: 0, mtg: 0 };
    pipeRows.forEach((r) => {
      t.opps += +r.opp_count || 0; t.amt += +r.total_amount || 0;
      t.won += +r.closed_won_count || 0; t.wonAmt += +r.closed_won_amount || 0;
      t.open += +r.open_opp_count || 0; t.openAmt += +r.open_pipeline_amount || 0;
      t.mtg += +r.opps_from_meetings || 0;
    });
    return t;
  }, [pipeRows]);
  const statusRows = useMemo(() => {
    const out = [];
    pipeRows.forEach((r) => {
      const k = r.opp_type + " / " + r.segment_label;
      out.push({ bucket: k, status: "Open pipeline", amount: +r.open_pipeline_amount || 0 });
      out.push({ bucket: k, status: "Closed won", amount: +r.closed_won_amount || 0 });
    });
    return out;
  }, [pipeRows]);
  const segMix = useMemo(() => (mix.rows || []).filter((r) => breakdownHas(r, "seg")).map((r) => Object.assign({}, r, { label: segLabel(r.label) })), [mix.rows]);
  const regMix = useMemo(() => (mix.rows || []).filter((r) => breakdownHas(r, "reg")), [mix.rows]);
  const grpRows = useMemo(() => GROUP_ORDER.map((g) => (grp.rows || []).find((r) => r.attendance_group === g)).filter(Boolean), [grp.rows]);
  const grpPipeRows = useMemo(() => {
    const out = [];
    GROUP_ORDER.forEach((g) => {
      const r = (grpPipe.rows || []).find((x) => x.attendance_group === g) || {};
      out.push({ attendance_group: g, status: "Open pipeline", amount: +r.open_pipeline || 0 });
      out.push({ attendance_group: g, status: "Closed won", amount: +r.closed_won_amount || 0 });
    });
    return out;
  }, [grpPipe.rows]);
  const gaDelta = useMemo(() => {
    const b = (ga.rows || [])[0], c = (ga.rows || [])[1];
    if (!b || !c) return null;
    return { berlin: ((c.berlin_events / b.berlin_events - 1) * 100).toFixed(1), cta: ((c.cta_clicks / b.cta_clicks - 1) * 100).toFixed(1) };
  }, [ga.rows]);
  const attrMap = useMemo(() => {
    const m = {};
    ATTR_KPIS.forEach((r) => { m[r.bucket] = r; });
    return m;
  }, []);
  const attrTabRows = useMemo(() => {
    if (attrTab === "Sourced") return ATTR_OPPS.filter((r) => r.attribution === "Sourced");
    if (attrTab === "Renewals") return ATTR_OPPS.filter((r) => r.attribution === "Renewal touched");
    return ATTR_OPPS.filter((r) => String(r.attribution).indexOf("Influenced") === 0);
  }, [attrTab]);
  const attrTabSum = useMemo(() => attrTabRows.reduce((s, r) => s + (+r.amount || 0), 0), [attrTabRows]);
  const personaOrder = PERSONA_ROWS.map((r) => r.persona);

  const mtg = stage["Had n8n Meeting"];
  const partnerDay = DAY_ROWS[0];
  const ecoDay = DAY_ROWS[1];
  const ready = pipe.hasData;
  const sourced = attrMap.Sourced, influenced = attrMap.Influenced, renewals = attrMap["Renewal touched"];
  const pagesReady = pages && pages.hasData;

  const bannerEl = h("div", { "data-testid": "nov10-banner", style: { background: "#ff6d5a", color: "#fff", padding: "12px 16px", borderRadius: "8px", fontWeight: 600 } },
    "NOV 10 FULL PASTE v8 is live - per-day visits only, no either-day unique.");

  const headerEl = h("header", { "data-testid": "header", style: { display: "flex", flexDirection: "column", gap: "var(--space-3)" } },
    h("h1", { style: { fontSize: "var(--text-3xl)", margin: 0 } }, "In the Loop 2026 - Lead & Pipeline Dashboard"),
    h("p", { style: { margin: 0, color: "var(--color-text-muted)" } }, "Who was in the room: Fliplet tickets and door scans. Pipeline: Salesforce / BigQuery from 12 Oct 2026."),
    h("div", { style: { borderLeft: "3px solid var(--color-accent, #4f7fb8)", padding: "var(--space-2) var(--space-4)", fontSize: "var(--text-sm)" } },
      "Per-day visits. Partner Day " + n(partnerDay.participants) + " and Ecosystem Day " + n(ecoDay.participants) + " both include the " + n(BOTH_DAYS) + " people who came both days. Unpaid/comp, Eco-only tickets, staff, speakers and guests are in. CAB is an overlay from the CAB sheet (39 people, all redeemed)."));

  const kpiEl = h("div", { "data-testid": "kpis", style: kpiGridStyle },
    h(KpiCard, { label: "Registered (Fliplet)", value: n(REGISTERED), comparison: "Paid + Free tickets, unique email" }),
    h(KpiCard, { label: "Partner Day visits", value: n(partnerDay.participants), comparison: "13 Oct door scans" }),
    h(KpiCard, { label: "Ecosystem Day visits", value: n(ecoDay.participants), comparison: "14 Oct door scans" }),
    h(KpiCard, { label: "Pipeline (USD deal amount)", value: ready ? money(tot.amt) : "-", comparison: ready ? (tot.opps + " opps - " + money(tot.openAmt) + " open") : "" }));

  const dayCards = h("div", { "data-testid": "day-cards", style: cardGridStyle },
    DAY_ROWS.map(function (r) {
      return h("div", { key: r.day, style: cardStyle },
        h("div", { style: { fontWeight: 600 } }, r.day),
        h("div", { style: muted }, r.date),
        h("div", { style: { fontSize: "var(--text-2xl)" } }, n(r.participants) + " came"),
        h("div", { style: muted }, n(r.registered) + " had a ticket for this"),
        h("div", { style: muted }, r.note));
    }));

  const cabCards = h("div", { "data-testid": "cab-overlay", style: cardGridStyle },
    CAB_ROWS.map(function (r) {
      return h("div", { key: r.attendance_group, style: Object.assign({}, cardStyle, { border: "1px solid #4f7fb8" }) },
        h("div", { style: { fontWeight: 600 } }, r.attendance_group),
        h("div", { style: { fontSize: "var(--text-2xl)" } }, r.on_cab_list + " people"),
        h("div", { style: muted }, "Partner Day " + r.partner_day + " / Eco Day " + r.eco_day),
        h("div", { style: muted }, r.redeemed + " redeemed on the CAB sheet"));
    }));

  const daysEl = h(Section, { testid: "days", title: "Who was in which days", note: "Source: Fliplet Scans (Berlin timezone) joined to Purchases (Paid + Free, including unpaid/comp, staff, speakers, VIP). A person can sit in more than one tile. This is the n8n ops grain, not Salesforce exclusive leftovers." },
    dayCards,
    cabCards,
    h("p", { style: muted }, n(BOTH_DAYS) + " people visited both days, so they sit in both Partner Day and Ecosystem Day. Raw Scans tab is Partner 391 / Eco 878 (Berlin day)."));

  const staffHead = HeadRow(["Crew", "Registered", "Partner Day scans", "Eco Day scans"]);
  const staffBody = h("tbody", null, STAFF_BUCKETS.map(function (r) {
    return h("tr", { key: r.bucket },
      h("td", { style: td }, r.bucket),
      h("td", { style: td }, n(r.registered)),
      h("td", { style: td }, n(r.partner_day)),
      h("td", { style: td }, n(r.eco_day)));
  }));
  const staffTable = h("div", { style: { overflowX: "auto" } },
    h("table", { style: tableStyle }, staffHead, staffBody));
  const staffKpis = h("div", { style: kpiGridStyle }, STAFF_KPIS.map(function (r) {
    return h(KpiCard, { key: r.label, label: r.label, value: String(r.value), comparison: r.note });
  }));
  const staffEl = h(Section, { testid: "staff", title: "Staff", note: "Fliplet Ticket family = Staff. Crew rarely went through the attendee door scan, so scan counts are lower than tickets." },
    staffKpis,
    staffTable,
    h("p", { style: muted }, "Purchases has Ticket family Staff (113). Fliplet People Type=Team from the debrief is not a column in that export."));

  const speakerKpis = h("div", { style: kpiGridStyle }, SPEAKER_KPIS.map(function (r) {
    return h(KpiCard, { key: r.label, label: r.label, value: String(r.value), comparison: r.note });
  }));
  const speakerChart = h("div", { style: { height: 260 } }, h(CartesianChart, {
    instanceId: "itl-speaker-days", title: "Programme speakers scanned by day", data: SPEAKER_DAYS, baseAxisField: "day", valueAxisField: "speakers",
    dataLabelsVisible: true, valueAxisNumericFormat: ",.0f", valueAxisTitle: "Speakers (Count)", baseAxisTitle: "Day"
  }));
  const speakersEl = h(Section, { testid: "speakers", title: "Speakers", note: "Programme list from the Speakers tab in the Fliplet raw workbook, not Salesforce titles." },
    speakerKpis,
    speakerChart,
    h("p", { style: muted }, "62 programme speakers scanned on Partner Day, 79 on Ecosystem Day. 43 of them are in both day counts."));

  const funnelEl = h(Section, { testid: "funnel", title: "Commercial funnel (Salesforce ITL Free/Paid)", note: "This funnel is the Salesforce campaign universe for conversion, not physical headcount. Do not compare these Registered/Attended numbers to the day tiles above." },
    h("div", { style: { height: 300 } },
      h(CartesianChart, {
        instanceId: "itl-stage-counts", title: "Registrants by funnel stage", data: funnel.rows || [], baseAxisField: "stage", valueAxisField: "count",
        orientation: "horizontal", baseAxisCategoricalOrder: stageOrder, dataLabelsVisible: true,
        valueAxisNumericFormat: ",.0f", valueAxisTickNumericFormat: "~s", valueAxisTitle: "Registrants (Count)", baseAxisTitle: "Stage"
      })),
    h("div", { style: { display: "flex", gap: "var(--space-6)", flexWrap: "wrap", fontSize: "var(--text-sm)" } },
      (funnel.rows || []).map(function (r) {
        return h("span", { key: r.stage }, h("strong", null, r.stage), " " + Number(r.count).toLocaleString() + " - " + pct(r.pct_of_registered));
      })));

  const registrantsEl = h(Section, { testid: "registrants", title: "Who registered (Salesforce commercial)", note: "Unique ITL Free/Paid campaign members by Salesforce segment and region." },
    h("div", { style: grid2 },
      h("div", { style: { height: 280 } }, h(CartesianChart, {
        instanceId: "itl-reg-segment", title: "Registrants by segment", data: segMix, baseAxisField: "label", valueAxisField: "registrant_count",
        colorField: "label", colorCategoricalMap: SEGMENT_COLORS, baseAxisCategoricalOrder: SEGMENT_ORDER, colorCategoricalOrder: SEGMENT_ORDER,
        showLegend: false, dataLabelsVisible: true, valueAxisNumericFormat: "~s", valueAxisTitle: "Registrants (Count)", baseAxisTitle: "Segment"
      })),
      h("div", { style: { height: 280 } }, h(CartesianChart, {
        instanceId: "itl-reg-region", title: "Registrants by region", data: regMix, baseAxisField: "label", valueAxisField: "registrant_count",
        baseAxisCategoricalOrder: REGION_ORDER, dataLabelsVisible: true, valueAxisNumericFormat: "~s", valueAxisTitle: "Registrants (Count)", baseAxisTitle: "Region"
      }))));

  const rolesEl = h(Section, { testid: "roles", title: "By role", note: "High-level persona from Salesforce Title on ITL registrants (1,119 unique emails). Directors convert to meetings best." },
    h("div", { style: { height: 360 } }, h(CartesianChart, {
      instanceId: "itl-persona-roles", title: "Registrants by role", data: PERSONA_ROWS, baseAxisField: "persona", valueAxisField: "registrants",
      orientation: "horizontal", baseAxisCategoricalOrder: personaOrder, dataLabelsVisible: true,
      valueAxisNumericFormat: ",.0f", valueAxisTitle: "Registrants (Count)", baseAxisTitle: "Role"
    })),
    h("div", { style: { display: "flex", gap: "var(--space-5)", flexWrap: "wrap", fontSize: "var(--text-sm)" } },
      PERSONA_ROWS.map(function (r) {
        return h("span", { key: r.persona }, h("strong", null, r.persona), " " + r.registrants + " - meet " + pct(r.meeting_rate_pct) + " - opp " + pct(r.opp_rate_pct));
      })));

  const pipelineEl = h(Section, { testid: "pipeline", title: "Pipeline & revenue", note: "New Business and Expansion opps created on or after 12 Oct 2026 at registrant accounts. Account-level overlap, not sourced vs influenced." },
    h("div", { style: grid2 },
      h("div", { style: { height: 300 } }, h(CartesianChart, {
        instanceId: "itl-pipeline-by-type", title: "Opportunity amount by type and segment", data: pipeRows, baseAxisField: "opp_type", valueAxisField: "total_amount",
        colorField: "segment_label", colorCategoricalMap: SEGMENT_COLORS, colorCategoricalOrder: SEGMENT_ORDER, markMode: "stacked-bar",
        dataLabelsVisible: true, totalDataLabelsVisible: true, valueAxisNumericFormat: "$.3~s", valueAxisTitle: "Opportunity Amount ($)", baseAxisTitle: "Opportunity Type", legendPosition: "top"
      })),
      h("div", { style: { height: 300 } }, h(CartesianChart, {
        instanceId: "itl-pipeline-status", title: "Open vs closed won by type and segment", data: statusRows, baseAxisField: "bucket", valueAxisField: "amount",
        colorField: "status", colorCategoricalMap: STATUS_COLORS, colorCategoricalOrder: ["Open pipeline", "Closed won"], markMode: "stacked-bar", orientation: "horizontal",
        dataLabelsVisible: true, valueAxisNumericFormat: "$.3~s", valueAxisTitle: "Opportunity Amount ($)", baseAxisTitle: "Type / Segment", legendPosition: "top"
      }))),
    h("p", { style: muted }, tot.mtg + " of " + tot.opps + " opportunities sit at an account in the meetings-booked campaign. Had n8n meeting (SFDC): " + (mtg ? n(mtg.count) : "-") + "."));

  const attrButtons = h("div", { style: { display: "flex", gap: "var(--space-2)", flexWrap: "wrap" } },
    ATTR_TABS.map(function (t) {
      const on = attrTab === t;
      return h("button", {
        key: t, type: "button", onClick: function () { setAttrTab(t); },
        style: {
          padding: "6px 12px", borderRadius: "8px", cursor: "pointer",
          background: on ? "#4f7fb8" : "transparent",
          border: on ? "1px solid #4f7fb8" : "1px solid var(--color-border)",
          color: on ? "#fff" : "inherit", fontSize: "var(--text-sm)"
        }
      }, t);
    }));
  const attributionEl = h(Section, { testid: "attribution", title: "Sourced vs influenced opportunities", note: "Sourced: Primary Campaign Source is an ITL campaign, created from 1 Oct. Influenced: ITL campaign member or CAB person linked on/after 13 Oct, and the opp is not ITL-sourced. Renewals are separate. Snapshot 10 Nov 2026." },
    h("div", { style: kpiGridStyle },
      h(KpiCard, { label: "Sourced", value: String(sourced.opp_count), comparison: money(sourced.amount) + " - " + sourced.open_count + " open" }),
      h(KpiCard, { label: "Influenced", value: String(influenced.opp_count), comparison: money(influenced.amount) + " - " + influenced.won_count + " won", intent: "success" }),
      h(KpiCard, { label: "Renewals touched", value: String(renewals.opp_count), comparison: money(renewals.amount) + " - not counted as influence" })),
    h("div", { style: { height: 260 } }, h(CartesianChart, {
      instanceId: "itl-attr-amount", title: "Deal amount by attribution", data: ATTR_KPIS, baseAxisField: "bucket", valueAxisField: "amount",
      colorField: "bucket", colorCategoricalMap: ATTR_COLORS, colorCategoricalOrder: ["Sourced", "Influenced", "Renewal touched"],
      showLegend: false, dataLabelsVisible: true, valueAxisNumericFormat: "$.3~s", valueAxisTitle: "Opportunity Amount ($)", baseAxisTitle: "Attribution"
    })),
    attrButtons,
    h("p", { style: muted }, attrTab + ": " + attrTabRows.length + " opportunities - " + money(attrTabSum)),
    h(OppTable, { rows: attrTabRows }));

  const groupCards = h("div", { "data-testid": "group-cards", style: cardGridStyle },
    grpRows.map(function (r) {
      return h("div", { key: r.attendance_group, style: cardStyle },
        h("div", { style: { fontWeight: 600 } }, r.attendance_group),
        h("div", { style: { fontSize: "var(--text-2xl)" } }, Number(r.registrants).toLocaleString() + " registrants"),
        h("div", { style: muted }, "Meeting rate " + pct(r.meeting_rate_pct) + " (" + r.meetings_booked + ")"),
        h("div", { style: muted }, "Opp rate " + pct(r.opp_rate_pct) + " (" + r.with_opp + ") - " + r.closed_won + " closed won"));
    }));
  const groupsEl = h(Section, { testid: "groups", title: "Salesforce conversion groups (not headcount)", note: "Kept only so pipeline can still be split on ITL Free/Paid exclusive leftovers. Do not use these as Partner / Eco / CAB participation. Sum to the Salesforce commercial universe, not Fliplet." },
    groupCards,
    h("div", { style: { height: 300 } }, h(CartesianChart, {
      instanceId: "itl-group-pipeline", title: "Pipeline by Salesforce attendance group", data: grpPipeRows, baseAxisField: "attendance_group", valueAxisField: "amount",
      colorField: "status", colorCategoricalMap: STATUS_COLORS, colorCategoricalOrder: ["Open pipeline", "Closed won"], baseAxisCategoricalOrder: GROUP_ORDER, markMode: "stacked-bar",
      dataLabelsVisible: true, totalDataLabelsVisible: true, valueAxisNumericFormat: "$.3~s", valueAxisTitle: "Opportunity Amount ($)", baseAxisTitle: "Attendance Group", legendPosition: "top"
    })),
    h("p", { style: muted }, "Do not sum groups. Partner Day only has no opportunities."));

  const gaEl = h(Section, { testid: "ga4", title: "Digital signals (GA4, n8n.io)", note: "Weeks through 8 Nov. No native sign_up event (trial starts are a proxy). No YouTube Analytics; YouTube -> n8n.io is referrer traffic." + (pagesReady ? "" : "") },
    gaDelta ? h("p", { style: { margin: 0, fontSize: "var(--text-sm)" } }, "Berlin events changed " + gaDelta.berlin + "% in conference week vs baseline, while global CTA clicks moved " + gaDelta.cta + "%.") : null,
    h("div", { style: grid2 },
      h("div", { style: { height: 260 } }, h(CartesianChart, {
        instanceId: "itl-ga-berlin", title: "Berlin events by week", data: TREND_ROWS, baseAxisField: "week_label", valueAxisField: "berlin_events",
        baseAxisCategoricalOrder: TREND_WEEKS, dataLabelsVisible: true, valueAxisNumericFormat: "~s", valueAxisTitle: "Berlin Events (Count)", baseAxisTitle: "Week"
      })),
      h("div", { style: { height: 260 } }, h(CartesianChart, {
        instanceId: "itl-ga-cta", title: "Global CTA clicks by week", data: TREND_ROWS, baseAxisField: "week_label", valueAxisField: "cta_clicks",
        baseAxisCategoricalOrder: TREND_WEEKS, dataLabelsVisible: true, valueAxisNumericFormat: "~s", valueAxisTitle: "CTA Clicks (Count)", baseAxisTitle: "Week"
      })),
      h("div", { style: { height: 260 } }, h(CartesianChart, {
        instanceId: "itl-ga-trials", title: "Trial-start proxy by week", data: TREND_ROWS, baseAxisField: "week_label", valueAxisField: "trial_starts",
        baseAxisCategoricalOrder: TREND_WEEKS, dataLabelsVisible: true, valueAxisNumericFormat: "~s", valueAxisTitle: "Trial Starts (Count)", baseAxisTitle: "Week"
      })),
      h("div", { style: { height: 260 } }, h(CartesianChart, {
        instanceId: "itl-ga-youtube", title: "YouTube to n8n.io events by week", data: TREND_ROWS, baseAxisField: "week_label", valueAxisField: "youtube_referrer_events",
        baseAxisCategoricalOrder: TREND_WEEKS, dataLabelsVisible: true, valueAxisNumericFormat: "~s", valueAxisTitle: "YouTube Referrer Events (Count)", baseAxisTitle: "Week"
      })),
      h("div", { style: { height: 260 } }, h(CartesianChart, {
        instanceId: "itl-ga-pages", title: "ITL page views by week", data: TREND_ROWS, baseAxisField: "week_label", valueAxisField: "itl_page_views",
        baseAxisCategoricalOrder: TREND_WEEKS, dataLabelsVisible: true, valueAxisNumericFormat: "~s", valueAxisTitle: "Page Views (Count)", baseAxisTitle: "Week"
      }))),
    h("p", { style: muted }, "ITL page views peak before the event and fall afterwards."));

  return h("div", { className: "app-container", style: { display: "flex", flexDirection: "column", gap: "var(--space-8)" } },
    bannerEl,
    headerEl,
    kpiEl,
    h("p", { style: muted }, "Currency: Salesforce Opportunity.Amount as stored (shown in $). Physical headcount is door scans, not campaign members."),
    daysEl,
    staffEl,
    speakersEl,
    funnelEl,
    registrantsEl,
    rolesEl,
    pipelineEl,
    attributionEl,
    groupsEl,
    gaEl);
}

render(h(App));
