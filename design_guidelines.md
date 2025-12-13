{
  "product_name": "Ward v0 — Disruption Lifecycle Management (India Logistics)",
  "brand_attributes": ["manager-first", "operational", "decisive", "accountable", "India-first", "no-nonsense"],
  "audience_and_goals": {
    "primary_user": "Logistics operations managers and duty leads",
    "key_tasks": [
      "Scan and filter active disruptions by lifecycle state",
      "Assign or reassign disruption ownership with audit trail",
      "Advance lifecycle (only decision owner)",
      "Add timeline context from voice/text/system events with reliability tags",
      "Review multi-source timeline quickly and make decisions"
    ],
    "success_criteria": [
      "Rapid scan-ability of state and owner",
      "Single-click ownership assignment",
      "Clear, unambiguous state transition controls",
      "Reliable, visually distinct timeline by source type and reliability",
      "IST-first timestamps and India logistics vocabulary (ports, customs)"
    ]
  },

  "design_personality": {
    "tone": "Control center — serious, crisp, high-contrast, low ornamentation",
    "style_mix": "Swiss layout discipline + Control-tower dashboards (Grafana/ICEDASH) — no gradients for content, deep neutrals with decisive accents"
  },

  "typography": {
    "fonts": {
      "heading": "Space Grotesk",
      "body": "IBM Plex Sans",
      "fallback": "system-ui, -apple-system, Segoe UI"
    },
    "scale": {
      "h1": "text-4xl sm:text-5xl lg:text-6xl",
      "h2": "text-base md:text-lg",
      "body": "text-base md:text-base",
      "small": "text-sm",
      "micro": "text-xs tracking-wide"
    },
    "usage": {
      "page_titles": "font-semibold tracking-tight",
      "section_labels": "uppercase text-xs tracking-wider text-muted-foreground",
      "numerics": "tabular-nums"
    }
  },

  "color_system": {
    "note": "Use deep, purposeful solids. No decorative gradients on content. Light/dark supported via CSS vars.",
    "semantic_tokens_css_to_add": """
    /* Add to /app/frontend/src/App.css after existing :root blocks */
    :root {
      /* Core neutrals */
      --ink-900: 217 33% 12%; /* deep navy for text */
      --slate-800: 215 25% 17%;
      --slate-700: 215 19% 25%;
      --steel-600: 215 16% 35%;
      --steel-300: 210 16% 85%;

      /* Brand/ops accents (India-first without gimmick) */
      --accent-blue-600: 205 61% 34%; /* primary */
      --accent-blue-500: 205 61% 45%;
      --accent-teal-600: 184 65% 32%;
      --accent-amber-600: 28 90% 54%;
      --accent-green-600: 146 46% 35%;
      --accent-red-600: 4 74% 45%;

      /* Lifecycle state tokens */
      --state-reported: 215 16% 85%;       /* neutral */
      --state-clarified: 205 61% 45%;      /* blue */
      --state-decision-required: 28 90% 54%; /* amber */
      --state-decided: 184 65% 32%;        /* teal */
      --state-in-progress: 201 96% 32%;    /* info blue */
      --state-resolved: 146 46% 35%;       /* green */

      /* Reliability tags */
      --reliability-low: 215 16% 85%;
      --reliability-medium: 28 90% 54%;
      --reliability-high: 146 46% 35%;

      /* Source type */
      --source-text: 215 16% 35%;
      --source-voice: 184 65% 32%;
      --source-system: 201 96% 32%;

      /* Radius tokens */
      --radius-sm: 0.375rem;
      --radius-md: 0.5rem;
      --radius-lg: 0.75rem;

      /* Button tokens */
      --btn-radius: 0.5rem;
      --btn-shadow: 0 1px 0 rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
      --focus-ring: 0 0 0 3px hsl(var(--accent-blue-500) / 0.25);
    }

    .dark {
      --ink-900: 0 0% 98%;
      --slate-800: 220 10% 7%;
      --slate-700: 220 8% 16%;
      --steel-600: 220 6% 70%;
      --steel-300: 220 8% 18%;

      --accent-blue-600: 205 61% 52%;
      --accent-blue-500: 205 61% 52%;
      --accent-teal-600: 184 65% 46%;
      --accent-amber-600: 28 90% 60%;
      --accent-green-600: 146 46% 42%;
      --accent-red-600: 4 74% 52%;
    }

    /* Utility badges for states */
    .state-badge { @apply px-2 py-0.5 rounded-md text-xs font-medium; }
    .state-badge[data-state='REPORTED'] { color: hsl(var(--foreground)); background-color: hsl(var(--state-reported)); }
    .state-badge[data-state='CLARIFIED'] { color: white; background-color: hsl(var(--state-clarified)); }
    .state-badge[data-state='DECISION_REQUIRED'] { color: #141414; background-color: hsl(var(--state-decision-required)); }
    .state-badge[data-state='DECIDED'] { color: white; background-color: hsl(var(--state-decided)); }
    .state-badge[data-state='IN_PROGRESS'] { color: white; background-color: hsl(var(--state-in-progress)); }
    .state-badge[data-state='RESOLVED'] { color: white; background-color: hsl(var(--state-resolved)); }

    /* Reliability chips */
    .reliability-chip { @apply px-1.5 py-0.5 rounded-sm text-[11px] font-medium; }
    .reliability-chip[data-level='low'] { color: hsl(var(--foreground)); background-color: hsl(var(--reliability-low)); }
    .reliability-chip[data-level='medium'] { color: #141414; background-color: hsl(var(--reliability-medium)); }
    .reliability-chip[data-level='high'] { color: white; background-color: hsl(var(--reliability-high)); }

    /* Source icons */
    .source-dot { @apply inline-block w-2 h-2 rounded-full; }
    .source-dot[data-type='text'] { background-color: hsl(var(--source-text)); }
    .source-dot[data-type='voice'] { background-color: hsl(var(--source-voice)); }
    .source-dot[data-type='system'] { background-color: hsl(var(--source-system)); }
    """
  },

  "component_path": {
    "button": "./components/ui/button",
    "badge": "./components/ui/badge",
    "card": "./components/ui/card",
    "tabs": "./components/ui/tabs",
    "table": "./components/ui/table",
    "select": "./components/ui/select",
    "dialog": "./components/ui/dialog",
    "dropdown_menu": "./components/ui/dropdown-menu",
    "tooltip": "./components/ui/tooltip",
    "separator": "./components/ui/separator",
    "scroll_area": "./components/ui/scroll-area",
    "sheet": "./components/ui/sheet",
    "calendar": "./components/ui/calendar",
    "sonner": "./components/ui/sonner"
  },

  "pages_and_layouts": {
    "app_shell": {
      "header": "Sticky top bar with product name, global search, quick filters by state; right cluster: timezone switch (fixed IST default), user menu",
      "nav": "Left rail 264px on desktop (collapsible to icons at 72px). Items: Dashboard, Disruptions, Owners, Audit",
      "content_grid": "Max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-6 gap-6"
    },
    "disruption_list": {
      "layout": "Two-pane optional. Primary: table of disruptions. Secondary (lg+): details preview panel when a row is selected",
      "table_columns": [
        "state_badge", "title", "owner", "last_event_source+reliability", "port/customs", "updated_at (IST)", "actions"
      ],
      "filters": "Tabs for 6 states using shadcn Tabs; additional Select for owner, source type, reliability >=; search input",
      "row_density": "h-12 on desktop, h-14 for touch; hover:bg-secondary/60 focus-visible:ring-2 ring-primary",
      "empty_state": "Crisp card with link to create or import; show image from image_urls.empty_state"
    },
    "disruption_detail": {
      "header": "Title, state badge, owner Select, Assign/Reassign button, timestamp cluster",
      "content_split": "grid grid-cols-1 lg:grid-cols-3 gap-6; timeline spans 2 cols; right rail has state transitions, properties, attachments",
      "timeline": "Scrollable vertical timeline with source markers, reliability chips, and expandable payload; sticky day markers; group by day (IST)",
      "actions_panel": "Visible only to decision owner: primary Transition button(s) + confirmation dialog; others see disabled with tooltip"
    }
  },

  "component_specs": {
    "DisruptionRow.js": {
      "import_paths": ["button", "badge", "tooltip", "dropdown_menu"],
      "snippet": """
      import React from 'react'
      import { Badge } from './components/ui/badge'
      import { Button } from './components/ui/button'
      import { Tooltip, TooltipTrigger, TooltipContent } from './components/ui/tooltip'
      import { MoreHorizontal, Phone, MessageSquareText, Server } from 'lucide-react'

      export const DisruptionRow = ({ item, onSelect, onAssign }) => {
        const SourceIcon = item.lastSource === 'voice' ? Phone : item.lastSource === 'system' ? Server : MessageSquareText
        return (
          <tr data-testid={`disruption-row-${item.id}`} className="group hover:bg-secondary/60">
            <td className="whitespace-nowrap"><span className="state-badge" data-state={item.state}>{item.state.replace('_',' ')}</span></td>
            <td className="font-medium text-foreground/90">{item.title}</td>
            <td><Badge variant="secondary" data-testid="owner-badge">{item.owner?.name || 'Unassigned'}</Badge></td>
            <td className="flex items-center gap-2">
              <SourceIcon className="w-4 h-4 text-muted-foreground" aria-hidden />
              <span className="reliability-chip" data-level={item.reliability}>{item.reliability}</span>
            </td>
            <td className="text-muted-foreground tabular-nums">{item.location}</td>
            <td className="text-muted-foreground tabular-nums">{item.updatedAtIST}</td>
            <td className="text-right">
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button data-testid="row-open-button" size="sm" variant="outline" onClick={() => onSelect(item.id)}>Open</Button>
                </TooltipTrigger>
                <TooltipContent>Open details</TooltipContent>
              </Tooltip>
            </td>
          </tr>
        )
      }
      """
    },
    "TimelineEvent.js": {
      "import_paths": ["card", "badge", "tooltip", "separator"],
      "snippet": """
      import React from 'react'
      import { Card } from './components/ui/card'
      import { Separator } from './components/ui/separator'
      import { Phone, MessageSquareText, Server } from 'lucide-react'

      export const TimelineEvent = ({ evt }) => {
        const Icon = evt.source === 'voice' ? Phone : evt.source === 'system' ? Server : MessageSquareText
        return (
          <div className="grid grid-cols-[20px_1fr] gap-3" data-testid={`timeline-event-${evt.id}`}>
            <div className="relative flex justify-center">
              <span className="source-dot" data-type={evt.source} />
            </div>
            <Card className="p-3 shadow-sm">
              <div className="flex items-center gap-2 text-xs text-muted-foreground tabular-nums">
                <Icon className="w-3.5 h-3.5" aria-hidden />
                <span>{evt.atIST}</span>
                <span>•</span>
                <span className="reliability-chip" data-level={evt.reliability}>{evt.reliability}</span>
                {evt.author && <span>• by {evt.author}</span>}
              </div>
              <Separator className="my-2" />
              <div className="text-sm leading-relaxed text-foreground/90">{evt.summary}</div>
              {evt.payload && <pre className="mt-2 bg-secondary/60 p-2 rounded-md text-xs overflow-x-auto" data-testid="timeline-payload">{evt.payload}</pre>}
            </Card>
          </div>
        )
      }
      """
    },
    "StateTransitionBar.js": {
      "import_paths": ["button", "dialog", "sonner"],
      "snippet": """
      import React from 'react'
      import { Button } from './components/ui/button'
      import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogFooter } from './components/ui/dialog'
      import { toast } from './components/ui/sonner'

      export const StateTransitionBar = ({ currentState, nextStates, canAdvance, onAdvance }) => {
        if (!canAdvance) {
          return (
            <div className="text-sm text-muted-foreground" data-testid="transition-guard">Only the decision owner can advance the state.</div>
          )
        }
        return (
          <div className="flex flex-wrap gap-2" data-testid="transition-actions">
            {nextStates.map(ns => (
              <Dialog key={ns}>
                <DialogTrigger asChild>
                  <Button data-testid={`advance-to-${ns}-button`} size="sm" className="font-medium">Advance to {ns.replace('_',' ')}</Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Confirm transition</DialogTitle>
                  </DialogHeader>
                  <p className="text-sm">Move from {currentState.replace('_',' ')} to {ns.replace('_',' ')}?</p>
                  <DialogFooter>
                    <Button variant="outline">Cancel</Button>
                    <Button
                      data-testid="confirm-transition-button"
                      onClick={() => { onAdvance(ns); toast.success(`State advanced to ${ns}`) }}
                    >Confirm</Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            ))}
          </div>
        )
      }
      """
    },
    "OwnershipAssigner.js": {
      "import_paths": ["select", "button"],
      "snippet": """
      import React from 'react'
      import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from './components/ui/select'
      import { Button } from './components/ui/button'

      export const OwnershipAssigner = ({ owners, value, onChange, onSubmit }) => (
        <div className="flex gap-2 items-center" data-testid="ownership-assigner">
          <Select value={value} onValueChange={onChange}>
            <SelectTrigger className="w-56" data-testid="owner-select-trigger">
              <SelectValue placeholder="Assign owner" />
            </SelectTrigger>
            <SelectContent>
              {owners.map(o => <SelectItem key={o.id} value={o.id}>{o.name}</SelectItem>)}
            </SelectContent>
          </Select>
          <Button data-testid="assign-owner-button" onClick={onSubmit}>Assign</Button>
        </div>
      )
      """
    }
  },

  "motion_and_micro_interactions": {
    "principles": [
      "Functional first; micro-animations only for affordance",
      "No transition: all; only specific properties (color, background-color, box-shadow, opacity, transform)"
    ],
    "examples_tailwind": {
      "buttons": "transition-colors duration-150 disabled:opacity-60 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 ring-offset-background",
      "rows": "transition-colors",
      "cards": "transition-shadow hover:shadow-md"
    },
    "optional_lib": {
      "framer_motion": {
        "install": "npm i framer-motion",
        "usage": "Use small motion.div for row entrance (opacity 0->1, y 4->0, 120ms, stagger 20ms)."
      }
    }
  },

  "accessibility": {
    "contrast": "Ensure WCAG AA (4.5:1) across all text on backgrounds — use the provided solid tokens",
    "focus": "Visible focus rings using ring-primary with --focus-ring shadow fallback",
    "keyboard": "All actions tab reachable; Enter/Space activates buttons; Esc closes dialogs",
    "aria": "Use aria-hidden for purely decorative icons; label inputs and controls; add descriptive aria-labels on icon-only buttons"
  },

  "testing_attributes": {
    "convention": "Use kebab-case data-testid values describing role and action",
    "coverage": [
      "All buttons, links, form inputs, menus, table rows",
      "Critical info surfaces: state labels, owner badges, confirmation messages",
      "Timeline payload blocks and filters"
    ]
  },

  "date_time_timezone": {
    "timezone": "IST (+05:30) shown explicitly; all times normalized server-side or via client util",
    "library": {
      "name": "date-fns-tz",
      "install": "npm i date-fns date-fns-tz",
      "usage_js": """
      import { format, utcToZonedTime } from 'date-fns-tz'
      const toIST = (iso) => {
        const zoned = utcToZonedTime(iso, 'Asia/Kolkata')
        return format(zoned, 'dd MMM, HH:mm (IST)')
      }
      """
    }
  },

  "states_and_permissions": {
    "states": ["REPORTED", "CLARIFIED", "DECISION_REQUIRED", "DECIDED", "IN_PROGRESS", "RESOLVED"],
    "rules": [
      "Only decision owner can advance states",
      "Anyone can add timeline context",
      "Reassignments recorded with audit info (who/when)"
    ],
    "ui_affordances": [
      "If user is not decision owner, show disabled transition buttons with tooltip",
      "OwnershipAssigner always visible with explicit labels"
    ]
  },

  "grid_and_spacing": {
    "container": "max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-6",
    "columns": {
      "list_page": "grid grid-cols-1 lg:grid-cols-[1fr_480px] gap-6",
      "detail_page": "grid grid-cols-1 lg:grid-cols-3 gap-6"
    },
    "timeline": "space-y-4 lg:space-y-5",
    "density": "Prefer roomy spacing (1.5x standard). Avoid cramped layouts"
  },

  "icons": {
    "library": "lucide-react",
    "mapping": {
      "text": "MessageSquareText",
      "voice": "Phone",
      "system": "Server",
      "owner": "UserCircle",
      "assign": "UserPlus",
      "decision": "CheckCircle2"
    }
  },

  "image_urls": [
    {
      "category": "empty_state",
      "description": "Container port at night — conveys Indian logistics operations",
      "url": "https://images.unsplash.com/photo-1639399688019-7c441d783782"
    },
    {
      "category": "login_or_welcome_side",
      "description": "Cargo ship docked at night (serious, operational)",
      "url": "https://images.unsplash.com/photo-1621697944804-d0a393f7e01a"
    },
    {
      "category": "dashboard_banner_small",
      "description": "Industrial cranes panorama (muted)",
      "url": "https://images.pexels.com/photos/27727861/pexels-photo-27727861.jpeg"
    }
  ],

  "usage_of_shadcn": {
    "rules": [
      "Use Shadcn/UI components from ./components/ui exclusively for primitives",
      "Avoid native HTML dropdowns/dialogs; prefer Select, Dialog, DropdownMenu, etc.",
      "Named exports for components; pages use default exports"
    ]
  },

  "button_system": {
    "tone": "Professional / Corporate",
    "variants": {
      "primary": "rounded-[var(--btn-radius)] bg-[hsl(var(--accent-blue-600))] text-white hover:bg-[hsl(var(--accent-blue-500))] shadow-[var(--btn-shadow)]",
      "secondary": "rounded-[var(--btn-radius)] bg-secondary text-foreground hover:bg-secondary/80",
      "ghost": "rounded-[var(--btn-radius)] hover:bg-secondary/60"
    },
    "sizes": {
      "sm": "h-8 px-3 text-xs",
      "md": "h-9 px-4 text-sm",
      "lg": "h-11 px-5 text-base"
    },
    "focus": "focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[hsl(var(--accent-blue-500))]"
  },

  "tables": {
    "component": "./components/ui/table",
    "row_states": "hover:bg-secondary/60 data-[selected=true]:bg-secondary focus-visible:outline-none",
    "empty": "min-h-[220px] grid place-content-center text-muted-foreground"
  },

  "filters_and_search": {
    "quick_tabs": "./components/ui/tabs",
    "owner_select": "./components/ui/select",
    "source_type": "text | voice | system",
    "reliability_levels": "low | medium | high",
    "search_input": "./components/ui/input"
  },

  "notifications": {
    "toast": "Use sonner (./components/ui/sonner). Place <Toaster /> at root. Use toast.success/error for transitions, assignments.",
    "examples": [
      "toast.success('State advanced to RESOLVED')",
      "toast.info('Ownership reassigned to A. Singh')"
    ]
  },

  "constraints": [
    "No decorative gradients over content. Keep backgrounds solid; subtle textures allowed if needed",
    "Manager-first: desktop optimized; responsive down to mobile with stacked panels",
    "Avoid emojis; use Lucide icons.",
    "Mobile-first responsive with sticky action bars where helpful"
  ],

  "references": [
    {"title": "Grafana Incident Timeline", "url": "https://grafana.com/docs/grafana-cloud/alerting-and-irm/irm/use/incident-management/incident-timeline/"},
    {"title": "ICEDASH (Indian Customs) Dashboard", "url": "https://www.icegate.gov.in/Webappl/EODB"}
  ],

  "instructions_to_main_agent": [
    "1) Add the semantic_tokens_css_to_add block to /app/frontend/src/App.css under the existing :root scope.",
    "2) Build Disruption List using ./components/ui/table with columns and state badges as defined. Ensure each interactive element carries data-testid attributes following the convention.",
    "3) Implement Disruption Detail with split layout; use TimelineEvent.js for each event; render source-dot and reliability-chip.",
    "4) Enforce permissions in UI: show disabled buttons with tooltip when user is not the decision owner.",
    "5) Normalize all timestamps to IST using date-fns-tz helper (see date_time_timezone.usage_js).",
    "6) Add Toaster from ./components/ui/sonner at App root and use for confirmations.",
    "7) Verify color contrast in both modes; do not introduce gradients in content areas.",
    "8) Ensure mobile: stack panels, make header sticky with filters, use ScrollArea for timeline on small screens.",
    "9) Keep .js files (no .tsx). Use named exports for components, default for pages.",
    "10) Add testing hooks: data-testid on buttons (e.g., 'assign-owner-button'), menus, filters, timeline events, and state transition confirms."
  ],

  "general_ui_ux_design_guidelines": """
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
  """
}
