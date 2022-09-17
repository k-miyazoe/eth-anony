<template>
    <v-app>
        <Header />
        <v-main>
            <NavHelpBar />
            <v-container grid-list-md>
                <v-card>
                    <v-card-title>MyPage</v-card-title>
                    <v-card-text>
                        ユーザー名: {{ user_info.username }}
                    </v-card-text>
                    <v-card-text>
                        所持通貨: {{ user_info.eth_stock }}
                    </v-card-text>
                    <v-card-text>
                        メールアドレス: {{ user_info.email }}
                    </v-card-text>
                </v-card>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import axios from "axios";
import router from "../router";
import Header from "../components/Header.vue";
import NavHelpBar from "../components/NavigationHelpBar.vue"

export default {
    components: {
        Header, NavHelpBar,
    },
    data: () => ({
        uid: "",
        axios: {},
        user_id: null,
        user_info: {},
    }),
    mounted() {
        this.checkToken();
        this.getUserInfo();
    },
    methods: {
        checkToken() {
            this.$session.start();
            if (!this.$session.has("token")) {
                router.push("/signin");
            }
        },
        //user情報取得
        getUserInfo() {
            const user_id = this.$session.get('user_id')
            //class使えそう
            axios
                .get(process.env.VUE_APP_API_URL + "/api/users/" + user_id)
                .then((res) => {
                    this.user_info = res.data
                })
                .catch((e) => {
                    console.log(e);
                });
        }
    },
}
</script>