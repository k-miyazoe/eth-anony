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
                                <v-text-field v-model="my_eth_password" :rules="rules.password" label="Password"
                                    required></v-text-field>
                                <v-btn :disabled="!valid" color="success" class="mr-4" @click="sendEth()">
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
import Header from "../components/Header.vue";
import NavHelpBar from "../components/NavigationHelpBar.vue"
import header from "/src/node/axios";

const axios = header.setHeader();
const Web3 = require("web3");
const web3 = new Web3(process.env.VUE_APP_GETH_API);
let user_eth_address = "";
let g_send_flag = true;


export default {
    components: {
        Header, NavHelpBar,
    },
    data: () => ({
        valid: true,
        uid: "",
        user_id: null,
        user_info: {},
        user_has_eth: 0,
        forward_address: "",
        send_eth: 0,
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
        this.getHasEth();
        //後で消す
        //this.log();
    },
    methods: {
        checkToken() {
            this.$session.start();
            if (!this.$session.has("token")) {
                router.push("/signin");
            }
            user_eth_address = this.$session.get('user_eth_address');
        },
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
        //user情報取得
        getUserInfo() {
            const user_id = this.$session.get('user_id')
            axios
                .get("/api/users/" + user_id)
                .then((res) => {
                    this.user_info = res.data;
                    //console.log(this.user_info)
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        //所持ethを取得
        async getHasEth() {
            await web3.eth.getBalance(user_eth_address)
                .then((ether) => {
                    this.user_has_eth = ether;
                    console.log('所持eth', ether)
                })
        },
        //イベント処理
        async getReceiveAddress() {
            //送るアドレスを取得しないといけない
            //userIdからeth_addressを取得
        },
        //送る上限設定 瞬間ごとの判定なる
        limitSetting() {
            return (this.user_has_eth >= this.send_eth)
        },
        async sendEth() {
            //実名と匿名(個人のeth間での送り合い)
            g_send_flag = this.limitSetting();
            //received_addressを取得
            if (g_send_flag) {
                const from = await web3.utils.toChecksumAddress(user_eth_address);
                const to = await web3.utils.toChecksumAddress(received_address);
                const transaction = {
                    from: from,
                    to: to,
                    value: this.send_eth,
                    gasPrice: 0,
                };
                await web3.eth.personal
                    .unlockAccount(from, this.my_eth_password, 15000)
                    .then(() => {
                        web3.eth.sendTransaction(transaction);
                        console.log("仮想通貨送金完了");
                    });

            } else {
                Swal.fire({
                    icon: "warning",
                    title: "Error",
                    text: "送れる上限を超えています",
                    showConfirmButton: false,
                    showCloseButton: false,
                    timer: 3000,
                });
            }
        },
        log() {
        }
    },
}
</script>