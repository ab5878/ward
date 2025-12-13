{
  "meta": {
    "product": "Ward v0 — Logistics Disruption Decision Support",
    "purpose": "Crisis-time decision structuring (not planning). Enforce 6-step protocol with accountability and auditability.",
    "audience": "Logistics operations managers under time pressure",
    "brand_attributes": ["operational", "accountable", "clear", "evidence-driven", "calm-under-pressure"],
    "design_style": "Functional Minimalism + Swiss/Operations Room aesthetic (solid surfaces, high-contrast UI, no visual noise)."
  },
  "color_system": {
    "principles": [
      "Neutral base for content surfaces",
      "High-contrast text (WCAG AA minimum)",
      "Alert colors reserved for risk, warnings, overrides",
      "No transparent backgrounds; all surfaces solid",
      "Use gradients only in section backgrounds if needed, never in content blocks"
    ],
    "tokens_hsl_for_index_css_root": {
      "--background": "210 20% 99%",
      "--foreground": "217 33% 12%",
      "--card": "0 0% 100%",
      "--card-foreground": "217 33% 12%",
      "--popover": "0 0% 100%",
      "--popover-foreground": "217 33% 12%",
      "--primary": "205 61% 34%", 
      "--primary-foreground": "0 0% 98%",
      "--secondary": "210 16% 94%",
      "--secondary-foreground": "217 33% 12%",
      "--accent": "210 16% 94%",
      "--accent-foreground": "217 33% 12%",
      "--muted": "213 16% 92%",
      "--muted-foreground": "215 16% 35%",
      "--destructive": "4 74% 45%",
      "--destructive-foreground": "0 0% 98%",
      "--warning": "28 90% 54%",
      "--warning-foreground": "20 16% 12%",
      "--success": "146 46% 35%",
      "--success-foreground": "0 0% 98%",
      "--info": "201 96% 32%",
      "--info-foreground": "0 0% 98%",
      "--border": "210 16% 85%",
      "--input": "210 16% 85%",
      "--ring": "205 61% 34%",
      "--radius": "0.5rem",
      "--shadow-elev-1": "0 1px 2px rgba(16,24,40,0.06), 0 1px 3px rgba(16,24,40,0.10)",
      "--shadow-elev-2": "0 4px 8px rgba(16,24,40,0.08), 0 2px 4px rgba(16,24,40,0.08)"
    },
    "dark_mode_overrides_hsl": {
      "--background": "220 10% 7%",
      "--foreground": "0 0% 98%",
      "--card": "220 10% 10%",
      "--card-foreground": "0 0% 98%",
      "--primary": "205 61% 52%",
      "--primary-foreground": "220 10% 10%",
      "--secondary": "220 8% 16%",
      "--secondary-foreground": "0 0% 98%",
      "--muted": "220 8% 16%",
      "--muted-foreground": "220 6% 70%",
      "--destructive": "4 74% 52%",
      "--warning": "28 90% 60%",
      "--success": "146 46% 42%",
      "--info": "201 96% 46%",
      "--border": "220 8% 18%",
      "--input": "220 8% 18%",
      "--ring": "205 61% 52%"
    },
    "semantic_usage": {
      "text_primary": "text-foreground",
      "text_muted": "text-[hsl(var(--muted-foreground))]",
      "surface": "bg-background",
      "card_surface": "bg-card",
      "border": "border-[hsl(var(--border))]",
      "cta": "bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))]",
      "success": "bg-[hsl(var(--success))] text-[hsl(var(--success-foreground))]",
      "warning": "bg-[hsl(var(--warning))] text-[hsl(var(--warning-foreground))]",
      "danger": "bg-[hsl(var(--destructive))] text-[hsl(var(--destructive-foreground))]",
      "info": "bg-[hsl(var(--info))] text-[hsl(var(--info-foreground))]"
    }
  },
  "typography": {
    "fonts": {
      "heading": "\"Space Grotesk\", ui-sans-serif, system-ui, -apple-system, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial",
      "body": "\"IBM Plex Sans\", ui-sans-serif, system-ui, -apple-system, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial",
      "mono": "\"Source Code Pro\", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas"
    },
    "import": {
      "google_fonts_links": [
        "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&display=swap",
        "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap"
      ],
      "apply": "body { font-family: var(--font-body); } h1,h2,h3,h4 { font-family: var(--font-heading); }"
    },
    "css_vars": {
      "--font-heading": "Space Grotesk",
      "--font-body": "IBM Plex Sans"
    },
    "scale": {
      "h1": "text-4xl sm:text-5xl lg:text-6xl",
      "h2": "text-base md:text-lg",
      "body": "text-base md:text-base",
      "small": "text-sm",
      "mono": "font-mono text-sm"
    },
    "usage": {
      "critical_numbers": "tabular-nums tracking-tight text-[hsl(var(--foreground))]",
      "labels": "text-xs uppercase tracking-wider text-[hsl(var(--muted-foreground))]"
    }
  },
  "layout": {
    "container": "mx-auto px-4 sm:px-6 lg:px-8",
    "grid": {
      "dashboard": "grid grid-cols-1 lg:grid-cols-12 gap-4 lg:gap-6",
      "editor_two_col": "grid grid-cols-1 lg:grid-cols-12 gap-4",
      "col_main": "lg:col-span-8",
      "col_side": "lg:col-span-4"
    },
    "cards": {
      "padding": "p-4 sm:p-5 lg:p-6",
      "radius": "rounded-md",
      "shadow": "shadow-[var(--shadow-elev-1)]"
    }
  },
  "buttons": {
    "style": "Professional / Corporate",
    "shape": "rounded-md",
    "variants": {
      "primary": "bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] hover:bg-[hsl(var(--primary))]/90 focus-visible:ring-2 focus-visible:ring-[hsl(var(--ring))]",
      "secondary": "bg-[hsl(var(--secondary))] text-foreground hover:bg-[hsl(var(--secondary))]/80",
      "ghost": "bg-transparent text-foreground hover:bg-[hsl(var(--secondary))]",
      "danger": "bg-[hsl(var(--destructive))] text-[hsl(var(--destructive-foreground))] hover:bg-[hsl(var(--destructive))]/90",
      "success": "bg-[hsl(var(--success))] text-[hsl(var(--success-foreground))] hover:bg-[hsl(var(--success))]/90"
    },
    "sizes": {
      "sm": "h-9 px-3 text-sm",
      "md": "h-10 px-4 text-sm",
      "lg": "h-11 px-5 text-base"
    },
    "motion": "transition-colors duration-150"
  },
  "pages": {
    "login_register": {
      "layout": "single column centered form, no marketing; solid card with title, inputs, submit",
      "components": ["./components/ui/card", "./components/ui/input", "./components/ui/label", "./components/ui/button", "./components/ui/alert"],
      "states": ["loading: disable submit", "error: alert with data-testid=\"auth-error-alert\""]
    },
    "dashboard": {
      "layout": "12-column grid; left: Active Disruptions list (lg:8), right: Recent Decisions/Audit highlights (lg:4)",
      "modules": [
        "KPI strip (Delayed Shipments, At-Risk Routes, Pending Approvals)",
        "Active Disruptions table/cards",
        "Recent Decisions timeline"
      ],
      "components": ["./components/ui/card", "./components/ui/badge", "./components/ui/table", "./components/ui/tooltip", "./components/ui/skeleton", "./components/ui/sonner"]
    },
    "create_disruption": {
      "layout": "form in card; left meta fields, right evidence and shipment selector",
      "components": ["./components/ui/form", "./components/ui/input", "./components/ui/textarea", "./components/ui/select", "./components/ui/badge", "./components/ui/button", "./components/ui/calendar"]
    },
    "decision_editor": {
      "layout": "Two-column: left vertical 6-step sections; right sidebar with Evidence, Risk Meter, and Actions",
      "sections": ["Decision Framing", "Known Inputs", "Assumptions", "Alternatives", "Risk Analysis", "Recommendation"],
      "components": [
        "./components/ui/accordion",
        "./components/ui/textarea",
        "./components/ui/badge",
        "./components/ui/radio-group",
        "./components/ui/card",
        "./components/ui/alert",
        "./components/ui/button",
        "./components/ui/separator",
        "./components/ui/skeleton",
        "./components/ui/progress",
        "./components/ui/tooltip"
      ],
      "critical_rules": [
        "Max 3 alternatives visible",
        "Worst-case shown first with destructive styling",
        "Clear Locked vs Unlocked section states",
        "Mandatory approval per section before lock"
      ]
    },
    "audit_trail": {
      "layout": "Full-width timeline with filters; table fallback",
      "components": ["./components/ui/select", "./components/ui/calendar", "./components/ui/input", "./components/ui/table", "./components/ui/separator", "./components/ui/badge", "./components/ui/tooltip", "./components/ui/button"]
    },
    "historical_disruptions": {
      "layout": "Read-only list/table with filters; link to details",
      "components": ["./components/ui/table", "./components/ui/select", "./components/ui/badge", "./components/ui/input"]
    }
  },
  "key_components": {
    "section_header": {
      "purpose": "Display step number, title, status badge, lock icon, and Approve/Lock button",
      "structure": "flex justify-between items-center py-3 border-b",
      "states": [
        "pending: neutral",
        "approved: success badge + lock icon",
        "locked: gray background, pointer-events-none on fields"
      ],
      "testids": [
        "data-testid=\"section-<step>-approve-button\"",
        "data-testid=\"section-<step>-lock-indicator\"",
        "data-testid=\"section-<step>-status-badge\""
      ]
    },
    "evidence_badge": {
      "elements": ["source", "freshness (age)", "reliability"],
      "style": "compact badges inline; muted background; tooltip with full metadata",
      "badge_colors": {
        "fresh": "success",
        "stale": "warning",
        "low_reliability": "destructive"
      },
      "testids": ["data-testid=\"evidence-badge\""]
    },
    "alternatives_card": {
      "layout": "Card with radio at top-left, title, brief, worst-case prominently; risk chips",
      "rules": ["show at most 3", "first line: worst-case in red/amber", "radio required"],
      "testids": [
        "data-testid=\"alternative-card\"",
        "data-testid=\"alternative-select-radio\"",
        "data-testid=\"alternative-worst-case\""
      ]
    },
    "override_modal": {
      "trigger": "If non-recommended alternative chosen or unlocking a locked section",
      "fields": [
        "Reason taxonomy (Select)",
        "Free-text justification (Textarea, min 50 chars)",
        "Evidence upload (future)",
        "Compensating controls (Textarea)"
      ],
      "actions": ["Confirm Override", "Cancel"],
      "testids": [
        "data-testid=\"override-reason-select\"",
        "data-testid=\"override-justification-textarea\"",
        "data-testid=\"override-confirm-button\""
      ]
    },
    "risk_alert": {
      "usage": "Use Alert (destructive or warning) with bold title and concise copy",
      "testids": ["data-testid=\"risk-alert\""]
    }
  },
  "component_path": {
    "button": "./components/ui/button",
    "badge": "./components/ui/badge",
    "card": "./components/ui/card",
    "textarea": "./components/ui/textarea",
    "select": "./components/ui/select",
    "radio_group": "./components/ui/radio-group",
    "accordion": "./components/ui/accordion",
    "alert": "./components/ui/alert",
    "table": "./components/ui/table",
    "tooltip": "./components/ui/tooltip",
    "skeleton": "./components/ui/skeleton",
    "progress": "./components/ui/progress",
    "calendar": "./components/ui/calendar",
    "sonner": "./components/ui/sonner"
  },
  "micro_interactions": {
    "rules": [
      "Never use transition: all; use transition-colors, transition-opacity, etc.",
      "Buttons: subtle shade shift and focus ring",
      "Cards: hover:shadow-md only on non-critical lists",
      "Lock/Unlock: animate lock icon scale-95 -> 100 with framer-motion",
      "Editor save: toast via sonner with role and timestamp"
    ],
    "examples_tailwind": {
      "button": "transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[hsl(var(--ring))]",
      "card_hover": "hover:shadow-lg"
    }
  },
  "data_testid": {
    "convention": "kebab-case that defines role not appearance",
    "examples": [
      "data-testid=\"generate-structure-button\"",
      "data-testid=\"section-1-approve-button\"",
      "data-testid=\"final-decision-submit-button\"",
      "data-testid=\"audit-filter-apply-button\"",
      "data-testid=\"error-message\""
    ]
  },
  "risk_and_states": {
    "locked_state": {
      "style": "bg-[hsl(var(--secondary))] border border-[hsl(var(--border))] opacity-90",
      "affordance": "show lock icon + tooltip: 'Locked on <datetime> by <actor>'",
      "inputs": "set readOnly and aria-readonly"
    },
    "warning_danger": {
      "worst_case": "use destructive alert with leading icon; text-sm; bold label",
      "badges": {
        "critical": "bg-[hsl(var(--destructive))] text-white",
        "high": "bg-[hsl(var(--warning))] text-[hsl(var(--warning-foreground))]",
        "medium": "bg-[hsl(var(--info))] text-white",
        "low": "bg-[hsl(var(--muted))] text-[hsl(var(--foreground))]"
      }
    },
    "success_approved": {
      "indicator": "small success badge + lock icon",
      "section_border": "border-l-4 border-l-[hsl(var(--success))]"
    }
  },
  "snippets_jsx": {
    "decision_section_card": "export const DecisionSection = ({ step, title, locked, value, onChange, onApprove }) => (\n  <div className={\`rounded-md border bg-card ${locked ? 'opacity-90' : ''}\`}>\n    <div className=\"flex items-center justify-between px-4 py-3 border-b\">\n      <div className=\"flex items-center gap-3\">\n        <span className=\"text-xs font-medium px-2 py-1 rounded bg-[hsl(var(--secondary))]\">Step {step}</span>\n        <h3 className=\"text-sm md:text-base font-semibold\">{title}</h3>\n        {locked && <span aria-label=\"locked\" className=\"text-[hsl(var(--success))]\">\uD83D\uDD12</span>}\n      </div>\n      <div className=\"flex items-center gap-2\">\n        <button data-testid=\"section-approve-button\" onClick={onApprove} className=\"h-9 px-3 rounded-md bg-[hsl(var(--success))] text-white hover:bg-[hsl(var(--success))]/90 transition-colors\">Approve & Lock</button>\n      </div>\n    </div>\n    <div className=\"p-4\">\n      <textarea\n        data-testid=\"section-editor-textarea\"\n        className=\"w-full min-h-[140px] rounded-md border p-3 text-sm\"\n        readOnly={locked}\n        value={value}\n        onChange={(e) => onChange?.(e.target.value)}\n      />\n      {locked && <p className=\"mt-2 text-xs text-[hsl(var(--muted-foreground))]\">This section is locked. Edits require an override.</p>}\n    </div>\n  </div>\n)\n",
    "alternatives_group": "export const AlternativesGroup = ({ options, selected, onSelect }) => (\n  <div className=\"grid gap-3\">\n    {options.slice(0,3).map((opt, idx) => (\n      <div key={opt.id} data-testid=\"alternative-card\" className=\"rounded-md border p-4\">\n        <div className=\"flex items-start gap-3\">\n          <input data-testid=\"alternative-select-radio\" type=\"radio\" name=\"alt\" checked={selected===opt.id} onChange={() => onSelect(opt.id)} className=\"mt-1\"/>\n          <div className=\"flex-1\">\n            <div className=\"flex items-center justify-between\">\n              <h4 className=\"font-medium\">{opt.title}</h4>\n              <span className=\"text-xs px-2 py-1 rounded bg-[hsl(var(--secondary))]\">Risk: {opt.risk}</span>\n            </div>\n            <p className=\"mt-1 text-sm text-[hsl(var(--muted-foreground))]\">{opt.summary}</p>\n            <div className=\"mt-3\">\n              <div data-testid=\"alternative-worst-case\" className=\"text-sm font-medium text-[hsl(var(--destructive))]\">Worst-case: {opt.worstCase}</div>\n            </div>\n          </div>\n        </div>\n      </div>\n    ))}\n  </div>\n)\n",
    "override_modal_stub": "export const OverrideModal = ({ open, onClose, onConfirm }) => {\n  if (!open) return null;\n  return (\n    <div role=\"dialog\" aria-modal=\"true\" className=\"fixed inset-0 z-50 bg-black/50 flex items-center justify-center\">\n      <div className=\"w-full max-w-lg rounded-md bg-white p-5\">\n        <h3 className=\"text-lg font-semibold\">Provide override rationale</h3>\n        <div className=\"mt-3 grid gap-3\">\n          <select data-testid=\"override-reason-select\" className=\"h-10 rounded-md border px-3\">\n            <option>Time-sensitive</option>\n            <option>Erroneous data</option>\n            <option>Exceptional business need</option>\n            <option>Regulatory waiver</option>\n          </select>\n          <textarea data-testid=\"override-justification-textarea\" minLength={50} placeholder=\"Explain why this override is necessary...\" className=\"min-h-[120px] rounded-md border p-3\"/>\n        </div>\n        <div className=\"mt-4 flex justify-end gap-2\">\n          <button onClick={onClose} className=\"h-10 px-4 rounded-md bg-[hsl(var(--secondary))]\">Cancel</button>\n          <button data-testid=\"override-confirm-button\" onClick={onConfirm} className=\"h-10 px-4 rounded-md bg-[hsl(var(--warning))]\">Confirm Override</button>\n        </div>\n      </div>\n    </div>\n  );\n}\n",
    "generate_loading_block": "export const GenerateLoading = () => (\n  <div className=\"rounded-md border p-4\">\n    <div className=\"flex items-center gap-3\">\n      <div className=\"h-4 w-4 animate-spin rounded-full border-2 border-[hsl(var(--primary))] border-t-transparent\"/>\n      <p className=\"text-sm\">Generating decision structure (5–10s)…</p>\n    </div>\n    <div className=\"mt-3 h-2 w-full overflow-hidden rounded bg-[hsl(var(--secondary))]\">\n      <div className=\"h-full w-1/3 animate-pulse bg-[hsl(var(--primary))]\"/>\n    </div>\n  </div>\n)\n"
  },
  "accessibility": {
    "contrast": "Maintain AA at minimum; destructive/warning alerts must be readable on both themes",
    "keyboard": [
      "Tab order aligns with visual order",
      "Space/Enter activates buttons and radios",
      "Escape closes modals"
    ],
    "aria": [
      "aria-readonly on locked sections",
      "role=alert for risk alerts",
      "aria-busy true on generation loading container"
    ]
  },
  "libraries": {
    "required": [
      {"name": "framer-motion", "why": "micro-interactions (lock/unlock, subtle entrances)", "install": "npm i framer-motion"},
      {"name": "recharts", "why": "risk meter, SLA sparklines", "install": "npm i recharts"},
      {"name": "sonner", "why": "toasts already included", "install": "already in ./components/ui/sonner"}
    ],
    "usage_notes": [
      "Use recharts RadialBarChart for risk score (color by threshold)",
      "Keep motion durations 120–200ms; no bounce"
    ]
  },
  "image_urls": [
    {
      "category": "login_hero",
      "description": "Ops room screens backdrop (subtle, darkened overlay)",
      "url": "https://images.unsplash.com/photo-1642775196125-38a9eb496568?crop=entropy&cs=srgb&fm=jpg&q=85"
    },
    {
      "category": "dashboard_banner",
      "description": "Aerial port containers (masked behind header with low opacity)",
      "url": "https://images.unsplash.com/photo-1724364552281-dbed323c4633?crop=entropy&cs=srgb&fm=jpg&q=85"
    },
    {
      "category": "empty_state",
      "description": "Warehouse loading docks/trucks",
      "url": "https://images.pexels.com/photos/2231743/pexels-photo-2231743.jpeg"
    }
  ],
  "instructions_to_main_agent": [
    "Update /app/frontend/src/index.css :root with tokens_hsl_for_index_css_root and .dark overrides",
    "Import Google Fonts in public/index.html or root layout",
    "Apply heading/body fonts across app",
    "Use shadcn components only for UI primitives; do not use raw HTML for dropdowns, calendars, toasts",
    "Ensure every interactive and key informational element includes a data-testid attribute (kebab-case role names)",
    "Implement decision editor with 6 vertical sections, each card controls its own approve/lock state",
    "Limit alternatives to max 3 and render Worst-case first using destructive styling",
    "On override flow, open OverrideModal; block submit until min 50 chars typed",
    "Use sonner for saved/approved toasts with role + timestamp",
    "No transparent surfaces; use bg-card or bg-background as applicable"
  ],
  "gradient_rules": {
    "restriction": [
      "Never use dark/saturated purple/pink/blue gradients",
      "Gradients cover <20% viewport",
      "No gradients on text-heavy content or small elements"
    ],
    "allowed_use": [
      "Section headers/background dividers",
      "Hero strip (top-only) with very mild blue-gray gradient"
    ],
    "fallback": "If gradient risks readability, revert to solid background"
  },
  "testing_ids_must_have": [
    "generate-structure-button",
    "section-<n>-approve-button",
    "section-<n>-lock-indicator",
    "alternative-card",
    "alternative-select-radio",
    "alternative-worst-case",
    "override-confirm-button",
    "final-decision-submit-button",
    "audit-filter-apply-button",
    "error-message"
  ]
}

