# WAIO Microdata Priority Matrix

**Version:** 1.0  
**Date:** January 2026  
**Purpose:** Strategic guide for determining which Schema.org types should be implemented as microdata (HTML) vs. JSON-LD, based on AI crawler parsing optimization and DOM tree priority.

---

## Executive Summary

This matrix provides a **strategic framework** for implementing Schema.org microdata in WAIO-optimized websites. The key principle is that **microdata in HTML is parsed faster by AI crawlers** than JSON-LD in `<script>` tags (which loads microseconds later). Therefore, **critical schema types** should be implemented as microdata to maximize crawler efficiency.

**Implementation Strategy:**
- **JSON-LD (Webflow AI Assistant):** Page-level schema, comprehensive context
- **Microdata (WAIO HTML):** Critical content sections that need fast parsing
- **Together:** Redundant but complementary - JSON-LD provides complete data, microdata provides fast access

---

## Microdata Priority Matrix

| Priority | Schema Type | Microdata? | JSON-LD? | LLM Crawlers | Use Case | WAIO Mapping | Best Practices |
|----------|-------------|-----------|---------|--------------|----------|--------------|-----------------|
| 🔴 **CRITICAL** | **FAQPage** | ✅ YES | ✅ YES | GPTBot, ClaudeBot, PerplexityBot, Google-Extended | FAQ sections with Q&A pairs | `data-ai-entity-type="Section"` + `data-ai-entity-detail="faq-section"` on container; `data-ai-entity-type="Question"` + `data-ai-entity-type="Answer"` on items | Use `<details>/<summary>` for accessibility; itemscope on container, itemprop on questions/answers |
| 🔴 **CRITICAL** | **Review / AggregateRating** | ✅ YES | ✅ YES | All LLM crawlers (credibility signals) | Customer testimonials, reviews, ratings | `data-ai-entity-type="Testimonial"` + `data-ai-confidence-signal="primary-source"` | Include ratingValue, reviewCount; link to reviewer profile |
| 🔴 **CRITICAL** | **Article / NewsArticle** | ✅ YES | ✅ YES | GPTBot, ClaudeBot, Google-Extended | Blog posts, news articles, long-form content | `data-ai-entity-type="BlogPost"` + `data-ai-intent="Informational"` | Include author (Person), datePublished, dateModified, headline |
| 🟡 **HIGH** | **BreadcrumbList** | ✅ YES | ✅ YES | All crawlers (navigation hierarchy) | Site navigation structure, category paths | `data-ai-entity-type="Section"` + `data-ai-entity-detail="breadcrumb"` on container | Use `itemListElement` for each level; include position and name |
| 🟡 **HIGH** | **Product / Service** | ✅ YES | ✅ YES | E-commerce crawlers, transactional crawlers | Product pages, service offerings | `data-ai-entity-type="Product"` + `data-ai-intent="Transactional"` | Include name, description, price, availability, image |
| 🟡 **HIGH** | **Organization** | ⚠️ OPTIONAL | ✅ YES | All crawlers (context) | Company info, about pages | `data-ai-entity-type="Organization"` | Microdata optional if JSON-LD present; include name, logo, contact |
| 🟢 **MEDIUM** | **Person** | ⚠️ OPTIONAL | ✅ YES | Crawlers looking for author/expert info | Team members, author bios, expert profiles | `data-ai-entity-type="Person"` + `data-ai-entity-detail="team-member"` | Include name, jobTitle, image, url; link to social profiles |
| 🟢 **MEDIUM** | **LocalBusiness** | ⚠️ OPTIONAL | ✅ YES | Google Maps, local search, geo-crawlers | Business location, hours, contact | `data-ai-entity-type="Organization"` + `data-ai-entity-detail="local-business"` | Include address, telephone, openingHours, geo coordinates |
| ⚪ **LOW** | **Event** | ❌ NO | ✅ YES | Event-specific crawlers | Event listings, webinars, conferences | N/A (use JSON-LD only) | Include startDate, endDate, location, description |
| ⚪ **LOW** | **VideoObject** | ❌ NO | ✅ YES | Video crawlers, YouTube integration | Video content, tutorials | N/A (use JSON-LD only) | Include name, description, thumbnailUrl, uploadDate |

---

## Implementation Priority by Website Type

### B2B SaaS / Service Companies
**Priority Order:**
1. Article (blog posts) - Microdata
2. FAQPage - Microdata
3. Product/Service - Microdata
4. Organization - JSON-LD
5. BreadcrumbList - Microdata (optional)

### E-Commerce
**Priority Order:**
1. Product - Microdata
2. AggregateRating/Review - Microdata
3. BreadcrumbList - Microdata
4. Organization - JSON-LD

