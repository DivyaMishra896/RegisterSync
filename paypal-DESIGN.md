---
version: alpha
name: "PayPal Marketing 2024"
description: "Typography baseline relies on PayPal Pro for hero headline — largest display text on the page."
colors:
  cool-gray: "#edf0f2"
  hero-sky-blue: "#60cdff"
  light-sky-tint: "#b8e9ff"
  paypal-blue: "#002991"
  pure-white: "#ffffff"
  warm-off-white: "#f1efea"
  browser-link-blue: "#0000ee"
  pure-black: "#000000"
  light-gray: "#e6e7e8"
typography:
  display-hero:
    fontFamily: "PayPal Pro"
    fontSize: "178px"
    fontWeight: "900"
    lineHeight: "195.8px"
    letterSpacing: "-7px"
  display-xl:
    fontFamily: "PayPal Pro"
    fontSize: "144.214px"
    fontWeight: "900"
    lineHeight: "144.214px"
    letterSpacing: "-4.33px"
  display-large:
    fontFamily: "PayPal Pro"
    fontSize: "82.9286px"
    fontWeight: "900"
    letterSpacing: "-1.73px"
  display-medium:
    fontFamily: "PayPal Pro"
    fontSize: "57.6429px"
    fontWeight: "900"
    lineHeight: "63.4071px"
    letterSpacing: "-1.73px"
  heading-large:
    fontFamily: "PayPal Pro"
    fontSize: "48.2857px"
    fontWeight: "900"
    lineHeight: "53.1143px"
    letterSpacing: "-0.97px"
  heading-medium:
    fontFamily: "PayPal Pro"
    fontSize: "40.2857px"
    fontWeight: "900"
    lineHeight: "46.3286px"
    letterSpacing: "-0.81px"
  heading-small:
    fontFamily: "PayPal Pro"
    fontSize: "28.6022px"
    fontWeight: "900"
    lineHeight: "34.3227px"
    letterSpacing: "-0.57px"
  label-nav:
    fontFamily: "PayPal Pro"
    fontSize: "17.1429px"
    fontWeight: "900"
    lineHeight: "21.1429px"
  body-regular:
    fontFamily: "Plain"
    fontSize: "16px"
    fontWeight: "400"
    lineHeight: "18.4px"
  body-small:
    fontFamily: "Plain"
    fontSize: "14px"
    fontWeight: "400"
    lineHeight: "21px"
  body-medium-weight:
    fontFamily: "Plain"
    fontSize: "14px"
    fontWeight: "500"
    lineHeight: "21px"
  body-large:
    fontFamily: "Plain"
    fontSize: "20.3571px"
    fontWeight: "400"
    lineHeight: "28.5px"
rounded:
  radius-pill: "1000px"
  radius-card-large: "104px"
  radius-card-medium: "56px"
  radius-segment: "26.7px"
  radius-card: "32px"
  radius-medium: "12px"
  radius-small: "8px"
spacing:
  spacing-1: "1px"
  spacing-6: "6px"
  spacing-8: "8px"
  spacing-16: "16px"
  spacing-24: "24px"
  spacing-25: "25px"
  spacing-32: "32.1px"
  spacing-44: "44.8px"
  spacing-61: "61.7px"
  spacing-67: "67.2px"
  spacing-71: "71.7px"
  spacing-89: "89.6px"
---

## Overview

Typography baseline relies on PayPal Pro for hero headline — largest display text on the page.

This system uses a 8px base grid with scale values 1, 6, 8, 16, 24, 32, 44, 62, 67, 72, 90.

**Signature traits:**
- Core token rhythm: Token evidence indicates consistent color, spacing, and radius rhythm across visible UI.

## Colors

The palette uses 9 validated color tokens across 1 theme profile. Semantic roles stay attached to observed usage so generation agents can choose accents without inventing new color meaning.

**Semantic naming:**
- **surface-background** maps to `hero-sky-blue`: Role "background" is grounded by usage context "Hero section background, brand accent surface".
- **action-text** maps to `pure-black`: Role "text" is grounded by usage context "All body text, headings, nav links, icon fills".
- **content-background** maps to `paypal-blue`: Role "background" is grounded by usage context "Logo mark, footer brand elements".
- **border-border** maps to `light-gray`: Role "border" is grounded by usage context "Dividers, subtle borders".

