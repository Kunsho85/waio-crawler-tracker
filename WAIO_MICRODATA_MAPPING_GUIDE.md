# WAIO + Microdata Mapping Guide

**Version:** 1.0  
**Date:** January 2026  
**Purpose:** Complete implementation guide for combining WAIO data-ai attributes with Schema.org microdata, including HTML code examples and Webflow-specific instructions.

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [FAQPage Pattern](#faqpage-pattern)
3. [Review / Testimonial Pattern](#review--testimonial-pattern)
4. [Article / BlogPost Pattern](#article--blogpost-pattern)
5. [Product Pattern](#product-pattern)
6. [BreadcrumbList Pattern](#breadcrumblist-pattern)
7. [Webflow Implementation Guide](#webflow-implementation-guide)
8. [Advanced Scenarios](#advanced-scenarios)

---

## Core Principles

### Principle 1: Attribute Layering
WAIO attributes and microdata work in **three layers**:

```
Layer 1: HTML Semantic Elements (native)
  ↓
Layer 2: WAIO data-ai Attributes (AI optimization)
  ↓
Layer 3: Microdata itemscope/itemprop (Schema.org)
```

**Example:**
```html
<article 
  data-ai-entity-type="BlogPost"
  data-ai-intent="Informational"
  data-ai-importance="high"
  itemscope 
  itemtype="https://schema.org/Article">
  <!-- Content -->
</article>
```

### Principle 2: Scope Inheritance
- `itemscope` defines the boundary of a schema object
- `itemprop` defines properties within that scope
- Never use `itemprop` outside `itemscope` (crawlers ignore orphaned attributes)
- WAIO attributes work independently of microdata scope

**Correct:**
```html
<div itemscope itemtype="https://schema.org/Review">
  <p itemprop="reviewBody">Review text</p>
</div>
```

**Incorrect:**
```html
<div>
  <p itemprop="reviewBody">Review text</p> <!-- Orphaned! -->
</div>
```

### Principle 3: WAIO + Microdata Alignment
WAIO attributes should **reinforce** microdata meaning:

| WAIO Attribute | Microdata | Purpose |
|---|---|---|
| `data-ai-entity-type` | `itemtype` | Both declare content type |
| `data-ai-entity-detail` | `itemprop` specifics | Both provide specificity |
| `data-ai-confidence-signal` | `reviewRating`, `author` | Both signal credibility |
| `data-ai-importance` | Schema hierarchy | Both signal priority |

---

## FAQPage Pattern

### Use Case
FAQ sections with question-answer pairs. This is the **most critical pattern** for AI optimization.

### HTML Structure

```html
<!-- FAQ Section Container -->
<section 
  data-ai-entity-type="Section"
  data-ai-entity-detail="faq-section"
  data-ai-intent="Support"
  data-ai-confidence-signal="expert-reviewed"
  data-ai-reviewer-url="https://linkedin.com/in/expert-name"
  data-ai-importance="high"
  itemscope 
  itemtype="https://schema.org/FAQPage">
  
  <!-- Section Headline -->
  <h2 data-ai-entity-type="Headline" 
      data-ai-importance="high">
    Frequently Asked Questions
  </h2>
  
  <!-- FAQ Item 1 -->
  <details class="faq-item"
           itemscope 
           itemprop="mainEntity" 
           itemtype="https://schema.org/Question">
    
    <!-- Question (Summary) -->
    <summary 
      data-ai-entity-type="Question"
      data-ai-entity-detail="faq-question"
      data-ai-intent="inherit"
      data-ai-importance="high"
      itemprop="name">
      What is WAIO and how does it work?
    </summary>
    
    <!-- Answer (Details) -->
    <div 
      data-ai-entity-type="Answer"
      data-ai-entity-detail="faq-answer"
      data-ai-intent="inherit"
      data-ai-confidence-signal="expert-reviewed"
      data-ai-importance="high"
      itemscope 
      itemprop="acceptedAnswer" 
      itemtype="https://schema.org/Answer">
      
      <p itemprop="text">
        WAIO (Web AI Optimization) is a framework of HTML data attributes 
        that provides explicit semantic signals to AI crawlers and LLMs. 
        It helps reduce ambiguity in how AI systems interpret web content 
        by declaring content type, purpose, credibility, and importance.
      </p>
    </div>
  </details>
  
  <!-- FAQ Item 2 -->
  <details class="faq-item"
           itemscope 
           itemprop="mainEntity" 
           itemtype="https://schema.org/Question">
    
    <summary 
      data-ai-entity-type="Question"
      data-ai-entity-detail="faq-question"
      data-ai-intent="inherit"
      data-ai-importance="high"
      itemprop="name">
      How do I implement WAIO in Webflow?
    </summary>
    
    <div 
      data-ai-entity-type="Answer"
      data-ai-entity-detail="faq-answer"
      data-ai-intent="inherit"
      data-ai-importance="high"
      itemscope 
      itemprop="acceptedAnswer" 
      itemtype="https://schema.org/Answer">
      
      <p itemprop="text">
        In Webflow, add data-ai-* attributes to your HTML elements using 
        the custom attributes panel. Start with the four core attributes: 
        entity-type, intent, confidence-signal, and importance. Use 
        entity-detail for additional specificity.
      </p>
    </div>
  </details>
  
</section>
```

### Webflow Implementation Steps

1. **Create the Section Element**
   - Add a `<section>` element in your Webflow page
   - Go to Settings → Custom Attributes
   - Add: `data-ai-entity-type="Section"`
   - Add: `data-ai-entity-detail="faq-section"`
   - Add: `data-ai-intent="Support"`
   - Add: `data-ai-confidence-signal="expert-reviewed"`
   - Add: `data-ai-reviewer-url="https://linkedin.com/in/your-expert"`
   - Add: `data-ai-importance="high"`

2. **Add Microdata to Section**
   - In the same Custom Attributes panel, add:
   - `itemscope` (no value needed)
   - `itemtype="https://schema.org/FAQPage"`

3. **Create FAQ Items**
   - For each FAQ item, create a `<details>` component
   - Add custom attributes to `<details>`:
     - `itemscope`
     - `itemprop="mainEntity"`
     - `itemtype="https://schema.org/Question"`

4. **Add Question (Summary)**
   - Inside `<details>`, add a `<summary>` element
   - Add custom attributes:
     - `data-ai-entity-type="Question"`
     - `data-ai-entity-detail="faq-question"`
     - `data-ai-intent="inherit"`
     - `data-ai-importance="high"`
     - `itemprop="name"`

5. **Add Answer (Details)**
   - After `<summary>`, add a `<div>` for the answer
   - Add custom attributes:
     - `data-ai-entity-type="Answer"`
     - `data-ai-entity-detail="faq-answer"`
     - `data-ai-intent="inherit"`
     - `data-ai-importance="high"`
     - `itemscope`
     - `itemprop="acceptedAnswer"`
     - `itemtype="https://schema.org/Answer"`

6. **Add Answer Text**
   - Inside the answer `<div>`, add a `<p>` element
   - Add custom attribute: `itemprop="text"`

---

## Review / Testimonial Pattern

### Use Case
Customer testimonials, reviews, ratings. Critical for credibility signals.

### HTML Structure

```html
<!-- Testimonials Section Container -->
<section 
  data-ai-entity-type="Section"
  data-ai-entity-detail="testimonials-section"
  data-ai-intent="Informational"
  data-ai-confidence-signal="primary-source"
  data-ai-importance="high">
  
  <h2 data-ai-entity-type="Headline" 
      data-ai-importance="high">
    What Our Customers Say
  </h2>
  
  <!-- Individual Testimonial/Review -->
  <div 
    data-ai-entity-type="Testimonial"
    data-ai-entity-detail="customer-review"
    data-ai-intent="inherit"
    data-ai-confidence-signal="primary-source"
    data-ai-importance="high"
    itemscope 
    itemtype="https://schema.org/Review">
    
    <!-- Review Rating -->
    <div data-ai-entity-type="Stat"
         data-ai-importance="high"
         itemscope 
         itemprop="reviewRating" 
         itemtype="https://schema.org/Rating">
      <span itemprop="ratingValue">5</span>
      <span itemprop="bestRating">5</span>
    </div>
    
    <!-- Review Body -->
    <p itemprop="reviewBody" 
       data-ai-entity-type="Testimonial"
       data-ai-importance="high">
      WAIO transformed how we approach AI optimization. Our content now ranks 
      higher in AI-generated answers, and we've seen a 40% increase in traffic 
      from AI-powered search platforms.
    </p>
    
    <!-- Reviewer (Author) -->
    <div 
      data-ai-entity-type="Person"
      data-ai-entity-detail="reviewer"
      data-ai-importance="medium"
      itemscope 
      itemprop="author" 
      itemtype="https://schema.org/Person">
      
      <p itemprop="name">Sarah Johnson</p>
      <p itemprop="jobTitle">Marketing Director at TechCorp</p>
    </div>
  </div>
  
  <!-- Additional Testimonials follow same pattern -->
  
</section>
```

### Webflow Implementation Steps

1. **Create Testimonials Section**
   - Add a `<section>` element
   - Custom attributes:
     - `data-ai-entity-type="Section"`
     - `data-ai-entity-detail="testimonials-section"`
     - `data-ai-intent="Informational"`
     - `data-ai-confidence-signal="primary-source"`
     - `data-ai-importance="high"`

2. **Create Individual Testimonial Container**
   - Add a `<div>` for each testimonial
   - Custom attributes:
     - `data-ai-entity-type="Testimonial"`
     - `data-ai-entity-detail="customer-review"`
     - `data-ai-intent="inherit"`
     - `data-ai-confidence-signal="primary-source"`
     - `data-ai-importance="high"`
     - `itemscope`
     - `itemtype="https://schema.org/Review"`

3. **Add Rating (if available)**
   - Add a `<div>` for the rating
   - Custom attributes:
     - `itemscope`
     - `itemprop="reviewRating"`
     - `itemtype="https://schema.org/Rating"`
   - Add `<span>` for rating value with `itemprop="ratingValue"`
   - Add `<span>` for best rating with `itemprop="bestRating"`

4. **Add Review Text**
   - Add a `<p>` element for the testimonial text
   - Custom attributes:
     - `itemprop="reviewBody"`
     - `data-ai-entity-type="Testimonial"`
     - `data-ai-importance="high"`

5. **Add Reviewer Information**
   - Add a `<div>` for reviewer details
   - Custom attributes:
     - `data-ai-entity-type="Person"`
     - `data-ai-entity-detail="reviewer"`
     - `data-ai-importance="medium"`
     - `itemscope`
     - `itemprop="author"`
     - `itemtype="https://schema.org/Person"`
   - Add `<p>` for name with `itemprop="name"`
   - Add `<p>` for job title with `itemprop="jobTitle"`

---

## Article / BlogPost Pattern

### Use Case
Blog posts, news articles, long-form content. Critical for content discovery.

### HTML Structure

```html
<!-- Article Container -->
<article 
  data-ai-entity-type="BlogPost"
  data-ai-entity-detail="how-to-guide"
  data-ai-intent="Informational"
  data-ai-confidence-signal="expert-reviewed"
  data-ai-reviewer-url="https://linkedin.com/in/author-name"
  data-ai-importance="high"
  itemscope 
  itemtype="https://schema.org/Article">
  
  <!-- Article Headline -->
  <h1 itemprop="headline"
      data-ai-entity-type="Headline"
      data-ai-importance="critical">
    Complete Guide to WAIO Implementation
  </h1>
  
  <!-- Article Metadata -->
  <div class="article-metadata">
    <!-- Author -->
    <div 
      data-ai-entity-type="Person"
      data-ai-entity-detail="author"
      data-ai-importance="medium"
      itemscope 
      itemprop="author" 
      itemtype="https://schema.org/Person">
      
      <p itemprop="name">John Smith</p>
      <p itemprop="jobTitle">SEO Specialist</p>
    </div>
    
    <!-- Publication Date -->
    <time itemprop="datePublished" 
          datetime="2026-01-13"
          data-ai-importance="high">
      January 13, 2026
    </time>
    
    <!-- Modified Date -->
    <time itemprop="dateModified" 
          datetime="2026-01-13"
          data-ai-importance="medium">
      Updated: January 13, 2026
    </time>
  </div>
  
  <!-- Article Image -->
  <img itemprop="image" 
       src="article-image.jpg" 
       alt="WAIO Implementation Guide"
       data-ai-importance="high">
  
  <!-- Article Description -->
  <p itemprop="description"
     data-ai-entity-type="Section"
     data-ai-importance="high">
    Learn how to implement WAIO attributes to optimize your website for AI crawlers 
    and improve content selection in AI-generated answers.
  </p>
  
  <!-- Article Body -->
  <div itemprop="articleBody"
       data-ai-entity-type="Section"
       data-ai-importance="high">
    
    <!-- Section 1 -->
    <section data-ai-entity-type="Section"
             data-ai-entity-detail="article-section"
             data-ai-importance="high">
      <h2 data-ai-entity-type="Headline"
          data-ai-importance="high">
        What is WAIO?
      </h2>
      <p>Article content here...</p>
    </section>
    
    <!-- Section 2 -->
    <section data-ai-entity-type="Section"
             data-ai-entity-detail="article-section"
             data-ai-importance="high">
      <h2 data-ai-entity-type="Headline"
          data-ai-importance="high">
        Why WAIO Matters
      </h2>
      <p>Article content here...</p>
    </section>
    
  </div>
  
  <!-- Publisher Information -->
  <div 
    data-ai-entity-type="Organization"
    data-ai-importance="medium"
    itemscope 
    itemprop="publisher" 
    itemtype="https://schema.org/Organization">
    
    <p itemprop="name">Your Company Name</p>
    <img itemprop="logo" 
         src="logo.png" 
         alt="Company Logo">
  </div>
  
</article>
```

### Webflow Implementation Steps

1. **Create Article Container**
   - Add an `<article>` element
   - Custom attributes:
     - `data-ai-entity-type="BlogPost"`
     - `data-ai-entity-detail="how-to-guide"`
     - `data-ai-intent="Informational"`
     - `data-ai-confidence-signal="expert-reviewed"`
     - `data-ai-reviewer-url="https://linkedin.com/in/your-name"`
     - `data-ai-importance="high"`
     - `itemscope`
     - `itemtype="https://schema.org/Article"`

2. **Add Article Headline**
   - Add an `<h1>` element
   - Custom attributes:
     - `itemprop="headline"`
     - `data-ai-entity-type="Headline"`
     - `data-ai-importance="critical"`

3. **Add Author Information**
   - Add a `<div>` for author
   - Custom attributes:
     - `data-ai-entity-type="Person"`
     - `data-ai-entity-detail="author"`
     - `data-ai-importance="medium"`
     - `itemscope`
     - `itemprop="author"`
     - `itemtype="https://schema.org/Person"`
   - Add `<p>` for name with `itemprop="name"`
   - Add `<p>` for job title with `itemprop="jobTitle"`

4. **Add Publication Dates**
   - Add `<time>` element for published date
   - Custom attributes: `itemprop="datePublished"` and `datetime="YYYY-MM-DD"`
   - Add `<time>` element for modified date
   - Custom attributes: `itemprop="dateModified"` and `datetime="YYYY-MM-DD"`

5. **Add Featured Image**
   - Add an `<img>` element
   - Custom attributes:
     - `itemprop="image"`
     - `data-ai-importance="high"`

6. **Add Article Description**
   - Add a `<p>` element for the article summary
   - Custom attributes:
     - `itemprop="description"`
     - `data-ai-entity-type="Section"`
     - `data-ai-importance="high"`

7. **Add Article Body**
   - Add a `<div>` for the main content
   - Custom attributes:
     - `itemprop="articleBody"`
     - `data-ai-entity-type="Section"`
     - `data-ai-importance="high"`

8. **Add Publisher Information**
   - Add a `<div>` for publisher
   - Custom attributes:
     - `data-ai-entity-type="Organization"`
     - `data-ai-importance="medium"`
     - `itemscope`
     - `itemprop="publisher"`
     - `itemtype="https://schema.org/Organization"`

---

## Product Pattern

### Use Case
Product pages, service offerings, e-commerce items.

### HTML Structure

```html
<!-- Product Container -->
<div 
  data-ai-entity-type="Product"
  data-ai-entity-detail="software-subscription"
  data-ai-intent="Transactional"
  data-ai-confidence-signal="verified-fact"
  data-ai-importance="critical"
  itemscope 
  itemtype="https://schema.org/Product">
  
  <!-- Product Name -->
  <h1 itemprop="name"
      data-ai-entity-type="Headline"
      data-ai-importance="critical">
    WAIO Pro - AI Optimization Suite
  </h1>
  
  <!-- Product Image -->
  <img itemprop="image" 
       src="product-image.jpg" 
       alt="WAIO Pro"
       data-ai-importance="high">
  
  <!-- Product Description -->
  <p itemprop="description"
     data-ai-entity-type="Section"
     data-ai-importance="high">
    Complete AI optimization framework for modern websites. Includes WAIO Lite, 
    WAIO CSS, and data-ai attribute system.
  </p>
  
  <!-- Product Price -->
  <div 
    data-ai-entity-type="Stat"
    data-ai-importance="critical"
    itemscope 
    itemprop="offers" 
    itemtype="https://schema.org/Offer">
    
    <span itemprop="priceCurrency">USD</span>
    <span itemprop="price">299</span>
    <span itemprop="availability">https://schema.org/InStock</span>
  </div>
  
  <!-- Product Rating -->
  <div 
    data-ai-entity-type="Stat"
    data-ai-importance="high"
    itemscope 
    itemprop="aggregateRating" 
    itemtype="https://schema.org/AggregateRating">
    
    <span itemprop="ratingValue">4.8</span>
    <span itemprop="bestRating">5</span>
    <span itemprop="reviewCount">127</span>
  </div>
  
  <!-- CTA Button -->
  <button 
    data-ai-entity-type="CTA"
    data-ai-intent="Transactional"
    data-ai-importance="critical">
    Purchase Now
  </button>
  
</div>
```

### Webflow Implementation Steps

1. **Create Product Container**
   - Add a `<div>` element
   - Custom attributes:
     - `data-ai-entity-type="Product"`
     - `data-ai-entity-detail="software-subscription"`
     - `data-ai-intent="Transactional"`
     - `data-ai-confidence-signal="verified-fact"`
     - `data-ai-importance="critical"`
     - `itemscope`
     - `itemtype="https://schema.org/Product"`

2. **Add Product Name**
   - Add an `<h1>` element
   - Custom attributes:
     - `itemprop="name"`
     - `data-ai-entity-type="Headline"`
     - `data-ai-importance="critical"`

3. **Add Product Image**
   - Add an `<img>` element
   - Custom attributes:
     - `itemprop="image"`
     - `data-ai-importance="high"`

4. **Add Product Description**
   - Add a `<p>` element
   - Custom attributes:
     - `itemprop="description"`
     - `data-ai-entity-type="Section"`
     - `data-ai-importance="high"`

5. **Add Price Information**
   - Add a `<div>` for pricing
   - Custom attributes:
     - `data-ai-entity-type="Stat"`
     - `data-ai-importance="critical"`
     - `itemscope`
     - `itemprop="offers"`
     - `itemtype="https://schema.org/Offer"`
   - Add `<span>` for currency with `itemprop="priceCurrency"`
   - Add `<span>` for price with `itemprop="price"`
   - Add `<span>` for availability with `itemprop="availability"`

6. **Add Rating Information**
   - Add a `<div>` for rating
   - Custom attributes:
     - `data-ai-entity-type="Stat"`
     - `data-ai-importance="high"`
     - `itemscope`
     - `itemprop="aggregateRating"`
     - `itemtype="https://schema.org/AggregateRating"`
   - Add `<span>` for rating value with `itemprop="ratingValue"`
   - Add `<span>` for best rating with `itemprop="bestRating"`
   - Add `<span>` for review count with `itemprop="reviewCount"`

---

## BreadcrumbList Pattern

### Use Case
Navigation hierarchy, category paths, site structure.

### HTML Structure

```html
<!-- Breadcrumb Navigation -->
<nav 
  data-ai-entity-type="Section"
  data-ai-entity-detail="breadcrumb"
  data-ai-intent="Navigational"
  data-ai-importance="medium"
  itemscope 
  itemtype="https://schema.org/BreadcrumbList">
  
  <!-- Breadcrumb Item 1 -->
  <a href="/"
     data-ai-entity-type="CTA"
     data-ai-intent="Navigational"
     data-ai-importance="medium"
     itemscope 
     itemprop="itemListElement" 
     itemtype="https://schema.org/ListItem">
    
    <span itemprop="name">Home</span>
    <meta itemprop="position" content="1">
    <meta itemprop="item" content="https://example.com/">
  </a>
  
  <!-- Breadcrumb Item 2 -->
  <a href="/blog"
     data-ai-entity-type="CTA"
     data-ai-intent="Navigational"
     data-ai-importance="medium"
     itemscope 
     itemprop="itemListElement" 
     itemtype="https://schema.org/ListItem">
    
    <span itemprop="name">Blog</span>
    <meta itemprop="position" content="2">
    <meta itemprop="item" content="https://example.com/blog">
  </a>
  
  <!-- Breadcrumb Item 3 (Current) -->
  <span 
    data-ai-entity-type="CTA"
    data-ai-intent="Navigational"
    data-ai-importance="medium"
    itemscope 
    itemprop="itemListElement" 
    itemtype="https://schema.org/ListItem">
    
    <span itemprop="name">WAIO Guide</span>
    <meta itemprop="position" content="3">
    <meta itemprop="item" content="https://example.com/blog/waio-guide">
  </span>
  
</nav>
```

### Webflow Implementation Steps

1. **Create Breadcrumb Navigation**
   - Add a `<nav>` element
   - Custom attributes:
     - `data-ai-entity-type="Section"`
     - `data-ai-entity-detail="breadcrumb"`
     - `data-ai-intent="Navigational"`
     - `data-ai-importance="medium"`
     - `itemscope`
     - `itemtype="https://schema.org/BreadcrumbList"`

2. **Add Breadcrumb Items**
   - For each breadcrumb item, add an `<a>` or `<span>` element
   - Custom attributes:
     - `data-ai-entity-type="CTA"`
     - `data-ai-intent="Navigational"`
     - `data-ai-importance="medium"`
     - `itemscope`
     - `itemprop="itemListElement"`
     - `itemtype="https://schema.org/ListItem"`

3. **Add Item Name**
   - Add a `<span>` for the item name
   - Custom attribute: `itemprop="name"`

4. **Add Position and URL**
   - Add `<meta>` tag with `itemprop="position"` and `content="1"` (increment for each item)
   - Add `<meta>` tag with `itemprop="item"` and `content="URL"`

---

## Webflow Implementation Guide

### How to Add Custom Attributes in Webflow

1. **Select the Element**
   - Click on the element in the Webflow canvas

2. **Open Settings Panel**
   - In the right panel, scroll down to find "Custom Attributes"
   - If not visible, click the "+" button to add a section

3. **Add Attributes**
   - Click "Add Attribute"
   - Enter attribute name (e.g., `data-ai-entity-type`)
   - Enter attribute value (e.g., `Testimonial`)
   - Click "Save"

4. **Add Multiple Attributes**
   - Repeat step 3 for each attribute
   - Webflow will combine them in the HTML output

### Webflow Custom Attributes Best Practices

- **Use lowercase with hyphens** for attribute names (e.g., `data-ai-entity-type`)
- **Use quotes for values** if they contain spaces or special characters
- **Test in preview** to ensure attributes are rendering correctly
- **Use Webflow's code inspector** to verify the final HTML output
- **Create reusable components** with pre-configured attributes

### Testing Microdata in Webflow

1. **Publish the page**
2. **Use Google Rich Results Test**
   - Go to https://search.google.com/test/rich-results
   - Enter your page URL
   - Check for schema validation errors

3. **Use Schema.org Validator**
   - Go to https://validator.schema.org/
   - Enter your page URL or paste HTML
   - Verify all schema types are recognized

---

## Advanced Scenarios

### Scenario 1: Nested Testimonials with Multiple Authors

```html
<div itemscope itemtype="https://schema.org/Review"
     data-ai-entity-type="Testimonial"
     data-ai-confidence-signal="primary-source">
  
  <p itemprop="reviewBody">Great product!</p>
  
  <!-- Multiple Authors (Co-reviewers) -->
  <div itemscope itemprop="author" itemtype="https://schema.org/Person"
       data-ai-entity-type="Person">
    <p itemprop="name">Author 1</p>
  </div>
  
  <div itemscope itemprop="author" itemtype="https://schema.org/Person"
       data-ai-entity-type="Person">
    <p itemprop="name">Author 2</p>
  </div>
  
</div>
```

### Scenario 2: Article with Multiple Sections

```html
<article itemscope itemtype="https://schema.org/Article"
         data-ai-entity-type="BlogPost">
  
  <h1 itemprop="headline">Article Title</h1>
  
  <div itemprop="articleBody"
       data-ai-entity-type="Section">
    
    <!-- Section 1 -->
    <section data-ai-entity-type="Section"
             data-ai-entity-detail="article-section">
      <h2 data-ai-entity-type="Headline">Section 1</h2>
      <p>Content...</p>
    </section>
    
    <!-- Section 2 with FAQ -->
    <section data-ai-entity-type="Section"
             data-ai-entity-detail="article-section">
      <h2 data-ai-entity-type="Headline">FAQ within Article</h2>
      
      <details itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"
               data-ai-entity-type="Question">
        <summary itemprop="name">Question?</summary>
        <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"
             data-ai-entity-type="Answer">
          <p itemprop="text">Answer.</p>
        </div>
      </details>
    </section>
    
  </div>
  
</article>
```

### Scenario 3: Product with Reviews

```html
<div itemscope itemtype="https://schema.org/Product"
     data-ai-entity-type="Product"
     data-ai-importance="critical">
  
  <h1 itemprop="name">Product Name</h1>
  
  <!-- Aggregate Rating -->
  <div itemscope itemprop="aggregateRating" itemtype="https://schema.org/AggregateRating"
       data-ai-entity-type="Stat">
    <span itemprop="ratingValue">4.8</span>
    <span itemprop="reviewCount">127</span>
  </div>
  
  <!-- Individual Reviews -->
  <div itemscope itemprop="review" itemtype="https://schema.org/Review"
       data-ai-entity-type="Testimonial">
    <p itemprop="reviewBody">Great product!</p>
    <div itemscope itemprop="author" itemtype="https://schema.org/Person"
         data-ai-entity-type="Person">
      <p itemprop="name">Reviewer Name</p>
    </div>
  </div>
  
</div>
```

---

## Validation Checklist

Before publishing, verify:

- [ ] All `itemscope` elements have corresponding `itemtype`
- [ ] All `itemprop` attributes are inside an `itemscope`
- [ ] WAIO attributes are paired with microdata
- [ ] No orphaned `itemprop` attributes
- [ ] Tested with Google Rich Results Test
- [ ] Tested with Schema.org Validator
- [ ] JSON-LD is also present for critical schemas
- [ ] Content is accurate and complete
- [ ] Webflow preview shows correct HTML output

---

## Resources

- **Schema.org Documentation:** https://schema.org/
- **Google Structured Data Guide:** https://developers.google.com/search/docs/appearance/structured-data
- **Webflow Custom Attributes:** https://university.webflow.com/lesson/custom-attributes
- **Google Rich Results Test:** https://search.google.com/test/rich-results
- **Schema.org Validator:** https://validator.schema.org/
