<template>
    <v-app>
        <Header />
        <!-- <v-btn color="primary" @click="log">
            log button
        </v-btn> -->
        <v-main>
            <NavHelpBar />
            <v-container grid-list-md>
                <v-card>
                    <v-card-title>MyPage</v-card-title>
                    <v-card-text>
                        ユーザー名: {{ user_info.user_name }}
                    </v-card-text>
                    <v-card-text>
                        <!--変更する-->
                        所持: {{ user_has_eth }} point
                        *所持ポイントの反映には時差がある時があります
                    </v-card-text>
                    <v-card-text>
                        メールアドレス: {{ user_info.user_email }}
                    </v-card-text>
                </v-card>
            </v-container>
            <v-container grid-list-md>
                <v-layout row wrap align-center justify-center fill-height>
                    <v-flex xs12 sm8 lg4 md5>
                        <v-card>
                            <v-card-title>
                                <span class="headline">仮想通貨を送る</span>
                            </v-card-title>
                            <v-form ref="form" v-model="valid" lazy-validation>
                                <v-text-field v-model="forward_address" :counter="10" :rules="rules.address"
                                    label="送り先のユーザーID" required></v-text-field>
                                <v-text-field v-model.number="send_eth" :rules="rules.eth" label="ETH" required>
                                </v-text-field>
                                <v-text-field v-model="my_eth_password" :rules="rules.password" label="現在サインインしているパスワード"
                                    required></v-text-field>
                                <v-btn :disabled="!valid" color="success" class="mr-4" @click="moveEth()">
                                    送金
                                </v-btn>
                            </v-form>
                        </v-card>
                    </v-flex>
                </v-layout>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import router from "../router";
import Swal from "sweetalert2";
import Header from "../components/Header.vue";
import NavHelpBar from "../components/NavigationHelpBar.vue"
import header from "/src/node/axios";

const axios = header.setHeader();
const Web3 = require("web3");
const web3 = new Web3(process.env.VUE_APP_GETH_API);
let user_id = "";
let user_eth_address = "";

export default {
    components: {
        Header, NavHelpBar,
    },
    data: () => ({
        valid: true,
        user_id: null,
        user_info: {},
        user_has_eth: 0,
        //受け取る側のethアドレス
        forward_address: "",
        send_eth: 10,
        my_eth_password: "",
        rules: {
            address: [
                (v) => !!v || "送り先は必須です",
            ],
            eth: [
                (v) => !!v || "必須です",
                (v) => /^[0-9]+$/.test(v) || "数値のみ",
                //送れる上限表示をここで行いたい
                // (v) => v < user_has_eth || "上限を超えています",
            ],
            password: [
                (v) => !!v || "パスワードは必須です",
            ]
        }
    }),
    mounted() {
        this.checkToken();
        this.getUserInfo();
        this.checkGeth();
        this.getHasEthAndBackup();
    },
    methods: {
        checkToken() {
            if (!this.$session.has("token")) {
                router.push("/signin");
            }
            user_id = this.$session.get('user_id')
            user_eth_address = this.$session.get('user_eth_address');
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
        //user情報取得
        getUserInfo() {
            const user_id = this.$session.get('user_id')
            axios
                .get("/api/users/" + user_id)
                .then((res) => {
                    this.user_info = res.data;
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        //所持ethを取得　+ バックアップ
        async getHasEthAndBackup() {
            await web3.eth.getBalance(user_eth_address)
                .then((ether) => {
                    //eth所持量を一時保存して,ethを移動する際に比較する変数
                    this.user_has_eth = ether;
                    //バックアップ
                    this.saveEthDataToDB(ether);
                    console.log('バックアップ成功')
                })
                .catch(() => {
                    console.log('eth情報の取得に失敗')
                })

        },
        //eth情報をdbへ更新
        async saveEthDataToDB(has_eth) {
            const user_point_data = {
                "user_point": has_eth,
            }
            axios
                .put("/api/users/" + user_id, user_point_data)
                .then(() => {
                    console.log('所持ethをdbへバックアップ');
                })
                .catch(() => {
                    console.log("バックアップに失敗しました");
                });
        },

        //イベント処理
        //送り先のethアドレスを取得し,ethを移動する
        async getReceiveAddressAndSendEth(forward_user_id) {
            axios
                .get("/api/user-eth-address/" + forward_user_id)
                .then((res) => {
                    //1 受け取り先のethアドレスを取得
                    let forward_address = res.data;
                    //2 ethの移動
                    this.sendEth(user_eth_address, forward_address, this.send_eth, this.my_eth_password);
                })
                .catch((e) => {
                    console.log(e);
                    Swal.fire({
                        icon: "warning",
                        title: "Error",
                        text: "送り先が見つかりませんでした!",
                        showConfirmButton: false,
                        showCloseButton: false,
                        timer: 3000,
                    });
                });
        },
        //送る上限設定 瞬間ごとの判定なる
        limitSetting() {
            return (this.user_has_eth >= this.send_eth)
        },
        async sendEth(from_eth_address, to_eth_address, value, from_eth_pass) {
            const from = await web3.utils.toChecksumAddress(from_eth_address);
            const to = await web3.utils.toChecksumAddress(to_eth_address);
            const transaction = {
                from: from,
                to: to,
                value: value,
                gasPrice: 0,
            };
            await web3.eth.personal
                .unlockAccount(from, from_eth_pass, 15000)
                .then(() => {
                    web3.eth.sendTransaction(transaction);
                    Swal.fire("仮想通貨が送金できました", "success");
                    //フォームを空にする
                    this.forward_address = ""
                    this.my_eth_password = ""
                })
                .catch((e) => {
                    console.log(e);
                    Swal.fire({
                        icon: "warning",
                        title: "Error",
                        text: "仮想通貨は送れませんでした",
                        showConfirmButton: false,
                        showCloseButton: false,
                        timer: 3000,
                    });
                    return
                });
        },
        //個人のethの移動
        async moveEth() {
            let flag = this.limitSetting();
            //送金できる場合
            if (flag && this.forward_address && this.my_eth_password) {
                //送り先のethアドレスを取得 + ethを移動
                await this.getReceiveAddressAndSendEth(this.forward_address);
                //手持ちのeth情報更新 + dbへバックアップ
                this.getHasEthAndBackup();
            }
            //送金できない場合
            else {
                Swal.fire({
                    icon: "warning",
                    title: "Error",
                    text: "送れる上限を超えています",
                    showConfirmButton: false,
                    showCloseButton: false,
                    timer: 3000,
                });
                return
            }
        },
        async log() {
        }
    },
}
</script>