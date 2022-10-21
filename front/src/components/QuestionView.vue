<template>
    <v-app>
        <Header />
        <v-main>
            <NavHelpBar />
            <v-container fluid>
                <v-btn color="primary" @click="log">
                    log button
                </v-btn>
                <!--質問詳細-->
                <!--解決済み-->
                <div v-if="one_quesiton.question_status">
                    <v-card class="mx-auto" max-height="344">
                        <v-col class="mb-10">
                            <!--質問タイトル-->
                            <v-card-title class="resolved_question_text">質問 {{ one_quesiton.question_title }} 解決済み!
                                <v-card-subtitle>質問者:{{ one_quesiton.question_user_name }}</v-card-subtitle>
                            </v-card-title>
                            <!--質問内容-->
                            <v-card>
                                <v-card-subtitle>内容</v-card-subtitle>
                                <v-card-text>{{ one_quesiton.question_content }}</v-card-text>
                            </v-card>
                            <!--ソースコード-->
                            <v-card>
                                <v-card-subtitle>ソースコード</v-card-subtitle>
                                <v-card-text>{{ one_quesiton.question_source_code }}</v-card-text>
                            </v-card>

                            <v-card-actions>
                                <!--高評価-->
                                <v-btn color="orange" text @click="likeQuestion">
                                    <v-icon>mdi-thumb-up</v-icon>
                                    {{ one_quesiton.question_value }}
                                </v-btn>
                                <!--解決を解除-->
                                <!-- <v-btn color="green" text @click="releaseResolvedQuestion">
                                    解決取り消し
                                </v-btn> -->
                            </v-card-actions>
                        </v-col>
                    </v-card>
                </div>
                <!--未解決-->
                <div v-else>
                    <v-card class="mx-auto" max-height="344">
                        <v-col class="mb-10">
                            <!--質問タイトル-->
                            <v-card-title>質問 {{ one_quesiton.question_title }}
                                <v-card-subtitle>質問者:{{ one_quesiton.question_user_name }}</v-card-subtitle>
                            </v-card-title>
                            <!--質問内容-->
                            <v-card>
                                <v-card-subtitle>内容</v-card-subtitle>
                                <v-card-text>{{ one_quesiton.question_content }}</v-card-text>
                            </v-card>
                            <!--ソースコード-->
                            <v-card>
                                <v-card-subtitle>ソースコード</v-card-subtitle>
                                <v-card-text>{{ one_quesiton.question_source_code }}</v-card-text>
                            </v-card>

                            <v-card-actions>
                                <!--高評価-->
                                <v-btn color="green" text @click="likeQuestion">
                                    <v-icon>mdi-thumb-up</v-icon>
                                    {{ one_quesiton.question_value }}
                                </v-btn>
                                <!--低評価-->
                                <v-btn color="orange" text @click="BadQuestion">
                                    <v-icon>mdi-thumb-down</v-icon>
                                    <!-- {{ one_quesiton.question_bad_value }} -->
                                </v-btn>
                                <!--解決-->
                                <v-btn color="green" text @click="resolvedQuestion" :disabled="!valid">
                                    解決
                                </v-btn>
                            </v-card-actions>
                        </v-col>
                    </v-card>
                </div>
                <v-divider></v-divider>

                <!--回答一覧-->
                <v-card v-for="(item, index) in any_answer" :key="index">
                    <!--ベストアンサーの回答-->
                    <div v-if="item.answer_best">
                        <v-card-title class="best_answer_text">回答 {{ index + 1 }} ベストアンサー
                            <v-icon>mdi-chess-king</v-icon>
                        </v-card-title>
                        <v-card-subtitle>回答者:{{ item.answer_user_name }}</v-card-subtitle>
                        <v-card-text>{{ item.answer_content }}</v-card-text>
                        <v-card-text>{{ item.answer_source_code }}</v-card-text>
                        <v-card-actions>
                            <!--高評価-->
                            <v-btn color="green" text @click="likeAnswer(index)">
                                <v-icon>mdi-thumb-up</v-icon>
                                {{ item.answer_value }}
                            </v-btn>
                            <!--低評価-->
                            <v-btn color="orange" text @click="BadAnswer(index)">
                                <v-icon>mdi-thumb-down</v-icon>
                                <!-- {{ item.answer_bad_value }} -->
                            </v-btn>
                        </v-card-actions>
                    </div>
                    <!--ベストアンサーではない回答-->
                    <div v-else>
                        <v-card-title>回答 {{ index + 1 }}</v-card-title>
                        <v-card-subtitle>回答者:{{ item.answer_user_name }}</v-card-subtitle>
                        <v-card-text>{{ item.answer_content }}</v-card-text>
                        <v-card-text>{{ item.answer_source_code }}</v-card-text>
                        <v-card-actions>
                            <!--高評価-->
                            <v-btn color="green" text @click="likeAnswer(index)">
                                <v-icon>mdi-thumb-up</v-icon>
                                {{ item.answer_value }}
                            </v-btn>
                            <!--低評価-->
                            <v-btn color="orange" text @click="BadAnswer(index)">
                                <v-icon>mdi-thumb-down</v-icon>
                                <!-- {{ item.answer_bad_value }} -->
                            </v-btn>
                        </v-card-actions>
                    </div>
                </v-card>
                <!--回答フォーム-->
                <v-card class="mt-10">
                    <v-card-title>
                        回答フォーム
                    </v-card-title>
                    <v-form ref="form" v-model="valid" lazy-validation>
                        <v-textarea v-model="answer_obj.answer_content" label="解決策・提案*" :rules="rules.answer_content"
                            clearable clear-icon="mdi-close-circle" auto-grow outlined>
                        </v-textarea>
                        <v-textarea v-model="answer_obj.answer_source_code" label="ソースコード" clearable
                            clear-icon="mdi-close-circle" auto-grow outlined>
                        </v-textarea>
                    </v-form>
                    <!--回答送信ボタン-->
                    <v-dialog v-model="dialog" width="500">
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn color="success" v-bind="attrs" v-on="on" :disabled="!valid">
                                回答する
                            </v-btn>
                        </template>

                        <v-card>
                            <v-card-title>
                                回答について
                            </v-card-title>
                            <v-card-text>
                                回答は削除できません．あとから編集することは可能です．
                                質問者が理解できる回答になっていますか？
                            </v-card-text>
                            <v-form>
                                <v-text-field type="password" v-model="eth_password" :counter="10" label="パスワード"
                                    :rules="rules.password" maxlength="10" required />
                            </v-form>
                            <v-divider></v-divider>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="primary" @click="postAnswer">
                                    回答を送信する
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>

                </v-card>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import router from "../router";
