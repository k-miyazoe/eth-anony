<template>
  <v-app>
    <Header />
    <v-container grid-list-md>
      <v-layout row wrap align-center justify-center fill-height>
        <v-flex xs12 sm8 lg4 md5>
          <v-card class="mt-12">
            <v-card-title>
              <span class="headline">サインイン</span>
            </v-card-title>
            <!-- <v-card-subtitle>
              <span class="notes-text">学籍番号が偶数の方は実名アカウントで、奇数の方は匿名アカウントでサインインしてください</span></v-card-subtitle>
            <v-spacer /> -->

            <v-card-text>
              <v-layout row fill-height justify-center align-center v-if="loading">
                <v-progress-circular :size="50" color="primary" indeterminate />
              </v-layout>

              <v-form v-else ref="form" v-model="valid" lazy-validation>
                <v-container>
                  <v-text-field v-model="credentials.user_key" label="ユーザーID" :rules="rules.user_key" required />

                  <v-text-field type="password" v-model="credentials.password" :counter="10" label="パスワード"
                    :rules="rules.password" maxlength="10" required v-on:keydown.enter="signIn" />
                </v-container>
                <v-btn class="pink white--text" :disabled="!valid" @click="signIn">
                  サインイン
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
          <router-link to='/signup'>
            アカウントを登録していない方はこちらから
          </router-link>
        </v-flex>
      </v-layout>
    </v-container>
  </v-app>
</template>

<script>
import Swal from "sweetalert2";
import router from "../router";
import Header from "../components/Header.vue";
import header from "/src/node/axios";

const axios = header.setHeader();

export default {
  components: {
    Header,
  },
  data: () => ({
    credentials: {},
    valid: true,
    loading: false,
    rules: {
      user_key: [
        (v) => !!v || "ユーザーIDは必須です",
      ],
      password: [
        (v) => !!v || "パスワードは必須です",
        (v) =>
          (v && v.length > 5) || "パスワードは6文字以上でなければなりません",
      ],
    },
    axios: {},
    user_id: null,
  }),
  mounted() {
    this.checkToken();
  },
  methods: {
    checkToken() {
      if (this.$session.has("token")) {
        router.push("/");
      }
    },
    //イベント処理
    signIn() {
      if (this.$refs.form.validate()) {
        this.loading = true;
        axios
          .post("/auth/", this.credentials)
          .then((res) => {
            //ながすぎるので関数にあとでまとめる
            this.$session.start();
            this.$session.set("token", res.data.token);
            this.$session.set("user_id", res.data.user_id);
            this.$session.set("user_name", res.data.user_name);
            this.$session.set("user_eth_address", res.data.user_eth_address);
            this.$session.set("user_group", res.data.user_group);
            this.loading = false;
            router.push("/");
          })
          .catch((e) => {
            this.loading = false;
            console.log(e);
            Swal.fire({
              icon: "warning",
              title: "Error",
              text: "ユーザーIDもしくはパスワード、または両方が間違っています",
              showConfirmButton: false,
              showCloseButton: false,
              timer: 3000,
            });
            this.credentials.password = ""
          });
      }
    },
  },
};
</script>
<style>
.notes-text {
  font-size: 15px;
  /* color: #2196F3; */
  color: red;
}
</style>