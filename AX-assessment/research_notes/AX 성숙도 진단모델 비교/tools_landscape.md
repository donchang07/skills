# AI Readiness / AI Maturity Assessment Tools — Product Landscape (as of 2026-10-01)

Research method note: Firecrawl search/scrape (rate-limited) plus WebSearch; WebFetch was egress-blocked for cisco.com, sectionai.com, cultureamp.com, so some pages were only seen as search excerpts or partial scrapes. Anything not confirmed on a page is listed under Gaps rather than asserted.

## 1. Which online AI readiness/maturity assessment tools exist?

### Takeaway
The market splits into five clusters: (a) free vendor/consultancy self-assessments used as lead-gen (Cisco, Microsoft, Avanade, IDC, AWS partners, Infosys/Korn Ferry); (b) analyst toolkits behind a paywall (Gartner); (c) workforce AI-skills/proficiency measurement platforms (Workera, Section); (d) HR/employee-survey platforms with AI-adoption templates (Culture Amp, Leapsome, Glint etc.); and (e) a fast-growing long tail of low-cost SaaS and white-label assessment builders aimed at SMEs and consultants (AssessmentCloud, Audity, Pointerpro, ScoreApp, Sensiwise SAIRA, Iternal). Almost no product in (a)/(b) surveys many employees; (c)/(d) survey many employees but don't produce an org-level "AI maturity model" report.