import Swal from "sweetalert2";
import Header from "../components/Header.vue";
import NavHelpBar from "../components/NavigationHelpBar.vue";
import header from "/src/node/axios";
import { User, Question, Answer } from "/src/node/class";
import { thisExpression } from "@babel/types";

const axios = header.setHeader();
let user_id = 0;
let user_name = "";
let question_id = 0;
let user_eth_address = "";
let user_group = "";
//おそらくこのbest_answerは意味を成してないかも
let best_answer = false;
let UserClass = null;
const QuestionClass = new Question(axios);
const AnswerClass = new Answer(axios);
const Web3 = require("web3");
const web3 = new Web3(process.env.VUE_APP_GETH_API);
const miner = process.env.VUE_APP_MINER;
const miner_password = process.env.VUE_APP_MINER_PASS;
let g_answer_flag = true;

export default {
    components: {
        Header,
        NavHelpBar,
    },
    data() {
        return {
            one_quesiton: {},
            any_answer: [],
            answer_obj: {
                "user": this.$session.get('user_id'),
                "answer_user_name": this.$session.get("user_name"),
            },
            eth_password: "",
            dialog: false,
            valid: false,//trueが規定値
            loading: false,
            rules: {
                answer_content: [
                    (v) => !!v || "回答内容は必須です",
                ],
                password: [
                    (v) => !!v || "パスワードを入力してください",
                ],
            },
        };
    },
    async mounted() {
        await this.checkToken()
        await this.checkGeth()
        await this.getOneQuestion()
        await this.getAnyAnswer()
        await this.addViewsQuestion()
        await this.checkHasBestAnswer()
    },
    methods: {
        checkToken() {
            if (!this.$session.has("token")) {
                router.push("/signin");
            }
            user_id = this.$session.get('user_id');
            user_name = this.$session.get('user_name');
            user_eth_address = this.$session.get('user_eth_address');
            user_group = this.$session.get('user_group');
            UserClass = new User(user_id, axios);
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
        //質問取得
        getOneQuestion() {
            question_id = Number(this.$route.params.id)
            axios
                .get("/api/get-question/" + question_id)
                .then((res) => {
                    this.one_quesiton = res.data;
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        //回答高評価との依存関係
        getAnyAnswer() {
            axios
                .get("/api/get-answer/" + question_id)
                .then((res) => {
                    this.any_answer = res.data;
                })
                .catch((e) => {
                    console.log(e);
                });
            console.log('回答取得')
        },
        //閲覧数増加 ok
        addViewsQuestion() {
            axios
                .put("/api/add-views-question/" + question_id + "/")
                .then(() => {
                    console.log('閲覧数追加')
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        //以下 イベント処理

        //回答送信 サクセスダイヤログを後で追加
        async postAnswer() {
            this.loading = true
            this.answerInit();
            //ethがあるか確認
            this.getHasEth(user_eth_address, 1);
            //ethの消費
            await this.ethDown(user_eth_address, 1, this.eth_password, g_answer_flag);
            console.log('ethの消費', g_answer_flag)
            //回答する
            await AnswerClass.postAnswer(this.answer_obj, g_answer_flag);
            console.log('回答投稿', g_answer_flag)
            this.pointDown(user_id, g_answer_flag);
            await QuestionClass.addNumberOfAnswers(question_id, g_answer_flag);
            console.log('回答数増加', g_answer_flag);
            // this.sendEmailQuestioner(this.answer_obj.answer_content, g_answer_flag);
            // console.log('メール通知', g_answer_flag);
            //画面更新
            this.getAnyAnswer();
            this.dialog = false
            this.answer_obj = {}
            this.loading = false
        },
        answerInit() {
            this.answer_obj["question_id"] = question_id;
            //ethアドレス追加
            this.answer_obj["answer_eth_address"] = user_eth_address;
        },
        //回答処理の中の関数
        async getHasEth(address, check_ether) {
            await web3.eth.getBalance(address)
                .then((has_ether) => {
                    console.log('所持eth', has_ether)
                    g_answer_flag = (has_ether - check_ether > 0)
                })
        },
        async ethDown(answer_user_eth_address, eth, answer_user_eth_password, flag) {
            if (flag) {
                const from = await web3.utils.toChecksumAddress(answer_user_eth_address);
                const to = await web3.utils.toChecksumAddress(miner);
                const transaction = {
                    from: from,
                    to: to,
                    value: eth,
                    gasPrice: 0,
                };
                await web3.eth.personal
                    .unlockAccount(from, answer_user_eth_password, 15000)
                    .then(() => {
                        web3.eth.sendTransaction(transaction);
                        console.log("回答によるethの消費");
                    })
                    .catch(() => {
                        Swal.fire({
                            icon: "warning",
                            title: "Error",
                            text: "パスワードが正しくない可能性があります",
                            showConfirmButton: false,
                            showCloseButton: false,
                            timer: 3000,
                        });
                        g_answer_flag = false;
                    });
            }
        },
        //回答の際point消費
        pointDown(answer_user_id, flag) {
            if (flag) {
                axios
                    .put("/api/point-down/" + answer_user_id + "/")
                    .then(() => {
                        console.log("point down");
                    })
                    .catch((e) => {
                        console.log(e);
                    });
            }
        },
        //質問者に対して、回答通知メールを送る
        sendEmailQuestioner(answer_content, flag) {
            // if (flag) {
            //     let _mail_obj = {
            //         subject: "質問に回答がありました",
            //         message: "[返信不可]" + answer_content,
            //         receipt_user_id: this.one_quesiton.user,
            //     }
            //     axios
            //         .post("/api/send-email/", _mail_obj)
            //         .then((res) => {
            //             console.log(res)
            //         })
            //         .catch((e) => {
            //             console.log(e)
            //         });
            // }
        },

        //いいね機能
        //質問のいいね機能 ok questionclass
        likeQuestion() {
            const question_like = {
                user: user_id,
                question_id: this.one_quesiton.id,
            }
            axios
                .put("/api/question-like/", question_like)
                .then(() => {
                    console.log('評価が変更されました')
                    this.getOneQuestion()
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        //回答のいいね機能 ok answerclass
        likeAnswer(answer_index) {
            //回答の評価値を1上げる 回答した人のetheridが必要
            let answer_like_obj = {
                user: user_id,
                answer_id: this.any_answer[answer_index].id
            }
            axios
                .post("/api/answer-like/", answer_like_obj)
                .then((res) => {
                    console.log(res);
                    console.log('評価が変更されました')
                    this.getAnyAnswer()
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        //bad機能追加
        BadQuestion() {
            const question_bad = {
                user: user_id,
                question_id: this.one_quesiton.id,
            }
            axios
                .put("/api/question-bad/", question_bad)
                .then(() => {
                    console.log('評価が変更されました')
                    this.getOneQuestion()
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        BadAnswer(answer_index) {
            let answer_bad = {
                user: user_id,
                answer_id: this.any_answer[answer_index].id
            }
            axios
                .post("/api/answer-bad/", answer_bad)
                .then((res) => {
                    console.log(res);
                    console.log('評価が変更されました')
                    this.getAnyAnswer()
                })
                .catch((e) => {
                    console.log(e);
                });
        },

        //bestanswer機能
        //回答に評価がない場合評価をリクエスト[呼び出し回数?] 0
        checkAnswerValue(){
            let flag = false;
            for(let index in this.any_answer){
                if(this.any_answer[index].answer_value > 0){
                    flag = true;
                }
            }
            return flag;
        },
        //最高高評価の値を返す[呼び出し回数1]ok 1
        searchBestAnswer(answers) {
            let max_value = 0;
            for (let item in answers) {
                if (max_value < answers[item].answer_value) {
                    max_value = answers[item].answer_value;
                }
            }
            console.log(max_value)
            return max_value
        },
        //このページ内のanswer_bestを更新する[呼び出し回数1] 2
        autoBestAnswer() {
            const max_value = this.searchBestAnswer(this.any_answer);
            for (let best in this.any_answer) {
                //低評価5未満かつ高評価Max
                if (this.any_answer[best].answer_bad_value < 5 && this.any_answer[best].answer_value == max_value) {
                    //ベストアンサーの更新
                    this.any_answer[best].answer_best = true;
                }
            }
        },
       
        //解決機能
        //質問解決 questionclass ok 変更
        resolvedQuestion() {
            //質問者の場合
            if (user_id == this.one_quesiton.user) {
                //回答が存在する場合
                if (this.any_answer.length != 0) {
                    //回答に評価があるか確認
                    //todo ベストアンサーが複数人いる場合の処理の変更に注意
                    if (this.checkAnswerValue()) {
                        //自動ベストアンサー処理
                        this.searchBestAnswer(this.any_answer);
                        this.autoBestAnswer();
                        //解決処理
                        const resolve = {
                            user: this.one_quesiton.user,
                            question_status: true
                        }
                        axios
                            .put("/api/update-question/" + question_id + "/", resolve)
                            .then(() => {
                                this.rewardQuestionUser();
                                this.rewardAnswerUser();
                                Swal.fire(
                                    '質問が解決されました!',
                                    'success',
                                )
                                this.getOneQuestion();
                            })
                            .catch((e) => {
                                console.log(e);
                            });
                    }
                    else {
                        Swal.fire({
                            icon: "warning",
                            title: "Error",
                            text: "回答に評価がありません．回答を評価してください!",
                            showConfirmButton: false,
                            showCloseButton: false,
                            timer: 3000,
                        });
                    }
                }
                //回答がない場合
                else {
                    Swal.fire({
                        icon: "warning",
                        title: "Error",
                        text: "回答が存在しません.自己解決した場合、自身で回答を作成してください",
                        showConfirmButton: false,
                        showCloseButton: false,
                        timer: 3000,
                    });
                }
            }
            //質問者以外
            else {
                Swal.fire({
                    icon: "warning",
                    title: "Error",
                    text: "質問者のみ有効です！",
                    showConfirmButton: false,
                    showCloseButton: false,
                    timer: 3000,
                });
            }
        },
        //報酬の計算
        calculationOfRewardEth(object) {
            if (object.bad_num < 5) {
                let reward = 1;
                //質問高評価
                if (object.type == "question" && object.good_num > 4) {
                    reward = reward + 5;
                    console.log('質問高評価')
                }
                //無評価の質問
                else if (object.type == "question") {
                    console.log('無評価の質問')
                }
                //回答ベストアンサー
                else if (object.type == "answer" && object.best_ans) {
                    reward = reward + 6;
                    console.log('ベストアンサー')
                    //ベストアンサーかつ高評価
                    if (object.good_num > 4) {
                        reward = reward + 1;
                        console.log('ベストアンサーかつ高評価')
                    }
                }
                //回答高評価
                else if (object.type == "answer" && object.good_num > 4) {
                    //回答報酬 2eth + 高評価 1eth
                    reward = reward + 2;
                    console.log('回答高評価')
                }
                //無評価の回答
                else if (object.type = "answer") {
                    reward = reward + 1;
                    console.log('無評価の回答')
                }
                console.log("受け取り報酬:", reward)
                return reward;
            }
            //低評価多数 ethなし
            else {
                console.log("低評価多数 eth没収")
                return 0;
            }
        },
        //報酬を与える userclass?
        async rewardEth(received_address, reward_eth) {
            const from = await web3.utils.toChecksumAddress(miner);
            const to = await web3.utils.toChecksumAddress(received_address);
            const transaction = {
                from: from,
                to: to,
                value: reward_eth,
            };
            await web3.eth.personal
                .unlockAccount(from, miner_password, 15000)
                .then(() => {
                    web3.eth.sendTransaction(transaction);
                    console.log("受け取り完了");
                });
        },
        //質問したユーザーに対してpoint計算[予備システム]
        putSendPoint(reward_point) {
            let update_point = {
                "user_point": reward_point,
            }
            axios
                .put("/api/users/" + user_id, update_point)
                .then((res) => {
                    console.log(res);
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        //質問者へ報酬[質問者が解決を押したときの処理]
        async rewardQuestionUser() {
            let cal_question_obj = {
                "bad_num": this.one_quesiton.question_bad_value,
                "type": "question",
                "good_num": this.one_quesiton.question_value,
                "best_ans": false,
            }
            //報酬の計算
            const question_reward = this.calculationOfRewardEth(cal_question_obj);
            //報酬eth 解決を押せるuserは必然的に質問者
            await this.rewardEth(user_eth_address, question_reward);
            //予備のpoint[mypageでバックupあるが、mypageに頻繁に行くとは限らない]
            this.putSendPoint(question_reward);
            console.log("質問者への報酬完了")
        },
        //複数の回答者への報酬
        async rewardAnswerUser() {
            //this.any_answerを変更するかも
            for (let index in this.any_answer) {
                let item = this.any_answer[index];
                //報酬の計算
                let cal_answer_obj = {
                    "bad_num": item.answer_bad_value,
                    "type": "answer",
                    "good_num": item.answer_value,
                    "best_ans": item.answer_best,
                }
                const answer_reward = this.calculationOfRewardEth(cal_answer_obj);
                //報酬eth
                await this.rewardEth(item.answer_eth_address, answer_reward);
                //予備のpoint[mypageでバックupあるが、mypageに頻繁に行くとは限らない]
                this.putSendPoint(answer_reward);
            }
            console.log("回答者への報酬完了")
        },
        log() {
        },
    }
}
</script>
<style>
.best_answer_text {
    background-color: gold;
}

.resolved_question_text {
    background-color: aquamarine;
}

/* 例 */
.font_test {
    font-size: 20px;
    color: #2196F3;
}
</style>