import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { UserService } from '../service/user.service';
import { ActivatedRoute } from "@angular/router";

@Component({
  selector: 'app-password-reset',
  templateUrl: './password-reset.component.html',
  styleUrls: ['./password-reset.component.css']
})
export class PasswordResetComponent {

  resetForm;
  token;

  constructor(
    private formBuilder: FormBuilder,
    private userService: UserService,
    private route: ActivatedRoute,
  ) {
    this.resetForm = this.formBuilder.group({
      token: '',
      password: ''
    });
    this.route.params.subscribe( params => this.token = params.token);
  }

  onSubmit(userData) {
    console.warn(userData);
    userData["token"] = this.token;
    this.userService.resetPassword(userData).subscribe(
      _ => alert('Reset de senha realizado com sucesso!'),
      error => alert('Erro ao requisitar reset de senha, tente novamente mais tarde.')
    );
    console.log(this.token);
  }

}
