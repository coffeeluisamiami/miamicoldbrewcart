const functions = require("firebase-functions/v1");
const admin = require("firebase-admin");

admin.initializeApp();

const fs = require("fs");
const path = require("path");

function getGmailPassword() {
  if (process.env.GMAIL_PASS) return process.env.GMAIL_PASS.trim();
  const possiblePaths = [
    path.join(__dirname, "gmail_credentials.json"),
    path.join(__dirname, "..", "gmail_credentials.json")
  ];
  for (const p of possiblePaths) {
    if (fs.existsSync(p)) {
      try {
        const creds = JSON.parse(fs.readFileSync(p, "utf8"));
        if (creds.app_password) return creds.app_password.replace(/\s+/g, "");
      } catch (e) {}
    }
  }
  return "";
}

const GMAIL_USER = process.env.GMAIL_USER || "mcardenas.cl@gmail.com";
const GMAIL_PASS = getGmailPassword();

// Scope Agent Logic (under CSO)
// Scope Agent Logic (under CSO) - Miami Cold Brew Cart
function defineScope(profile) {
  const helpWith = (profile.helpWith || "Nitro Cold Brew").toLowerCase();
  const bottleneck = (profile.bottleneck || "").toLowerCase();
  const kw = helpWith + " " + bottleneck;

  if (kw.includes("combination") || kw.includes("multi-bar") || kw.includes("combo") || (kw.includes("cold brew") && kw.includes("espresso")) || (kw.includes("cold brew") && kw.includes("matcha"))) {
    return {
      service: "Luisa Coffee Group Custom Multi-Bar Experience (Cold Brew + Espresso + Matcha)",
      deliverables: [
        "Dual mobile cart stations: Signature Nitro Cold Brew + Commercial Italian Espresso & Matcha bar",
        "Unlimited single-origin 18-hour cold brew on tap, velvety nitro cascades, and hot espresso specialties",
        "Ceremonial Uji matcha whisked fresh to order + tropical handcrafted refreshers",
        "Custom branded cup sleeves and personalized event menu signage with your logo",
        "3 Certified professional baristas delivering ultra-fast service for 200+ guests with zero line waiting",
        "Complete dairy and organic plant-based milk bar (oat, almond, whole) and gourmet artisan syrups"
      ],
      timeline: "3 to 4 hours unlimited multi-station beverage service",
      outOfScope: "Alcoholic cocktail mixing without designated venue liquor liability rider."
    };
  } else if (kw.includes("office") || kw.includes("corporate service") || kw.includes("lab") || kw.includes("service")) {
    return {
      service: "Miami Coffee Services & Lab Corporate Program",
      deliverables: [
        "Commercial automated bean-to-cup espresso equipment setup tailored for corporate spaces",
        "Fresh weekly delivery of 100% Arabica Colombian specialty roast from Luisa Coffee",
        "Full staff barista training and cupping workshop from Miami Coffee Lab",
        "Turnkey preventive maintenance, water filtration exchange, and continuous bean replenishment"
      ],
      timeline: "Ongoing corporate service subscription & on-site event activation",
      outOfScope: "Third-party equipment repair for uncertified hardware."
    };
  } else if (kw.includes("matcha") || kw.includes("refresher") || kw.includes("content")) {
    return {
      service: "Ceremonial Matcha & Tropical Refresher Activation (Miami Matcha & Refresher Cart)",
      deliverables: [
        "Premium Uji ceremonial-grade matcha whisked fresh to order (iced or warm)",
        "Handcrafted tropical refresher bar: Strawberry Hibiscus, Mango Passionfruit, Yuzu Mint",
        "Boutique cart presentation with tropical Miami floral staging",
        "2 Experienced baristas serving 150+ guests per hour with zero line congestion",
        "All cups, sleeves, eco-straws, and customized menu signage included"
      ],
      timeline: "3 hours high-throughput beverage activation",
      outOfScope: "Full food catering or hot breakfast prep."
    };
  } else if (kw.includes("espresso") || kw.includes("hot coffee") || kw.includes("latte") || kw.includes("lead")) {
    return {
      service: "Full Specialty Espresso & Latte Art Bar (Miami Coffee Cart)",
      deliverables: [
        "Commercial 2-group Italian espresso machine mounted on boutique coffee cart",
        "Complete hot espresso menu: Cortados, Flat Whites, Cappuccinos, Lattes, and Americanos",
        "Live latte art demonstrations for guests by professional lead baristas",
        "House-made syrups, leches vegetales (oat, almond), and organic whole milk",
        "3 hours of unlimited barista service with premium ceramic or branded takeaway cups",
        "Dedicated quiet power station and self-contained water filtration"
      ],
      timeline: "3 hours continuous espresso service",
      outOfScope: "Gasoline generators indoors or outdoor setups lacking overhead rain shelter."
    };
  } else if (kw.includes("hot chocolate") || kw.includes("winter") || kw.includes("cocoa") || kw.includes("custom")) {
    return {
      service: "Winter Gourmet Hot Chocolate & Warm Beverage Bar (Miami Hot Chocolate Cart)",
      deliverables: [
        "Rich European-style melted chocolate & velvety Swiss cocoa bars",
        "Gourmet toppings: hand-torched artisan marshmallows, crushed peppermint, cinnamon whipped cream",
        "Festive cart dressing and cozy winter display for holiday parties and galas",
        "Full service by 2 dedicated baristas for 3 hours of warm beverage bliss"
      ],
      timeline: "3 hours holiday event service",
      outOfScope: "Outdoor service in unshielded heavy rain."
    };
  }

  // Default: Signature Nitro Cold Brew
  return {
    service: "Signature Nitro Cold Brew & Iced Specialty Bar (Miami Cold Brew Cart)",
    deliverables: [
      "Handcrafted wooden mobile cart with dual-tap nitrogen draft system",
      "Single-origin nitrogen-infused cold brew & ceremonial iced matcha on tap",
      "Full artisan syrup station (Tahitian vanilla, lavender honey, salted caramel)",
      "Organic oat, almond, and whole milk options",
      "2 Certified hospitality baristas providing 3 hours of unlimited rapid service",
      "Custom cups, compostable straws, ice service, and turnkey setup & cleanup"
    ],
    timeline: "3 hours unlimited guest service (1-hour setup prior)",
    outOfScope: "Alcoholic beverage pouring without venue rider and extra hours beyond contract."
  };
}

