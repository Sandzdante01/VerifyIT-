# VerifyIT Frontend

The VerifyIT frontend is a React + TypeScript + Vite application for analyzing and verifying technical claims against trusted sources.

## Project Overview

VerifyIT is an educational misinformation detection system designed to help users validate technology-related statements using evidence-based analysis.
The app provides the following capabilities:

- Claim analysis with confidence scoring and verdicts.
- Intelligent domain selection and out-of-scope warning suggestions.
- Detailed evidence review from trusted technical sources.
- Analysis history with search, view, and delete actions.
- User authentication and profile management.
- Personalized settings for trust threshold and alert preferences.
- Feedback submission for claim results.

## Key Features

- **Claim Verification**: Enter a technical claim to receive a verdict and confidence score.
- **Domain Focus**: Choose a topic domain such as Cybersecurity, Databases, Networking, Web Development, Hardware, or let the system auto-detect.
- **Evidence Dashboard**: Inspect matched evidence sources, trust scores, and verified content.
- **History & Audit Trail**: Browse previous analyses, search claims, and revisit result details.
- **User Settings**: Configure trust thresholds, preferred source types, alert settings, and view profile details.
- **Feedback Flow**: Submit feedback on analysis outcomes and report incorrect evidence.
- **Protected Routes**: Secure authenticated pages using login and signup flows.

## Tech Stack

- React 19
- TypeScript
- Vite
- Tailwind CSS
- Axios
- React Router DOM
- Framer Motion
- Lucide Icons
- ESLint

## Folder Structure

- `src/pages` — application views such as Analyze, Result, History, Sources, Feedback, and Settings.
- `src/components` — reusable UI components for analysis, auth, layout, and common controls.
- `src/services/api.ts` — API client and backend integration for authentication, claim analysis, history, sources, feedback, and settings.
- `src/types` — shared TypeScript models used across the app.
- `src/utils` — utility helpers for label formatting and PDF export.

## Local Development

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run dev
```

3. Preview the production build:

```bash
npm run preview
```

## Environment

The frontend expects an API base URL from environment variables:

- `VITE_API_BASE_URL` — default is `http://127.0.0.1:8000/api`

## Notes

- Authentication tokens are stored in `localStorage` under `verifyit_access_token`.
- The frontend connects with backend endpoints for `/auth`, `/claims`, `/sources`, `/feedback`, and `/settings`.
- The app includes user-friendly feedback for out-of-scope claims and alternative suggestion flows.
