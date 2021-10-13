import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { AuthService } from '../service/auth.service';

@Component({
  selector: 'app-registration-page',
  templateUrl: './registration-page.component.html',
  styleUrls: ['./registration-page.component.css']
})
export class RegistrationPageComponent implements OnInit {

  registerForm;
  image;
  loaded = false;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService
  ) {
    this.registerForm = this.formBuilder.group({
      email: '',
      password: '',
      user_type: '',
      phone: '',
      address: '',
      professional_email: '',
      professional_title: '',
      image: '',
    });
  }

  ngOnInit(): void {}

  @ViewChild("fileInput") fileInput;
  getFile(): File {
    let fi = this.fileInput.nativeElement;
    if (fi.files && fi.files[0]) {
      return fi.files[0];
    }
  }

  async onSubmit(userData) {
    const file: File = this.getFile();
    const reader = new FileReader();
    reader.onloadend = (e) => {
      this.image = reader.result;
      this.loaded = true;
    }
    reader.readAsDataURL(file);

    while (!this.loaded) {
      await new Promise(r => setTimeout(r, 500));
    }
    userData.image = this.image;
    this.loaded = false;

    console.warn(userData);
    this.authService.register(userData).subscribe(
      _ => {
        alert('Registrado com sucesso! Aguarde um operador aprovar sua conta.');
        this.authService.checkLogin();
      },
      error => console.log(error)
    );
    this.registerForm.reset();
  }

}
