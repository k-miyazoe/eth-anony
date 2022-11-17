<template>
  <v-app>
    <Header />
    <!-- <v-btn color="primary" @click="log">
      log button
    </v-btn> -->
    <!-- <v-text>ユーザーIDとパスワードは重要なのでメモをお願いします</v-text>
    <v-text>実名アカウントとは違うユーザーID,パスワードを登録してください</v-text> -->
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
                  <v-text-field v-model="main_account.user_key" label="ユーザーID*(半角英数)" :rules="rules.user_key"
                    required />
                  <v-text-field type="password" v-model="main_account.password" :counter="10" label="パスワード*(半角英数)"
                    :rules="rules.password" maxlength="10" required />
                  <!--確認用passoword-->
                  <v-text-field type="password" v-model="check_password_main" :counter="10" label="パスワード(確認用)*"
                    :rules="rules.password" maxlength="10" required />
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
            <v-card-subtitle>*実名アカウントとは違うユーザーID,パスワードを登録してください</v-card-subtitle>
            <v-spacer />
            <v-card-text>
              <v-layout row fill-height justify-center align-center v-if="loading">
                <v-progress-circular :size="50" color="primary" indeterminate />
              </v-layout>

              <v-form v-else ref="form" v-model="valid" lazy-validation>
                <v-container>
                  <v-text-field v-model="sub_account.user_key" label="ユーザーID*(半角英数)" :rules="rules.user_key" required />
                  <v-text-field type="password" v-model="sub_account.password" :counter="10" label="パスワード*(半角英数)"
                    :rules="rules.password" maxlength="10" required />
                  <!--確認用passoword-->
                  <v-text-field type="password" v-model="check_password_sub" :counter="10" label="パスワード(確認用)*"
                    :rules="rules.password" maxlength="10" required />
                  <v-text-field v-model="sub_account.email" label="学籍番号メールアドレス(任意)" />
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
let g_main_eth_address = "";
let g_sub_eth_address = "";

