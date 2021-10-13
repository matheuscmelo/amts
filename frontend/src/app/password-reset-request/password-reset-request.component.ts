import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { UserService } from '../service/user.service';

@Component({
  selector: 'app-password-reset-request',
  templateUrl: './password-reset-request.component.html',
  styleUrls: ['./password-reset-request.component.css']
})
export class PasswordResetRequestComponent {

  resetForm;

  constructor(
    private formBuilder: FormBuilder,
    private userService: UserService,
  ) {
    this.resetForm = this.formBuilder.group({
      email: '',
    });
  }

  onSubmit(userData) {
    console.warn(userData);
    this.userService.requestPasswordReset(userData).subscribe(
      _ => alert('Reset de senha requisitado com sucesso! Verifique seu email.'),
      error => alert('Erro ao requisitar reset de senha, tente novamente mais tarde.')
    );
  }


}
