# BHOOMI Officer Land Verification Portal (Phase 1)

Official Land Verification & Agricultural Operations Portal for SIH25076.

## Architecture
- **Framework**: React 18 with Vite
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui design language
- **Server State**: TanStack Query (`@tanstack/react-query`)
- **HTTP Client**: Axios
- **Routing**: React Router DOM
- **Icons**: Lucide React

## Phase 1 Workflow
1. **Land Queue**: Fetches land records from `GET /api/v1/officer/land-queue`.
2. **Review Panel**: Displays farmer-stated survey number, self-reported area (acres), farm ID, submission timestamp, and preserved polygon GeoJSON.
3. **Approve Action**: Opens official verification modal and submits `POST /api/v1/officer/land/{id}/review` with `decision: "verified"`.
4. **Queue Synchronization**: Automatically invalidates and refreshes the land queue on successful verification.
