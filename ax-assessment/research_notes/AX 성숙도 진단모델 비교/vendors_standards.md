# AI Readiness / Adoption / Maturity Frameworks — Technology Vendors and Standards/Government Bodies (non-Korea)

Research date: 2026-10-01. Network note: several primary domains (learn.microsoft.com, cisco.com, docs.aws.amazon.com, aisingapore.org, services.google.com) were blocked for direct fetch in this environment; where possible they were read via a scraping proxy (Firecrawl) or via search snippets. Items marked **[search-snippet only]** were not read in full from the primary page. Items marked **[background knowledge, not re-verified this session]** come from prior knowledge with the official URL given; the report writer should treat them as lower-confidence.

---

## Q1. How do technology vendors define AI readiness and maturity (Microsoft, Google, AWS, IBM, Cisco, ServiceNow, Salesforce, others)?

### Takeaway
Vendors converge on 5–7 dimensions (strategy/leadership, data, infrastructure/platform, governance/security/responsible AI, talent/culture, plus ops/model management) and 3–5 stage maturity scales; the most reusable survey designs are Microsoft's AI Readiness Wizard (10 questions, 5 anchored answer options per question that map directly to 5 stages) and Cisco's AI Readiness Index (49 indicators, weighted pillars, 4 named respondent segments with "Pacesetters" as the top group).

### Cited Findings

