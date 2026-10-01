# Enterprise AI Maturity / AI Readiness Models from Global Consulting & Research-Advisory Firms

Research date: 2026-10-01. Tools: Firecrawl search/scrape, WebSearch. Several publisher domains (mckinsey.com, cisr.mit.edu full text, idc.com via WebFetch) were blocked or rate-limited, so some items come from search excerpts. These are flagged **[excerpt]** (publisher search snippet, not full-page read) or **[secondary]** (non-publisher source). Anything marked **[unverified-memory]** comes from background knowledge that I could not re-confirm this session. The report writer should treat those as leads to check, not as facts.

---

## Q1. Gartner AI Maturity Model (5 levels) and the Gartner AI Maturity Assessment / toolkit

### Takeaway
Gartner's current, client-gated **AI Maturity Assessment** scores organizations on **7 pillars** (strategy, data, governance, engineering, operating model, culture, AI product/value) using a guided questionnaire. The outputs are a heat map of current vs. target maturity per capability, a gap visualization, analyst recommendations and a roadmap. Gartner's public page now names the 5 stages **Foundational, Emerging, Operational, Scaled, Transformational**. This differs from the older and widely cited **Awareness, Active, Operational, Systemic, Transformational** naming, so the version should be stated explicitly.

### Cited Findings
- Official product name on gartner.com: "Gartner AI Maturity Assessment" (page title "Gartner AI Maturity Model and AI Roadmap Toolkit"). The page says that "In one assessment, get a clear maturity score across strategy, data, governance, engineering, operating model, culture and AI product/value — plus a prioritized roadmap to move from pilots to measurable ROI." — [Gartner](https://www.gartner.com/en/chief-information-officer/research/ai-maturity-model-toolkit)
- Method: "Take the guided AI maturity assessment questionnaire to gauge your current capabilities in **seven core AI pillars**." The page also says to "Use the scoring system to prioritize your AI initiatives" and to "Export visualizations and action plans." — [Gartner](https://www.gartner.com/en/chief-information-officer/research/ai-maturity-model-toolkit)
- Client report outputs: an "AI maturity heat map" (current and target maturity level for each capability), "a visualization of key gaps" (largest current-vs-target gaps), and "analyst recommendations." There are also playbooks for governance, use cases and operating models. — [Gartner](https://www.gartner.com/en/chief-information-officer/research/ai-maturity-model-toolkit)
- Scope: the model "can be applied enterprisewide or to specific functions (for example finance or marketing)." Uses include establishing a baseline, setting adoption targets and building roadmaps, and tracking progress over time. — [Gartner](https://www.gartner.com/en/chief-information-officer/research/ai-maturity-model-toolkit)
- **Current 5 stages (gartner.com FAQ, page cached 2026-10-01):**
  1. **Foundational:** "Ad hoc experimentation with limited coordination"
  2. **Emerging:** "Early pilots and growing executive interest"
  3. **Operational:** "AI embedded in select processes with defined ownership"
  4. **Scaled:** "AI capabilities deployed across functions with measurable ROI"
  5. **Transformational:** "AI reshapes decision making, operating models and competitive advantage"
  — [Gartner](https://www.gartner.com/en/chief-information-officer/research/ai-maturity-model-toolkit)
- **Legacy/widely cited 5 levels** (Gartner, c. 2018–2020, "CIO's Guide to AI"): Level 1 Awareness, Level 2 Active, Level 3 Operational, Level 4 Systemic, Level 5 Transformational — [BMC blog, secondary](https://www.bmc.com/blogs/ai-maturity-models/). LXT's study gives these level definitions: Awareness = "early interest in and conversations around AI strategy"; Active = "initial experimentation and pilot projects"; Operational = "AI used in at least one workflow"; Systemic = "AI is present in the majority of workflows/operations, inspiring new, digital business models"; Transformational = "AI is inherent in the DNA of the business" — [LXT, secondary](https://www.lxt.ai/path-ai-maturity/)
- Access: the questionnaire and full report are for Gartner clients (paid). A non-client can "Launch demo" (an interactive demo) after filling in a lead form. — [Gartner](https://www.gartner.com/en/chief-information-officer/research/ai-maturity-model-toolkit)
- Benchmark (third party using Gartner's levels, not Gartner data): in LXT's survey, "40% of organizations rate themselves within the three highest levels" (Operational/Systemic/Transformational) — [LXT, secondary](https://www.lxt.ai/path-ai-maturity/). Survey date was not captured.

### Inferences
- The 7 pillars map closely onto the dimension list the coordinator gave (strategy, value/product, organization/operating model, people/culture, governance, engineering, data). This is a good default backbone for the AX survey.
- The "current vs. target per capability" heat map and gap ranking is a reusable output pattern. It implies each item is answered twice (as-is and to-be).
- Gartner's change of level names (Awareness→Foundational, Active→Emerging, Systemic→Scaled) points to a vocabulary shift toward "scale/ROI." A Korean AX app could use similar names (e.g., 기반 / 태동 / 운영 / 확산 / 전환).

### Gaps
- Gartner's item count, the definitions of each level per pillar, respondent design (single vs. multi) and the scoring formula are **not public** (client-gated).
- No Gartner-published distribution of companies by maturity level was found this session.
- The date when Gartner renamed the levels is not confirmed.
- Not confirmed whether the current assessment includes GenAI- or agentic-specific items.

---

## Q2. MIT CISR Enterprise AI Maturity Model (Weill, Woerner, Sebastian; 2024, updated 2025)

### Takeaway
This is the strongest public evidence base: 4 stages derived from a survey of 721 companies. Stage membership comes from a simple **3-item "Total AI Effectiveness" score**, and the stages link to profit and growth relative to industry average. Stages 1–2 underperform their industry and stages 3–4 outperform it. The 2025 update shows that the biggest financial jump comes from moving from stage 2 to stage 3.

### Cited Findings
- Publication: "Building Enterprise AI Maturity," MIT CISR Research Briefing, Dec 19, 2024, by Peter Weill, Stephanie L. Woerner and Ina M. Sebastian. It is based on "a 2022 MIT CISR survey of 721 companies" (October 2022, Future Ready Survey), "supplemented ... with sixteen interviews ... August to November 2024 with senior executives at nine enterprises." — [MIT CISR](https://cisr.mit.edu/publication/2024_1201_EnterpriseAIMaturityModel_WeillWoernerSebastian) [excerpt]; [press release](https://cisr.mit.edu/content/press-release-enterprise-ai-maturity-121924)
- **4 stages and share of enterprises (2022 data):**
  - Stage 1 **Experiment and Prepare**, 28%: educate the workforce, formulate AI policies, become more evidence-based, and experiment. Funding targets AI literacy for the board/TMT and skill building.
  - Stage 2 **Build Pilots and Capabilities**, 34%: pilots, plus investment in APIs that link data and technologies.
  - Stage 3 **Develop AI Ways of Working** (industrialize AI), 31%: scalable enterprise architecture, transparent dashboards, a test-and-learn culture, process automation, and foundation models and SLMs applied to own data on secure platforms. Weill calls this "the holy trinity of AI — architecture, reuse, and agents."
  - Stage 4 **Become AI Future Ready**, 7%: AI embedded in all decision-making, proprietary AI, and selling AI-based services or AI-as-a-service to others.
  — [MIT Sloan](https://mitsloan.mit.edu/ideas-made-to-matter/whats-your-companys-ai-maturity-level); [MIT CISR press release](https://cisr.mit.edu/content/press-release-enterprise-ai-maturity-121924)
- **Scoring method (public):** "Total AI Effectiveness" is "the equally weighted combination of three measures: effectiveness of AI to (i) improve operations, (ii) improve customer experience, and (iii) support and develop the ecosystem." On a 0–100% scale: Stage 1 = 0–49%, Stage 2 = 50–74%, Stage 3 = 75–99%, Stage 4 = 100%. — [MIT CISR](https://cisr.mit.edu/publication/2024_1201_EnterpriseAIMaturityModel_WeillWoernerSebastian) [excerpt]
- **Financial link (2022):** profit vs. industry average was -9.6 pp (S1), -2.2 pp (S2), +8.7 pp (S3) and +10.4 pp (S4). — [MIT CISR](https://cisr.mit.edu/publication/2024_1201_EnterpriseAIMaturityModel_WeillWoernerSebastian) [excerpt]. Growth figures per stage (e.g., S4 +17.1 pp) appear only in a [LinkedIn post, secondary](https://www.linkedin.com/pulse/enterprise-ai-maturity-model-mit-cisr-uriel-castro-krqae) and are not verified.
- **2025 update** ("Grow Enterprise AI Maturity for Bottom-Line Impact," Aug 2025, Woerner, Sebastian, Weill, Kaganer): a new survey found that "enterprises today are making significant progress in their AI maturity, with the greatest financial impact seen in the progression from stage 2 ... to stage 3." Profit in 2025 vs. industry was -15.1 pp (S1), -1.4 pp (S2), +0.8 pp (S3) and +9.9 pp (S4). — [MIT CISR 2025](https://cisr.mit.edu/publication/2025_0801_EnterpriseAIMaturityUpdate_WoernerSebastianWeillKaganer) [excerpt]
- GenAI and agentic coverage: the 2024 interviews covered "traditional and generative AI and their early thoughts on agentic and robotic AI." Executives expect value from "four types of AI: analytical, generative, agentic, and robotic." — [MIT Sloan](https://mitsloan.mit.edu/ideas-made-to-matter/whats-your-companys-ai-maturity-level)
- Access: briefings are free to read (some CISR content is limited to members). Free "Talking Points" exist (Dec 2024) — [MIT CISR](https://cisr.mit.edu/publication/EnterpriseAIMaturity_TalkingPoints). CISR's suggested self-diagnosis is that organizations consider "which of the four stages describes most of their AI activity" — [MIT Sloan](https://mitsloan.mit.edu/ideas-made-to-matter/whats-your-companys-ai-maturity-level).

### Inferences
- The 3-item outcome-effectiveness score is a ready-made, validated short form. An AX app could use it as the "outcome" layer (operations / customer / ecosystem effectiveness, each rated 0–100%) and add capability items on top.
- Thresholds such as "Stage 4 = 100%" are strict. Any Korean adaptation should calibrate its cut-offs.

### Gaps
- The stage distribution for the 2025 survey and its sample size could not be retrieved (cisr.mit.edu was blocked for full text).
- The exact survey wording and Likert anchors are not public in what I accessed.
- Single respondent (likely a senior executive per company) is assumed but not confirmed.

---

## Q3a. McKinsey: State of AI survey, AI high performers, "Rewired"

### Takeaway
McKinsey has no public staged maturity model. It defines **AI high performers** by outcome (≥5% of EBIT from AI plus "significant value"; about 6% of respondents in 2025) and tracks adoption stages (experimenting / piloting / scaling) and practices. The 2025 edition explicitly measures **agentic AI**.

### Cited Findings
- "The state of AI in 2025: Agents, innovation, and transformation" (Nov 2025) was an online survey fielded June 25 to July 29, 2025, with 1,993 participants in 105 nations. — [McKinsey PDF via search](https://www.mckinsey.com/~/media/mckinsey/business%20functions/quantumblack/our%20insights/the%20state%20of%20ai/the-state-of-ai-in-2025-vf.pdf) [excerpt]
- 88% of organizations use AI in at least one business function (up from 78%). Most organizations are still in the experimenting or piloting stage. — [Silicon Canals, secondary](https://siliconcanals.com/m-mckinseys-2025-global-ai-survey-88-of-organizations-now-use-ai-in-at-least-one-function-up-from-78-but-most-are-still-stuck-in-pilot-mode-and-only-a-minority-can-point-to-any-real-impact/)
- High performers (about 6%) attribute ≥5% of EBIT to AI and report "significant value." 39% of respondents report any enterprise-level EBIT impact, and most of those say it is under 5% of EBIT. 64% say AI enables innovation. 62% are at least experimenting with AI agents and 23% are scaling an agentic system somewhere. — [McKinsey](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) [excerpt via search summary]
- High performers are about 3x more likely to fundamentally redesign workflows and 3.6x more likely to intend transformative change. They also show more senior leadership ownership and spend more than 20% of digital budgets on AI. — [colabsoftware / search summaries, secondary](https://www.colabsoftware.com/post/mckinseys-state-of-ai-2025-what-separates-high-performers-from-the-rest)
- "Rewired" (Lamarre, Smaje, Zemmel, Wiley 2023) structures digital and AI transformation around 6 capabilities: business-led roadmap, talent, operating model, technology, data, and adoption and scaling. — **[unverified-memory]**

### Inferences
- McKinsey's approach suggests an outcome-based classification (EBIT share, value) that sits alongside capability maturity. It also suggests tracking adoption breadth across functions and agent adoption (experimenting vs. scaling).

### Gaps
- McKinsey has no public self-assessment questionnaire, item count or levels. Its "Rewired" diagnostic is consultant-led and not public.
- mckinsey.com was blocked, so the full practice list (e.g., the ~12 adoption and scaling practices) could not be extracted.

---

## Q3b. BCG: "Where's the Value in AI?" (Oct 2024), "The Widening AI Value Gap" (Sep 2025), 10-20-70

### Takeaway
BCG segments companies into **4 maturity groups** (stagnating, emerging, scaling, future-built) based on **30 enterprise capabilities** in 5 categories. This is the most detailed public capability list from any consulting firm, and it explicitly includes GenAI items; the 2025 edition adds AI agents. The **10-20-70** rule (10% algorithms, 20% tech and data, 70% people and processes) is BCG's resource-allocation principle.

### Cited Findings
- 2024 study: more than 1,000 CxOs and senior executives across more than 20 industries in 59 countries, conducted in Q3 2024. — [BCG](https://www.bcg.com/publications/2024/wheres-value-in-ai) [via search summary]
- **Segmentation (2024):** Leaders make up 26%, split into **AI future-built 4%** ("systematically building cutting-edge AI capabilities across functions and consistently generating substantial value") and **AI scaling 22%** ("developed an AI strategy and advanced capabilities, and are scaling them effectively while starting to generate value"). Stagnating makes up 74%, split into **AI stagnating** ("minimal or no AI action, lack foundational capabilities") and **AI emerging** ("foundational capabilities and initial experimentation but struggling to scale"). — [BCG PDF](https://web-assets.bcg.com/a5/37/be4ddf26420e95aa7107a35aae8d/bcg-wheres-the-value-in-ai.pdf); [BCG press release](https://www.bcg.com/press/24october2024-ai-adoption-in-2024-74-of-companies-struggle-to-achieve-and-scale-value)
- **30 capabilities in 5 categories** (as extracted from the PDF):
  - Governance: AI/GenAI strategy, data governance, responsible AI, tech innovation, C-suite expertise, risk and responsible-AI tools.
  - Customer experience: customer journey, customer service, digital marketing, next-gen sales, GenAI pricing.
  - Operating model: talent and skills, culture and change, product/platform orientation, roles and responsibilities, partnership ecosystem.
  - Data and AI/GenAI platform: data analytics, data management, AI/GenAI platforms, model quality, cybersecurity, third-party risk, AI/GenAI tools, data security.
  - Operations: AI delivery office, AI/GenAI portfolio, rapid ideation and testing, service process reimagination, vendor selection, AI deployment guardrails, new product build, digital supply chain, digital support functions, Industry 4.0.
  — [BCG PDF](https://web-assets.bcg.com/a5/37/be4ddf26420e95aa7107a35aae8d/bcg-wheres-the-value-in-ai.pdf). This came from LLM extraction and the count per category may not sum exactly to 30, so verify against the PDF exhibit.
- Leader financial results (3-year): 50% greater revenue growth, 60% higher TSR and 40% higher ROIC. 62% of AI value comes from core business functions and 38% from support functions. Leaders pursue about half as many opportunities as their peers. — [BCG PDF](https://web-assets.bcg.com/a5/37/be4ddf26420e95aa7107a35aae8d/bcg-wheres-the-value-in-ai.pdf)
- 10-20-70: "about 10 percent of resources on algorithms, 20 percent on technology and data, 70 percent on people and processes." — [BCG](https://www.bcg.com/publications/2024/wheres-value-in-ai) [via search summary]
- **2025 update** ("The Widening AI Value Gap," published Sep 17, 2025, modified Jun 2026): **future-built 5%, scalers 35%, laggards 60%**. Future-built companies achieve 5x the revenue increases and 3x the cost reductions from AI. AI agents make up about 17% of total AI value in 2025, expected to reach 29% by 2028. Future-built companies allocate 15% of AI budgets to agents. A third of future-built companies use agents, versus 12% of scalers and almost none of the laggards. — [BCG 2025](https://www.bcg.com/publications/2025/are-you-generating-value-from-ai-the-widening-gap)
- Note on terminology: BCG's own 2025 page describes the 2024 result as "only 22% ... beyond proof-of-concept, only 4% creating substantial value." This differs from the 26% headline because 26% = 22% + 4%. — [BCG 2025](https://www.bcg.com/publications/2025/are-you-generating-value-from-ai-the-widening-gap)

### Inferences
- BCG's 5-category, 30-capability list is the best public template for AX survey items. GenAI-specific items (GenAI pricing, AI deployment guardrails, AI/GenAI portfolio) show how to embed GenAI readiness.
- 10-20-70 can be turned into a survey check that compares the organization's actual spend or effort split with 10/20/70.

### Gaps
- The scoring thresholds that map 30 capability scores to the 4 groups are **not public**. The diagnostic is consultant-led and BCG has no public self-assessment tool.
- The 2025 survey sample size and countries were not captured.

---

## Q3c. Deloitte: State of (Generative) AI in the Enterprise

### Takeaway
Deloitte runs a recurring benchmark survey (the GenAI quarterly series in 2024–25, now "State of AI in the Enterprise 2026"). It measures **preparedness across strategy, infrastructure, data, risk/governance and talent**, and since 2025 it also covers agentic AI. It does not publish a staged maturity model.

### Cited Findings
- "The State of AI in the Enterprise: The Untapped Edge" (2026, launched around Davos, January 2026) surveyed **over 3,000 director-to-C-suite leaders** with direct involvement in AI, with the sample "split equally between IT and line of business leaders." — [Deloitte press release](https://www.deloitte.com/us/en/about/press-room/state-of-ai-report-2026.html); [Deloitte](https://www.deloitte.com/us/en/what-we-do/capabilities/applied-artificial-intelligence/content/state-of-ai-in-the-enterprise.html)
- Findings: worker access to sanctioned AI tools rose from under 40% to about 60%, "50% in one year." The number of companies with ≥40% of AI projects in production "is set to double in six months." 42% believe their **strategy** is highly prepared, but companies feel less prepared on **infrastructure, data, risk, and talent**. 85% expect to customize agents. — [Deloitte](https://www.deloitte.com/us/en/what-we-do/capabilities/applied-artificial-intelligence/content/state-of-ai-in-the-enterprise.html); [press release](https://www.deloitte.com/us/en/about/press-room/state-of-ai-report-2026.html)
- Agentic AI: Deloitte reports that "agentic AI usage is scaling faster than guardrails." — [Deloitte Insights](https://www.deloitte.com/us/en/insights/topics/emerging-technologies/ai-agents-scaling-faster.html)

### Inferences
- Deloitte's 5 preparedness areas (strategy, tech infrastructure, data management, risk and governance, talent) are a light "readiness" frame.
- The dual-respondent sampling (IT plus business) is a useful design cue for multi-respondent AX surveys.

### Gaps
- Deloitte's Trustworthy AI framework dimensions and its client AI readiness diagnostic tools were not retrieved this session.
- Deloitte has no public self-assessment item set.

---

## Q3d. Accenture: "The Art of AI Maturity" (2022)

### Takeaway
Accenture uses a 2-axis index (foundational vs. differentiation capabilities, each scored 0–100) that yields 4 archetypes. **AI Achievers** are 12% of companies, and the median overall maturity is 36 out of 100.

### Cited Findings
- Sample: 1,615 executives (CEOs, C-suite, CAIOs, data-science leaders) at about 1,200 companies with revenue over US$1B, fielded August to September 2021. The report was published in 2022. — [Accenture PDF](https://www.accenture.com/content/dam/system-files/acom/custom-code/ai-maturity/Accenture-Art-of-AI-Maturity-Report-Global-Revised.pdf). The press release cites "financial and non-financial data of 1,176 companies" — [Accenture newsroom](https://newsroom.accenture.com/news/2022/more-than-60-percent-of-companies-are-only-experimenting-with-ai-creating-significant-opportunities-for-value-on-their-journey-to-ai-maturity-accenture-research-finds). Note the small inconsistency between 1,176 and about 1,200.
- Capabilities: **foundational** capabilities (e.g., cloud platforms and tools, data platforms, architecture and governance) and **differentiation** capabilities (e.g., AI strategy and C-suite sponsorship combined with a culture of innovation). The report lists 16 key capabilities in total, but the full list was not extracted. — [Accenture PDF](https://www.accenture.com/content/dam/system-files/acom/custom-code/ai-maturity/Accenture-Art-of-AI-Maturity-Report-Global-Revised.pdf)
- **Scoring:** "the overall AI maturity index is built as the arithmetic average of both AI foundational index and AI differentiation index." Groups are clustered using the top quartile on each axis. — [Accenture PDF](https://www.accenture.com/content/dam/system-files/acom/custom-code/ai-maturity/Accenture-Art-of-AI-Maturity-Report-Global-Revised.pdf)
- **4 groups:**

  | Group | Share of companies | Profile | Median index |
  |---|---|---|---|
  | **AI Achievers** | 12% | top quartile on both axes | 64/100 |
  | **AI Builders** | 12% | strong foundational, average differentiation | 44/100 |
  | **AI Innovators** | 13% | strong differentiation, average foundational | 50/100 |
  | **AI Experimenters** | 63% | average on both | 29/100 |

  The median across all companies is 36/100. — [Accenture PDF](https://www.accenture.com/content/dam/system-files/acom/custom-code/ai-maturity/Accenture-Art-of-AI-Maturity-Report-Global-Revised.pdf)
- Achiever traits:
  1. Champion AI as a strategic priority with full leadership sponsorship.
  2. Invest heavily in talent.
  3. Industrialize AI tools and teams (the "AI core").
  4. Design AI responsibly from the start.
  5. Prioritize both long- and short-term AI investments.

  Achievers are 3.5x more likely than Experimenters to have AI-influenced revenue above 30% of total revenue. The share of Achievers was projected to rise from 12% to 27% by 2024. — [Accenture PDF](https://www.accenture.com/content/dam/system-files/acom/custom-code/ai-maturity/Accenture-Art-of-AI-Maturity-Report-Global-Revised.pdf)

### Inferences
- The 2-axis (foundation × differentiation) quadrant is a strong visualization idea for the AX app's results page. It works alongside a radar chart.
- The data predates GenAI. Accenture's later GenAI and agentic work (e.g., "Reinventing enterprise operations" and "Front-runners" reports) was not checked this session.

### Gaps
- The full list of 16 capabilities, the item count and Accenture's AI maturity diagnostic tool are not public, or were not retrieved.
- Accenture's 2024–2026 GenAI and agentic maturity updates were not researched due to the tool budget.

---

## Q3e. PwC, KPMG, EY

### Takeaway
PwC (US) publishes the most specific productized readiness assessment found in this research: **12 domains, 285+ questions, 5 levels (AI-Vulnerable → AI-Driven Leader), and benchmarking against 500+ organizations**. KPMG Germany has a **6-level (0–5) GenAI capability-oriented** maturity scale. EY specifics were not found.

### Cited Findings
- **PwC "Enterprise AI readiness assessment"** (US page, released Jul 29, 2026):
  - Domains (12): strategic vision, innovation culture, product innovation, measurement, business model resilience, operational excellence, technology infrastructure, data assets and governance, talent, customer experience, financial resilience, and risk management.
  - Items: "285+" diagnostic questions.
  - Levels: "five maturity levels" from "AI-Vulnerable" to "AI-Driven Leader." The intermediate level names are not on the page.
  - Outputs: "peer comparison across 500+ organizations" and a "90-day, 6-month, 12-month action plan."
  - Method, respondents and price are not stated (likely a paid consulting engagement).

  — [PwC](https://www.pwc.com/us/en/services/consulting/strategy/enterprise-functional-strategy/ai-readiness-assessment.html)
- **KPMG Germany "AI Capability Maturity Assessment"**, with levels:
  - 0 Foundational Data Readiness
  - 1 Basic Interaction & Prompting
  - 2 Contextualisation
  - 3 Enhanced Reliability & Control
  - 4 Advanced Adaptation & Integration
  - 5 Operationalisation & Optimisation at Scale

  A white paper download is offered. — [KPMG DE](https://kpmg.com/de/en/insights/digital-transformation/artificial-intelligence/ai-capability-maturity-assessment.html). The level names (prompting, contextualisation, i.e., RAG) indicate a **GenAI/LLM-specific** technical maturity ladder.
- KPMG's Trusted AI framework is reported to have 10 pillars (accountability, data integrity, explainability, transparency, sustainability, fairness, privacy, reliability, safety, security). — [search summary, secondary](https://kpmg.com/us/en/articles/2025/when-trust-ai-matters.html)
- EY: no public maturity model details found; search results only mentioned the EY.ai platform. — gap

### Inferences
- PwC's 285+ items over 12 domains (about 24 per domain) is a benchmark for a "deep" diagnostic. An AX app might offer a short form of about 30–60 items and a deep form.
- KPMG's ladder is a template for a separate **GenAI/agent technical maturity** sub-scale.

### Gaps
- PwC's level definitions, respondent design and pricing are not stated.
- KPMG's dimensions and method are not on the page (they are in the white paper, which was not retrieved).
- EY is not covered.

---

## Q3f. IDC (AI MaturityScape) and Forrester

### Takeaway
IDC uses its standard 5-stage MaturityScape (Ad hoc, Opportunistic, Repeatable, Managed, Optimized). Its "AI MaturityScape 2.0" dates from May 2022, and a 2025 FutureScape reframes the stages around **agentic** enablement. A public Forrester enterprise AI maturity model was not found.

### Cited Findings
- All IDC MaturityScapes use 5 stages: "ad hoc, opportunistic, repeatable, managed, and optimized." — [IDC DX MaturityScapes PDF](https://www.idc.com/downloads/DX_UBER.pdf) [excerpt]
- "IDC MaturityScape: Artificial Intelligence 2.0" (May 2022) has stage names Ad hoc / Opportunistic / Repeatable / Managed / Optimized and includes a "Vision/Strategy" dimension ("The organization is still devising AI strategy..."). — [CourseHero copy, secondary](https://www.coursehero.com/file/154550182/IDC-MaturityScape-Artificial-Intelligence-20-2022-Maypdf/)
- IDC FutureScape "Determine the AI Maturity Stage" (Oct 2025) gives a timeline view:
  - 2023–24: "Uncoordinated initiatives with no AI strategy or central leadership"
  - 2025: "Repeatable / AI central function drives more consistent practices and use cases in production"
  - 2028–29: "AI Alignment / Productivity and revenue focus through agentic enablement of functions"
  - 2030+: "Optimized / AI-Fueled Organization ... AI-first strategy with agentic-based processes reshapes business operating model"

  IDC MaturityScapes typically cover "3-5 dimensions." — [IDC PDF](https://www.idc.com/wp-content/uploads/2025/10/IDC-FutureScape_Understand-the-AI-Maturity-Stage.pdf)
- IDC also publishes a sector benchmark ("AI-Fueled Public Sector Organization" MaturityScape) whose stages carry labels such as "Ad Hoc — AI Scramble" and "Opportunistic — AI Pivot." — [IDC TOC](https://my.idc.com/research/viewtoc.jsp?containerId=US53583125) [excerpt]
- Forrester: no enterprise AI maturity model was found. Search results show Forrester's Digital Maturity Model 4.0 (Skeptics / Adopters / Collaborators / Differentiators) — [secondary](http://forrester.nitro-digital.com/pdf/Forrester-s%20Digital%20Maturity%20Model%204.0.pdf) — and a commissioned Forrester Consulting AI maturity study for Experian (credit risk and fraud, 2026) — [Experian](https://experianacademy.com/blog/2026/04/08/ai-maturity-assessment-credit-risk-fraud/).

### Inferences
- IDC's 5-stage ladder is the classic CMM-style progression. It is easy to localize and familiar to Korean IT buyers.

### Gaps
- IDC's AI MaturityScape dimensions (names and count), its stage distribution benchmarks and its assessment tool are behind a paywall. The definitions for the 2025 stage are only partial.
- Forrester has no verifiable AI maturity model.

---

## Q4. Which models measure GenAI / agentic readiness specifically (2024–2026)?

### Takeaway
Explicit GenAI or agentic measurement appears in:
- **BCG** (GenAI capabilities among the 30; agents' share of value and budget in 2025)
- **McKinsey** (agent experimenting vs. scaling, 2025)
- **Deloitte** (agentic adoption and guardrails, 2026)
- **KPMG DE** (a GenAI-oriented technical ladder)
- **IDC** (agentic stages in the 2025 FutureScape)
- **MIT CISR** (agentic discussed qualitatively in Stage 3 and 4 commentary)

Accenture's 2022 index predates GenAI. Gartner's public page does not show GenAI-specific pillars.

### Cited Findings
- BCG 2025: agents make up 17% of AI value (expected 29% by 2028), and future-built companies spend 15% of AI budgets on agents — [BCG](https://www.bcg.com/publications/2025/are-you-generating-value-from-ai-the-widening-gap). BCG 2024 capabilities include "AI and GenAI strategy," "GenAI pricing" and "AI and GenAI platforms" — [BCG PDF](https://web-assets.bcg.com/a5/37/be4ddf26420e95aa7107a35aae8d/bcg-wheres-the-value-in-ai.pdf)
- McKinsey 2025: 62% are experimenting with agents and 23% are scaling — [McKinsey](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai) [excerpt]
- Deloitte 2026: 85% expect to customize agents, and agentic usage is "scaling faster than guardrails" — [Deloitte](https://www.deloitte.com/us/en/about/press-room/state-of-ai-report-2026.html); [Deloitte Insights](https://www.deloitte.com/us/en/insights/topics/emerging-technologies/ai-agents-scaling-faster.html)
- KPMG levels: "Basic Interaction & Prompting," "Contextualisation" and others — [KPMG DE](https://kpmg.com/de/en/insights/digital-transformation/artificial-intelligence/ai-capability-maturity-assessment.html)
- IDC 2025: "agentic enablement of functions" and "agentic-based processes" — [IDC](https://www.idc.com/wp-content/uploads/2025/10/IDC-FutureScape_Understand-the-AI-Maturity-Stage.pdf)
- MIT CISR: Stage 3 "architecture, reuse, and agents"; four AI types (analytical, generative, agentic, robotic) — [MIT Sloan](https://mitsloan.mit.edu/ideas-made-to-matter/whats-your-companys-ai-maturity-level)

### Inferences
- An AX survey for 2026 should include an agent-specific module covering:
  - agent adoption stage (none / experimenting / piloting / scaled)
  - share of AI budget going to agents
  - agent guardrails and governance
  - workflow redesign for agents

### Gaps
- Not confirmed whether Gartner's current toolkit contains GenAI- or agent-specific questions.

---

## Q5. Which offer public self-assessment questionnaires, and what do sample questions look like?

### Takeaway
None of the major firms publishes its full item bank. Of the six assessments below, the only one with a public scoring formula is MIT CISR's 3-measure Total AI Effectiveness; the others are paid, client-gated or consultant-led:

| Publisher | Access to the questionnaire |
|---|---|
| MIT CISR | Free: 3-measure Total AI Effectiveness formula plus stage cut-offs are public |
| Gartner | Client-only online questionnaire; non-clients can view a demo after a lead form |
| PwC | 285+ questions, not published |
| BCG | Consultant-scored, not public |
| McKinsey | Consultant-led, not public |
| Accenture | Index method described, items not public |

### Cited Findings
- MIT CISR measures: effectiveness of AI to "(i) improve operations, (ii) improve customer experience, and (iii) support and develop the ecosystem," on a 0–100% scale — [MIT CISR](https://cisr.mit.edu/publication/2024_1201_EnterpriseAIMaturityModel_WeillWoernerSebastian) [excerpt]
- Gartner: "guided AI maturity assessment questionnaire ... seven core AI pillars," for clients; non-clients can launch a demo after a lead form — [Gartner](https://www.gartner.com/en/chief-information-officer/research/ai-maturity-model-toolkit)
- PwC: "285+" diagnostic questions; the questions themselves are not published — [PwC](https://www.pwc.com/us/en/services/consulting/strategy/enterprise-functional-strategy/ai-readiness-assessment.html)
- Example of item stems that can be derived (not quoted from any vendor; illustration only): "To what extent has AI improved our operations? (0–100%)". This mirrors the CISR measures. Any other sample items in the report should be labeled as our own design, not as vendor items.

### Inferences
- Respondent design is mostly a single senior respondent per company in the surveys (Accenture: C-suite and data-science leaders; MIT CISR: senior executives; BCG: CxOs). Deloitte deliberately balances IT and business respondents. For an AX app, multi-respondent input (CEO/strategy, CIO/CDO, business unit heads, HR) with aggregation would improve on the vendor practice.

### Gaps
- No publicly released vendor sample questions (verbatim) were found for Gartner, BCG, McKinsey, Accenture, PwC, KPMG, EY, IDC or Forrester.
- Free online self-assessment tools from these firms (for example, country-specific Deloitte or KPMG quick checks) may exist but were not found within the tool budget.