// Proposal Agent Logic (under CSO) - Miami Cold Brew Cart
function generateProposalPitch(profile, scope) {
  const firstName = (profile.name || "there").split(" ")[0];
  const business = profile.businessName || profile.company || "your upcoming event";
  const bottleneck = profile.bottleneck || "world-class guest hospitality";
  const deliverables = scope.deliverables.map(d => `• ${d}`).join("\n");

  return `Hey ${firstName},

Thank you for reaching out about bringing the coffee cart experience to ${business}!

We reviewed your event details and noted that your primary priority is:
"${bottleneck}"

Delivering rapid, world-class guest hospitality with zero line congestion is exactly what we specialize in. For ${business}, we have engineered our ${scope.service}.

Here is what your all-inclusive event package includes:

${deliverables}

Service Duration: ${scope.timeline} with seamless 1-hour setup and full breakdown included.
Budget Alignment: Fully structured to deliver five-star hospitality well within your ${profile.budget || "$1,000-$5,000"} range.

What is Out of Scope:
${scope.outOfScope}

Next Step:
Let's lock in your date on our calendar before the weekend books up. Click the booking link below or reply directly to this email to reserve your cart setup.

Warm regards,
Marcelo Cardenas
Founder & Event Director
Miami Cold Brew Cart • An Experiential Branch of Luisa Coffee & Miami Coffee Cart
${GMAIL_USER}`;
}

