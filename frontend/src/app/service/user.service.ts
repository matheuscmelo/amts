import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../service/auth.service';

@Injectable({
    providedIn: 'root'
  })
export class UserService {

    constructor(
        private http: HttpClient,
        private authService: AuthService,
    ) {}

    requestPasswordReset(userData) {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });
        return this.http.post("/api/request_reset_password", userData,{ headers });
    }

    resetPassword(userData) {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });
        return this.http.post("/api/reset_password", userData,{ headers });
    }

    updateUser(userData) {
        this.authService.checkLogin();
        const token = localStorage.getItem('user_token');
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': token? `Bearer ${token}` : ''
        });
        return this.http.put("/api/user", userData,{ headers });
    }

    addImage(imageData) {
        this.authService.checkLogin();
        const token = localStorage.getItem('user_token');
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': token? `Bearer ${token}` : ''
        });
        return this.http.post(`/api/user/image`, imageData, { headers });
    }

    getUserRequests() {
        this.authService.checkLogin();
        const token = localStorage.getItem('user_token');
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': token? `Bearer ${token}` : ''
        });
        return this.http.get("/api/requests", { headers });
    }

    approveRequest(id) {
        this.authService.checkLogin();
        const token = localStorage.getItem('user_token');
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': token? `Bearer ${token}` : ''
        });
        return this.http.put("/api/requests/" + id, {
            action: "approve"
        }, {headers})
    }

    disapproveRequest(id) {
        this.authService.checkLogin();
        const token = localStorage.getItem('user_token');
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': token? `Bearer ${token}` : ''
        });
        return this.http.put("/api/requests/" + id, {
            action: "disapprove"
        }, {headers})
    }

}