export default {
  components: {
    Header,
  },
  data: () => ({
    main_account: {},
    sub_account: {
      user_name: "匿名"
    },
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
          (v && v.length > 5) || "パスワードは6文字以上でなければなりません",
      ],
      user_name: [
        (v) => !!v || "名前は必須です",
      ],
    },
  }),
  mounted() {
    this.checkToken();
    this.checkGeth();
  },
  methods: {
    checkToken() {
      this.$session.start();
      if (this.$session.has("token")) {
        router.push("/");
      }
    },
    //gethが動いてないとアカウント作成できないようにする ok
    checkGeth() {
      web3.eth.personal.getAccounts().then(
        (data) => {
          console.log("geth 起動中");
        },
        (err) => {
          console.log("geth 停止中", err);
          this.valid = false;
        }
      );
    },
    //イベント処理
    async signUp() {
      this.loading = true;
      let flag = true;
      flag = this.checkForm();
      flag = this.checkUserId(flag);
      //正しいpasswordの入力か確認
      flag = this.checkPassword(this.main_account.password, this.check_password_main, flag);
      flag = this.checkPassword(this.sub_account.password, this.check_password_sub, flag);
      //mainとsubのパスワードが一致してないか確認する関数
      flag = this.checkMainSubPassword(this.main_account.password, this.sub_account.password);
      await this.createEthAccount(this.main_account.password, flag, "main");
      await this.createEthAccount(this.sub_account.password, flag, "sub");
      flag = this.checkEthAddressType(g_main_eth_address, g_sub_eth_address);
      console.log('check eth address typeのflag確認', flag)

      await this.createAccount(this.main_account, 100, flag, g_main_eth_address);
      //flagがundefinedになる　-> subが作成されなくなる
      console.log("5 createAccount main", flag);
      await this.createAccount(this.sub_account, 0, flag, g_sub_eth_address);
      console.log("6 createAccount sub", flag);
      await this.initialEth(g_main_eth_address, 100, flag);
      console.log("7 initialEth", flag);
      this.loading = false;
      this.signUpResult(flag);
    },
    //改めて動作テストの必要あり
    checkForm() {
      return this.$refs.form.validate();
    },
    //実名と匿名のuserkeyの確認 うまく行ってない 
    checkUserId(flag) {
      if (flag) {
        if (this.main_account.user_key == this.sub_account.user_key) {
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
      } else {
        console.log('userkey checkなし')
        return false;
      }

    },
    //ok
    checkPassword(pass1, pass2, flag) {
      if (!flag) {
        console.log('パスワードチェックなし')
        return false;
      }
      else if (pass1 == pass2) {
        return true;
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
        this.main_account.password = ""
        this.sub_account.password = ""
        this.check_password = ""
        return false;
      }
    },
    //mainとsubのパスワードが一致してないか確認 ok
    checkMainSubPassword(main_pass, sub_pass) {
      if (main_pass == sub_pass) {
        Swal.fire({
          icon: "warning",
          title: "Error",
          text: "実名アカウントもしくは匿名アカウントどちらかのパスワードを変更してください",
          showConfirmButton: false,
          showCloseButton: false,
          timer: 3000,
        });
        return false
      } else {
        console.log('mainとsubパスワード重複なし')
        return true;
      }
    },
    //ethアカウント作成  処理に5秒程度時間がかかる ok
    async createEthAccount(password, flag, account_type) {
      if (!flag) {
        console.log('ethアカウント生成しない')
        return false;
      }
      await web3.eth.personal.newAccount(password).then(
        (data) => {
          if (account_type == "main") {
            console.log("ethアカウント作成ok[main]", data, "ethアドレスの型", typeof (data));
            g_main_eth_address = data;
          } else {
            console.log("ethアカウント作成ok[sub]", data, "ethアドレスの型", typeof (data));
            g_sub_eth_address = data;
          }
          return true;
        },
        (err) => {
          console.log("error", err);
          return false;
        }
      );
    },
    //ethのアドレスの型を確認 正しくない場合アカウントを作成しない　ok
    checkEthAddressType(main_eth_address, sub_eth_address) {
      if (typeof (main_eth_address) == "string" && typeof (sub_eth_address) == "string") {
        return true;
      } else {
        return false;
      }
    },
    //ok 予期せぬメールアドレスを使用する学生がいるかも..
    getStudentNumber(saga_email_address) {
      const student_number = saga_email_address.replace(/[^0-9]/g, '');
      console.log('学籍番号抽出確認', student_number);
      return student_number;
    },
    //ok 偶数番号がtrue
    groupingAccount(student_number) {
      if (student_number % 2 == 0) {
        return true;
      } else {
        return false;
      }
    },
    //mainとsubを作成する(2回呼び出される)
    async createAccount(account, point, flag, eth_address) {
      if (!flag) {
        console.log('アカウント生成しない')
        Swal.fire({
          icon: "warning",
          title: "Error",
          text: "アカウントが作成できませんでした",
          showConfirmButton: false,
          showCloseButton: false,
          timer: 3000,
        });
        return false;
      }
      //初期のpointを与える
      const student_num = this.getStudentNumber(this.main_account.user_email);
      account.user_group = this.groupingAccount(student_num);
      console.log('アカウントグループ',account.user_group)
      account.user_eth_password = account.password;
      account.user_point = point;
      account.user_eth_address = eth_address;
      console.log("createAccount:", account)
      await axios
        .post("/api/create-user/", account)
        .then(() => {
          console.log("アカウント作成");
          //ここが問題あり booleanを返せてない return flagでもだめ
          return true;
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
          return false;
        });
    },
    //100eth受け取る
    async initialEth(received_address, value, flag) {
      if (!flag) {
        console.log('初期eth与えない')
        return false;
      }
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
    //アカウント作成の結果を表示 ok
    signUpResult(result) {
      if (result) {
        Swal.fire("アカウントを作成しました!", "success");
        router.push('/signin');
      } else {
        Swal.fire({
          icon: "warning",
          title: "Error",
          text: "アカウントの作成ができませんでした!ページを閉じて再度やり直してください",
          showConfirmButton: false,
          showCloseButton: false,
          timer: 3000,
        });
        this.loading = false;
      }
    },
    async log() {
    },
  },
};
</script>