import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RegistrationPageComponent } from './registration-page/registration-page.component';
import { ApprovalPageComponent } from './approval-page/approval-page.component';
import { LoginPageComponent } from './login-page/login-page.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { PasswordResetRequestComponent } from './password-reset-request/password-reset-request.component';
import { PasswordResetComponent } from './password-reset/password-reset.component';

const routes: Routes = [
  { path: 'login', component: LoginPageComponent },
  { path: 'approval', component:  ApprovalPageComponent},
  { path: 'register', component:  RegistrationPageComponent},
  { path: 'dashboard', component: DashboardComponent },
  { path: 'request-reset-password', component: PasswordResetRequestComponent },
  { path: 'reset-password/:token', component: PasswordResetComponent },
  { path: '',   redirectTo: '/login', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
