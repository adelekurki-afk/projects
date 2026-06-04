import {
  Activity,
  ArrowUpRight,
  BarChart3,
  CircleDollarSign,
  MousePointerClick,
  Sparkles,
  Target,
  Users,
} from 'lucide-react'
import type { ComponentType } from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

type IconComponent = ComponentType<{
  className?: string
  size?: number
  strokeWidth?: number
}>

type Kpi = {
  label: string
  value: string
  change: string
  helper: string
  icon: IconComponent
}

const kpis: Kpi[] = [
  {
    label: 'Influenced pipeline',
    value: '$1.84M',
    change: '+18.6%',
    helper: 'Salesforce opportunity influence',
    icon: CircleDollarSign,
  },
  {
    label: 'Avg. success rate',
    value: '54.8%',
    change: '+7.4 pts',
    helper: 'Converted member rate',
    icon: Target,
  },
  {
    label: 'Campaign members',
    value: '14,820',
    change: '+2,310',
    helper: 'Net new members this quarter',
    icon: Users,
  },
  {
    label: 'ROI multiple',
    value: '4.8x',
    change: '+0.9x',
    helper: 'Closed-won revenue / spend',
    icon: BarChart3,
  },
]

const successByType = [
  { type: 'ABM', rate: 68, fill: '#8b5cf6' },
  { type: 'Webinar', rate: 61, fill: '#06b6d4' },
  { type: 'Nurture', rate: 54, fill: '#22c55e' },
  { type: 'Partner', rate: 49, fill: '#f59e0b' },
  { type: 'Event', rate: 43, fill: '#ec4899' },
  { type: 'Paid Social', rate: 38, fill: '#64748b' },
]

const activityMix = [
  { label: 'Email replies', value: '42%', color: 'bg-violet-400' },
  { label: 'Meetings booked', value: '27%', color: 'bg-cyan-400' },
  { label: 'Content clicks', value: '19%', color: 'bg-emerald-400' },
  { label: 'Form fills', value: '12%', color: 'bg-amber-300' },
]

const rollupRows = [
  ['ABM', '2,480', '68%', '$690K', '6.1x'],
  ['Webinar', '3,220', '61%', '$420K', '4.9x'],
  ['Nurture', '4,810', '54%', '$310K', '3.8x'],
  ['Partner', '1,340', '49%', '$265K', '4.2x'],
  ['Event', '1,060', '43%', '$110K', '2.7x'],
]

const topCampaigns = [
  ['Dreamforce ABM acceleration', '$420K', '74%', '312'],
  ['Healthcare CIO webinar', '$286K', '66%', '529'],
  ['Partner cloud migration sprint', '$244K', '58%', '188'],
  ['Q2 enterprise nurture', '$196K', '51%', '2,104'],
]

function KpiCard({ kpi }: { kpi: Kpi }) {
  const Icon = kpi.icon

  return (
    <article className="rounded-3xl border border-white/10 bg-white/[0.06] p-5 shadow-2xl shadow-slate-950/30 backdrop-blur">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm text-slate-400">{kpi.label}</p>
          <p className="mt-3 text-3xl font-semibold tracking-tight text-white">{kpi.value}</p>
        </div>
        <div className="rounded-2xl border border-violet-300/20 bg-violet-400/10 p-3 text-violet-200">
          <Icon size={22} strokeWidth={1.8} />
        </div>
      </div>
      <div className="mt-5 flex items-center justify-between gap-3 text-sm">
        <span className="inline-flex items-center gap-1 rounded-full bg-emerald-400/10 px-3 py-1 font-medium text-emerald-300">
          <ArrowUpRight size={14} />
          {kpi.change}
        </span>
        <span className="text-right text-slate-500">{kpi.helper}</span>
      </div>
    </article>
  )
}

