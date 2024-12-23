import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.css'],
})
export class LoginPageComponent {

  email = new FormControl('', [Validators.required, Validators.email]);
  registerForm: FormGroup;
  data: any;

  constructor(
    private fb: FormBuilder, 
    private http: HttpClient, 
    private router: Router) 
  {
    this.registerForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  getErrorMessage() {
    if (this.email.hasError('required')) {
      return 'You must enter a value';
    }

    return this.email.hasError('email') ? 'Not a valid email' : '';
  }
  hide = true;
  
  onLogin(){
    // this.router.navigate(['/schedulesPage']);

    if (this.registerForm.valid) {
      const apiUrl = ' http://127.0.0.1:8000/users/login/';
    
      const headers = { 'Content-Type': 'application/json' };
      const body = JSON.stringify(this.registerForm.value);

      this.http.post(apiUrl, body, { headers }).subscribe(
        (response: any) => {

          console.log(this.registerForm.value.username)
          const username = this.registerForm.value.username;
          localStorage.setItem('username', username);

          let user = response.user;
          if (user === 'manager') {
            this.router.navigate(['/schedulesPage']); // Route to manager path
          } else {
            this.router.navigate(['/UsersDashboard']); // Route to employee path
          }
        },
        (error) => {
          console.error(error)
        }
      );

    }
  }
}
