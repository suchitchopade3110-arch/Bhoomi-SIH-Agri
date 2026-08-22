# BHOOMI Farmer Mobile App (Phase 1)

AI-Powered Farmer Companion for SIH25076.

## Architecture
- **Framework**: Flutter (Dart)
- **State Management**: Riverpod (`flutter_riverpod`)
- **Navigation**: `go_router`
- **HTTP Client**: `dio`
- **Storage**: `flutter_secure_storage`
- **Connectivity**: `connectivity_plus`

## Phase 1 Feature Flow
1. **WelcomeScreen**: Entry point introducing BHOOMI.
2. **OnboardingScreen**: Voice-first multi-step farm profile collection (crop, area, growth stage, soil type, irrigation access, season) with voice interaction simulation and instant tap fallback controls.
3. **ConfirmFarmScreen**: Review parsed farm profile before calling `POST /api/v1/farms`.
4. **FarmHomeScreen**: Displays summary fetched from `GET /api/v1/farms/{id}/summary`, strictly adhering to contract fields (null health score displays as "Unrated").
5. **Network Resilience**: Degraded network banner and error/retry states.
