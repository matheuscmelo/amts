import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { AuthService } from '../service/auth.service';
import { Router, ActivatedRoute } from '@angular/router';
import { ReCaptcha2Component } from 'ngx-captcha';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.css']
})
export class LoginPageComponent implements OnInit {

  loginForm;
  isProd = true;

  @ViewChild('captchaElem') captchaElem: ReCaptcha2Component;
  @ViewChild('langInput') langInput: ElementRef;

  public captchaIsLoaded = false;
  public captchaSuccess = false;
  public captchaIsExpired = false;
  public captchaResponse?: string;

  public theme: 'light' | 'dark' = 'light';
  public size: 'compact' | 'normal' = 'normal';
  public lang = 'en';
  public type: 'image' | 'audio';

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute,
  ) {
    this.loginForm = this.formBuilder.group({
      email: '',
      password: '',
      recaptcha: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.authService.checkLogin('dashboard', '', true);
    this.checkEnvironment();
  }

  private checkEnvironment() {
    const self = this;
    this.authService.getInfo().subscribe( (data) => {
        self.isProd = data['environment'] === 'prod'
        console.log(self.isProd);
    } )
  }

  handleSuccess(data) {
    this.captchaSuccess = true;
  }

  onSubmit(userData) {
    if (this.captchaSuccess || !this.isProd) {
      this.authService.login(userData);
    } else {
      alert('Preencha o captcha');
    }
  }

}