// Email Writer Logic (under CMO) - Branded Luxury Coffee HTML
function buildBrandedHtmlEmail(firstName, businessName, bottleneck, proposalPitch) {
  const formattedBody = proposalPitch
    .split("\n\n")
    .map(p => {
      if (p.includes("•")) {
        const items = p.split("\n").filter(l => l.trim().startsWith("•")).map(l => `<li style="margin-bottom: 8px;"><strong>•</strong> ${l.replace("•", "").trim()}</li>`).join("");
        return `<ul style="margin: 14px 0; padding-left: 22px; line-height: 1.7; color: #334155;">${items}</ul>`;
      }
      return `<p style="margin: 14px 0; line-height: 1.65; color: #334155; font-size: 15px;">${p.replace(/\n/g, "<br>")}</p>`;
    })
    .join("");

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Your Event Proposal from Miami Cold Brew Cart</title>
</head>
<body style="margin: 0; padding: 0; background-color: #faf5ee; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #faf5ee; padding: 36px 16px;">
    <tr>
      <td align="center">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 620px; background-color: #ffffff; border-radius: 16px; overflow: hidden; border: 1px solid #e7dfd5; box-shadow: 0 10px 30px rgba(78, 42, 12, 0.08);">
          <tr>
            <td style="background: linear-gradient(135deg, #78350f 0%, #ea580c 50%, #f59e0b 100%); padding: 36px 30px; text-align: left;">
              <span style="display: inline-block; background-color: rgba(255,255,255,0.2); color: #ffffff; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 1.2px; padding: 4px 10px; border-radius: 20px; margin-bottom: 10px;">Event Catering Proposal</span>
              <h1 style="margin: 0; font-size: 26px; font-weight: 900; color: #ffffff; letter-spacing: -0.5px;">Miami Cold Brew Cart</h1>
              <p style="margin: 6px 0 0; font-size: 13px; color: #fed7aa; font-weight: 500;">In Partnership with Luisa Coffee & Miami Coffee Cart</p>
            </td>
          </tr>
          <tr>
            <td style="padding: 34px 30px;">
              <p style="margin: 0 0 14px; font-size: 17px; font-weight: 800; color: #1e1b18;">
                Hi ${firstName}, thank you for inquiring about ${businessName}!
              </p>
              <div style="background-color: #fffbeb; border-left: 4px solid #ea580c; padding: 14px 18px; margin-bottom: 24px; border-radius: 6px;">
                <p style="margin: 0; font-size: 14px; font-weight: 600; color: #92400e; line-height: 1.5;">
                  ☕ We specifically reviewed your event priorities regarding "${bottleneck}" and engineered this tailored beverage package for you.
                </p>
              </div>
              <div style="color: #334155;">
                ${formattedBody}
              </div>
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin: 32px 0 24px; background: linear-gradient(135deg, #fff7ed 0%, #fef3c7 100%); border: 2px solid #fed7aa; border-radius: 14px; text-align: center; padding: 26px 20px;">
                <tr>
                  <td>
                    <h3 style="margin: 0 0 8px; font-size: 19px; font-weight: 900; color: #78350f;">Ready to reserve your event date?</h3>
                    <p style="margin: 0 0 18px; font-size: 14px; color: #92400e;">Dates fill quickly across South Florida. Lock in your mobile coffee bar setup today.</p>
                    <a href="https://miamicoldbrewcart.web.app/#book-event" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #ea580c 0%, #d97706 100%); color: #ffffff; font-size: 15px; font-weight: 800; text-decoration: none; padding: 13px 32px; border-radius: 10px; box-shadow: 0 6px 18px rgba(234, 88, 12, 0.35);">Lock In Your Event Date &rarr;</a>
                  </td>
                </tr>
              </table>
              <div style="border-top: 1px solid #e7dfd5; padding-top: 22px; margin-top: 28px; text-align: left;">
                <p style="margin: 0; font-size: 15px; font-weight: 800; color: #1e1b18;">Marcelo Cardenas</p>
                <p style="margin: 2px 0 0; font-size: 13px; color: #78350f; font-weight: 600;">Founder & Hospitality Lead &bull; Miami Cold Brew Cart</p>
                <p style="margin: 4px 0 0; font-size: 13px; color: #64748b;">
                  Direct: <a href="mailto:${GMAIL_USER}" style="color: #ea580c; text-decoration: none; font-weight: 600;">${GMAIL_USER}</a> &bull; 
                  <a href="https://miamicoffeecart.com" target="_blank" style="color: #78350f; text-decoration: none;">Miami Coffee Cart</a> &bull; 
                  <a href="https://luisacoffee.com" target="_blank" style="color: #78350f; text-decoration: none;">Luisa Coffee</a>
                </p>
                <p style="margin: 12px 0 0; font-size: 11px; color: #a8a29e; font-style: italic;">Specialty Cold Brew, Espresso, Matcha & Warm Refreshers serving Miami, Brickell, Coral Gables, Wynwood and Fort Lauderdale.</p>
              </div>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>`;
}

// CSO Agent Logic: Structure Prospect Profile
function structureProspectProfile(data) {
  const unknowns = [];
  const name = (data.name || data.fullName || "").trim();
  if (!name) unknowns.push("Prospect name not specified");

  const business = (data.businessName || data.company || "").trim();
  if (!business) unknowns.push("Business name not specified");

  const email = (data.email || "").trim();
  if (!email) unknowns.push("Email address not provided");

  const industry = (data.industry || "").trim();
  if (!industry) unknowns.push("Industry not specified");

  const helpWith = (data.helpWith || data.need || "").trim();
  if (!helpWith || helpWith.toLowerCase() === "not sure yet") {
    unknowns.push(`Need help with: ${helpWith || "Not specified"}`);
  }

  const bottleneck = (data.bottleneck || data.message || "").trim();
  if (!bottleneck) {
    unknowns.push("Biggest bottleneck not specified");
  } else if (bottleneck.split(" ").length <= 4) {
    unknowns.push(`Brief/vague bottleneck statement: '${bottleneck}'`);
  }

  const budget = (data.budget || data.budgetRange || "").trim();
  if (!budget || budget.toLowerCase() === "not sure yet") {
    unknowns.push(`Budget: ${budget || "Not specified"}`);
  }

  const timeline = (data.timeline || "").trim();
  if (!timeline || timeline.toLowerCase() === "just exploring") {
    unknowns.push(`Timeline: ${timeline || "Just exploring"}`);
  }

  return {
    who: {
      name: name || "Unknown Prospect",
      business_name: business || "Unknown Business",
      email: email || "Unknown",
      industry: industry || "Not specified"
    },
    problem: {
      need: helpWith || "Automation",
      bottleneck: bottleneck || "Manual operational bottlenecks"
    },
    budget_and_timeline: {
      budget: budget || "Under $1,000",
      timeline: timeline || "Flexible"
    },
    unknowns: unknowns.length > 0 ? unknowns : ["None"]
  };
}

// TRIGGER: On new contact submission
exports.draftContactReply = functions.firestore
  .document("contacts/{docId}")
  .onCreate(async (snap, context) => {
    const data = snap.data();
    if (!data || data.proposal_sent) return null;

    console.log(`[CSO Pipeline] Triggered for: ${snap.id} (${data.email})`);

    // 1. CSO structures Prospect Profile
    const profile = structureProspectProfile(data);

    // 2. Scope Agent defines scope
    const scope = defineScope({
      ...data,
      helpWith: profile.problem.need,
      bottleneck: profile.problem.bottleneck
    });

    // 3. Proposal Agent writes pitch
    const pitch = generateProposalPitch(data, scope);

    // 4. Email Writer builds HTML
    const firstName = profile.who.name.split(" ")[0];
    const businessName = profile.who.business_name;
    const bottleneck = profile.problem.bottleneck;
    const htmlEmail = buildBrandedHtmlEmail(firstName, businessName, bottleneck, pitch);

    // 4. Send via Gmail if email is provided
    let emailSent = false;
    if (data.email) {
      try {
        const nodemailer = require("nodemailer");
        const transporter = nodemailer.createTransport({
          service: "gmail",
          auth: {
            user: GMAIL_USER,
            pass: GMAIL_PASS
          }
        });
        await transporter.sendMail({
          from: `"Marcelo Cardenas" <${GMAIL_USER}>`,
          to: data.email,
          subject: `Your proposal from Marcelo Cardenas -- ${businessName}`,
          text: pitch,
          html: htmlEmail
        });
        emailSent = true;
        console.log(`[Email Writer] Proposal successfully sent to ${data.email}`);
      } catch (err) {
        console.error(`[Email Writer] Failed to dispatch email:`, err);
      }
    }

    // 5. Update Firestore document with all outputs
    return snap.ref.update({
      prospect_profile: profile,
      scope_service: scope.service,
      scope_deliverables: scope.deliverables,
      scope_timeline: scope.timeline,
      proposal_pitch: pitch,
      proposal_html: htmlEmail,
      proposal_sent: emailSent,
      pipeline_status: emailSent ? "delivered" : "draft_ready",
      pipeline_updated_at: admin.firestore.FieldValue.serverTimestamp()
    });
  });

// TRIGGER: Chatbot leads (Runs complete autonomous pipeline from interactive chat)
exports.draftLeadReply = functions.firestore
  .document("leads/{docId}")
  .onCreate(async (snap, context) => {
    const data = snap.data();
    if (!data || data.proposal_sent) return null;

    console.log(`[CSO Pipeline] Triggered for chatbot lead: ${snap.id} (${data.email})`);

    const quote = data.interactiveQuote || {};
    const concept = quote.concept || "Signature Nitro Cold Brew Bar";
    const guests = quote.guests || "Up to 50 guests";
    const price = quote.price || "$750";
    const location = quote.location || "Miami & South Florida";

    // 1. Structure profile
    const profile = structureProspectProfile({
      name: data.name || "Specialty Beverage Host",
      businessName: "Upcoming " + location + " Event",
      email: data.email,
      industry: "Hospitality & Live Events",
      helpWith: concept,
      bottleneck: `Seamless live cart catering for ${guests} in ${location} with instant quote ${price}`,
      budget: price,
      timeline: "Upcoming Event Season"
    });

    // 2. Define scope based on selected cart experience
    const scope = defineScope({
      helpWith: concept,
      bottleneck: `Catering for ${guests} in ${location}`
    });

    // 3. Generate proposal pitch
    const pitch = generateProposalPitch({
      name: profile.who.name,
      businessName: profile.who.business_name,
      bottleneck: profile.problem.bottleneck,
      budget: price
    }, scope);

    // 4. Build branded luxury HTML email
    const firstName = profile.who.name.split(" ")[0];
    const htmlEmail = buildBrandedHtmlEmail(
      firstName,
      profile.who.business_name,
      profile.problem.bottleneck,
      pitch
    );

    // 5. Send proposal via Gmail
    let emailSent = false;
    if (data.email) {
      try {
        const nodemailer = require("nodemailer");
        const transporter = nodemailer.createTransport({
          service: "gmail",
          auth: {
            user: GMAIL_USER,
            pass: GMAIL_PASS
          }
        });
        await transporter.sendMail({
          from: `"Marcelo Cardenas" <${GMAIL_USER}>`,
          to: data.email,
          subject: `Your Miami Cold Brew Cart Event Quote & Proposal -- ${concept}`,
          text: pitch,
          html: htmlEmail
        });
        emailSent = true;
        console.log(`[Email Writer] Chatbot proposal email sent to ${data.email}`);
      } catch (err) {
        console.error(`[Email Writer] Failed to send chatbot proposal:`, err);
      }
    }

    // 6. Update Firestore document
    return snap.ref.update({
      prospect_profile: profile,
      scope_service: scope.service,
      scope_deliverables: scope.deliverables,
      scope_timeline: scope.timeline,
      proposal_pitch: pitch,
      proposal_html: htmlEmail,
      proposal_sent: emailSent,
      pipeline_status: emailSent ? "delivered" : "draft_ready",
      pipeline_updated_at: admin.firestore.FieldValue.serverTimestamp()
    });
  });
