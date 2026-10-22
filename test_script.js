
    // --- Firebase Configuration ---
    const firebaseConfig = {
      apiKey: "AIzaSyCigaGarSwaOj_RX8VEmoIEDwa2RL0moTM",
      authDomain: "miamicoldbrewcart.firebaseapp.com",
      projectId: "miamicoldbrewcart",
      storageBucket: "miamicoldbrewcart.firebasestorage.app",
      messagingSenderId: "585917755546",
      appId: "1:585917755546:web:ac66c6a98f383689c4af23",
      measurementId: "G-GMWKJ9KTZW"
    };

    firebase.initializeApp(firebaseConfig);
    const db = firebase.firestore();

    // Contact Form
    const contactForm = document.getElementById('contactForm');
    const submitBtn = document.getElementById('submitBtn');
    const successAlert = document.getElementById('successAlert');

    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      submitBtn.disabled = true;
      submitBtn.innerText = "Submitting to Firebase...";

      const guestCount = document.getElementById('guestCount').value;
      const eventLocation = document.getElementById('eventLocation').value.trim();
      const eventDate = document.getElementById('eventDate').value;
      const duration = document.getElementById('duration').value;
      const concept = document.getElementById('helpWith').value;
      const notes = document.getElementById('bottleneck').value.trim();

      const formData = {
        name: document.getElementById('name').value.trim(),
        businessName: document.getElementById('businessName').value.trim(),
        email: document.getElementById('email').value.trim(),
        eventLocation: eventLocation,
        eventDate: eventDate,
        duration: duration,
        guestCount: guestCount,
        helpWith: concept,
        concept: concept,
        industry: guestCount + " • " + eventLocation,
        budget: document.getElementById('budget').value,
        timeline: eventDate ? "Event Date: " + eventDate : "1-3 months",
        bottleneck: notes + " (Location: " + eventLocation + " | Duration: " + duration + " | Guests: " + guestCount + ")",
        notes: notes,
        source: "miami_cold_brew_cart_booking",
        createdAt: firebase.firestore.FieldValue.serverTimestamp()
      };

      try {
        const docRef = await db.collection('contacts').add(formData);
        console.log("Document successfully written with ID:", docRef.id);
        successAlert.style.display = "block";
        submitBtn.style.display = "none";
        contactForm.reset();
      } catch (error) {
        console.error("Error saving document:", error);
        alert("Error saving: " + error.message);
        submitBtn.disabled = false;
        submitBtn.innerText = "Submit Request →";
      }
    });

    // --- Enhanced AI Chatbot Concierge with Project Nexus Memory (English) ---
    const chatToggle = document.getElementById('chatToggle');
    const chatWindow = document.getElementById('chatWindow');
    const chatClose = document.getElementById('chatClose');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const chatChips = document.getElementById('chatChips');

    // Project Nexus & CSO Agent Memory (from .nexus/memory/context.json & .agent/cso-agent/business_profile.json)
    const NEXUS_PROJECT_MEMORY = {
      parentCompany: {
        name: "Luisa Coffee",
        url: "https://luisacoffee.com",
        originStory: "We purchase 100% Arabica green beans directly at origin in Colombia, roast them ourselves, and bring them fresh to Miami. No middlemen, no shortcuts: the exact same specialty roast across every cart, corporate office, and retail bag.",
        phone: "+1-786-530-2517",
        officePhone: "+1-786-659-4164",
        email: "cart@luisacoffee.com",
        address: "Miami, FL 33130"
      },
      mobileCartEcosystem: [
        { name: "Miami Cold Brew Cart", specialty: "Exclusive Nitro Cold Brew bars featuring nitrogen-infused cold tap cascades and artisan syrups.", url: "https://miamicoldbrewcart.com" },
        { name: "Miami Coffee Cart", specialty: "Full Italian espresso bars, live latte art demonstrations, and 'Luisa Moments' live guestbook photo activations.", url: "https://miamicoffeecart.com" },
        { name: "Miami Matcha Cart", specialty: "Ceremonial Uji matcha whisked fresh to order, strawberry matcha lattes, and organic plant-based milks.", url: "https://miamimatchacart.com" },
        { name: "Miami Hot Chocolate Cart", specialty: "Gourmet Swiss/Belgian melted chocolate with hand-torched marshmallow toppings and edible gold flakes.", url: "https://miamihotchocolatecart.com" },
        { name: "Miami Refresher Cart", specialty: "Handcrafted fruit refreshers, sparkling iced teas, and botanical herbal infusions.", url: "https://miamirefreshercart.com" }
      ],
      trustedClients: [
        "Mana Tech", "Mana Wynwood", "Saks Fifth Avenue", "Merrill (A Bank of America Company)",
        "City of Miami Beach", "Morgan", "ClareMedica", "Marsh Re", "Betterfly", "Cargill", "Riviera School"
      ],
      serviceAreas: [
        "Miami-Dade (Brickell, Downtown, Wynwood, Coral Gables, Miami Beach, Doral)",
        "Broward County (Fort Lauderdale, Hollywood)",
        "Palm Beach County (Boca Raton, West Palm Beach)"
      ],
      specs: {
        power: "Standard 120V household outlet (ultra-quiet, low power draw)",
        space: "Compact 5x5 ft footprint",
        mobility: "Fits effortlessly inside standard passenger elevators and conventional interior doors",
        advanceTime: "2 to 4 weeks recommended for large events and weddings (priority holds for advance bookings)"
      },
      pricingTiers: {
        tier50: { guests: "Up to 50 guests", price: "$750", hours: "2 hours", baristas: 1 },
        tier100: { guests: "50 to 100 guests", price: "$950", hours: "3 hours", baristas: "1-2" },
        tier150: { guests: "100 to 150 guests", price: "$1,200", hours: "3 hours", baristas: 2 },
        tierCorporate: { guests: "200+ guests", price: "Custom Enterprise", hours: "3-4+ hours", baristas: "2+" }
      }
    };

    // State of interactive quotation
    let interactiveQuoteState = {
      concept: null,
      guests: null,
      price: null,
      location: null,
      email: null
    };

    let conversationHistory = [];
    let leadCapturedEmail = null;

    chatToggle.addEventListener('click', () => {
      chatWindow.classList.toggle('open');
      if (chatWindow.classList.contains('open')) {
        chatInput.focus();
      }
    });

    chatClose.addEventListener('click', () => {
      chatWindow.classList.remove('open');
    });

    // Chips clicks
    if (chatChips) {
      chatChips.addEventListener('click', (e) => {
        const btn = e.target.closest('.chat-chip');
        if (!btn) return;
        const action = btn.getAttribute('data-action');
        const query = btn.getAttribute('data-query');
        if (action === 'quote') {
          startInteractiveQuote();
        } else if (query) {
          handleUserMessage(query);
        }
      });
    }

    chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const text = chatInput.value.trim();
      if (!text) return;
      chatInput.value = '';
      handleUserMessage(text);
    });

    function showTypingIndicator() {
      const typingDiv = document.createElement('div');
      typingDiv.className = 'chat-typing';
      typingDiv.id = 'chatTypingIndicator';
      typingDiv.innerHTML = '<span></span><span></span><span></span>';
      chatMessages.appendChild(typingDiv);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTypingIndicator() {
      const indicator = document.getElementById('chatTypingIndicator');
      if (indicator) indicator.remove();
    }

    function appendMessage(text, type, extraHtml = '') {
      const msgDiv = document.createElement('div');
      msgDiv.className = `chat-msg ${type}`;
      msgDiv.innerHTML = text.replace(/\n/g, '<br>') + (extraHtml ? `<div style="margin-top:0.4rem;">${extraHtml}</div>` : '');
      chatMessages.appendChild(msgDiv);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // --- Interactive Wizard Functions in English (Exposed to Window) ---
    window.startInteractiveQuote = function() {
      showTypingIndicator();
      setTimeout(() => {
        removeTypingIndicator();
        appendMessage(
          `📊 <strong>Interactive Event Quote Calculator</strong><br>
Select your preferred beverage cart experience:`,
          'bot',
          `<div class="chat-interactive-box">
            <div class="chat-interactive-title">Step 1: Choose Your Cart</div>
            <div class="chat-options-grid">
              <button type="button" class="chat-opt-btn" onclick="selectInteractiveConcept('Signature Nitro Cold Brew Bar')">☕ Nitro Cold Brew</button>
              <button type="button" class="chat-opt-btn" onclick="selectInteractiveConcept('Ceremonial Matcha & Refreshers')">🍵 Matcha Bar</button>
              <button type="button" class="chat-opt-btn" onclick="selectInteractiveConcept('Specialty Espresso & Latte Art')">☕ Espresso & Latte</button>
              <button type="button" class="chat-opt-btn" onclick="selectInteractiveConcept('Gourmet Hot Chocolate Bar')">🍫 Hot Chocolate</button>
            </div>
          </div>`
        );
      }, 400);
    };

    window.selectInteractiveConcept = function(conceptName) {
      interactiveQuoteState.concept = conceptName;
      appendMessage(`Selected: <strong>${conceptName}</strong>`, 'user');

      showTypingIndicator();
      setTimeout(() => {
        removeTypingIndicator();
        appendMessage(
          `Great choice! The <em>${conceptName}</em> setup is one of our most popular activations.<br><br>
How many guests are you expecting?`,
          'bot',
          `<div class="chat-interactive-box">
            <div class="chat-interactive-title">Step 2: Guest Count & Duration</div>
            <div class="chat-options-grid">
              <button type="button" class="chat-opt-btn" onclick="selectInteractiveGuests('Up to 50 guests', '$750', '2 hours')">👥 Up to 50 ($750)</button>
              <button type="button" class="chat-opt-btn" onclick="selectInteractiveGuests('50 - 100 guests', '$950', '3 hours')">👥 100 guests ($950)</button>
              <button type="button" class="chat-opt-btn" onclick="selectInteractiveGuests('100 - 150 guests', '$1,200', '3 hours')">👥 150 guests ($1,200)</button>
              <button type="button" class="chat-opt-btn" onclick="selectInteractiveGuests('200+ guests', 'Custom Corporate', 'Custom')">🏢 200+ (Corporate)</button>
            </div>
          </div>`
        );
      }, 450);
    };

    window.selectInteractiveGuests = function(guestsText, priceText, duration) {
      interactiveQuoteState.guests = guestsText;
      interactiveQuoteState.price = priceText;
      interactiveQuoteState.duration = duration;

      appendMessage(`Guests: <strong>${guestsText}</strong> (${priceText})`, 'user');

      showTypingIndicator();
      setTimeout(() => {
        removeTypingIndicator();
        appendMessage(
          `Got it: <strong>${guestsText}</strong>.<br><br>
Where in Miami or South Florida will your event take place?`,
          'bot',
          `<div class="chat-interactive-box">
            <div class="chat-interactive-title">Step 3: Event Location</div>
            <div class="chat-options-grid">
              <button type="button" class="chat-opt-btn" onclick="finalizeInteractiveQuote('Brickell / Downtown Miami')">🌴 Brickell / Downtown</button>
              <button type="button" class="chat-opt-btn" onclick="finalizeInteractiveQuote('Wynwood / Miami Beach')">🏖️ Wynwood / Beach</button>
              <button type="button" class="chat-opt-btn" onclick="finalizeInteractiveQuote('Coral Gables / Doral')">🏙️ Gables / Doral</button>
              <button type="button" class="chat-opt-btn" onclick="finalizeInteractiveQuote('Fort Lauderdale / Broward')">🌊 Ft Lauderdale</button>
            </div>
          </div>`
        );
      }, 450);
    };

    window.finalizeInteractiveQuote = function(location) {
      interactiveQuoteState.location = location;
      appendMessage(`Location: <strong>${location}</strong>`, 'user');

      showTypingIndicator();
      setTimeout(() => {
        removeTypingIndicator();

        const quoteCardHtml = `
          <div class="chat-calc-card">
            <div class="calc-row">
              <span style="color:#94a3b8; font-weight:700;">EXPERIENCE:</span>
              <strong style="color:#fff;">${interactiveQuoteState.concept}</strong>
            </div>
            <div class="calc-row">
              <span style="color:#94a3b8; font-weight:700;">GUESTS:</span>
              <span>${interactiveQuoteState.guests} (${interactiveQuoteState.duration})</span>
            </div>
            <div class="calc-row">
              <span style="color:#94a3b8; font-weight:700;">LOCATION:</span>
              <span>${interactiveQuoteState.location}</span>
            </div>
            <div class="calc-row" style="margin-top:0.5rem; padding-top:0.5rem; border-top:1px dashed #475569;">
              <span style="font-weight:800; font-size:0.95rem;">ESTIMATED TOTAL:</span>
              <span class="calc-price">${interactiveQuoteState.price}</span>
            </div>
            <div style="font-size:0.75rem; color:#94a3b8; margin-top:0.4rem; line-height:1.4;">
              ✓ 100% Colombian Arabica single-origin beans (Luisa Coffee)<br>
              ✓ Certified barista + unlimited cups and premium ingredients<br>
              ✓ Turnkey compact cart setup (requires standard 120V outlet)
            </div>
          </div>
          <div style="margin-top:0.6rem; font-size:0.83rem;">
            📩 <strong>To reserve your date and receive your formal PDF proposal:</strong><br>
            Enter your <em>email address</em> below.
          </div>
        `;

        appendMessage(
          `✨ <strong>Custom Estimate Ready!</strong><br>Here is your quote breakdown based on our Luisa Coffee event pricing:`,
          'bot',
          quoteCardHtml
        );
      }, 600);
    };

    // --- Knowledge Base Handler with Nexus Context (English) ---
    function getKnowledgeBaseResponse(query) {
      const q = query.toLowerCase();

      // Email match
      const emailMatch = query.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/);
      if (emailMatch) {
        return {
          type: 'email',
          email: emailMatch[0],
          text: `Perfect! We have registered your email <strong>${emailMatch[0]}</strong> with priority status.<br><br>
Our <strong>Luisa Coffee & Miami Cold Brew Cart</strong> event team will send your complete menu package, date availability, and formal estimate to your inbox shortly.`
        };
      }

      // Origin story & Luisa Coffee
      if (q.includes('luisa') || q.includes('origin') || q.includes('bean') || q.includes('colombia') || q.includes('coffee') || q.includes('roast') || q.includes('grano')) {
        return {
          type: 'info',
          text: `🌱 <strong>The Luisa Coffee Origin Story:</strong><br><br>
${NEXUS_PROJECT_MEMORY.parentCompany.originStory}<br><br>
Every cart from <em>Miami Cold Brew Cart</em> and <em>Miami Coffee Cart</em> pours this exact specialty roast, delivering an elevated beverage standard your guests will remember from the first sip.`
        };
      }

      // Enterprise clients
      if (q.includes('client') || q.includes('company') || q.includes('trust') || q.includes('corporate') || q.includes('brand') || q.includes('empresa')) {
        const clientList = NEXUS_PROJECT_MEMORY.trustedClients.join(', ');
        return {
          type: 'info',
          text: `🏆 <strong>Clients Who Trust Our Carts:</strong><br><br>
We have delivered high-volume catering and custom activations for premier brands and institutions:<br>
• <strong>${clientList}</strong>.<br><br>
Our carts regularly serve inside the <em>Miami Beach Convention Center</em>, <em>Mana Wynwood</em>, and top Brickell financial towers.`
        };
      }

      // Technical specs
      if (q.includes('spec') || q.includes('power') || q.includes('requirement') || q.includes('outlet') || q.includes('size') || q.includes('dimension') || q.includes('elevator')) {
        return {
          type: 'info',
          text: `🔌 <strong>Cart Technical Specifications:</strong><br><br>
• <strong>Electrical:</strong> ${NEXUS_PROJECT_MEMORY.specs.power}.<br>
• <strong>Space Footprint:</strong> ${NEXUS_PROJECT_MEMORY.specs.space}.<br>
• <strong>Accessibility:</strong> ${NEXUS_PROJECT_MEMORY.specs.mobility}.<br>
• <strong>Advance Notice:</strong> ${NEXUS_PROJECT_MEMORY.specs.advanceTime}.<br><br>
Clean, whisper-quiet, self-contained setups with zero event disruption.`
        };
      }

      // Contact & Phone
      if (q.includes('phone') || q.includes('whatsapp') || q.includes('contact') || q.includes('call') || q.includes('email') || q.includes('telefono')) {
        return {
          type: 'info',
          text: `📞 <strong>Direct Contact Channels:</strong><br><br>
• <strong>Cart Direct Phone / WhatsApp:</strong> <a href="tel:${NEXUS_PROJECT_MEMORY.parentCompany.phone}" style="color:var(--primary); font-weight:800;">${NEXUS_PROJECT_MEMORY.parentCompany.phone}</a><br>
• <strong>Roastery Headquarters (Luisa Coffee):</strong> ${NEXUS_PROJECT_MEMORY.parentCompany.officePhone}<br>
• <strong>Direct Email:</strong> <a href="mailto:${NEXUS_PROJECT_MEMORY.parentCompany.email}">${NEXUS_PROJECT_MEMORY.parentCompany.email}</a><br>
• <strong>Central Miami Hub:</strong> ${NEXUS_PROJECT_MEMORY.parentCompany.address}<br><br>
Or type your email or phone number here and we'll connect with you right away!`
        };
      }

      // Packages
      if (q.includes('package') || q.includes('menu') || q.includes('offer') || q.includes('option') || q.includes('paquete')) {
        return {
          type: 'info',
          text: `☕ <strong>Our 5 Mobile Beverage Experiences:</strong><br><br>
1️⃣ <strong>Signature Nitro Cold Brew Bar:</strong> Nitrogen-infused cold brew on tap with velvety cascading foam and artisan syrups.<br>
2️⃣ <strong>Ceremonial Matcha Bar:</strong> Uji ceremonial-grade matcha whisked fresh to order and organic fruit refreshers.<br>
3️⃣ <strong>Specialty Espresso Bar:</strong> Italian commercial espresso machine, cortados, flat whites, and live latte art.<br>
4️⃣ <strong>Gourmet Hot Chocolate Bar:</strong> Rich Belgian chocolate with torched artisan marshmallows and gold leaf flake.<br>
5️⃣ <strong>Craft Fruit Refresher Bar:</strong> Cold-pressed juices, sparkling botanical infusions, and mocktails.<br><br>
Click <strong>'⚡ Quote in 3 Clicks'</strong> above to calculate your event price in seconds!`
        };
      }

      // Pricing & Estimates
      if (q.includes('price') || q.includes('cost') || q.includes('quote') || q.includes('estimate') || q.includes('budget') || q.includes('precio')) {
        return {
          type: 'info',
          text: `Our packages are <strong>all-inclusive</strong> (designer mobile cart, lead baristas, self-contained setup, cups, syrups, and unlimited drinks):<br><br>
• <strong>Intimate Events (Up to 50 guests):</strong> Starting at $750 (2 hours of unlimited service).<br>
• <strong>Mid-Size Events (50 - 100 guests):</strong> $950 (3 hours).<br>
• <strong>Large Gatherings (100 - 150 guests):</strong> $1,200 (3 hours with 2 baristas).<br>
• <strong>Corporate Summits (200+ guests):</strong> High-throughput custom corporate packages.<br><br>
Click <strong>'⚡ Quote in 3 Clicks'</strong> or enter your email to get a tailored estimate!`
        };
      }

      // Branding & Customization
      if (q.includes('brand') || q.includes('logo') || q.includes('custom') || q.includes('cup') || q.includes('wrap')) {
        return {
          type: 'info',
          text: `🎨 <strong>Brand Activations & Customization:</strong><br><br>
We specialize in corporate brand activations! We can customize:<br>
• <strong>Custom Branded Cups & Sleeves:</strong> High-definition logo print on eco-friendly takeaway cups.<br>
• <strong>Cart Medallion & Front Wrap:</strong> Custom decals and panels matching your company colors and branding.<br>
• <strong>Personalized Menu Signage:</strong> Custom-named drinks tailored to your company or campaign theme.<br><br>
Drop your email to receive photos and examples of past brand activations!`
        };
      }

      // Default fallback
      return {
        type: 'general',
        text: `We would love to help! We cater weddings, corporate conferences, product launches, and private galas across Miami and Broward with the specialty beans of <strong>Luisa Coffee</strong>.<br><br>
Click <strong>'⚡ Quote in 3 Clicks'</strong> for an instant estimate or drop your email address below.`
      };
    }

    async function handleUserMessage(userText) {
      appendMessage(userText, 'user');
      conversationHistory.push({ sender: 'user', text: userText });

      showTypingIndicator();

      const kbResponse = getKnowledgeBaseResponse(userText);

      setTimeout(async () => {
        removeTypingIndicator();

        let extraCard = '';
        if (kbResponse.type === 'email') {
          leadCapturedEmail = kbResponse.email;
          extraCard = `<div class="lead-captured-card">✅ <span>Lead registered in Firebase Firestore with attached event quote</span></div>`;

          // Sync lead + quote with Firebase Firestore
          try {
            await db.collection('leads').add({
              email: leadCapturedEmail,
              name: "Website Interactive Chat Lead",
              fullConversation: conversationHistory,
              interactiveQuote: interactiveQuoteState,
              source: "website_chatbot_nexus_memory",
              status: "qualified_lead",
              createdAt: firebase.firestore.FieldValue.serverTimestamp()
            });
            console.log("Interactive Lead synchronized to Firestore:", leadCapturedEmail, interactiveQuoteState);
          } catch (err) {
            console.warn("Firestore notice:", err.message);
          }
        }

        appendMessage(kbResponse.text, 'bot', extraCard);
        conversationHistory.push({ sender: 'bot', text: kbResponse.text });
      }, 600);
    }
  