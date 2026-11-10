import * as React from "react";
import "app/app.css";
import { render } from "app/_data.js";

/* Crash-proof Generative Preview: no JSX, no hooks, no Hex chart components.
   Hex compiles some files to React.createElement and does not inject a React global.
   import * as React binds the name the bundler expects. */

function n(v) {
  return Number(v).toLocaleString("en-US");
}

function tile(value, label, hint, accent) {
  return React.createElement(
    "div",
    { key: label, style: { border: "1px solid #E5E7EB", borderRadius: 10, padding: 16, background: "#fff" } },
    React.createElement("div", { style: { fontSize: 32, fontWeight: 700, color: accent ? "#FF6D5A" : "#111827" } }, value),
    React.createElement("div", { style: { marginTop: 8, fontWeight: 600, color: "#6B7280", fontSize: 13 } }, label),
    React.createElement("div", { style: { marginTop: 4, fontSize: 11, color: "#9CA3AF" } }, hint)
  );
}

function App() {
  return React.createElement(
    "div",
    {
      className: "app-container",
      style: { padding: 24, fontFamily: "Inter, sans-serif", display: "flex", flexDirection: "column", gap: 20, maxWidth: 1100 }
    },
    React.createElement("div", { style: { fontSize: 12, fontWeight: 700, letterSpacing: "0.08em", color: "#FF6D5A" } }, "IN THE LOOP 2026"),
    React.createElement("h1", { style: { margin: 0, fontSize: 28 } }, "Conference visits"),
    React.createElement("p", { style: { margin: 0, color: "#6B7280" } }, "Fliplet door scans. People who came both days are counted on both days."),
    React.createElement(
      "div",
      { style: { display: "grid", gridTemplateColumns: "repeat(4, minmax(140px, 1fr))", gap: 12 } },
      tile(n(1269), "Registered", "Paid + Free, unique email", false),
      tile(n(391), "Partner Day visits", "13 Oct door scans", true),
      tile(n(878), "Ecosystem Day visits", "14 Oct door scans", true),
      tile(n(39), "CAB overlay", "All 39 redeemed", false)
    ),
    React.createElement(
      "div",
      { style: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 } },
      React.createElement(
        "div",
        { style: { border: "1px solid #E5E7EB", borderRadius: 10, padding: 18, background: "#fff" } },
        React.createElement("div", { style: { fontSize: 14, color: "#6B7280", fontWeight: 600 } }, "PARTNER DAY · 13 OCT"),
        React.createElement("div", { style: { fontSize: 44, fontWeight: 700, color: "#FF6D5A" } }, n(391)),
        React.createElement("div", { style: { marginTop: 10, color: "#6B7280", fontSize: 13 } }, "487 had a ticket for this day")
      ),
      React.createElement(
        "div",
        { style: { border: "1px solid #E5E7EB", borderRadius: 10, padding: 18, background: "#fff" } },
        React.createElement("div", { style: { fontSize: 14, color: "#6B7280", fontWeight: 600 } }, "ECOSYSTEM DAY · 14 OCT"),
        React.createElement("div", { style: { fontSize: 44, fontWeight: 700, color: "#FF6D5A" } }, n(878)),
        React.createElement("div", { style: { marginTop: 10, color: "#6B7280", fontSize: 13 } }, "1,205 had a ticket for this day")
      )
    ),
    React.createElement(
      "div",
      { style: { display: "grid", gridTemplateColumns: "repeat(3, minmax(140px, 1fr))", gap: 12 } },
      tile(n(113), "Staff tickets", "Fliplet Ticket family = Staff", false),
      tile(n(116), "Programme speakers", "62 Partner Day · 79 Eco Day", false),
      tile(n(39), "CAB", "11 members · 28 guests", false)
    ),
    React.createElement(
      "p",
      { style: { margin: 0, color: "#6B7280", fontSize: 13, padding: 12, background: "#F9FAFB", border: "1px solid #E5E7EB", borderRadius: 8 } },
      "272 people visited both days, so they appear in Partner Day and Ecosystem Day. There is no either-day unique."
    )
  );
}

render(React.createElement(App));
