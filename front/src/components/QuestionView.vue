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
                                <v-btn color="green" text @click="releaseResolvedQuestion">
                                    解決取り消し
                                </v-btn>
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
                                <v-btn color="orange" text @click="likeQuestion">
                                    <v-icon>mdi-thumb-up</v-icon>
                                    {{ one_quesiton.question_value }}
                                </v-btn>
                                <!--解決-->
                                <v-btn color="green" text @click="resolvedQuestion">
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
                            <!--いいねボタン-->
                            <v-btn color="orange" text @click="likeAnswer(index)">
                                <v-icon>mdi-thumb-up</v-icon>
                                {{ item.answer_value }}
                            </v-btn>
                            <!--ベストアンサ解除ー-->
                            <v-btn color="red" text @click="releaseBestAnswer(item)">
                                解除
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
                            <!--いいねボタン-->
                            <v-btn color="orange" text @click="likeAnswer(index)">
                                <v-icon>mdi-thumb-up</v-icon>
                                {{ item.answer_value }}
                            </v-btn>
                            <!--ベストアンサー-->
                            <v-btn color="red" text @click="bestAnswer(item)">
                                ベストアンサー
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
                            <v-btn dark v-bind="attrs" v-on="on" :disabled="!valid">
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

const api_url = process.env.VUE_APP_API_URL;
const axios = header.setHeader();
let now_user_id = 0;
let now_user_name = "";
let question_id = 0;
//おそらくこのbest_answerは意味を成してない
let best_answer = null;
let UserClass = null;
const QuestionClass = new Question(axios);
const AnswerClass = new Answer(axios);

