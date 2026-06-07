# Padhai Check

## Overview

Padhai Check is a misinformation detection platform built specifically for Indian students preparing for competitive and board examinations. The platform addresses a critical and growing problem: the rapid spread of false or misleading information about examinations through social media, messaging applications, and unofficial channels. Rumors regarding paper leaks, exam postponements, result manipulation, and fake official circulars cause significant distress among students and their families, often leading to poor decision-making during high-stakes academic periods.

Padhai Check allows students and parents to submit any suspicious claim, message, image, or document for verification. The system analyzes the content using a pipeline of specialized AI agents, each responsible for a distinct stage of the verification process, and returns a structured verdict along with a student-friendly explanation, supporting evidence, and emotional support where the student appears distressed.

The system is designed specifically for the Indian educational context, with knowledge of national examination bodies such as NTA, CBSE, NCERT, UGC, and AICTE, and covers major examinations including JEE Main, JEE Advanced, NEET, CUET, UPSC, SSC, CAT, GATE, and all major state board examinations.

---

## AI Agents

## 1. Ingestion Agent

Prepares raw input for all downstream agents.

- Detects input language: English, Hindi, or Hinglish
- Translates Hindi and Hinglish content to English while preserving original meaning
- Extracts key named entities: JEE, NEET, NTA, CBSE, NCERT, UPSC, UGC, AICTE, and related institutions
- Identifies dates and deadlines mentioned in the text
- Produces a cleaned, normalized version of the text and a one-to-two sentence summary

---

## 2. Claim Agent

Identifies and categorizes the central claim being made.

| Category | Description |
|---|---|
| EXAM_POSTPONEMENT | Exam date change or postponement rumors |
| PAPER_LEAK | Question paper leak allegations |
| RESULT_ISSUE | Result delays, re-evaluation, or grace marks |
| RULE_CHANGE | Eligibility criteria or rule modification |
| ADMISSION_UPDATE | Cutoffs, seat allotment, or admission process |
| FEE_CHANGE | Fee hike or reduction claims |
| SYLLABUS_CHANGE | Curriculum or syllabus modification rumors |
| FAKE_CIRCULAR | Forged official-looking documents or circulars |
| OTHER | Any other education-related claim |

Also determines urgency level (low, medium, high, or critical), the related official body, affected exams, and whether immediate verification is required.

---

## 3. Fact-Check Agent

The core verification engine. Operates with domain knowledge covering NTA, CBSE, NCERT, UGC, AICTE, IITs, NITs, and all major national and state examinations.

**Verdict options:**

| Verdict | Meaning |
|---|---|
| True | Claim is consistent with official sources |
| False | Claim is contradicted by official sources |
| Misleading | Claim contains partial truth presented deceptively |
| Unverified | Cannot be confirmed or denied; official verification recommended |

**Red flags detected by this agent:**
- Sensational language such as "BREAKING" or excessive punctuation
- Missing official reference numbers, notice numbers, or dates
- Claims sourced from WhatsApp forwards or unofficial channels
- Unrealistic timelines (e.g., exam rescheduled within two days)
- Grammar or spelling errors in documents claiming to be official
- No corroboration found on official websites

Outputs a confidence score from 0.0 to 1.0 alongside the verdict and detailed reasoning.

---

## 4. Explainability Agent

Translates the technical verdict into language accessible to students and parents.

- Produces the explanation in standard English
- Produces the same explanation in Hinglish (natural Hindi-English mix used by Indian students)
- Lists concrete action steps the student should take
- Provides evidence entries with source name, URL, relevant snippet, and reliability score
- References official websites: nta.ac.in, cbse.gov.in, ncert.nic.in, ugc.ac.in
- References official social media handles: @DG_NTA, @cbseboard

---

## 5. Wellbeing Agent

Detects emotional distress in the student's message and provides mental health support where needed.

**Stress indicators analyzed:**
- Excessive punctuation (multiple exclamation marks or question marks)
- Text written entirely in uppercase
- Distress vocabulary in English: panic, scared, worried, anxious, nervous
- Distress vocabulary in Hindi/Hinglish: tension, dar, ghabra, pareshaan, kya hoga, sab khatam
- Urgency phrases: "please help", "urgent", "emergency", "kya karein"
- Negative self-talk: "I am going to fail", "my life is ruined"
- Multiple unrelated questions in a single message indicating confusion
- Questions about long-term career impact

If stress is detected, the agent returns a warm supportive message in Hinglish and a coping suggestion. If no stress is detected, no wellbeing message is surfaced to the user.

---

## 6. Trend Agent

Classifies the claim into known misinformation patterns and assesses its potential for viral spread.

**Known misinformation patterns tracked:**
- Pre-exam postponement rumors, which historically spike before JEE and NEET
- Paper leak claims appearing immediately before or after examination dates
- Fake circulars with official-looking government letterheads
- Result manipulation allegations
- New rule or regulation fake announcements
- Admission scams and fake seat allotment messages
- Scholarship fraud messages
- Fake websites mimicking official government domains

Outputs a trend category, whether the claim matches a known pattern, a description of the pattern, related claims students should watch for, seasonal relevance, and spread risk rated as low, medium, or high.
