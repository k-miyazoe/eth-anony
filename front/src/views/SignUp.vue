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
              <span class="headline">実名アカウント</span>
            </v-card-title>
            <v-spacer />
            <v-card-text>
              <v-layout row fill-height justify-center align-center v-if="loading">
                <v-progress-circular :size="50" color="primary" indeterminate />
              </v-layout>

              <v-form v-else ref="form" v-model="valid" lazy-validation>
                <v-container>
                  <v-text-field v-model="main_account.user_key" label="ユーザーID*(半角英数)" :rules="rules.user_key" required />
                  <v-text-field type="password" v-model="main_account.password" :counter="20" label="パスワード*(半角英数)" :rules="rules.password"
                    maxlength="10" required />
                  <!--確認用passoword-->
                  <v-text-field type="password" v-model="check_password_main" :counter="20" label="パスワード(確認用)*" :rules="rules.password"
                    maxlength="10" required />
                  <v-text-field v-model="main_account.user_email" label="学籍番号メールアドレス*" :rules="rules.email" required />
                  
                  <v-text-field v-model="main_account.user_name" label="氏名*" :rules="rules.user_name" required />
                </v-container>
              </v-form>
            </v-card-text>
          </v-card>

          <v-card class="mt-12">
            <v-card-title>
              <span class="headline">匿名アカウント</span>
            </v-card-title>
            <v-spacer />
            <v-card-text>
              <v-layout row fill-height justify-center align-center v-if="loading">
                <v-progress-circular :size="50" color="primary" indeterminate />
              </v-layout>
          
              <v-form v-else ref="form" v-model="valid" lazy-validation>
                <v-container>
                  <v-text-field v-model="sub_account.user_key" label="ユーザーID*(半角英数)" :rules="rules.user_key" required />
                  <v-text-field type="password" v-model="sub_account.password" :counter="20" label="パスワード*(半角英数)"
                    :rules="rules.password" maxlength="10" required />
                  <!--確認用passoword-->
                  <v-text-field type="password" v-model="check_password_sub" :counter="20" label="パスワード(確認用)*" :rules="rules.password"
                    maxlength="10" required />
                  <v-text-field v-model="sub_account.email" label="学籍番号メールアドレス(任意)"/>
                </v-container>
              </v-form>
            </v-card-text>
          </v-card>
          <router-link to='/signin'>
            アカウントがある方はこちらから
          </router-link>
          <v-btn class="pink white--text" :disabled="!valid" @click="signUp">
            サインアップ
          </v-btn>
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
const miner = process.env.VUE_APP_MINER;
const miner_password = process.env.VUE_APP_MINER_PASS;


export default {
  components: {
    Header,
  },
  data: () => ({
    main_account: {},
    sub_account: {},
    valid: true,
    loading: false,
    check_password_main: "",
    check_password_sub: "",
    rules: {
      user_key: [
        (v) => !!v || "ユーザーidは必須です",
      ],
      email: [
        (v) => !!v || "メールアドレスは必須です",
      ],
      password: [
        (v) => !!v || "パスワードは必須です",
        (v) =>
          (v && v.length > 7) || "パスワードは8文字以上でなければなりません",
      ],
      user_name: [
        (v) => !!v || "名前は必須です",
      ],
    },
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
    async signUp() {
      this.loading = true;
      let flag = true;
      while(flag){
        console.log("signupのobjの中身", this.main_account, this.sub_account);
        flag = this.checkForm();
        flag = this.checkUserId();
        flag = this.checkPassword(this.main_account.password,this.check_password_main);
        flag = this.checkPassword(this.sub_account.password,this.check_password_sub);
        //this.main_account.user_eth_addressがよろしくない
        this.main_account.user_eth_address = await this.createEthAccount(this.main_account.password);
        this.sub_account.user_eth_address =  await this.createEthAccount(this.sub_account.password);
        await this.createAccount(this.main_account,100);
        await this.createAccount(this.sub_account,0);
        await this.initialEth(this.main_account.user_eth_address,100);
        flag = false;
      }
      this.loading = false;
      router.push('/signin');
    },
    //改めて動作テストの必要あり
    checkForm() {
      return this.$refs.form.validate();
    },
    //実名と匿名のuserkeyの確認
    checkUserId() {
      if(this.main_account.user_key == this.sub_account.user_key){
        Swal.fire({
          icon: "warning",
          title: "Error",
          text: "ユーザーidが一致しています.どちらか変更してください",
          showConfirmButton: false,
          showCloseButton: false,
          timer: 1000,
        });
        return false;
      } else {
        return true;
      }
    },
    //ok
    checkPassword(pass1, pass2) {
      if (pass1 == pass2) {
        return true;
      } else {
        Swal.fire({
          icon: "warning",
          title: "Error",
          text: "パスワードが一致しません.もう一度入力してください",
          showConfirmButton: false,
          showCloseButton: false,
          timer: 1000,
        });
        this.loading = false;
        this.main_account.password = ""
        this.sub_account.password =""
        this.check_password = ""
        return false;
      }
    },
    //ok 予期せぬメールアドレスを使用する学生がいるかも..
    getStudentNumber(saga_email_address) {
      const student_number = saga_email_address.replace(/[^0-9]/g, '');
      console.log('学籍番号抽出確認',student_number);
      return student_number;
    },
    //ok 偶数番号がtrue
    groupingAccount(student_number) {
      if(student_number % 2 == 0) {
        return true;
      } else {
        return false;
      }
    },

    //ethアカウント作成  処理に5秒程度時間がかかる
    async createEthAccount(password) {
      let ether_address = "";
      await web3.eth.personal.newAccount(password).then(
        (data) => {
          console.log("etherアカウント作成ok", data);
          ether_address = data;
        },
        (err) => {
          console.log("error", err);
        }
      );
      return ether_address
    },
    //100eth受け取る ok
    async initialEth(received_address, value) {
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
          console.log("受け取り完了");
        });
    },
    //mainとsubを作成する(2回呼び出される) ok
    async createAccount(account,point){
      //初期のpointを与える
      const student_num = this.getStudentNumber(this.main_account.user_email);
      account.user_group = this.groupingAccount(student_num);
      account.user_eth_password = account.password;
      account.user_wallet = point;
      account.user_point = point;
      console.log("createAccount:",account)
      await axios
        .post("/api/create-user/", account)
        .then(() => {
          console.log("アカウント作成");
        })
        .catch(() => {
          Swal.fire({
            icon: "warning",
            title: "Error",
            text: "入力が正しくありません",
            showConfirmButton: false,
            showCloseButton: false,
            timer: 3000,
          });
        });
    },
    async log() {
      //this.initialEth("0xAba3feF8D1E8F837ee8134BF951AACD6cc100cf9",100);
      //this.checkEth("0xAba3feF8D1E8F837ee8134BF951AACD6cc100cf9")
      this.checkUserId();
      
    },

    //メモ用関数
    //共通処理 送る関数 ok
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