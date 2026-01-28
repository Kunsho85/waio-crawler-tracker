# WAIO Page Analysis - Complete Guide

**Version:** 2.0 Complete  
**Purpose:** Comprehensive reference guide for analyzing web pages and providing WAIO implementation recommendations.

---

## Table of Contents

1. [Reference Documents](#reference-documents)
2. [Data Integrity & Accuracy Rules](#data-integrity--accuracy-rules)
3. [Analysis Workflow - Detailed](#analysis-workflow---detailed)
4. [Output Formats & Examples](#output-formats--examples)
5. [Analysis Report Template](#analysis-report-template)
6. [Key Principles](#key-principles)
7. [Resources](#resources)

---

## Reference Documents

Before analyzing, consult these project files:

1. **WAIO_FRAMEWORK_DOCUMENTATION_V2.1.md** - Core framework with 24 templates and 4 core attributes
2. **WAIO_MICRODATA_PRIORITY_MATRIX.md** - Determine which schemas need microdata vs. JSON-LD
3. **WAIO_MICRODATA_MAPPING_GUIDE.md** - HTML code examples and Webflow implementation steps

These documents are available in the project files and should be referenced throughout the analysis.

---

## Data Integrity & Accuracy Rules

**CRITICAL:** These rules prevent hallucinations and ensure analysis accuracy.

### Rule 1: Analyze Only What You Receive
- Use **ONLY** the HTML code provided by the user
- Do **NOT** generate, assume, or hallucinate CSS classes
- Do **NOT** invent HTML structures that aren't in the code
- If something is not in the code, skip it or explicitly ask for clarification
- Every recommendation must be grounded in actual code

### Rule 2: Cite All Recommendations
- Every CSS class mentioned **MUST** be found in the provided HTML
- Every element recommendation **MUST** reference the actual code location
- If you cannot find it in the code, explicitly state: **"This class/structure was not found in the provided HTML"**
- Include line numbers or code snippets when citing

### Rule 3: Transparency About Limitations
- If web scraping is used to extract HTML, acknowledge it may be imprecise
- For complex sites (Webflow, dynamic sites, JavaScript-heavy), recommend HTML code submission for accuracy
- Never guess or fill gaps with invented code
- If analysis is incomplete due to missing code, clearly communicate this to the user

### Rule 4: Validation Before Recommendation
- Cross-reference every class/element with the actual HTML before including in recommendations
- Use search/grep to confirm existence in the provided code
- If a class/element is not found, do **NOT** include it in recommendations
- Document what was found vs. what was not found

### Rule 5: Handling Missing Information
- If HTML is incomplete or missing sections, ask the user to provide the complete code
- Do **NOT** assume structure for missing sections
- Do **NOT** create placeholder recommendations for sections not in the provided HTML
- Be explicit: "Section X was not found in the provided HTML. Please provide the code if you'd like recommendations for it."

### Rule 6: Complete Analysis Coverage
- **ANALYZE EVERY SECTION** on the page - do not skip any sections
- Create recommendations for **ALL sections**, not just the obvious ones
- Include sections that might seem less important (footer, navigation, secondary content)
- For each section found, provide:
  - Current HTML assessment
  - WAIO attribute recommendations (if applicable)
  - Semantic HTML improvements (if applicable)
  - Microdata recommendations (if applicable)
- At the end of the analysis, include a **Coverage Checklist** listing all sections analyzed
- If a section is intentionally skipped (e.g., gallery with no text), explicitly state why: **"Section X: Skipped because [reason]"**
- **Do NOT leave sections unanalyzed** - every section on the page deserves recommendations or explicit explanation for skipping

---

## Analysis Workflow - Detailed

### Step 1: Page Assessment & Content Audit

**Input:** User provides a URL or page content

**Actions:**

1. **Extract Page HTML** - Get the actual HTML structure of the page
2. **Identify Major Sections** - Map sections to WAIO template categories:
   - **Structural Sections (10 types):** Hero, FAQ, Pricing, Features, Testimonials, Team, Stats, Gallery, Blog, Comparison
   - **Content Elements (9 types):** Headline, Feature, Question, Answer, Testimonial, CTA, Stat, Person, Product
   - **Navigation (3 types):** Main Nav, Footer, Socials
   - **Forms & Interactive (2 types):** Contact Form, Signup Form

3. **Document Current HTML** - For each section, capture:
   - Current HTML structure (semantic vs. div-based)
   - CSS classes used
   - Content type (informational, transactional, support, comparative, navigational)

4. **Create Section Inventory** - List all sections with current state

**Output:** Section inventory with HTML code samples

**Example Output:**

```
PAGE STRUCTURE ANALYSIS: forethought.ai

Section 1: HEADER/NAVIGATION
Current HTML:
<header class="ft-header">
  <nav class="ft-header__nav">
    <a href="/">Home</a>
    <a href="/about">About</a>
  </nav>
</header>

Assessment: Uses semantic <header> and <nav>. Good structure.

---

Section 2: HERO SECTION
Current HTML:
<div class="ft-homepage-hero-simple__head">
  <h1 class="eyebrow">AI AGENT PLATFORM</h1>
  <h2 class="h1">Enterprise AI Agents for Every Customer Moment</h2>
  <div class="ft-homepage-hero-simple__form">...</div>
</div>

Assessment: Uses div container. Heading hierarchy needs improvement (h1 for eyebrow, h2 for main).

---

[Continue for each section...]
```

---

### Step 2: WAIO Attribute Analysis

**Input:** Section inventory from Step 1

**Actions:**

1. **Determine Primary WAIO Attributes** - For each section, decide:
   - `data-ai-entity-type` - What is this section? (from WAIO template system)
   - `data-ai-entity-detail` - What is the specific variant?
   - `data-ai-intent` - What is the user intent?
   - `data-ai-confidence-signal` - What credibility signal?
   - `data-ai-importance` - What priority? (critical/high/medium/low)

2. **Apply Critical Cap Rule** - Maximum 2 `critical` importance per section

3. **Identify Must-Have vs. Optional Sections:**
   - **MUST HAVE:** Hero, FAQ, Testimonials, Features, Pricing, Blog/Articles, CTAs
   - **OPTIONAL:** Gallery, Team, Footer, Social Links

**Output:** WAIO attribute recommendations with concrete HTML examples and Webflow locators

---

### Step 3: Semantic HTML Analysis

**Input:** Current HTML structure from Step 1

**Actions:**

1. **Audit Current Semantic Elements:**
   - Check for `<article>`, `<section>`, `<aside>`, `<nav>`, `<header>`, `<footer>`, `<main>`
   - Check for `<h1>-<h6>` hierarchy
   - Check for `<details>/<summary>` in FAQ sections
   - Check for `<ul>/<ol>/<li>` in lists
   - Check for `<figure>/<figcaption>` in images with captions
   - Check for `<time>` in date/time content

2. **Identify Improvement Opportunities:**
   - Replace generic `<div>` with semantic elements
   - Improve heading hierarchy
   - Use `<details>/<summary>` for FAQ
   - Use `<article>` for blog posts
   - Use `<section>` for content sections

3. **Provide Specific Refactoring Recommendations:**
   - Show current HTML
   - Show recommended HTML
   - Explain semantic benefit
   - Include Webflow locator

**Example Output:**

```
📝 SEMANTIC HTML: FAQ SECTION

📍 Webflow Location:
   Page: Home
   → FAQ Container

❌ CURRENT HTML:
<div class="faq-section">
  <h2>Frequently Asked Questions</h2>
  <div class="faq-item">
    <div class="faq-question">What is Forethought?</div>
    <div class="faq-answer">Forethought is an AI-powered...</div>
  </div>
</div>

✅ RECOMMENDED HTML:
<section data-ai-entity-type="Section"
         data-ai-entity-detail="faq-section"
         data-ai-intent="Support"
         data-ai-importance="high">
  <h2>Frequently Asked Questions</h2>
  <details>
    <summary>What is Forethought?</summary>
    <p>Forethought is an AI-powered customer support platform...</p>
  </details>
</section>

💡 Benefit:
- <section> provides semantic meaning
- <details>/<summary> provides native accessibility
- No JavaScript needed for accessibility
```

---

### Step 4: Schema.org JSON-LD Analysis

**Input:** Page content and metadata from Step 1

**Actions:**

1. **Identify Relevant Schema Types:**
   - **Always include:** WebPage, Organization
   - **Conditionally include:**
     - Article/NewsArticle (if blog post)
     - Product (if product/service page)
     - LocalBusiness (if local business)
     - FAQPage (if FAQ section exists)
     - BreadcrumbList (if navigation hierarchy exists)

2. **Recommend JSON-LD Structure** with all relevant properties

3. **Note:** JSON-LD should be placed in `<head>` tag, generated by Webflow AI Assistant

**Output:** JSON-LD recommendations

**Example Output:**

```
✅ REQUIRED - Organization Schema

Location: Page Settings → Schema markup (Webflow AI Assistant)

Recommended JSON-LD:
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Forethought",
  "logo": "https://forethought.ai/logo.png",
  "url": "https://forethought.ai",
  "description": "AI-powered customer support platform",
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "Customer Support",
    "telephone": "+1-XXX-XXX-XXXX",
    "email": "support@forethought.ai"
  },
  "sameAs": [
    "https://linkedin.com/company/forethought",
    "https://twitter.com/forethought"
  ]
}

📝 Properties to Include:
- name: Company name
- logo: Company logo URL
- url: Company website URL
- description: Brief company description
- contactPoint: Support contact information
- sameAs: Links to social profiles
```

---

### Step 5: Microdata Analysis

**Input:** Critical content sections from Step 2

**Actions:**

1. **Identify Sections Needing Microdata** (from WAIO Microdata Priority Matrix):
   - 🔴 CRITICAL: FAQPage, Review/AggregateRating, Article/NewsArticle
   - 🟡 HIGH: BreadcrumbList, Product/Service
   - 🟢 MEDIUM: Organization, Person, LocalBusiness
   - ⚪ LOW: Event, VideoObject (JSON-LD only)

2. **For Each Critical Section, Recommend Microdata:**
   - Show HTML structure with itemscope/itemprop
   - Align with WAIO attributes
   - Provide Webflow implementation steps

3. **Apply Microdata Priority Rule:**
   - Only add microdata to critical sections
   - Use JSON-LD for supplementary information
   - Combine both for maximum crawler efficiency

**Output:** Microdata recommendations with HTML examples

**Example Output:**

```
🔴 CRITICAL - FAQPage (Add Microdata)

📍 Webflow Location:
   Page: Home
   → FAQ Container

Rationale: FAQ is parsed early in DOM tree; microdata enables faster parsing by AI crawlers

❌ CURRENT HTML:
<div class="faq-section">
  <div class="faq-item">
    <div class="faq-question">What is Forethought?</div>
    <div class="faq-answer">Forethought is...</div>
  </div>
</div>

✅ RECOMMENDED HTML WITH MICRODATA:
<section data-ai-entity-type="Section"
         data-ai-entity-detail="faq-section"
         itemscope 
         itemtype="https://schema.org/FAQPage">
  
  <details itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
    <summary data-ai-entity-type="Question"
             itemprop="name">
      What is Forethought?
    </summary>
    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
      <p itemprop="text">Forethought is an AI-powered customer support platform...</p>
    </div>
  </details>
</section>

🔧 Webflow Implementation:
1. Select FAQ Container element
2. Add custom attributes:
   - data-ai-entity-type="Section"
   - data-ai-entity-detail="faq-section"
   - itemscope
   - itemtype="https://schema.org/FAQPage"
3. For each FAQ item <details> element, add:
   - itemscope
   - itemprop="mainEntity"
   - itemtype="https://schema.org/Question"
4. For <summary> element, add:
   - data-ai-entity-type="Question"
   - itemprop="name"
5. For answer <div>, add:
   - itemscope
   - itemprop="acceptedAnswer"
   - itemtype="https://schema.org/Answer"
6. For answer text <p>, add:
   - itemprop="text"

📚 Reference: See WAIO_MICRODATA_MAPPING_GUIDE.md for detailed FAQ pattern example
```

---

### Step 6: Priority Ranking & Implementation Roadmap

**Input:** All recommendations from Steps 2-5

**Actions:**

1. **Rank Recommendations by Impact:**
   - **Phase 1 (Immediate):** Critical WAIO attributes + semantic HTML + JSON-LD
   - **Phase 2 (Short-term):** Microdata for critical sections + additional WAIO attributes
   - **Phase 3 (Long-term):** Optional WAIO attributes + microdata for secondary sections

2. **Provide Implementation Roadmap** with effort estimates

**Output:** Prioritized implementation roadmap

**Example Output:**

```
🚀 PHASE 1 - CRITICAL SECTIONS (Week 1)

Priority: CRITICAL - Highest AI crawler impact
Effort: 2-4 hours
Expected Impact: +40% improvement in crawler efficiency

✅ Tasks:

1. Hero Section - Add WAIO Attributes
   - Webflow Location: Page: Home → Hero Container
   - Attributes to Add:
     * data-ai-entity-type="Section"
     * data-ai-entity-detail="hero-section"
     * data-ai-intent="Transactional"
     * data-ai-importance="critical"

2. FAQ Section - Add Semantic HTML + Microdata
   - Webflow Location: Page: Home → FAQ Container
   - Changes: Replace <div> with <section>, use <details>/<summary>
   - Attributes to Add: [See Step 5 example]

3. Generate JSON-LD
   - Location: Page Settings → Schema markup
   - Schemas: WebPage, Organization

Expected Outcome: Hero section is now machine-readable; FAQ is accessible and microdata-enhanced
```

---

### Step 7: Validation & Testing Recommendations

**Input:** All implementation recommendations

**Actions:**

1. **Provide Validation Checklist**
2. **Recommend Testing Tools**
3. **Provide Testing Steps**

**Output:** Validation checklist and testing instructions

**Example Output:**

```
✅ VALIDATION CHECKLIST

Before publishing, verify:

✅ WAIO Attributes:
- [ ] All major sections have data-ai-entity-type
- [ ] Critical sections have data-ai-importance="critical"
- [ ] Maximum 2 critical per section
- [ ] data-ai-confidence-signal is only on credible content
- [ ] data-ai-reviewer-url is present for expert-reviewed content

✅ Semantic HTML:
- [ ] Page has one <h1>
- [ ] Heading hierarchy is correct
- [ ] FAQ uses <details>/<summary>
- [ ] Articles use <article>
- [ ] Sections use <section>

✅ Microdata:
- [ ] All itemscope elements have itemtype
- [ ] All itemprop attributes are inside itemscope
- [ ] No orphaned itemprop attributes
- [ ] Scope boundaries are correct

✅ JSON-LD:
- [ ] WebPage schema is present
- [ ] Organization schema is present
- [ ] All schemas are valid

---

🔍 TESTING INSTRUCTIONS

1. Google Rich Results Test:
   - Go to https://search.google.com/test/rich-results
   - Enter your page URL
   - Verify all expected schema types are recognized

2. Schema.org Validator:
   - Go to https://validator.schema.org/
   - Enter your page URL
   - Verify all schemas are valid

3. Webflow Inspect:
   - Right-click on element → Inspect
   - Verify custom attributes are present
   - Verify microdata is correctly structured
```

---

## Output Formats & Examples

### Format for WAIO Attribute Recommendations:

```
🔴 PRIORITY - SECTION NAME

📍 Webflow Location:
   Page: [Page Name]
   → [Container Name]
     → [Child Element]
       → [Target Element]

❌ CURRENT HTML:
[Show the actual current HTML code from the page]

✅ RECOMMENDED HTML:
[Show the recommended HTML with data-ai attributes added]

📝 Rationale:
[Explain why these attributes are recommended]

🔧 Implementation Steps:
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

### Format for Semantic HTML Recommendations:

```
📝 SEMANTIC HTML: [Section Name]

📍 Webflow Location:
   Page: [Page Name]
   → [Container Name]

❌ CURRENT HTML:
[Current code]

✅ RECOMMENDED HTML:
[Recommended code]

💡 Semantic Benefit:
[Explain why this is better]
```

### Format for Microdata Recommendations:

```
🔴 CRITICAL - [Schema Type] (Add Microdata)

📍 Webflow Location:
   Page: [Page Name]
   → [Container Name]

Rationale: [Why microdata is needed]

❌ CURRENT HTML:
[Current code]

✅ RECOMMENDED HTML WITH MICRODATA:
[Code with itemscope/itemprop]

🔧 Webflow Implementation:
1. [Step 1]
2. [Step 2]
3. [Step 3]

📚 Reference: See WAIO_MICRODATA_MAPPING_GUIDE.md for detailed examples
```

---

## Analysis Report Template

```
# WAIO Page Analysis Report

**Page URL:** [URL]
**Analysis Date:** [Date]
**Analyst:** [Name]

---

## 1. Page Structure Assessment

[Section inventory with current HTML code]

---

## 2. WAIO Attribute Recommendations

[Attribute recommendations with Webflow locators and HTML examples]

---

## 3. Semantic HTML Recommendations

[Before/after HTML examples with semantic benefits]

---

## 4. Schema.org JSON-LD Recommendations

[JSON-LD schemas with all relevant properties]

---

## 5. Microdata Recommendations

[Microdata examples for critical sections with implementation steps]

---

## 6. Implementation Roadmap

[Prioritized phases with effort estimates and expected outcomes]

---

## 7. Validation Checklist

[Checklist and testing instructions]

---

## Coverage Checklist

✅ [Section 1] - ANALYZED
✅ [Section 2] - ANALYZED
⏭️ [Section 3] - SKIPPED because [reason]

Total: [X] sections analyzed

---

## Summary

**Total Effort:** [X hours]
**Expected Impact:** [Brief summary of improvements]
**Priority:** [Immediate/Short-term/Long-term]
**Next Steps:** [What to do after Phase 1]
```

---

## Key Principles

1. **Show Actual HTML** - Use real code from the page, not generic examples
2. **Webflow Locators** - Always include where to find elements in Webflow Designer
3. **Concrete Steps** - Provide step-by-step implementation instructions
4. **Focus on Critical First** - Hero, FAQ, Testimonials, CTAs
5. **Avoid Signal Inflation** - Max 2 critical per section
6. **Pair WAIO with Microdata** - They work together for maximum efficiency
7. **Test Everything** - Always validate before publishing
8. **Complete Coverage** - Analyze every section, skip none without explanation
9. **Reference Documents** - Link to WAIO_MICRODATA_MAPPING_GUIDE.md and WAIO_MICRODATA_PRIORITY_MATRIX.md
10. **Ground in Evidence** - Every recommendation must be from actual HTML code

---

## Resources

- **WAIO Framework Documentation:** WAIO_FRAMEWORK_DOCUMENTATION_V2.1.md
- **Microdata Priority Matrix:** WAIO_MICRODATA_PRIORITY_MATRIX.md
- **Microdata Mapping Guide:** WAIO_MICRODATA_MAPPING_GUIDE.md
- **Schema.org:** https://schema.org/
- **Google Structured Data:** https://developers.google.com/search/docs/appearance/structured-data
- **Webflow Custom Attributes:** https://university.webflow.com/lesson/custom-attributes
- **Google Rich Results Test:** https://search.google.com/test/rich-results
- **Schema.org Validator:** https://validator.schema.org/
- **Best Practices for Schema.org:** https://schema.org/docs/documents.html