### News / Publishing
**Priority Order:**
1. Article/NewsArticle - Microdata
2. BreadcrumbList - Microdata
3. Organization - JSON-LD
4. Person (author) - Microdata (optional)

### Local Business
**Priority Order:**
1. LocalBusiness - Microdata
2. AggregateRating/Review - Microdata
3. Organization - JSON-LD
4. BreadcrumbList - Microdata

---

## LLM Crawler Schema Preferences

| Crawler | Primary Schema | Secondary | Notes |
|---------|----------------|-----------|-------|
| **GPTBot** | FAQPage, Article, Product | Review, Organization | Prefers structured Q&A and content hierarchy |
| **ClaudeBot** | Article, FAQPage, Review | Person, Organization | Values author info and credibility signals |
| **PerplexityBot** | Article, FAQPage, Review | BreadcrumbList | Focuses on source attribution and verification |
| **Google-Extended** | All standard schemas | FAQPage (high priority) | Comprehensive schema support; FAQPage for AI Overviews |
| **BingBot** | Product, LocalBusiness, Review | Organization | E-commerce and local business focused |

---

## Schema.org Best Practices Links

- **Official Schema.org Documentation:** https://schema.org/
- **Google Structured Data Guide:** https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- **Schema.org Microdata Specification:** https://schema.org/docs/gs.html
- **JSON-LD Format:** https://json-ld.org/
- **Google Rich Results Test:** https://search.google.com/test/rich-results
- **Schema.org Validator:** https://validator.schema.org/

---

## Implementation Rules

### Rule 1: DOM Tree Priority
Implement as **microdata** if:
- Content is critical for AI understanding
- Content appears early in DOM tree
- Content benefits from microsecond-faster parsing

### Rule 2: Redundancy is OK
Implement as **both microdata + JSON-LD** if:
- Content is critical (FAQPage, Review, Article)
- You want maximum compatibility across crawlers
- Redundancy doesn't significantly impact performance

### Rule 3: JSON-LD Only
Implement as **JSON-LD only** if:
- Content is supplementary (Events, Videos)
- Content is page-level metadata
- Microdata would complicate HTML structure

### Rule 4: Scope Inheritance
Use `itemscope` on containers and `itemprop` on children:
```html
<section itemscope itemtype="https://schema.org/FAQPage">
  <details itemprop="mainEntity" itemscope itemtype="https://schema.org/Question">
    <summary itemprop="name">Question?</summary>
    <div itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer">
      <p itemprop="text">Answer.</p>
    </div>
  </details>
</section>
```

### Rule 5: WAIO + Microdata Alignment
Always pair microdata with WAIO attributes:
```html
<div itemscope itemtype="https://schema.org/Review"
     data-ai-entity-type="Testimonial"
     data-ai-confidence-signal="primary-source"
     data-ai-importance="high">
  <p itemprop="reviewBody" data-ai-entity-type="Testimonial">Review text</p>
</div>
```

---

## Validation Checklist

Before implementing microdata, verify:

- [ ] Schema type is in the Priority Matrix
- [ ] Schema type is marked as "Microdata? YES"
- [ ] WAIO attributes are paired with microdata
- [ ] `itemscope` is on the correct container
- [ ] `itemprop` attributes are on child elements
- [ ] No orphaned `itemprop` attributes (outside itemscope)
- [ ] Schema structure matches official Schema.org definition
- [ ] Content is valid and complete
- [ ] JSON-LD is also present for critical schemas
- [ ] Tested with Schema.org Validator

---

## Quick Reference: WAIO + Microdata Combinations

### FAQ Section
```
data-ai-entity-type="Section" + data-ai-entity-detail="faq-section"
+ itemtype="https://schema.org/FAQPage"
```

### Testimonial/Review
```
data-ai-entity-type="Testimonial" + data-ai-confidence-signal="primary-source"
+ itemtype="https://schema.org/Review"
```

### Blog Article
```
data-ai-entity-type="BlogPost" + data-ai-intent="Informational"
+ itemtype="https://schema.org/Article"
```

### Product
```
data-ai-entity-type="Product" + data-ai-intent="Transactional"
+ itemtype="https://schema.org/Product"
```

### BreadcrumbList
```
data-ai-entity-type="Section" + data-ai-entity-detail="breadcrumb"
+ itemtype="https://schema.org/BreadcrumbList"
```

---

## Notes

- This matrix is based on **DOM tree parsing theory** - microdata is parsed before JSON-LD
- **LLM crawlers vary** in their schema preferences; redundancy ensures maximum compatibility
- **Best practices evolve** - check Schema.org and Google documentation regularly
- **Testing is essential** - use Schema.org Validator and Google Rich Results Test