**Microsoft — AI Readiness Wizard (adoption.microsoft.com)**
- Free online tool; asks **10 questions** grouped under **five "drivers of AI value"**: Business strategy; Technology & data strategy; AI strategy & experience; Organization & culture; AI governance & security (2 questions each). Output: "Your AI readiness score" plus "the next best area to focus on and a few resources." Page last modified 2026-04-02. — [Microsoft AI Readiness Wizard](https://adoption.microsoft.com/en-us/ai-readiness-wizard/)
- Each question has **5 behaviourally anchored answer options that read as a maturity ladder** — e.g., "Has your organization aligned your AI objectives with business priorities?" → "Early stages, no clearly defined goals" / "Specific objectives defined and aligned" / "AI models implemented and monitored for alignment" / "Successful initiatives being scaled" / "Continuous focus on maximizing AI value." Other questions cover approved use cases, data sources aligned to use cases, security protocol, model selection approach, AI team diversity, leadership communication of AI vision, AI skilling/credentialing availability, transparency/explainability/interpretability (TEI) controls, and user transparency about model limitations. — [Microsoft AI Readiness Wizard](https://adoption.microsoft.com/en-us/ai-readiness-wizard/)
- Microsoft's **five stages of AI readiness**: **Exploring** ("focus on building your AI strategy and experience"), **Planning** ("concentrate on formalizing your business strategy"), **Implementing** ("focusing on leadership support and scaling AI expertise"), **Scaling** ("create an organization and culture of innovation"), **Realizing** ("fostering continuous innovation within every team"). Published 2024-11-06. Stated principle: "AI success isn't solely about technology—strategic, organizational, and cultural factors are equally critical." — [Microsoft Cloud blog, "A strategic approach to assessing your AI readiness"](https://www.microsoft.com/en-us/microsoft-cloud/blog/2024/11/06/a-strategic-approach-to-assessing-your-ai-readiness/)
- Longer **Microsoft Learn "AI Readiness Assessment"** covers **seven pillars**: Business Strategy, AI Governance & Security, Data Foundations, AI Strategy & Experience, Organization & Culture, Infrastructure for AI, Model Management; multiple-choice/multiple-response; output = one of the same five stages plus "curated and personalized guidance." **[search-snippet only]** Length conflict: one secondary source says "**45 questions**" ([Augment Code](https://www.augmentcode.com/tools/ai-readiness-assessment-tools)); another snippet says "length of **45 minutes**" (search result summarising [Microsoft Learn Assessments](https://learn.microsoft.com/en-us/assessments/94f1c697-9ba7-4d47-ad83-7c6bd94b1505/)). Could not open the primary page to resolve.
- Microsoft also publishes a "Frontier Transformation" readiness framing (May 2026) — [Microsoft Cloud blog, 2026-05-14](https://www.microsoft.com/en-us/microsoft-cloud/blog/2026/05/14/from-ai-ambition-to-frontier-transformation-readiness-defines-the-leaders/) **[title only seen; contents not read]**; and an internal "Enterprise AI maturity in five steps" guide — [Microsoft Inside Track](https://www.microsoft.com/insidetrack/blog/enterprise-ai-maturity-in-five-steps-our-guide-for-it-leaders/) **[title only seen]**.
- Microsoft Cloud Adoption Framework (CAF) for AI: page could not be fetched (egress blocked). **[background knowledge, not re-verified this session]** it is organised as AI Strategy → AI Plan → AI Ready → Govern AI → Manage AI → Secure AI, and links to the AI readiness assessment — [learn.microsoft.com CAF AI](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/ai/).

**Google Cloud — AI Adoption Framework (whitepaper)**
- Anchored in **four pillars: People, Process, Technology, Data**; their interplay yields **six themes**: — [Google Cloud AI Adoption Framework whitepaper](https://services.google.com/fh/files/misc/ai_adoption_framework_whitepaper.pdf)
  - **Learn** — quality and scale of learning programs to upskill staff, hire external talent, augment DS/ML staff with partners.
  - **Lead** — extent data scientists are supported by a leadership mandate to apply ML to business use cases; cross-functional, collaborative, self-motivated teams.
  - **Access** — recognition of data management as key to AI; ability to share, discover, reuse data and ML artifacts.
  - **Scale** — use of cloud-native ML services that scale with data and jobs with reduced operational overhead.
  - **Secure** — protecting data and ML services from unauthorized access, plus responsible and explainable AI.
  - **Automate** — deploying/operating data and ML pipelines in production efficiently, frequently, reliably.
- **Three phases** (the "AI Maturity Scale" = 6 themes × 3 phases): **Tactical** (simple, short-term, narrow use cases; no coherent plan; quick wins), **Strategic** (several ML systems in production; broader vision governs adoption; ML no longer "domain of a special few"), **Transformational** (AI stimulates innovation and agility; ML expertise diffused across lines of business; mechanism for scaling ML capabilities). — [Google whitepaper](https://services.google.com/fh/files/misc/ai_adoption_framework_whitepaper.pdf)
- The whitepaper says the framework lets you "assess your organization's AI maturity and determine what you'll need to bridge the gap," but **no public questionnaire/question count was found in the document**. — [Google whitepaper](https://services.google.com/fh/files/misc/ai_adoption_framework_whitepaper.pdf). Blog announcement: [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/build-a-transformative-ai-capability-with-ai-adoption-framework). Publication date not shown in the extracted text (gap; commonly dated ~2021).

**AWS — CAF for AI/ML/GenAI (CAF-AI) and Generative AI Maturity Model**
- CAF-AI extends the AWS Cloud Adoption Framework with **six perspectives: Business, People, Governance, Platform, Security, Operations**; adds AI-specific foundational capabilities such as **Generative AI** (Business), **ML Fluency** (People), **Responsible use of AI** (Governance), **AI Lifecycle Management and MLOps** (Platform). — [AWS CAF-AI whitepaper, foundational capabilities](https://docs.aws.amazon.com/whitepapers/latest/aws-caf-for-ai/foundational-ai-capabilities.html); [PDF](https://docs.aws.amazon.com/pdfs/whitepapers/latest/aws-caf-for-ai/aws-caf-for-ai.pdf) **[search-snippet only]**
- **AWS Prescriptive Guidance — Generative AI maturity model**: **4 levels** — **Envision** (foundational understanding/awareness of GenAI and trends), **Experiment** (hands-on PoCs and pilots), **Launch** (methodical deployment of proven solutions into production), **Scale** (multiple departments adopt; enterprise-wide GenAI infrastructure and tooling). "Lower levels generally encompass more tactical … higher levels … more strategic and transformative." Model also defines "aspects" of maturity (page not readable). — [AWS GenAI maturity model overview](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-gen-ai-maturity-model/overview.html); [levels](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-gen-ai-maturity-model/overview-levels.html); [aspects](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-gen-ai-maturity-model/overview-aspects.html) **[search-snippet only]**

**IBM — AI Ladder**
- Four rungs: **Collect** (make data simple/accessible), **Organize** (business-ready analytics foundation; data quality, governance), **Analyze** (build and scale AI with trust/transparency), **Infuse** (operationalize AI across the business). Implemented through Cloud Pak for Data; dates from ~2019. It is a data-to-AI capability sequence, not a scored survey. — [IBM Cloud Architecture Center](https://ibm-cloud-architecture.github.io/refarch-data-ai-analytics/data/); [SiliconANGLE 2019](https://siliconangle.com/2019/03/01/qa-ibms-data-strategy-aims-help-enterprise-ai-ladder-think2019/) **[search-snippet only]**
- No public watsonx-branded scored readiness self-assessment was found (gap).

**Cisco — AI Readiness Index (annual survey, 2023/2024/2025)**
- 2025 edition: **8,039 senior business leaders** responsible for AI integration and deployment, **30 markets**, organisations with **500+ employees**, **49 indicators**, **six pillars: Strategy, Infrastructure, Data, Governance, Talent, Culture**. — [Cisco AI Readiness Index 2025 PDF](https://www.cisco.com/c/dam/m/en_us/solutions/ai/readiness-index/2025-m10/documents/cisco-ai-readiness-index-2025-realizing-the-value-of-ai.pdf)
- **Scoring method (very copyable):** each indicator weighted by importance; responses scored by deployment level (**25–50% credit for partial deployment, 100% for full deployment**); pillar scores combined into an overall score with **pillar weights: Strategy 15%, Infrastructure 25%, Data 20%, Governance 15%, Talent 15%, Culture 10%**. — [Cisco 2025 PDF](https://www.cisco.com/c/dam/m/en_us/solutions/ai/readiness-index/2025-m10/documents/cisco-ai-readiness-index-2025-realizing-the-value-of-ai.pdf)
- **Four readiness segments**: **Pacesetters** (fully prepared), **Chasers** (moderately prepared), **Followers** (limited preparedness), **Laggards** (unprepared). 2023 global split: **Pacesetters 14%, Chasers 34%, Followers 48%, Laggards 4%**. — [Cisco Global AI Readiness Index 2023 PDF](https://www.cisco.com/c/dam/m/en_us/solutions/ai/readiness-index/documents/cisco-global-ai-readiness-index.pdf); [Cisco newsroom 2023](https://investor.cisco.com/news/news-details/2023/Cisco-Launches-New-Research-Highlighting-Seismic-Gap-in-Companies-Preparedness-for-AI/default.aspx) **[split via search summary]**
- **Pacesetters ≈ 13% in 2025** (stable vs ~13–14% in prior years). 2025 segment splits for Chasers/Followers/Laggards not extracted (gap). — [Cisco 2025 PDF](https://www.cisco.com/c/dam/m/en_us/solutions/ai/readiness-index/2025-m10/documents/cisco-ai-readiness-index-2025-realizing-the-value-of-ai.pdf); [RCR Wireless](https://www.rcrwireless.com/20251209/ai/cisco-ai-readiness-index-2025)
- 2025 headline stats: 83% plan to deploy AI agents; only 32% have a process to measure AI impact (Pacesetters 95%); 58% have a well-defined strategy; 81% report a clear AI owner; 34% say IT infrastructure is fully adaptable/scalable; 54% cite high compute costs as top ROI hurdle; 31% feel fully capable of securing agentic AI. Pacesetters ~4× more likely to move pilots into production; 77% of Pacesetters have finalized AI use cases. — [Cisco 2025 PDF](https://www.cisco.com/c/dam/m/en_us/solutions/ai/readiness-index/2025-m10/documents/cisco-ai-readiness-index-2025-realizing-the-value-of-ai.pdf); [Kramer & Co](https://kramerand.co/cisco-ai-readiness-index-highlights-ai-value-gap/)
- Cisco offers an online **AI Readiness Assessment / Look-up tool** for benchmarking against the index. — [Cisco look-up tool](https://www.cisco.com/c/m/en_us/solutions/ai/readiness-index/lookup-tool.html); [Cisco AI Readiness Assessment](https://www.cisco.com/c/m/en_us/solutions/ai/readiness-index/realizing-the-value-of-ai.html) (question count not verified — gap).

**ServiceNow — Enterprise AI Maturity Index (annual, 2024/2025/2026)**
- **Five pillars: AI strategy and leadership, workflow integration, talent and workforce, AI governance, AI investment**; 2025 edition surveyed just under **4,500 executives, 16 countries, 11 industries**; score **0–100**. "Robust and effective leadership is the most predictive factor of a high overall AI index score." — [ServiceNow EAMI 2025](https://www.servicenow.com/workflow/ai/enterprise-ai-maturity-index-2025.html) **[search-snippet only]**
- Scores: 2025 average **35/100**; **Pacesetters averaged 44**, down from **54** in 2024 (vendor interprets decline as rising bar / agentic AI raising expectations). — [ServiceNow EAMI 2025](https://www.servicenow.com/workflow/ai/enterprise-ai-maturity-index-2025.html); [CIO.com](https://www.cio.com/article/4011788/is-declining-ai-maturity-a-sign-of-progress.html)
- 2026 edition: **4,500 executives, 19 countries**; average score rose to **51**; Pacesetters = "the one-fifth of organizations … having achieved advanced AI maturity"; Pacesetter AI ROI averages 160%; 59% use agentic AI but only 18% scale agentic processes across key functions; only 26% have systems to manage governance/compliance; 71% struggle with data accuracy/access/management. — [ServiceNow EAMI 2026](https://www.servicenow.com/workflow/ai/enterprise-ai-maturity-index-2026.html); [2026 PDF](https://www.servicenow.com/content/dam/servicenow-assets/public/en-us/doc-type/resource-center/white-paper/wp-enterprise-ai-maturity-index-2026.pdf)

**Salesforce — Global AI Readiness Index (national-level, not enterprise)**
- 2025: **16 markets, 31 indicators, five dimensions: governance, diffusion, innovation, investment, talent**; countries tiered as top performers (US, Singapore, UK, Canada, Germany), growing momentum (incl. South Korea, Japan), emerging progress. — [Salesforce newsroom](https://www.salesforce.com/news/stories/global-ai-readiness-index-insights-2025/)
- Salesforce enterprise-level "AI readiness" content is mostly data readiness for Agentforce plus partner-delivered assessments; no first-party scored public enterprise survey found. — [Salesforce blog: 5 ways to measure data readiness](https://www.salesforce.com/blog/measure-your-data-readiness/)

### Inferences
- Common dimension core across vendors: **Strategy/Leadership, Data, Infrastructure/Platform, Governance/Security/Responsible AI, Talent/Skills, Culture/Change**; vendor-specific additions are **Model management/MLOps** (Microsoft, AWS, Google "Automate"), **Investment/Value** (ServiceNow), **Workflow integration** (ServiceNow).
- Two design archetypes: (a) **short wizard** (Microsoft 10 Q, anchored 5-point ladder, instant stage + next-best-area), and (b) **benchmark index** (Cisco 49 indicators / ServiceNow 0–100) with peer segmentation ("Pacesetters"). An AX app can combine both: short pulse + deep module, with benchmark segment labels.
- Cisco's partial-credit scoring and explicit pillar weights are a transparent, defensible scoring template; Microsoft's per-question anchors that encode the stage names are the best item-writing pattern for self-assessment reliability.
- Vendor frameworks are self-interested (Cisco overweights infrastructure at 25%; ServiceNow emphasises single-platform workflow integration) — weights should be re-derived for a neutral AX tool.

### Gaps
- Microsoft Learn AI Readiness Assessment: exact question count vs. 45 minutes unresolved; primary page blocked.
- Microsoft CAF for AI current structure and any formal "AI maturity model" levels not verified this session.
- Cisco 2024 and 2025 full four-segment splits not extracted; Cisco online assessment question count unknown.
- ServiceNow EAMI number of questions and 2026 pillar list (2026 page emphasises data, agentic AI, workflows, governance) not confirmed.
- AWS GenAI maturity model "aspects" list and any assessment instrument not read.
- No information found for Intel or NVIDIA enterprise AI maturity frameworks; no Anthropic/OpenAI staged maturity models were researched successfully (not searched due to tool budget) — treat as open.

---

## Q2. How do standards and government bodies define AI readiness/maturity and governance (ISO/IEC, NIST, OECD, EU AI Act, Singapore, UK, Oxford Insights, WEF)?

### Takeaway
Standards bodies do not publish maturity *levels*; they publish requirement/control sets (ISO/IEC 42001: clauses 4–10 + 38 Annex A controls; NIST AI RMF: 4 functions / 19 categories / 72 subcategories; NIST AI 600-1: 12 GenAI risks / 200+ actions) that an AX survey can use as the item bank for its governance dimension. Government-backed enterprise tools with true maturity levels are rare — Singapore's AIRI (5 pillars, 15 dimensions, 5 levels on a 0–5 scale, ~15-minute online survey) is the clearest model.

### Cited Findings

**ISO/IEC 42001:2023 — AI Management System (AIMS)**
- Clauses 4–10 are the auditable management-system requirements: Context, Leadership, Planning, Support, Operation, Performance evaluation, Improvement. **Annex A = 38 controls under 9 control objectives (A.2–A.10)** covering AI policy, roles, impact assessment, AI life cycle, data, supplier relationships etc.; controls are selected by risk assessment and recorded in a **Statement of Applicability**. — [Konfirmity: 38 Annex A controls](https://www.konfirmity.com/blog/iso-42001-controls); [Konfirmity clause guide](https://www.konfirmity.com/blog/iso-42001-requirements) (secondary sources; primary ISO text is paywalled at [iso.org](https://www.iso.org/standard/81230.html))
- Certifiable standard (third-party audit), paid document; no maturity levels — conformity is binary per requirement.

**ISO/IEC 5338 and ISO/IEC 8183** — **[background knowledge, not re-verified this session]**
- ISO/IEC 5338:2023 defines AI system life cycle processes (adapting ISO/IEC/IEEE 15288/12207 to AI) — [iso.org 5338](https://www.iso.org/standard/81118.html).
- ISO/IEC 8183:2023 defines an AI data life cycle framework (stages from data conception/acquisition through preparation, use, and decommissioning) — [iso.org 8183](https://www.iso.org/standard/83002.html).
- Neither defines maturity levels; both are useful as checklists for "AI lifecycle/MLOps" and "data" dimensions.

**NIST AI RMF 1.0 (Jan 2023) and Generative AI Profile NIST AI 600-1 (26 Jul 2024)**
- AI RMF Core: **4 functions — Govern, Map, Measure, Manage; 19 categories; 72 subcategories** (Govern 6 categories/19 subcategories; Map 5/18; Measure 4/22; Manage 4/13). — [NIST AIRC — AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/); breakdown per [Modulos NIST AI RMF guide](https://docs.modulos.ai/frameworks/nist-ai-rmf)
- NIST AI 600-1 (released 2024-07-26): **12 GenAI risk categories** — CBRN information or capabilities; Confabulation; Dangerous/violent/hateful content; Data privacy; Environmental impacts; Harmful bias and homogenization; Human-AI configuration; Information integrity; Information security; Intellectual property; Obscene/degrading/abusive content; Value chain and component integration — with **200+ suggested actions** mapped to the four functions. — [Modulos: GenAI Profile](https://docs.modulos.ai/frameworks/nist-ai-rmf/generative-ai-profile); [DeepInspect](https://www.deepinspect.ai/blog/nist-genai-profile)
- Voluntary, free; no maturity tiers in AI RMF 1.0 (organisations build "profiles" of current vs. target state). A Cloud Security Alliance "Agentic Profile" has been published as an extension. — [CSA Agentic NIST AI RMF Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)

**Singapore**
- **AI Readiness Index (AIRI)** — developed by AI Singapore (AISG), now also run via SGTech and sector partners (NTUC, SMF). **5 pillars → 15 dimensions**: Organisational Readiness, Business Value Readiness, Ethics & Governance Readiness, Data Readiness, Infrastructure Readiness. **AIRI v3.1 scores 0–5 across 5 levels: AI Unaware (0.00–0.99), AI Aware (1.00–1.99), AI Ready (2.00–2.99), AI Competent (3.00–3.99), AI Catalyst (4.00–5.00)**; "AI Ready (Level 2)" recommended target for most organisations. Online self-assessment **~15 minutes**; system-generated report shows gaps between current and desired state. — [AI Singapore AIRI](https://aisingapore.org/innovation/airi/); [SGTech AIRI](https://airi.sgtech.org.sg/); [NTUC AIRI](https://ntuc.airi.sg/); [SMF AIRI FAQ](https://smfederation.airi.sg/faq/) **[search-snippet only; question count not confirmed]**
- **AI Verify** (testing framework/toolkit) and **Model AI Governance Framework** (2nd ed. 2020; GenAI edition 2024) — **[background knowledge, not re-verified this session]**: governance/assurance tools, not maturity scales — [IMDA / AI Verify Foundation](https://aiverifyfoundation.sg/).

**UK**
- **AI Playbook for the UK Government** (GDS/DSIT, **Feb 2025**), updates the Generative AI Framework for HMG; **10 principles**; built by 50+ experts with input from 20+ departments. It **does not provide a maturity model or self-assessment benchmarking tool**. — [AI Playbook PDF (gov.uk)](https://assets.publishing.service.gov.uk/media/67aca2f7e400ae62338324bd/AI_Playbook_for_the_UK_Government__12_02_.pdf); gap noted by [AIGL blog](https://www.aigl.blog/artificial-intelligence-playbook-for-the-uk-government/)
- No current UK government enterprise AI maturity self-assessment found (gap; earlier CDDO "data maturity assessment for government" exists but was not verified this session).

**Oxford Insights — Government AI Readiness Index (national-level, for contrast)**
- 2025 = **8th edition**; research question reframed to "To what extent can a government harness AI to benefit the public?"; **195 countries, 69 indicators, 14 dimensions, 6 pillars: Policy Capacity, Governance, AI Infrastructure, Public Sector Adoption, Development and Diffusion, Resilience**. US ranks 1st (87.20); North America regional average 79.75, Western Europe 62.75. Desk-research indicators, no self-assessment. — [Oxford Insights 2025 report](https://oxfordinsights.com/wp-content/uploads/2026/01/2025-Government-AI-Readiness-Index-Report_01_26.pdf); [Methodology 2025](https://oxfordinsights.com/wp-content/uploads/2026/01/Methodology-Report-2025-1.pdf)

**World Economic Forum**
- "Advancing Responsible AI Innovation: A Playbook" (2025, with Accenture, AI Governance Alliance): **9 plays** for operationalising responsible AI. A 2025 survey of **1,500 companies** found **81% in the first two stages of a four-stage responsible-AI maturity scale**, and **<1%** have fully operationalised responsible AI. — [WEF Playbook PDF](https://reports.weforum.org/docs/WEF_Advancing_Responsible_AI_Innovation_A_Playbook_2025.pdf); [WEF story](https://www.weforum.org/stories/2025/09/responsible-ai-governance-innovations/) (stage names not extracted — gap)
- "The AI-First Operating System" (2026): five building blocks of AI-first enterprises. — [WEF 2026 PDF](https://reports.weforum.org/docs/WEF_The_AI_First_Operating_System_A_Blueprint_for_Operating_and_Business_Model_Innovation_2026.pdf) **[title/snippet only]**

**EU AI Act and OECD** — **[background knowledge, not re-verified this session]**
- EU AI Act (Reg. 2024/1689) in force 1 Aug 2024; prohibited practices and **Art. 4 AI literacy obligation** applicable from 2 Feb 2025; GPAI obligations from 2 Aug 2025; most high-risk obligations scheduled 2 Aug 2026, with a Commission "Digital Omnibus" proposal (Nov 2025) to delay some high-risk deadlines — **current status as of Oct 2026 not verified**. Readiness implications: AI inventory, risk classification, AI literacy training, documentation/human oversight for high-risk uses. — [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- OECD AI Principles (2019, updated May 2024) and OECD definition of an AI system underpin the EU Act and many national frameworks; OECD publishes no enterprise maturity scale — [OECD.AI](https://oecd.ai/en/ai-principles).

### Inferences
- For an AX survey, standards supply the **governance/risk item bank** (ISO 42001 Annex A objectives; NIST Govern/Map/Measure/Manage; NIST 600-1's 12 GenAI risks) rather than the level definitions; levels must be designed by the tool (e.g., adopt AIRI's 0–5 continuous score with named bands).
- An "EU AI Act / regulatory readiness" sub-score (inventory, risk classification, AI literacy) is a differentiating module for multinational respondents.
- National indices (Oxford Insights, Salesforce) are useful only as context/benchmarks, not as enterprise item sources.

### Gaps
- Primary ISO texts are paywalled; Annex A count relies on secondary sources (consistent across them).
- AIRI: exact question count and current version beyond v3.1 not confirmed (primary site blocked).
- EU AI Act implementation timeline changes in 2025–2026 not verified.
- WEF four-stage responsible-AI scale names not extracted.

---

## Q3. Which public self-assessment tools exist online, with question counts, and what do their outputs look like?

### Takeaway
Confirmed public free tools: Microsoft AI Readiness Wizard (10 questions, 5 options each, score + next-best focus area + resources) and Singapore AIRI (~15 min, 0–5 score, level band, gap report). Microsoft Learn's 7-pillar assessment and Cisco's online assessment exist but their item counts could not be verified.

### Cited Findings
| Tool | Publisher | Items / time | Response format | Output | Cost |
|---|---|---|---|---|---|
| AI Readiness Wizard | Microsoft | **10 questions**, 5 drivers × 2 | 5 anchored options per item (ladder) | Readiness score; "next best area to focus on"; resource links; link to AI Strategy Roadmap | Free — [source](https://adoption.microsoft.com/en-us/ai-readiness-wizard/) |
| AI Readiness Assessment (Learn) | Microsoft | 7 pillars; "45 questions" vs "45 minutes" (conflicting) | Multiple-choice / multiple-response | Stage (Exploring→Realizing) + personalised guidance | Free — [Learn](https://learn.microsoft.com/en-us/assessments/94f1c697-9ba7-4d47-ad83-7c6bd94b1505/); [Augment Code](https://www.augmentcode.com/tools/ai-readiness-assessment-tools) |
| AIRI | AI Singapore / SGTech | ~15 minutes; 5 pillars, 15 dimensions | Online survey | 0–5 score, 5 named levels, system-generated gap report (current vs desired) | Free to members/partners (pricing not verified) — [AISG](https://aisingapore.org/innovation/airi/) |
| Cisco AI Readiness Assessment / Look-up tool | Cisco | Not verified (index uses 49 indicators) | Online | Benchmark vs Pacesetters/Chasers/Followers/Laggards | Free — [Cisco](https://www.cisco.com/c/m/en_us/solutions/ai/readiness-index/lookup-tool.html) |
| Salesforce (partner) AI/Agentforce readiness | Partners (e.g., Arovy, Wipro) | Varies | Consultant-led or web form | Maturity scorecard, gap analysis, 90-day roadmap | Mixed — [Arovy](https://www.arovy.com/free-ai-agentforce-readiness-assessment) |

### Inferences
- Best-practice output pattern = **overall stage + per-dimension profile + single "next best focus area" + linked resources/roadmap**; benchmark-index vendors add **peer segment label** (Pacesetter etc.).
- Short instruments (10 items, <5 min) maximise completion; deep ones (40–50 items) give diagnostic value — an AX app could offer both tiers and multi-respondent aggregation (none of the vendor tools found support multi-respondent organisational aggregation — a differentiation opportunity).

### Gaps
- Could not verify item counts for Microsoft Learn assessment, Cisco online assessment, AIRI.
- No public online self-assessment found for Google AI Adoption Framework, AWS GenAI maturity model, IBM, NIST, or ISO 42001 (beyond third-party gap-analysis checklists).
