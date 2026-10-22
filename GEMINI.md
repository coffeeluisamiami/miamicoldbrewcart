# GEMINI.md - Intelligence, Brand Memory & Agent Architecture
## Project: Miami Cold Brew Cart & Luisa Coffee Mobile Cart Ecosystem

---

### 1. Language & Interaction Policy
- **User Communication:** Always communicate with the user in **Spanish** (español).
- **Deliverables & Code:** Website copy, email templates, proposals, client packages, and codebase remain in **English** (luxury US catering standard).

---

### 2. Business Profile & Origin
- **Parent Company:** **Luisa Coffee** (`https://luisacoffee.com`)
  - **Tagline:** *"One specialty coffee, three ways to meet it: a handcrafted cart for your event, a machine for your office, and beans roasted at origin for your home."*
  - **Origin Story:** *"We buy the green bean directly at origin, roast it ourselves in Colombia (100% Arabica variety), and bring it to Miami. No resellers, no shortcuts — the same bean in every cart, office, and bag."*
  - **Headquarters:** Miami, FL 33130
  - **Contact Office:** `+1 (786) 659-4164` | `info@luisacoffee.com`
  - **Cart Operations Phone:** `+1 (786) 530-2517` | `cart@luisacoffee.com`
  - **Socials:** Instagram `@luisa.coffee` (`https://www.instagram.com/luisa.coffee/`) | LinkedIn: `https://www.linkedin.com/company/luisa-coffee/`

- **Mobile Cart Brands:**
  1. **Miami Cold Brew Cart** (`https://miamicoldbrewcart.com` / `https://miamicoldbrewcart.web.app`): Luxury mobile cold brew & nitro bar catering for events, corporate pop-ups, weddings, and brand activations in South Florida.
  2. **Miami Coffee Cart** (`https://miamicoffeecart.com`): Handcrafted mobile espresso bar for weddings and corporate gatherings. Includes *Luisa Moments* (live photo wall & guestbook).
  3. **Miami Matcha Cart** (`https://miamimatchacart.com` | `matcha@luisacoffee.com`): Ceremonial-grade Japanese matcha prepared fresh on-site with specialty infusions (Strawberry Matcha, Iced Matcha Lattes).
  4. **Miami Hot Chocolate Cart** (`https://miamihotchocolatecart.com` | `hotchocolate@luisacoffee.com`): Gourmet hot chocolate bar with artisanal toppings (shaved chocolate, gold flake, torched marshmallows).
  5. **Miami Refresher Cart** (`https://miamirefreshercart.com` | `refresher@luisacoffee.com`): Craft fruit refreshers, sparkling iced teas, and botanical hydration mocktails.
  6. **Sister Brands:** Miami Coffee Services (`miamicoffeeservices.com`), Miami Coffee Lab (`miamicoffeelab.com`).

---

### 3. Service Specs & Pricing Standard
- **Starting Price:** **$750 USD** minimum base package.
- **Base Package Covers:** 2 hours of unlimited live service, 1 certified professional barista, setup/breakdown, premium cups/napkins, syrups, and dairy + plant-based milks for up to 50 guests.
- **Technical Requirements:**
  - Standard `120V` dedicated electrical outlet (15-20 Amps).
  - Minimum space footprint: `5 × 5 ft` flat surface.
  - Indoor or covered outdoor space; elevator access required for upper floors.
- **Custom Branding Add-ons:**
  - Custom branded edible foam art / logos.
  - Branded cup sleeves & personalized cart vinyl wraps.
  - Custom personalized drink menu boards.
- **Service Territory:**
  - Miami-Dade County (Brickell, Downtown Miami, Coral Gables, Miami Beach, Wynwood, Coconut Grove, Doral).
  - Broward County (Fort Lauderdale, Hollywood, Weston).
  - Palm Beach County (Boca Raton, Delray Beach, West Palm Beach).
