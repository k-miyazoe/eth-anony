<template>
  <v-app>
    <Header />
    <v-btn color="primary" @click="log">
      log button
    </v-btn>
    <v-container grid-list-md>
      <v-layout row wrap align-center justify-center fill-height>
        <v-flex xs12 sm8 lg4 md5>
          <v-card class="mt-12">
            <v-card-title>
              <span class="headline">サインアップ</span>
            </v-card-title>

            <v-spacer />

            <v-card-text>
              <v-layout row fill-height justify-center align-center v-if="loading">
                <v-progress-circular :size="50" color="primary" indeterminate />
              </v-layout>

              <v-form v-else ref="form" v-model="valid" lazy-validation>
                <v-container>
                  <v-text-field v-model="credentials.email" label="学籍番号メールアドレス" :rules="rules.email" required />
                  <v-text-field type="password" v-model="credentials.password" :counter="20" label="パスワード"
                    :rules="rules.password" maxlength="20" required />
                  <!--確認用passoword-->
                  <v-text-field type="password" v-model="check_password" :counter="20" label="パスワード(確認用)"
                    :rules="rules.password" maxlength="20" required />
                  <v-text-field v-model="credentials.username" label="名前" :rules="rules.username" required />
                  <v-row>
                    <v-checkbox v-model="credentials.status" label="履修生" value="false" :rules="rules.status">
                    </v-checkbox>
                    <v-checkbox v-model="credentials.status" label="その他" value="true" :rules="rules.status">
                    </v-checkbox>
                  </v-row>
                  <!--追加 group これだと追加できてない-->
                  <v-row>
                    <v-select v-model="credentials.user_group" :items="items" label="グループを選択" outlined
                      :rules="rules.user_group">
                    </v-select>
                  </v-row>
                </v-container>
                <v-btn class="pink white--text" :disabled="!valid" @click="signUp">
                  サインアップ
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
          <router-link to='/signin'>
            アカウントがある方はこちらから
          </router-link>
        </v-flex>
      </v-layout>
    </v-container>
  </v-app>
</template>

<script>
import Swal from "sweetalert2";
import router from "../router";
import header from "/src/node/axios";
import Header from "../components/Header.vue";

const axios = header.setHeader();

const Web3 = require("web3");
const web3 = new Web3(process.env.VUE_APP_GETH_API);
const miner = "0x0fcA84baf65fB28dDFeA1B71e66DA579144cbB55";
//const miner = process.env.VUE_APP_MINER;
const miner_password = "admin";
//const miner_password = process.env.VUE_APP_MINER_PASS;
let create_ether = {};


export default {
  components: {
    Header,
  },
  data: () => ({
    credentials: {},
    axios: {},
    valid: true,
    loading: false,
    check_password: "",
    rules: {
      email: [
        (v) => !!v || "メールアドレスは必須です",
      ],
      password: [
        (v) => !!v || "パスワードは必須です",
        (v) =>
          (v && v.length > 7) || "パスワードは8文字以上でなければなりません",
      ],
      username: [
        (v) => !!v || "名前は必須です",
      ],
      status: [
        (v) => !!v || "選択は必須です",
      ],
      user_group: [
        (v) => !!v || "選択は必須です",
      ],
    },
    userId: null,
    status: null, //履修生(false) 先生,TA(true)
    //A 実名 B 匿名 C 完全匿名
    items: ['A', 'B', 'C'],
  }),
  mounted() {
    this.checkToken();
  },
  methods: {
    checkToken() {
      this.$session.start();
      if (this.$session.has("token")) {
        router.push("/");
      }
    },
    //ここは長すぎるから関数にきりわける
    signUp() {
      if (this.$refs.form.validate()) {
        this.loading = true;
        //所持通貨の初期値を0に設定しておく
        this.credentials.eth_stock = 0;
        console.log("signupのobjの中身", this.credentials)
        //パスワードの確認
        if (this.checkPassword(this.credentials.password, this.check_password)) {
          axios
            .post(process.env.VUE_APP_API_URL + "/api/create-user/", this.credentials)
            .then((res) => {
              console.log(res);
              router.push("/signin");
            })
            .catch((e) => {
              this.loading = false;
              console.log(e);
              Swal.fire({
                icon: "warning",
                title: "Error",
                text: "入力が正しくありません",
                showConfirmButton: false,
                showCloseButton: false,
                timer: 3000,
              });
            });
        }
        else {
          Swal.fire({
            icon: "warning",
            title: "Error",
            text: "パスワードが一致しません.もう一度入力してください",
            showConfirmButton: false,
            showCloseButton: false,
            timer: 1000,
          });
          this.loading = false;
          this.credentials.password = ""
          this.check_password = ""
        }
      }
    },
    checkPassword(pass1, pass2) {
      if (pass1 == pass2) {
        return true
      } else {
        return false
      }
    },

    //new

    //ethアカウント作成はここだけ ok 処理に5秒程度時間がかかる
    createEthAccount(password){
      web3.eth.personal.newAccount(password).then(
        (res) => {
          //0x4118E288dD9317e45950F2A4E9403776F0aec728
          //signin関数内で使用するオブジェクト
          create_ether["adress"] = res;
          create_ether["password"] = password;
          console.log("etherアカウント作成ok", res);
        },
        (err) => {
          console.log("error", err);
        }
      );
    },
    //5eth与える 二つのアカウントの合計で10ethの想定 関数の共通化ができる ok　受け取る関数
    async initialEth(received_address,value) {
      const from = await web3.utils.toChecksumAddress(miner);
      const to = await web3.utils.toChecksumAddress(received_address);
      const transaction = {
        from: from,
        to: to,
        value: value,
      };
      await web3.eth.personal
        .unlockAccount(from, miner_password, 15000)
        .then(() => {
          web3.eth.sendTransaction(transaction);
        });
      console.log("受け取り完了");
    },
    //共通処理 送る関数
    async sendEth(sender_address,sender_pass,value) {
      const from = await web3.utils.toChecksumAddress(sender_address);
      const to = await web3.utils.toChecksumAddress(miner);
      const transaction = {
        from: from,
        to: to,
        value: value,
        gasPrice: 0,
      };
      await web3.eth.personal
        .unlockAccount(from, sender_pass, 15000)
        .then(() => {
          web3.eth.sendTransaction(transaction);
        });
      console.log("送金完了");
    },
    log() {
      const new_account = "0x4118E288dD9317e45950F2A4E9403776F0aec728";
      // // this.checkEth(new_account);
      // // this.initialEth(new_account,1);
      this.checkEth(new_account);
      //this.sendEth(new_account,"test",1);
    },
    //メモ用関数
    checkMining() {
      web3.eth.isMining().then(console.log);
    },
    checkMinerAddress() {
      web3.eth.getCoinbase().then(console.log);
    },
    showMinerEth() {
      const miner = "0x0fca84baf65fb28ddfea1b71e66da579144cbb55"
      web3.eth.getBalance(miner).then(console.log);
    },
    checkEthAccountNum() {
      web3.eth.personal.getAccounts().then(
        (data) => {
          console.log("OK", data);
        },
        (err) => {
          console.log("error", err);
        }
      );
    },
    checkEth(address) {
      //0x4118E288dD9317e45950F2A4E9403776F0aec728
      //const receive = "0x4118E288dD9317e45950F2A4E9403776F0aec728"
      web3.eth.getBalance(address)
      .then(console.log);
    },
  },
};
</script>