export default {
    components: {
        Header,
        NavHelpBar,
    },
    data() {
        return {
            one_quesiton: {},
            any_answer: [],
            answer_obj: {},
            dialog: false,
            valid: true,
            loading: false,
            rules: {
                answer_content: [
                    (v) => !!v || "回答内容は必須です",
                ],
            },
        };
    },
    async mounted() {
        await this.checkToken()
        await this.getOneQuestion()
        await this.getAnyAnswer()
        //コメントアウトを後で外す
        //await this.addViewsQuestion()
        //await this.checkHasBestAnswer()
    },
    methods: {
        checkToken() {
            if (!this.$session.has("token")) {
                router.push("/signin");
            }
            now_user_id = this.$session.get('user_id');
            now_user_name = this.$session.get('user_name');
            UserClass = new User(now_user_id, axios);
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
        //booleanを返す
        checkHasBestAnswer() {
            for (let item of this.any_answer) {
                if (item.answer_best == true) {
                    console.log("ベストアンサーあり");
                    best_answer = true;
                }
            }
            return best_answer;
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

        //回答送信 回答が即時反映されない
        async postAnswer() {
            this.loading = true
            this.answer_obj["user"] = now_user_id
            this.answer_obj["answer_user_name"] = now_user_name;
            this.answer_obj["question_id"] = question_id;
            await AnswerClass.postAnswer(this.answer_obj);
            await UserClass.sendPoint(now_user_id);
            await QuestionClass.addNumberOfAnswers(question_id);
            this.sendEmailQuestioner(this.answer_obj.answer_content);
            this.getAnyAnswer();
            this.dialog = false
            this.answer_obj = {}
            this.loading = false
        },
        //質問したユーザーに対して，ポイントを送る[高評価を受けた場合] 未完成 questionclass
        putSendPoint() {
            axios
                .put("/api/users/" + now_user_id + "/", update_obj)
                .then((res) => {
                    console.log(res);
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        //質問のいいね機能 ok questionclass
        likeQuestion() {
            const question_like = {
                user: now_user_id,
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
        //質問解決 questionclass ok
        resolvedQuestion() {
            //質問者の場合
            if (now_user_id == this.one_quesiton.user) {
                //回答が存在する場合
                if (this.any_answer.length != 0) {
                    //ベストアンサーが存在しているなら
                    if (this.checkHasBestAnswer()) {
                        //解決処理
                        const resolve = {
                            user: this.one_quesiton.user,
                            question_status: true
                        }
                        axios
                            .put("/api/update-question/" + question_id + "/", resolve)
                            .then(() => {
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
                    //ベストアンサーが存在してない場合
                    else {
                        Swal.fire({
                            icon: "warning",
                            title: "Error",
                            text: "ベストアンサーが存在しません．ベストアンサーを選択してください!",
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
        //質問解決解除 questionclass ok
        releaseResolvedQuestion() {
            if (now_user_id == this.one_quesiton.user) {
                const release_resolve_obj = {
                    user: this.one_quesiton.user,
                    question_status: false
                }
                axios
                    .put("/api/update-question/" + question_id + "/", release_resolve_obj)
                    .then(() => {
                        Swal.fire(
                            '解決を取り消しました!',
                            'success',
                        )
                        this.getOneQuestion()
                    })
                    .catch((e) => {
                        console.log(e);
                    });
            }
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
        //回答のいいね機能 ok answerclass
        likeAnswer(answer_index) {
            //回答の評価値を1上げる 回答した人のetheridが必要
            let answer_like_obj = {
                user: now_user_id,
                answer_id: this.any_answer[answer_index].id
            }
            axios
                .post(api_url + "/api/answer-like/", answer_like_obj)
                .then((res) => {
                    console.log(res);
                    console.log('評価が変更されました')
                    this.getAnyAnswer()
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        //bestanswerの二つの処理は一つにできる
        //bestanswer処理　answerclass ok
        bestAnswer(answer) {
            //bestアンサーがすでに存在している場合 ここが動いてない
            if (this.checkHasBestAnswer()) {
                Swal.fire({
                    icon: "warning",
                    title: "Error",
                    text: "すでにベストアンサーは存在しています！",
                    showConfirmButton: false,
                    showCloseButton: false,
                    timer: 3000,
                });
            }
            //bestanswerがない場合
            else {
                //質問者のみベストアンサー決定可能
                if (now_user_id == this.one_quesiton.user) {
                    const answer_update_obj = {
                        user: this.one_quesiton.user,
                        question_id: question_id,
                        answer_best: true
                    }
                    axios
                        .put("/api/update-answer/" + answer.id + "/", answer_update_obj)
                        .then(() => {
                            best_answer = true;
                            Swal.fire(
                                'ベストアンサーを決定しました!',
                                'success',
                            )
                            //ページの更新
                            this.getAnyAnswer()
                        })
                        .catch((e) => {
                            console.log(e);
                        });
                }
                //質問者でないユーザーはできない
                else {
                    Swal.fire({
                        icon: "warning",
                        title: "Error",
                        text: "質問者のみベストアンサーを決めることができます",
                        showConfirmButton: false,
                        showCloseButton: false,
                        timer: 3000,
                    });
                }
            }
        },
        //bestanswer解除処理 answerclass ok
        releaseBestAnswer(answer) {
            if (now_user_id == this.one_quesiton.user && !this.one_quesiton.question_status) {
                const not_best_answer = {
                    user: this.one_quesiton.user,
                    question_id: question_id,
                    answer_best: false
                }
                axios
                    .put(api_url + "/api/update-answer/" + answer.id + "/", not_best_answer)
                    .then(() => {
                        best_answer = false;
                        Swal.fire(
                            'ベストアンサーを解除しました!',
                            'success',
                        )
                        //ページの更新
                        this.getAnyAnswer()
                    })
                    .catch((e) => {
                        console.log(e);
                    });
            }
            //質問者でないユーザーはできない
            else {
                Swal.fire({
                    icon: "warning",
                    title: "Error",
                    text: "質問者のみベストアンサーを解除できます.また解決済みの場合ベストアンサーは解除できません",
                    showConfirmButton: false,
                    showCloseButton: false,
                    timer: 3000,
                });
            }
        },
        //質問者に対して、回答通知メールを送る ok
        sendEmailQuestioner(answer_content) {
            let _subject = "質問に回答がありました"
            let _message = answer_content
            let _user_id = this.one_quesiton.user
            let _mail_obj = {
                subject: _subject,
                message: "[返信不可]" + _message,
                receipt_user_id: _user_id,
            }
            axios
                .post(api_url + "/api/send-email/", _mail_obj)
                .then((res) => {
                    console.log(res)
                })
                .catch((e) => {
                    console.log(e)
                });
        },
        //web3.js test func ok
        web3(){
            const Web3 = require("web3");
            const web3 = new Web3("http://localhost:9090");
            web3.eth.isMining().then(console.log);
        },
        log() {
            this.web3();
        }
    },
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