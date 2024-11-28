import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import {FormControl, Validators, FormsModule, ReactiveFormsModule, FormBuilder, FormGroup} from '@angular/forms';

@Component({
  selector: 'app-sign-up-page',
  templateUrl: './sign-up-page.component.html',
  styleUrls: ['./sign-up-page.component.css']
})
export class SignUpPageComponent {
  
  email = new FormControl('', [Validators.required, Validators.email]);

  registerForm: FormGroup;
  data: any;

  constructor(private fb: FormBuilder, private http: HttpClient) {
    this.registerForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  getErrorMessage() {
    if (this.email.hasError('required')) {
      return 'You must enter a value';
    }

    return this.email.hasError('email') ? 'Not a valid email' : '';
  }
  hide = true;
  onRegister() : void | any{
    if (this.registerForm.valid) {
      console.log(1);
      console.log(this.registerForm);
      const apiUrl = ' http://127.0.0.1:8000/users/register/';
    
      return this.http.post(apiUrl, this.registerForm.value)
    }

    
  }

  
}