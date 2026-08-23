export interface OfficerUser {
  id: string;
  name: string;
  role: 'officer';
  jurisdiction: string;
  verifierTag: string;
}

const DEFAULT_OFFICER: OfficerUser = {
  id: 'off_erode_01',
  name: 'K. Rangarajan',
  role: 'officer',
  jurisdiction: 'Taluk Office, Erode District',
  verifierTag: 'officer:taluk_erode',
};

const TOKEN_KEY = 'bhoomi_officer_jwt';

export const authStore = {
  getToken: (): string | null => {
    return localStorage.getItem(TOKEN_KEY) || 'mock_officer_jwt_token_sih25076';
  },

  setToken: (token: string): void => {
    localStorage.setItem(TOKEN_KEY, token);
  },

  clearToken: (): void => {
    localStorage.removeItem(TOKEN_KEY);
  },

  getCurrentOfficer: (): OfficerUser => {
    return DEFAULT_OFFICER;
  },

  isAuthenticated: (): boolean => {
    return true; // Officer portal ready
  },
};
