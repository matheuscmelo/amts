import { Component, OnInit, ViewChild } from '@angular/core';
import { AuthService } from '../service/auth.service';
import { FormBuilder } from '@angular/forms';
import { UserService } from '../service/user.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  imageForm;
  userForm;
  image;
  loaded = false;
  requests = [];

  constructor(
    private authService: AuthService,
    private formBuilder: FormBuilder,
    private userService: UserService,
  ) {
    this.imageForm = this.formBuilder.group({
      image: '',
    });
    this.userForm = this.formBuilder.group({
      phone: this.getUserData().phone,
      address: this.getUserData().address,
      professional_email: this.getUserData().professional_email,
      professional_title: this.getUserData().professional_title,
    });
  }

  async ngOnInit() {
    this.authService.checkLogin();
    this.getRequests();
  }

  @ViewChild("fileInput") fileInput;
  getFile(): File {
    let fi = this.fileInput.nativeElement;
    if (fi.files && fi.files[0]) {
      return fi.files[0];
    }
  }

  onSubmitUser(userData) {
    this.userService.updateUser(userData).subscribe(_ => this.authService.checkLogin(), error => console.log(error));
  }

  async onSubmitImage(imageData) {
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
    imageData.image = this.image;
    this.loaded = false;
    this.userService.addImage(imageData).subscribe(_ => this.authService.checkLogin(), error => console.log(error));
  }

  getUserImages() {
    return this.authService.userData.images;
  }

  getUserData() {
    return this.authService.userData;
  }

  logout() {
    this.authService.logout();
    this.authService.checkLogin();
  }

  async getRequests() {
    var dat;
    await this.userService.getUserRequests().toPromise().then(
      data => dat = data,
    );
    this.requests = dat;
  }

  async approveRequest(id) {
    await this.userService.approveRequest(id).subscribe();
    await sleep(500);
    this.getRequests();
  }

  async disapproveRequest(id) {
    await this.userService.disapproveRequest(id).subscribe();
    await sleep(500);
    this.getRequests();
  }

}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