- **Target Event Types:** Corporate Summits, Conferences, Luxury Weddings, VIP Brand Activations, Tech Expos, Film/Photo Shoots, Private Galas.
- **Clients Who Trust Us:** Mana Tech, Saks Fifth Avenue, Merrill (Bank of America), City of Miami Beach, ClareMedica, Morgan, Marsh Re, Betterfly, Financial Design, Riviera School, Cargill.

---

### 4. Brand Design & Visual Tokens
- **Typography:**
  - Primary Display / Headings: `Playfair Display` (400, 700, 900 Italic)
  - Clean Sans / Body & UI: `Inter` (300, 400, 500, 600, 700)
  - Editorial Accent: `Georgia, serif`
- **Color Palette:**
  - `#F97316` — Coffee Orange / Amber CTA
  - `#1F4A4A` & `#143232` — Deep Luxury Teal & Dark Teal
  - `#6B8F3A` & `#3F6B3F` — Matcha Green & Forest Olive
  - `#E0A83F` — Warm Mustard Accent
  - `#FAF7F0` — Warm Cream Background
  - `#FFFFFF` — Pure White Card Background
  - `#22322F` — Deep Charcoal Text
  - `#5A675F` — Slate Muted Text

---

### 5. Multi-Agent Organization & Autonomous Pipeline
The workspace runs a dual-boss agent structure located in `.agent/`:

```
                    ┌─────────────────────────┐
                    │      CSO Agent          │  (Chief Sales Officer - .agent/cso-agent/)
                    │  Intake & Qualification │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Lead Gen Agent  │    │   Scope Agent    │    │  Proposal Agent  │
│ .agent/lead-gen/ │    │.agent/scope-agent│    │.agent/proposal-..│
└──────────────────┘    └────────┬─────────┘    └────────┬─────────┘
                                 │                       │
                                 └───────────┬───────────┘
                                             │ Hands off client package
                                             ▼
                                ┌─────────────────────────┐
                                │       CMO Agent         │  (Chief Marketing Officer - .agent/cmo-agent/)
                                │   Delivery & Routing    │
                                └────────────┬────────────┘
                                             │
                                             ▼
                                ┌─────────────────────────┐
                                │      Email Writer       │  (.agent/email-writer/)
                                │  Sends Gmail to Lead    │  -> logs to client-package.md
                                └─────────────────────────┘
```

#### Pipeline Steps:
1. **Intake:** Real event booking form submissions from `index.html` or Firestore `prospects` collection.
2. **Step 1 (CSO):** Structures data into Who, Problem/Vision, Budget & Timeline, Unknowns.
3. **Step 2 (Scope):** Calculates duration, baristas needed, coffee/nitro volume, and add-ons.
4. **Step 3 (Proposal):** Drafts a luxury, high-conversion proposal letter matching Miami Cold Brew Cart's voice.
5. **Step 4 (Handoff to CMO):** CSO transfers the package to CMO Agent.
6. **Step 5 (Email Writer):** CMO triggers `email-writer.py`, sending a formatted proposal to the client via Gmail (`mcardenas.cl@gmail.com`).
7. **Step 6 (Audit Trail):** Writes `client-package.md` with `SEND TO: <email>` on line 1 and `EMAIL SENT` on line 2.

---

### 6. Firebase & Infrastructure
- **Firebase Project:** `miamicoldbrewcart`
- **Hosting URL:** `https://miamicoldbrewcart.web.app`
- **Functions:** Node.js 22 (`draftContactReply`, `draftLeadReply`) in `functions/index.js`.
- **Firestore Collections:**
  - `prospects`: Incoming leads from website booking form.
  - `messages`: Live chatbot concierge conversations.
  - `leads`: Qualified leads captured by the AI Concierge chatbot.
- **Gmail Integration:** App password authenticated in `gmail_credentials.json` sending as `mcardenas.cl@gmail.com`.
