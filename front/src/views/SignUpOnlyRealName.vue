<template>
    <v-app>
        <Header />
        <v-container grid-list-md>
            <NavHelpBar />
            <h1>TAまたは匿名アカウントから実名アカウントに送金できないかたのみ</h1>
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
                                    <v-text-field v-model="main_account.user_key" label="ユーザーID*(半角英数)"
                                        :rules="rules.user_key" required />
                                    <v-text-field type="password" v-model="main_account.password" :counter="10"
                                        label="パスワード*(半角英数)" :rules="rules.password" maxlength="10" required />
                                    <!--確認用passoword-->
                                    <v-text-field type="password" v-model="check_password_main" :counter="10"
                                        label="パスワード(確認用)*" :rules="rules.password" maxlength="10" required />
                                    <v-text-field v-model="main_account.user_email" label="学籍番号メールアドレス*"
                                        :rules="rules.email" required />

                                    <v-text-field v-model="main_account.user_name" label="氏名*" :rules="rules.user_name"
                                        required />
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
import NavHelpBar from "../components/NavigationHelpBar.vue"

const axios = header.setHeader();
const Web3 = require("web3");
const web3 = new Web3(process.env.VUE_APP_GETH_API);
const miner = process.env.VUE_APP_MINER;
const miner_password = process.env.VUE_APP_MINER_PASS;
let g_main_eth_address = 0;

export default {
    components: {
        Header,
        NavHelpBar,
    },
    data: () => ({
        main_account: {},
        check_password_main: "",
        valid: true,
        loading: false,
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
        checkGeth() {
            web3.eth.personal.getAccounts().then(
                () => {
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
            console.log("1 入力情報の確認:", flag);
            flag = this.checkPassword(this.main_account.password, this.check_password_main, flag);
            console.log("2 パスワードの間違えがないか確認:", flag);
            flag = this.checkSagaEmailAddress(this.main_account.user_email);
            console.log("3 メールアドレスの確認:", flag);
            await this.createEthAccount(this.main_account.password, flag);
            flag = this.checkEthAddressType(g_main_eth_address);
            console.log("4 ethアカウント:", flag);
            await this.createAccount(this.main_account, 100, flag, g_main_eth_address);
            console.log("5 アカウント:", flag);
            await this.initialEth(g_main_eth_address, 100, flag);
            console.log("6 eth受け取り:", flag);
            this.loading = false;
            this.signUpResult(flag);
        },
        checkForm() {
            if(!this.$refs.form.validate()){
                Swal.fire({
                    icon: "warning",
                    title: "Error",
                    text: "入力フォームを全て入力してください",
                    timer: 1000,
                });
                this.loading = false;
            }
            return this.$refs.form.validate();
        },
        checkPassword(pass1, pass2, flag) {
            if (!flag) {
                console.log('パスワードチェックなし')
                this.loading = false;
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
                this.check_password = ""
                return false;
            }
        },
        checkSagaEmailAddress(saga_email_address) {
            const student_number = saga_email_address.replace(/[^0-9]/g, '');
            if(student_number == "" || student_number.length < 8){
                Swal.fire({
                    icon: "warning",
                    title: "Error",
                    text: "学籍番号のメールアドレスを入力してください",
                    showConfirmButton: false,
                    showCloseButton: false,
                    timer: 1000,
                });
                this.main_account.user_email = ""
                this.loading = false;
                return false;
            } else{
                return true;
            }
        },
        async createEthAccount(password, flag) {
            if (!flag) {
                console.log('ethアカウント生成しない')
                this.loading = false;
                return false;
            }
            await web3.eth.personal.newAccount(password).then(
                (data) => {
                    console.log("ethアカウント作成完了", data);
                    g_main_eth_address = data;
                    return true;
                },
                (err) => {
                    console.log("アカウント作成error", err);
                    return false;
                }
            );
        },
        //正しくethアカウントが作成できているか確認
        checkEthAddressType(main_eth_address) {
            if (typeof (main_eth_address) == "string") {
                return true;
            } else {
                return false;
            }
        },
        getStudentNumber(saga_email_address) {
            const student_number = saga_email_address.replace(/[^0-9]/g, '');
            return student_number;
        },
        groupingAccount(student_number) {
            //*文字列でも剰余が可能
            if (student_number % 2 == 0) {
                return true;
            } else {
                return false;
            }
        },
        async createAccount(account, point, flag, eth_address) {
            if (!flag) {
                Swal.fire({
                    icon: "warning",
                    title: "Error",
                    text: "アカウントが作成できませんでした",
                    showConfirmButton: false,
                    showCloseButton: false,
                    timer: 3000,
                });
                this.loading = false;
                this.$refs.form.reset()
                return false;
            }
            const student_num = this.getStudentNumber(this.main_account.user_email);
            account.user_group = this.groupingAccount(student_num);
            console.log('アカウントグループ', account.user_group)
            account.user_eth_password = account.password;
            account.user_point = point;//pointはbackup用のデータ
            account.user_eth_address = eth_address;
            console.log("登録前のアカウント情報", account)
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
                    this.$refs.form.reset()
                    return false;
                });
        },
        async initialEth(received_address, value, flag) {
            if (!flag) {
                this.loading = false;
                console.log('初期のeth受け取り失敗')
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
                this.$refs.form.reset()
                this.loading = false;
            }
        },
        async log() {
        },
    },
};
</script>