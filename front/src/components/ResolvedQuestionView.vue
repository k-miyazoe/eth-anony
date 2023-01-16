<template>
    <v-app>
        <Header />
        <v-main>
            <NavHelpBar />
            <SubTitle />
            <v-container fluid>
                <!--解決済み-->
                <div v-if="one_quesiton.question_status">
                    <v-card class="mx-auto" max-height="344">
                        <v-col class="mb-10">
                            <!--質問タイトル-->
                            <v-card-title class="resolved_question_text">[解決済み!] {{ one_quesiton.question_title }}
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
                        </v-col>
                    </v-card>
                </div>
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
                    </div>
                    <!--ベストアンサーではない回答-->
                    <div v-else>
                        <v-card-title>回答 {{ index + 1 }}</v-card-title>
                        <v-card-subtitle>回答者:{{ item.answer_user_name }}</v-card-subtitle>
                        <v-card-text>{{ item.answer_content }}</v-card-text>
                        <v-card-text>{{ item.answer_source_code }}</v-card-text>
                    </div>
                </v-card>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import router from "../router";
import Header from "../components/Header.vue";
import NavHelpBar from "../components/NavigationHelpBar.vue";
import SubTitle from "../components/SubTitle.vue";
import header from "/src/node/axios";

const axios = header.setHeader();
let question_id = 0;

export default {
    components: {
        Header,
        NavHelpBar,
        SubTitle,
    },
    data() {
        return {
            one_quesiton: {},
            any_answer: [],
        };
    },
    async mounted() {
        await this.checkToken()
        await this.getOneQuestion()
        await this.getAnyAnswer()
    },
    methods: {
        checkToken() {
            if (!this.$session.has("token")) {
                router.push("/signin");
            }
        },
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
        getAnyAnswer() {
            axios
                .get("/api/get-answer/" + question_id)
                .then((res) => {
                    this.any_answer = res.data;
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        log() {
            this.autoBestAnswer()
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