### Cited Findings
**Free vendor / consultancy self-assessments (single respondent, lead-gen)**
- Cisco AI Readiness Assessment: six pillars — Strategy, Infrastructure, Data, Governance, Talent, Culture; output is a score and results by pillar; four readiness tiers: Pacesetters (Fully Prepared, >86/100), Chasers (61–85), Followers (31–60), Laggards (0–30). Page metadata dated Sep 2026. — [Cisco AI Readiness Assessment](https://www.cisco.com/c/m/en_us/solutions/ai/readiness-index/assessment-tool.html)
- Cisco benchmarks the user against its AI Readiness Index, a double-blind survey of 8,161 business leaders at 500+ employee organizations across 30 markets; the 2025 index scores 49 indicators with pillar weights Infrastructure 25%, Data 20%, Strategy 15%, Governance 15%, Talent 15%, Culture 10%. — [Augment Code tools review](https://www.augmentcode.com/tools/ai-readiness-assessment-tools) citing [Cisco 2025 Index PDF](https://www.cisco.com/c/dam/m/en_us/solutions/ai/readiness-index/2025-m10/documents/cisco-ai-readiness-index-2025-realizing-the-value-of-ai.pdf)
- Cisco also offers a separate Index "Look-up Tool" to compare regions, markets and industries across the six pillars (public benchmark explorer). — [Cisco Look-up Tool](https://www.cisco.com/c/m/en_us/solutions/ai/readiness-index/lookup-tool.html)
- Microsoft AI Readiness Assessment (Microsoft Learn Assessments): seven pillars — Business Strategy, AI Governance & Security, Data Foundations, AI Strategy & Experience, Organization & Culture, Infrastructure for AI, Model Management; listed at ~45 minutes. — [Microsoft Learn](https://learn.microsoft.com/en-in/assessments/94f1c697-9ba7-4d47-ad83-7c6bd94b1505/); format described as "45-minute multiple-choice online assessment, free" — [Augment Code](https://www.augmentcode.com/tools/ai-readiness-assessment-tools)
- Microsoft partners sell remediation services on Azure Marketplace that explicitly "re-score all seven pillars" of Microsoft's assessment (i.e., the free tool feeds a partner services funnel). — [Azure Marketplace listing](https://marketplace.microsoft.com/en-sg/product/simplicityitinc1734733403274.aireadinessassessment)
- Avanade AI Readiness Assessment: online assessment "informed by insights from Avanade and Microsoft research", evaluating people, processes and platforms, to "identify actions to increase AI maturity". — [Avanade AI Readiness Hub](https://www.avanade.com/en/services/artificial-intelligence/ai-readiness-hub); [Avanade assessment page](https://www.avanade.com/en-ca/services/artificial-intelligence/ai-readiness-hub/ai-readiness-assessment)
- Infosys + Korn Ferry developed a maturity-assessment tool for firms (described in an Infosys Knowledge Institute article). — [Infosys "Maturing AI in the Organization"](https://www.infosys.com/iki/perspectives/maturing-ai-organization.html)
- Other free/low-touch entries named in a 2026 roundup: IDC "CIO Playbook: AI Readiness Assessment" (free online self-assessment); Accenture + CMU SEI "AI Adoption Maturity Model" (assessment + benchmarking, launched 2026); Fivetran 2026 Agentic AI Readiness Index (report). — [Augment Code](https://www.augmentcode.com/tools/ai-readiness-assessment-tools)
- A Connxions AWS assessment has 22 questions and a 0–100 score; Microsoft's takes ~45 min. (Hong Kong vendor comparison, 2026-09-30.) — [UD.hk comparison](https://www.ud.hk/en/blogs/insight/article/free-ai-readiness-assessments-compared-2026-09-30)
- Google Cloud AI Readiness (AIR) Program is a 2–3 week engagement (survey + meetings + workshops) priced by quote — more consulting than questionnaire. — [Summit Trails buyer's guide](https://summittrails.com/blog/best-ai-readiness-assessment-tools/)
- Iternal Technologies offers a free "AI Readiness Assessment for Enterprises". — [Iternal](https://iternal.ai/assessments/ai-readiness-assessment)

**Analyst toolkit**
- Gartner AI Maturity Assessment: online tool to gauge maturity across seven capability categories — strategy, value, organization, people and culture, governance, engineering, data. — [Gartner doc 6383743](https://www.gartner.com/en/documents/6383743)
- Gartner AI Maturity Model and AI Roadmap Toolkit: five stages Foundational → Emerging → Operational → Scaled → Transformational; the client report shows current vs target maturity per capability (a roadmap feature). — [Gartner toolkit page](https://www.gartner.com/en/chief-information-officer/research/ai-maturity-model-toolkit)
- A Gartner survey instrument used a seven-question survey rated Level 1–5; Gartner's Q4 2024 benchmark (432 respondents) showed high-maturity orgs averaging 4.2–4.5 vs 1.6–2.2 for low-maturity. — [Augment Code](https://www.augmentcode.com/tools/ai-readiness-assessment-tools) citing [Gartner press release 2025-06-30](https://www.gartner.com/en/newsroom/press-releases/2025-06-30-gartner-survey-finds-forty-five-percent-of-organizations-with-high-artificial-intelligence-maturity-keep-artificial-intelligence-projects-operational-for-at-least-three-years)

**Workforce AI-skills / proficiency platforms (multi-respondent)**
- Workera AI Readiness: scenario-based assessments ("not a multiple-choice form") across six dimensions: AI fluency; prompt & agent design; model & tool judgment; AI risk, ethics & governance; applied AI in role; durable human skills. Also an "always-on Ambient signal". — [Workera AI Readiness](https://www.workera.ai/solutions/ai-readiness)
- Section (sectionai.com) runs an AI Proficiency benchmark that scores workers (e.g., average proficiency 42 at orgs with a full-time Head of AI vs 33 without; segments such as "Novices" = 20.9%). — [Section AI Proficiency Report](https://www.sectionai.com/ai/the-ai-proficiency-report)

**Employee-survey / HR platforms with AI templates**
- Culture Amp "AI Effectiveness at Work" template: 20-question pulse survey, attributed (snapshot) type, four factors — Culture, Confidence, Conscience, Capability; sample item: "Our leaders have clearly explained how we plan to use AI to reach our goals". Can be run standalone or a few items embedded in engagement surveys. — [Culture Amp support](https://support.cultureamp.com/en/articles/11788533-welcome-to-the-ai-effectiveness-at-work-survey); [Culture Amp templates overview](https://support.cultureamp.com/en/articles/7048360-survey-templates-overview); [Culture Amp blog](https://www.cultureamp.com/blog/employees-stuck-in-technical-challenge)
- Leapsome publishes AI readiness assessment content (blog positioning its survey platform for measuring AI maturity). — [Leapsome blog](https://www.leapsome.com/blog/ai-readiness-assessment)

**Low-cost SaaS / white-label tools for consultants**
- AssessmentCloud: scores five dimensions (data & digital maturity, AI skills, process readiness, governance, culture) 0–100 against an industry median, ranks the weakest foundation first, positions re-check "in six months"; flat price from $49/month for the whole company, no per-employee fees. — [AssessmentCloud](https://assessmentcloud.com/ai-readiness-assessment)
- Audity (auditynow.com): white-label AI readiness platform for consultants — full branded surface (assessment, report, deliverables), unlimited "ReadyLink" assessments, prioritized gap analysis, ROI projections, web intelligence on client environment, stakeholder-specific deliverables. Pricing: Scout $99/mo; Pro $397/mo; Teams $397/seat. (Article dated 2026-04-14, vendor's own blog.) — [Audity](https://auditynow.com/blog/white-label-ai-readiness-assessment-platform)
- Pointerpro: generic assessment builder that auto-generates personalized PDF/.ppt advice reports; white-label on all paid plans; advanced scoring with custom multi-step formulas; "AI prompt widget" to scale narrative report content. ScoreApp restricts white-label (own domain, removing badge) and PDF reports to its top Pro plan and lacks custom formulas (per Pointerpro's comparison page — vendor-biased). — [Pointerpro vs ScoreApp](https://pointerpro.com/comparisons/scoreapp-alternative/); [Pointerpro home](https://pointerpro.com/); [Pointerpro white-label](https://pointerpro.com/features/white-label-assessment-platform/)
- ScoreApp has an "AI Assessment Builder" that drafts an assessment in minutes, aimed at marketers building lead magnets. — [ScoreApp](https://www.scoreapp.com/ai-assessment-builder/)
- Other named: Sensiwise SAIRA (SME-priced), AWS AI Readiness Assessment via partners (quote-based) — [TheTechFounders roundup](https://thetechfounders.co.uk/guides/10-best-ai-readiness-assessment-platforms-available-in-2026/); White Label IQ: 10-week AI readiness audit across seven departments for agencies — [White Label IQ](https://www.whitelabeliq.com/readiness-assessment/); Cloudiway MSP program with white-labeled paid audit reports (Copilot readiness) — [Cloudiway](https://cloudiway.com/ai-readiness-msp-program/)

### Inferences
- Big-vendor free tools (Cisco/Microsoft/Avanade) are infrastructure-weighted (Cisco weights Infrastructure+Data at 45%) and designed to funnel into services/products; they are poor at measuring employee-level adoption, skills or sentiment.
- The "survey many employees → org maturity report" job is currently stitched together from two product categories (HR survey tools + strategic self-assessment). A product that natively combines both is a visible white space.

### Gaps
- Could not verify Cisco question count / completion time / lead-capture form (page scrape returned no such detail).
- No product page found for Wipro, Capgemini or Cognizant online self-assessment tools in this pass; they appear to sell assessments as consulting services (unverified).
- Multiverse, Coursera, Udemy AI skills assessments and BCG's own client diagnostic tooling were not researched due to tool-call limits.
- Gartner toolkit pricing (client-only access) not public.

## 2. Features (multi-respondent, branching, anonymity, benchmarking, visualization, perception gap, roadmap, GenAI narrative, PDF, white-label, longitudinal)

### Takeaway
Benchmarking and a pillar score are near-universal; roadmap/gap prioritization is common in paid tools; GenAI narrative and white-label PDF exist in assessment builders (Pointerpro, Audity). Features that are rare or absent in the products found: true role-segmented multi-respondent org surveys with an explicit leader-vs-employee perception-gap view, anonymity thresholds tied to maturity reporting, and longitudinal tracking built into a maturity model.

### Cited Findings
- Multi-respondent with privacy: Workera is "consent-first by default" — individual sees own data first, managers/admins see aggregate only, users opt in to share more. — [Workera](https://www.workera.ai/solutions/ai-readiness)
- Rollups/heatmap-like views: Workera provides cohort, function and individual rollups configurable to the leadership's readiness framework, plus an executive readout with "one narrative for the board, one diagnostic for the CHRO, one capability plan for the CTO" (audience-specific report variants). — [Workera](https://www.workera.ai/solutions/ai-readiness)
- Benchmarking: Workera plots results against industry and function peers; Cisco benchmarks against its 8,161-leader index; AssessmentCloud scores vs industry median; Culture Amp templates use benchmark items to compare against "hundreds of other organizations". — [Workera](https://www.workera.ai/solutions/ai-readiness); [Augment Code](https://www.augmentcode.com/tools/ai-readiness-assessment-tools); [AssessmentCloud](https://assessmentcloud.com/ai-readiness-assessment); [Culture Amp templates](https://support.cultureamp.com/en/articles/7048360-survey-templates-overview)
- Recommendations/roadmap: Gartner shows current vs target maturity per capability (roadmap toolkit); AssessmentCloud ranks weakest foundation first; Audity produces prioritized gap analysis and ROI projections; Workera generates AI-personalized learning against verified gaps. — [Gartner](https://www.gartner.com/en/chief-information-officer/research/ai-maturity-model-toolkit); [AssessmentCloud](https://assessmentcloud.com/ai-readiness-assessment); [Audity](https://auditynow.com/blog/white-label-ai-readiness-assessment-platform); [Workera](https://www.workera.ai/solutions/ai-readiness)
- Longitudinal re-assessment: Workera triggers re-assessment "surgically against a verified gap" and markets "Measured. Verified. On repeat."; AssessmentCloud positions six-month re-checks; Culture Amp pulse design implies repeatable cadence. — [Workera](https://www.workera.ai/solutions/ai-readiness); [AssessmentCloud](https://assessmentcloud.com/ai-readiness-assessment)
- GenAI narrative & PDF: Pointerpro auto-generates personalized PDF/.ppt reports and has an AI prompt widget for narrative text; ScoreApp offers PDF reports only on Pro. — [Pointerpro vs ScoreApp](https://pointerpro.com/comparisons/scoreapp-alternative/)
- White-labeling: Audity (full branded surface under firm's brand/domain), Pointerpro (all paid plans), ScoreApp (Pro only), Cloudiway (white-labeled reports for MSPs). — sources above.
- Integrations: Workera feeds HRIS, ATS and L&D tools. — [Workera](https://www.workera.ai/solutions/ai-readiness)

### Inferences
- A differentiated AX tool could combine: (1) role-branched multi-respondent survey (exec / manager / IC) with anonymity thresholds; (2) leader-vs-employee perception-gap visualization (none of the tools found advertises this explicitly); (3) consultant white-label + GenAI narrative report (already table stakes in builders); (4) built-in re-assessment and delta tracking.
- Audience-specific report variants (Workera's board/CHRO/CTO pattern) are a UX pattern worth copying.

### Gaps
- No product found that explicitly markets "perception gap analysis between leaders and employees" — absence in this search, not proof of non-existence.
- Anonymity minimum-group thresholds (e.g., n≥5) for AI templates in Culture Amp/Glint not confirmed in pages accessed (Culture Amp AI template is "attributed", i.e., linked to demographics, but threshold rules not seen).
- Role-based question branching in Cisco/Microsoft tools not confirmed.
- No G2/Capterra review data collected.

## 3. Pricing models, question count, completion time

### Takeaway
Pricing is bimodal: free single-respondent lead-gen quizzes (Cisco, Microsoft, Avanade, IDC, AWS partner) vs consulting engagements in the tens to hundreds of thousands of dollars; a thin middle of SaaS at $49–$400/month is emerging. Completion: ~20-question pulse (Culture Amp), 22 questions (AWS partner), ~45 min (Microsoft).

### Cited Findings
- Free tier: Microsoft (45-min, free), Cisco (free self-assessment + annual report), IDC (free). — [Augment Code](https://www.augmentcode.com/tools/ai-readiness-assessment-tools)
- Paid consulting ranges (Augment Code estimate, secondary source): independent mid-market $15k–$75k for 2–4 weeks; enterprise practitioner $40k–$120k for 4–8 weeks; Big Four/strategy firm $100k–$500k+; AI-native sprints $75k–$250k over 90 days. — [Augment Code](https://www.augmentcode.com/tools/ai-readiness-assessment-tools)
- SaaS: AssessmentCloud from $49/month flat per company — [AssessmentCloud](https://assessmentcloud.com/ai-readiness-assessment); Audity $99 / $397 per month / $397 per seat — [Audity](https://auditynow.com/blog/white-label-ai-readiness-assessment-platform)
- HR survey platforms (general engagement pricing, not AI-specific): Microsoft Viva Glint from $2/user/month; Lattice engagement add-on $4/seat/month; 15Five $4/user/month; Workleap $5/user/month (10-user min); SurveyMonkey Engage ~ $19/user/month; QuestionPro Workforce has a free tier. — [Engagedly 2026 roundup](https://engagedly.com/blog/best-employee-engagement-survey-softwares/)
- Google Cloud AIR: quote-based, 2–3 weeks. AWS readiness via partners: quote-based. — [Summit Trails](https://summittrails.com/blog/best-ai-readiness-assessment-tools/); [TheTechFounders](https://thetechfounders.co.uk/guides/10-best-ai-readiness-assessment-platforms-available-in-2026/)
- Question counts: Culture Amp 20 items; Connxions AWS 22 questions; Gartner instrument 7 questions (L1–L5); Microsoft ~45 min. — sources above.

### Inferences
- A consultant-facing AX SaaS could price per assessment project or per respondent band, sitting between $49/mo self-serve tools and $15k+ consulting — a "tool + consultant report" package.

### Gaps
- Workera, Section, Pointerpro, ScoreApp and Gartner pricing not found on pages accessed (Workera page lists no pricing).
- Cisco and Avanade question counts/times unverified.

## 4. Published survey evidence on executive–employee AI perception gaps

### Takeaway
Every major 2024–2026 workforce survey shows leaders use, trust and feel excited about AI far more than frontline staff, and employees report weak strategy communication and training — strong evidence for a "perception gap" feature.

### Cited Findings
**BCG AI at Work**
- 2025 (published 2025-06-26; 3rd annual; >10,600 leaders, managers, frontline white-collar employees, 11 countries/regions): >75% of leaders and managers use GenAI several times a week vs frontline regular use "stalled at 51%" ("silicon ceiling"); only ~1/3 of employees say they've been properly trained; only ~1/4 of frontline employees say they receive leadership support; >50% will use alternative tools if not provided (shadow AI); 43% of leaders/managers vs 36% frontline worry about losing their job in 10 years. — [BCG 2025](https://www.bcg.com/publications/2025/ai-at-work-momentum-builds-but-gaps-remain)
- 2026 (published 2026-06-03; 4th annual; ~12,000 respondents, >12 markets): 74% of frontline employees are now regular AI users (+23 pts vs 2025); 42% of frontline regular users save ~8 hours/week; only 1/3 of frontline say leadership's AI communications are clear; only 28% of frontline see a strong connection between what leaders say and what the organization does; 36% feel adequately upskilled; 72% say skill expectations have shifted; 48% of leaders report increased mental strain vs 41% overall. — [BCG 2026](https://www.bcg.com/publications/2026/ai-at-work-why-strategy-matters-more-than-tools)

**Section AI Proficiency Report**
- Jan 2026 edition (press release 2026-01-21): 85% of enterprise employees aren't using AI to drive business value; vs C-suite, individual contributors more likely to feel anxious/overwhelmed (68% vs 26%) and less likely to report transformative impact (5% vs 42%); C-suite largely believes deployments are succeeding. — [BusinessWire 2026-01-21](https://www.businesswire.com/news/home/20260121007017/en/85-of-Enterprise-Employees-Arent-Using-AI-to-Drive-Business-Value) (search excerpt; page not scrapeable)
- 80% of C-suite say their company has AI tools with clear access and processes vs only 32% of ICs. — [SmarterX summary](https://smarterx.ai/smarterxblog/ai-proficiency-report-2026) (secondary)
- Current report page (edition/date not shown, likely later 2026): 82% of C-suite excited about AI vs 30% of ICs, managers <50%; 8% of C-suite vs 22% of ICs anxious/overwhelmed; C-suite >2x as likely to have access to agent-capable tools and 5x as likely to have received agentic training; only 33% of managers use AI daily; managers' proficiency barely higher than ICs'. — [Section report page](https://www.sectionai.com/ai/the-ai-proficiency-report)
- CONFLICT: anxiety figures differ between editions (68% vs 26% in Jan 2026 press release; 22% vs 8% on current page). Treat as different survey waves; cite with date.

**Microsoft Work Trend Index 2025 (published 2025-04-23)**
- 67% of leaders familiar with AI agents vs 40% of employees; 79% of leaders vs 67% of employees believe AI will accelerate their careers; 82% of leaders say this is a pivotal year to rethink strategy/operations; 82% expect to use digital labor within 12–18 months; 46% say they use agents to fully automate workstreams. — [Microsoft blog 2025-04-23](https://blogs.microsoft.com/blog/2025/04/23/the-2025-annual-work-trend-index-the-frontier-firm-is-born/); [WorkLab](https://www.microsoft.com/en-us/worklab/work-trend-index/2025-the-year-the-frontier-firm-is-born)

**Slack Workforce Index**
- June 2024 (>10,000 desk workers): 96% of executives feel urgency to incorporate AI, yet >2/3 of desk workers had never used AI at work; ~2 in 5 say company has no AI usage guidelines. — [Slack June 2024](https://slack.com/blog/news/the-workforce-index-june-2024)
- Fall/Nov 2024: 99% of execs plan AI investment, 97% feel urgency; 48% of desk workers would be uncomfortable telling their manager they used AI (feel like cheating / seen as less competent / lazy). — [Slack Fall 2024](https://slack.com/blog/news/the-fall-2024-workforce-index-shows-executives-and-employees-investing-in-ai-but-uncertainty-holding-back-adoption)
- 2025 (survey of 5,000 desk workers, Nov 2024 → Apr 2025): use rose 36% → 60%; daily use: 43% of executives vs 35% senior managers vs 23% middle managers; 29% say company issued no formal guidance, 50% say AI use isn't explicitly encouraged; workers at companies promoting AI ~3x more likely to be power users. — [Slack "New AI Advantage"](https://slack.com/blog/news/the-new-ai-advantage); [Salesforce](https://www.salesforce.com/news/stories/daily-ai-workforce-use-growth/)

**Gallup**
- Q4 (year per article, likely 2025): 69% of leaders use AI at least a few times a year vs 55% of managers vs 40% of individual contributors. — [Gallup](https://www.gallup.com/workplace/701195/frequent-workplace-continued-rise.aspx)
- Frequent AI use among leaders (managers of managers) at 33% (earlier article). — [Gallup "nearly doubled"](https://www.gallup.com/workplace/691643/work-nearly-doubled-two-years.aspx)
- Only 25% of U.S. workers strongly agree their organization has communicated a clear AI plan/strategy. — [Gallup AI Adoption](https://www.gallup.com/workplace/650153/ai-adoption.aspx)
- As of May 2026: 15% of U.S. employees use AI daily; 30% a few times a week or more. — [Gallup Global Indicator](https://www.gallup.com/699797/indicator-artificial-intelligence.aspx)

**EY Work Reimagined Survey 2025** (fielded Aug 2025, published Nov 2025; 15,000 employees + 1,500 employers, 29 countries, orgs 1,000+)
- 88% of employees use AI but mostly for basic tasks; only 5% use it in advanced, transformative ways; only 12% receive sufficient AI training; 37% worry overreliance erodes skills; 64% report increased workloads; shadow AI 23–58% by sector; only 28% of orgs on track to "Talent Advantage"; up to 40% of AI productivity gains lost. — [EY press release](https://www.ey.com/en_gl/newsroom/2025/11/ey-survey-reveals-companies-are-missing-out-on-up-to-40-percent-of-ai-productivity-gains-due-to-gaps-in-talent-strategy); [EY insights](https://www.ey.com/en_us/insights/workforce/work-reimagined-survey)

### Inferences
- Recurring measurable gap dimensions suitable as perception-gap survey constructs: usage frequency, excitement vs anxiety, perceived tool access/processes, perceived training adequacy, strategy-communication clarity, say-do alignment, perceived impact/ROI, psychological safety to disclose AI use.
- These public benchmarks (BCG, Section, Slack, Gallup, EY) can be cited as external reference points in an AX report next to the client's own leader–employee deltas.

### Gaps
- Microsoft Work Trend Index 2024 numbers (e.g., BYOAI, training) were not verified in this pass; WTI 2026 edition not checked.
- Section report sample sizes and exact edition dates for the current page not confirmed.
- BCG AI at Work 2024 edition figures not collected.
- Gallup Q4 article year not confirmed in the excerpt.
