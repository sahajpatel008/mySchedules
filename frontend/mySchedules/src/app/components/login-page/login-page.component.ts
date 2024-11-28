import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.css'],
})
export class LoginPageComponent {

  email = new FormControl('', [Validators.required, Validators.email]);

  registerForm: FormGroup;
  data: any;

  constructor(private fb: FormBuilder, private http: HttpClient) {
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
  onLogin() : void | any{
    if (this.registerForm.valid) {
      console.log(1);
      console.log(this.registerForm);
      const apiUrl = ' http://127.0.0.1:8000/users/login/';
    
       this.http.post(apiUrl, this.registerForm.value).subscribe(
        (response) => {
          this.data = response; // Handle the response here
          console.log(this.data);
        },
        (error) => {
          console.error('API call failed:', error); // Handle errors
        });
    }

    
  }

}
