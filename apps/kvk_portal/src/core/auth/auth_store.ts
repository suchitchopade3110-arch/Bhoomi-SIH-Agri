export interface AgronomistProfile {
  id: string;
  name: string;
  role: 'agronomist';
  kvkCenter: string;
  specialization: string;
}

class AuthStore {
  private currentAgronomist: AgronomistProfile = {
    id: 'agr_kvk_01',
    name: 'Dr. S. Sundaram',
    role: 'agronomist',
    kvkCenter: 'ICAR-KVK Erode (MYRADA)',
    specialization: 'Crop Protection & Plant Pathology',
  };

  private token: string = 'demo_kvk_agronomist_jwt_token';

  getCurrentAgronomist(): AgronomistProfile {
    return this.currentAgronomist;
  }

  getToken(): string {
    return this.token;
  }

  isAuthenticated(): boolean {
    return true;
  }
}

export const authStore = new AuthStore();
