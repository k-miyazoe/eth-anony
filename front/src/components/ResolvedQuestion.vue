<template>
    <v-app>
        <Header />
        <v-main>
            <v-spacer />
            <v-container fluid>
                <v-row class="justify-center">
                    <p>解決済みの質問一覧</p>
                </v-row>
                <v-card v-for="item in resolved_questions" :key="item.id" class="pa-md-4 mx-lg-auto" width="750px">
                    <v-card-text>
                        <router-link :to="{ name: 'resolved-question-detail', params: { id: item.id } }">
                            {{ item.question_title }}
                        </router-link>
                    </v-card-text>
                    <v-card-text>
                        回答数:{{ item.question_number_of_responses }}
                        閲覧数:{{ item.question_views }}
                    </v-card-text>
                </v-card>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import router from "../router";
import Header from "../components/Header.vue";
import SubTitle from "../components/SubTitle.vue";
import header from "/src/node/axios";
const axios = header.setHeader();

export default {
    components: {
        Header,
        SubTitle,
    },
    data() {
        return {
            resolved_questions: {},
            items: [],
        }
    },
    mounted() {
        this.checkToken();
        this.getResolvedQuestion();
    },
    methods: {
        checkToken() {
            if (!this.$session.has("token")) {
                router.push("/signin");
            }
        },
        //ok
        getResolvedQuestion() {
            axios
                .get("/api/get-question/resolved/everyone")
                .then((res) => {
                    console.log(res.data);
                    this.resolved_questions = res.data
                })

                .catch((e) => {
                    console.log(e);
                });
        },
    },
}
</script>