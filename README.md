# ⚙️ Automated Lead-Scoring Engine & Workflow Architecture

**Project Status:** MVP Deployed  
**Role:** Full Stack

## 📖 Executive Summary
Client acquisition for high-end commercial media projects traditionally relies on manual web searches and subjective visual assessments, resulting in a low ROI on prospecting time. 

This project replaces that manual workflow with a data-driven, automated pipeline. The system scrapes target business directories, extracts media assets, runs a simulated vision analysis to detect visual brand deficits, and scores the leads in a centralized dashboard for the sales team.

## 🏗️ System Architecture & Tech Stack
This MVP was built using a custom Python and Next.js stack, though the underlying logic maps directly to enterprise workflow tools like the **Microsoft Power Platform**.

* **Data Ingestion (The Trigger):** Python / Selenium (Playwright equivalent)
* **Business Logic (The Action):** Python assessment algorithm (scoring parameters based on contrast ratios and visual fidelity)
* **Data Layer (The Database):** SQLite (Relational database structuring)
* **Presentation Layer (The UI):** Next.js / Tailwind CSS (Server-side rendering for dashboard metrics)

## 🔄 Process Flow
1. **Target Identification:** System reads target URLs from `targets.csv`.
2. **Asset Extraction:** Scraper navigates to the target, bypassing rate limits via timed execution, and extracts primary visual assets.
3. **Deficit Tagging & Scoring:** Assets are evaluated against a baseline metric (e.g., "Low Resolution," "Poor Lighting"). A priority score (1-10) is assigned based on the severity of the deficit.
4. **Dashboard Push:** Data is written to `leads.db` and rendered on a Next.js frontend, providing the business development team with actionable, scored targets.

## 🚀 Enterprise Application Parallels (Microsoft 365)
The architectural logic designed in this custom stack translates directly to enterprise environments:
* The Python routing script mirrors the trigger-and-action logic of **Power Automate Cloud Flows**.
* The relational SQLite database utilizes the same structuring principles as **Microsoft Dataverse**.
* The Next.js dashboard functions identically to a **PowerApps Canvas App**, providing a clean UI for stakeholder review.

## 🗺️ Future Roadmap (Phase 2)
* **API Integration:** Swap the localized scoring algorithm for a live integration with the Google Cloud Vision API for true machine-learning asset analysis.
* **CRM Routing:** Implement webhook functionality to push leads scoring >7 directly into Salesforce or HubSpot.
* **Automated Outreach:** Generate dynamic email templates based on the specific "Deficit Tag" identified by the system.
