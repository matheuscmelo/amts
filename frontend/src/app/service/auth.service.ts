import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router, ActivatedRoute } from '@angular/router';
import CryptoJS from 'crypto-js';


@Injectable({
    providedIn: 'root'
  })
export class AuthService {

    userData = JSON.parse(localStorage.getItem('user_data'));

    constructor(
        private http: HttpClient,
        private router: Router,
        private route: ActivatedRoute,
    ) {}


    getInfo() {
        return this.http.get('/api/info')
    }


    register(userData) {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });

        userData['password'] = this.encryptPassword(userData['email'], userData['password']);

        return this.http.post('/api/users', userData, { headers } );
    }

    encryptPassword(email, password) {
        return CryptoJS.SHA256(email+password).toString(CryptoJS.enc.Hex);
    }

    login(userData) {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });
        userData['password'] = this.encryptPassword(userData['email'], userData['password']);

        return this.http.post('/api/login', userData, { headers } ).subscribe(
            data => {
                localStorage.setItem('user_token', data['access_token']);
                this.checkLogin('dashboard', '', true);
            },
            _ => {
                alert('Email não encontrado ou senha errada!')
            }
        );
    }

    logout() {
        localStorage.removeItem('user_token');
        localStorage.removeItem('user_data');
        this.userData = {};
    }

    getUserData() {
        this.checkLogin();
        return this.userData;
    }

    checkLogin(successRedirect: String = '', failRedirect: String = 'login', onSuccessRedirect: Boolean = false, onFailRedirect: Boolean = true) {
        const token = localStorage.getItem('user_token');
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': token? `Bearer ${token}` : ''
        });
        return this.http.get('/api/auth', { headers } ).subscribe(
            data => {
                this.userData = data;
                console.log(this.userData);
                localStorage.setItem('user_data', JSON.stringify(this.userData));
                onSuccessRedirect? this.router.navigate([successRedirect]) : null;
            },
            error => {
                console.log(error);
                this.logout();
                onFailRedirect? this.router.navigate([failRedirect]) : null;
            }
        );

    }


}