### Text Scale
- **Browser Link Blue** (#0000ee): Inline hyperlinks, QR badge link color. Role: text. {authored: rgb(0, 0, 238), space: rgb}
- **Pure Black** (#000000): All body text, headings, nav links, icon fills. Role: text. {authored: rgb(0, 0, 0), space: rgb, alpha: 0.1}

### Interactive
- **Light Gray** (#e6e7e8): Dividers, subtle borders. Role: border. {authored: rgb(230, 231, 232), space: rgb}

### Surface & Shadows
- **Cool Gray** (#edf0f2): Footer background, muted surface. Role: background. {authored: rgb(237, 240, 242), space: rgb}
- **Hero Sky Blue** (#60cdff): Hero section background, brand accent surface. Role: background. {authored: rgb(96, 205, 255), space: rgb}
- **Light Sky Tint** (#b8e9ff): Subtle section tint, footer accent surface. Role: background. {authored: rgb(184, 233, 255), space: rgb}
- **PayPal Blue** (#002991): Logo mark, footer brand elements. Role: background. {authored: rgb(0, 41, 145), space: rgb}
- **Pure White** (#ffffff): Page background, card surfaces, nav background. Role: background. {authored: rgb(255, 255, 255), space: rgb, alpha: 0}
- **Warm Off-White** (#f1efea): Alternate section background, card fill. Role: background. {authored: rgb(241, 239, 234), space: rgb}

## Typography

Typography uses PayPal Pro, Plain across extracted hierarchy roles. Keep hierarchy mapped to these token rows before adding decorative type styles.

Mixes PayPal Pro and Plain for visual contrast. Weight range spans bold, regular, medium. Sizes range from 14px to 178px.

### Font Roles
- **Headline Font**: PayPal Pro
- **Body Font**: PayPal Pro

### Type Scale Evidence
| Role | Font | Size | Weight | Line Height | Letter Spacing | Stack / Features | Notes |
|------|------|------|--------|-------------|----------------|------------------|-------|
| Hero headline — largest display text on the page | PayPal Pro | 178px | 900 | 195.8px | -7px | PayPal Pro, Century Gothic, Helvetica, Arial, sans-serif | Extracted token |
| Large section display headings | PayPal Pro | 144.214px | 900 | 144.214px | -4.33px | PayPal Pro, Century Gothic, Helvetica, Arial, sans-serif | Extracted token |
| Section hero headings (h2.text-group-headline) | PayPal Pro | 82.9286px | 900 | ~91px | -1.73px | PayPal Pro, Century Gothic, Helvetica, Arial, sans-serif | Extracted token |
| Mid-page section headings | PayPal Pro | 57.6429px | 900 | 63.4071px | -1.73px | PayPal Pro, Century Gothic, Helvetica, Arial, sans-serif | Extracted token |
| Card and feature headings | PayPal Pro | 48.2857px | 900 | 53.1143px | -0.97px | PayPal Pro, Century Gothic, Helvetica, Arial, sans-serif | Extracted token |
| Sub-section headings | PayPal Pro | 40.2857px | 900 | 46.3286px | -0.81px | PayPal Pro, Century Gothic, Helvetica, Arial, sans-serif | Extracted token |
| Card titles, smaller headings | PayPal Pro | 28.6022px | 900 | 34.3227px | -0.57px | PayPal Pro, Century Gothic, Helvetica, Arial, sans-serif | Extracted token |
| Navigation labels, segment control labels | PayPal Pro | 17.1429px | 900 | 21.1429px | normal | PayPal Pro, Century Gothic, Helvetica, Arial, sans-serif | Extracted token |
| Body copy, nav items, general UI text | Plain | 16px | 400 | 18.4px | normal | Plain, Helvetica Neue, Arial, sans-serif | Extracted token |
| Secondary body text, captions, footer links | Plain | 14px | 400 | 21px | normal | Plain, Helvetica Neue, Arial, sans-serif | Extracted token |
| Emphasized small text, labels | Plain | 14px | 500 | 21px | normal | Plain, Helvetica Neue, Arial, sans-serif | Extracted token |
| Lead paragraph / intro body text | Plain | 20.3571px | 400 | 28.5px | normal | Plain, Helvetica Neue, Arial, sans-serif | Extracted token |

## Layout

Responsive system uses 3 breakpoint tier(s): mobile, tablet, desktop.

### Responsive Strategy
- **mobile (<= 752px)**: Constrain layout for small viewports and prioritize vertical stacking.
- **tablet (>= 752px)**: Increase spacing and column structure for medium-width viewports.
- **desktop (>= 1024px)**: Expand layout density and horizontal composition for wide viewports.

### Spacing System
| Token | Value | Px | Notes |
|------|-------|----|-------|
| spacing-1 | 1px | 1 | Extracted spacing token |
| spacing-6 | 6px | 6 | Extracted spacing token |
| spacing-8 | 8px | 8 | Extracted spacing token |
| spacing-16 | 16px | 16 | Extracted spacing token |
| spacing-24 | 24px | 24 | Extracted spacing token |
| spacing-25 | 25px | 25 | Extracted spacing token |
| spacing-32 | 32.1px | 32 | Extracted spacing token |
| spacing-44 | 44.8px | 45 | Extracted spacing token |
| spacing-61 | 61.7px | 62 | Extracted spacing token |
| spacing-67 | 67.2px | 67 | Extracted spacing token |
| spacing-71 | 71.7px | 72 | Extracted spacing token |
| spacing-89 | 89.6px | 90 | Extracted spacing token |

## Elevation & Depth

Keep depth flat unless validated shadow or interaction evidence appears in the extraction payload. Do not invent shadows beyond this evidence boundary.

### Shadow Evidence
| Shadow Token | Layers | Details |
|--------------|--------|---------|
| shadow-none-inset | 1 | inset 0px 0px 0px 1px rgba(0, 0, 0, 0) |
| shadow-card-ambient | 1 | 0px 24px 48px 0px rgba(0, 0, 0, 0.08) |
| shadow-white-top | 1 | 0px -28.5714px 0px 28.5714px rgb(255, 255, 255) |
| shadow-white-bottom | 1 | 0px 28.5714px 0px 28.5714px rgb(255, 255, 255) |

### Interaction Signals
| Theme | Signal | Evidence |
|-------|--------|----------|
| Light | backdrop-filter | blur(30px) ; blur(21.3014px) |
| Light | outline-color | rgb(0, 0, 0) ; rgb(255, 255, 255) ; rgb(0, 0, 238) |
| Light | outline-width | 3px |
| Light | outline-offset | 0px |
| Light | transform | matrix(1, 0, 0, 1, 12, 12) ; matrix(1, 0, 0, 1, 0, 0) ; matrix(1, 0, 0, 1, 0.75, 0.75) |

## Shapes

Shape language maps directly to rounded tokens. Keep component corners consistent with the role mapping below before introducing bespoke geometry.

### Radius Roles
| Token | Value | Px | Role Mapping |
|------|-------|----|--------------|
| radius-small | 8px | 8 | Control corner |
| radius-medium | 12px | 12 | Control corner |
| radius-segment | 26.7px | 27 | Large surface corner |
| radius-card | 32px | 32 | Large surface corner |
| radius-card-medium | 56px | 56 | Large surface corner |
| radius-card-large | 104px | 104 | Large surface corner |
| radius-pill | 1000px | 1000 | Large surface corner |

### Geometry Evidence
| Radius Token | Shape | Units |
|--------------|-------|-------|
| radius-pill | 1000px | px |
| radius-card-large | 104px | px |
| radius-card-medium | 56px | px |
| radius-segment | 26.7px | px |
| radius-card | 32px | px |
| radius-medium | 12px | px |
| radius-small | 8px | px |

## Components

(none detected)

## Do's and Don'ts

Guardrails protect Core token rhythm without adding unsupported visual claims.

| Do | Don't |
|----|---------|
| Do maintain consistent spacing using the base grid | Don't make unsupported claims about absent visual features |
| Do maintain WCAG AA contrast ratios (4.5:1 for normal text) | Don't mix rounded and sharp corners in the same view |
| Do use the primary color only for the single most important action per screen |  |
| Do verify evidence before writing new design-system guidance |  |

## Responsive Evidence

### Breakpoints
| Name | Width | Key Changes |
|------|-------|-------------|
| Mobile | <= 752px | screen and (max-width: 752px) |
| Mobile | >= 752px | only screen and (min-width: 752px) |
| Desktop | >= 1024px | only screen and (min-width: 1024px) |
| Desktop | >= 1152px | only screen and (min-width: 1152px) |
| Breakpoint 5 | Unknown | (max-width: 41rem) |

## Agent Prompt Guide

### Example Component Prompts
- Create button component using validated primary color role and spacing tokens.
- Create card component with mapped radius role and evidence-backed elevation.
- Create form input component using inferred typography hierarchy and border roles.

### Iteration Guide
1. Start with extracted palette and typography roles only.
2. Map spacing and radius directly from token tables before visual polish.
3. Apply component patterns one section at a time and compare against source intent.
4. Keep elevation claims tied to explicit evidence in output.
5. Iterate with smallest diffs and re-check section hierarchy after each change.