<General UI UX Design Guidelines>  
    - You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms
    - You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text
   - NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇 etc for icons. Always use **FontAwesome cdn** or **lucid-react** library already installed in the package.json

 **GRADIENT RESTRICTION RULE**
NEVER use dark/saturated gradient combos (e.g., purple/pink) on any UI element.  Prohibited gradients: blue-500 to purple 600, purple 500 to pink-500, green-500 to blue-500, red to pink etc
NEVER use dark gradients for logo, testimonial, footer etc
NEVER let gradients cover more than 20% of the viewport.
NEVER apply gradients to text-heavy content or reading areas.
NEVER use gradients on small UI elements (<100px width).
NEVER stack multiple gradient layers in the same viewport.

**ENFORCEMENT RULE:**
    • Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors

**How and where to use:**
   • Section backgrounds (not content backgrounds)
   • Hero section header content. Eg: dark to light to dark color
   • Decorative overlays and accent elements only
   • Hero section with 2-3 mild color
   • Gradients creation can be done for any angle say horizontal, vertical or diagonal

- For AI chat, voice application, **do not use purple color. Use color like light green, ocean blue, peach orange etc**

</Font Guidelines>

- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead. 
   
- Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.

- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations: separates good from extraordinary.
   
- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion) and immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors), rather than relying on any library defaults. Don't make the background dark as a default step, always understand problem first and define colors accordingly
    Eg: - if it implies playful/energetic, choose a colorful scheme
           - if it implies monochrome/minimal, choose a black–white/neutral scheme

**Component Reuse:**
	- Prioritize using pre-existing components from src/components/ui when applicable
	- Create new components that match the style and conventions of existing components when needed
	- Examine existing components to understand the project's component patterns before creating new ones

**IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component

**Best Practices:**
	- Use Shadcn/UI as the primary component library for consistency and accessibility
	- Import path: ./components/[component-name]

**Export Conventions:**
	- Components MUST use named exports (export const ComponentName = ...)
	- Pages MUST use default exports (export default function PageName() {...})

**Toasts:**
  - Use `sonner` for toasts"
  - Sonner component are located in `/app/src/components/ui/sonner.tsx`

Use 2–4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals.
</General UI UX Design Guidelines>