function DataTable({
  title,
  headers,
  rows,
}: {
  title: string
  headers: string[]
  rows: string[][]
}) {
  return (
    <section className="rounded-3xl border border-white/10 bg-slate-900/80 p-5 shadow-2xl shadow-slate-950/30">
      <h2 className="text-lg font-semibold text-white">{title}</h2>
      <div className="mt-4 overflow-x-auto">
        <table className="w-full min-w-[520px] border-separate border-spacing-y-2 text-left text-sm">
          <thead className="text-xs uppercase tracking-[0.22em] text-slate-500">
            <tr>
              {headers.map((header) => (
                <th key={header} className="px-3 py-2 font-medium">
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row[0]} className="rounded-2xl bg-white/[0.04] text-slate-300">
                {row.map((cell, index) => (
                  <td
                    key={`${row[0]}-${cell}`}
                    className={`px-3 py-3 ${index === 0 ? 'rounded-l-2xl font-medium text-white' : ''} ${
                      index === row.length - 1 ? 'rounded-r-2xl' : ''
                    }`}
                  >
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

function App() {
  return (
    <main className="min-h-screen bg-[#060814] px-4 py-6 text-slate-200 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-[1200px]">
        <header className="overflow-hidden rounded-[2rem] border border-white/10 bg-[radial-gradient(circle_at_top_left,_rgba(139,92,246,0.35),_transparent_34%),linear-gradient(135deg,_rgba(15,23,42,0.96),_rgba(2,6,23,0.96))] p-6 shadow-2xl shadow-violet-950/20 sm:p-8">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <div className="inline-flex items-center gap-2 rounded-full border border-violet-300/20 bg-violet-300/10 px-3 py-1 text-sm text-violet-100">
                <Sparkles size={15} />
                Salesforce campaign snapshot
              </div>
              <h1 className="mt-5 text-4xl font-semibold tracking-tight text-white sm:text-5xl">
                Salesforce campaign performance
              </h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-400">
                Dark-mode executive dashboard using Salesforce campaign, campaign member,
                and opportunity influence values. Data is static mock data for now.
              </p>
            </div>
            <div className="rounded-3xl border border-white/10 bg-white/[0.06] p-4 text-sm text-slate-300">
              <p className="text-slate-500">Reporting window</p>
              <p className="mt-1 text-lg font-semibold text-white">Q2 FY26</p>
              <p className="mt-3 text-slate-400">Updated from Salesforce export</p>
            </div>
          </div>
        </header>

        <section className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {kpis.map((kpi) => (
            <KpiCard key={kpi.label} kpi={kpi} />
          ))}
        </section>

        <section className="mt-6 grid gap-6 lg:grid-cols-[1.45fr_0.9fr]">
          <article className="rounded-3xl border border-white/10 bg-slate-900/80 p-5 shadow-2xl shadow-slate-950/30">
            <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-lg font-semibold text-white">Campaign type success</h2>
                <p className="text-sm text-slate-500">Converted member rate by campaign type</p>
              </div>
              <span className="rounded-full bg-cyan-400/10 px-3 py-1 text-sm font-medium text-cyan-200">
                Recharts
              </span>
            </div>
            <div className="mt-6 h-72">
              <ResponsiveContainer width="100%" height="100%" minWidth={0}>
                <BarChart data={successByType} margin={{ top: 10, right: 8, left: -18, bottom: 0 }}>
                  <CartesianGrid stroke="#1f2937" strokeDasharray="4 4" vertical={false} />
                  <XAxis dataKey="type" stroke="#64748b" tickLine={false} axisLine={false} />
                  <YAxis stroke="#64748b" tickLine={false} axisLine={false} tickFormatter={(value) => `${value}%`} />
                  <Tooltip
                    cursor={{ fill: 'rgba(148, 163, 184, 0.08)' }}
                    contentStyle={{
                      background: '#0f172a',
                      border: '1px solid rgba(255,255,255,0.12)',
                      borderRadius: '16px',
                      color: '#e2e8f0',
                    }}
                    formatter={(value) => [`${value}%`, 'Success rate']}
                  />
                  <Bar dataKey="rate" radius={[12, 12, 4, 4]}>
                    {successByType.map((entry) => (
                      <Cell key={entry.type} fill={entry.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </article>

          <div className="grid gap-6">
            <article className="rounded-3xl border border-violet-300/20 bg-violet-400/10 p-5 shadow-2xl shadow-violet-950/20">
              <div className="flex items-center gap-3">
                <div className="rounded-2xl bg-violet-300/15 p-3 text-violet-100">
                  <Sparkles size={21} />
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-white">Insight card</h2>
                  <p className="text-sm text-violet-200/70">Pipeline quality signal</p>
                </div>
              </div>
              <p className="mt-5 text-sm leading-7 text-violet-50/85">
                ABM campaigns generate the strongest Salesforce opportunity influence at 6.1x
                ROI. Shift nurture follow-ups toward accounts that attended webinars and have
                open Stage 2+ opportunities.
              </p>
            </article>

            <article className="rounded-3xl border border-white/10 bg-slate-900/80 p-5 shadow-2xl shadow-slate-950/30">
              <div className="flex items-center gap-3">
                <div className="rounded-2xl bg-cyan-400/10 p-3 text-cyan-200">
                  <Activity size={21} />
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-white">Activity mix</h2>
                  <p className="text-sm text-slate-500">Salesforce campaign member engagement</p>
                </div>
              </div>
              <div className="mt-5 space-y-4">
                {activityMix.map((item) => (
                  <div key={item.label}>
                    <div className="mb-2 flex justify-between text-sm">
                      <span className="text-slate-300">{item.label}</span>
                      <span className="font-medium text-white">{item.value}</span>
                    </div>
                    <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                      <div className={`h-full rounded-full ${item.color}`} style={{ width: item.value }} />
                    </div>
                  </div>
                ))}
              </div>
            </article>
          </div>
        </section>

        <section className="mt-6 grid gap-6 xl:grid-cols-2">
          <DataTable
            title="Campaign type rollup"
            headers={['Type', 'Members', 'Success', 'Pipeline', 'ROI']}
            rows={rollupRows}
          />
          <DataTable
            title="Top campaigns"
            headers={['Campaign', 'Pipeline', 'Success', 'Members']}
            rows={topCampaigns}
          />
        </section>

        <section className="mt-6 rounded-3xl border border-dashed border-white/15 bg-white/[0.04] p-5">
          <div className="flex items-start gap-3">
            <div className="rounded-2xl bg-emerald-400/10 p-3 text-emerald-200">
              <MousePointerClick size={21} />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-white">Method notes</h2>
              <p className="mt-2 text-sm leading-7 text-slate-400">
                Mock values are modeled as if exported from Salesforce Campaigns, Campaign
                Members, Campaign Influence, Opportunities, and Tasks. Success rate is converted
                members divided by total members; ROI compares closed-won influenced revenue to
                campaign spend.
              </p>
            </div>
          </div>
        </section>
      </div>
    </main>
  )
}

export default App
