<template>
    <v-app>
        <Header />
        <v-main>
            <NavHelpBar />
            <v-container grid-list-md>
                <v-card>
                    <v-card-title>MyPage</v-card-title>
                    <v-card-text>
                        ユーザー名: {{ user_info.user_name }}
                    </v-card-text>
                    <v-card-text>
                        所持: {{ user_info.user_wallet }} (ETH or Point)
                    </v-card-text>
                    <v-card-text>
                        メールアドレス: {{ user_info.user_email }}
                    </v-card-text>
                </v-card>
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

export default {
    components: {
        Header, NavHelpBar,
    },
    data: () => ({
        uid: "",
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
            axios
                .get("/api/users/" + user_id)
                .then((res) => {
                    this.user_info = res.data;
                })
                .catch((e) => {
                    console.log(e);
                });
        }
    },
}
</script>