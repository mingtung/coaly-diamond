<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1 v-if="login">Login</h1>
        <h1 v-else>Register</h1>
        <b-form @submit="onSubmit" @reset="onReset" class="w-100">
          <b-form-group id="form-username-group"
                        label="Username:"
                        label-for="form-title-input">
              <b-form-input id="form-username-input"
                            type="text"
                            v-model="userForm.username"
                            required
                            placeholder="Enter username">
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-password-group"
                          label="Password:"
                          label-for="form-password-input">
                <b-form-input id="form-password-input"
                              type="password"
                              v-model="userForm.password"
                              required
                              placeholder="Enter password">
                </b-form-input>
              </b-form-group>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
          </b-form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',
  data() {
    return {
      userForm: {
        username: '',
        password: '',
      },
      login: false,
    };
  },
  methods: {
    postRegister(payload) {
      const path = 'http://127.0.0.1:5000/auth/register';
      axios
        .post(path, payload)
        .then(res => {
          console.log(res);
          this.login = true;
        })
        .catch(error => {
          console.log(error);
        });
    },
    postLogin(payload) {
      const path = 'http://127.0.0.1:5000/auth/vue_login';
      axios
        .post(path, payload)
        .then(res => {
          console.log(res);
          // TODO to the blog page
        })
        .catch(error => {
          console.log(error);
        });
    },
    initForm() {
      this.userForm.username = '';
      this.userForm.password = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        username: this.userForm.username,
        password: this.userForm.password,
      };
      if (!this.login) {
        this.postRegister(payload);
      } else {
        this.postLogin(payload);
      }
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.initForm();
    },
  },
  created() {},
};
</script>
