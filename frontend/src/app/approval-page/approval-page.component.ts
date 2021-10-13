import { Component, OnInit } from '@angular/core';
import { UserService } from '../service/user.service';

@Component({
  selector: 'app-approval-page',
  templateUrl: './approval-page.component.html',
  styleUrls: ['./approval-page.component.css']
})
export class ApprovalPageComponent implements OnInit {

  requests = [];

  constructor(private userService: UserService) { }

  ngOnInit() {
    this.getRequests();
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
