<template>
    <v-app>
        <Header />
        <v-main>
            <NavHelpBar />
            <v-spacer />
            <v-container fluid>
                <v-card v-for="item in ranking_list" :key="item.id" class="pa-md-4 mx-lg-auto" width="750px">
                    <v-card-text>{{ item.user_ranking }}位 {{ item.user_email }}{{ item.user_name
                    }} {{ item.user_point }}point</v-card-text>
                </v-card>
            </v-container>
        </v-main>
    </v-app>

</template>

<script>
import Header from "../components/Header.vue";
import NavHelpBar from "../components/NavigationHelpBar.vue";
import header from "/src/node/axios";
const axios = header.setHeader();
let g_user_group = "";
let g_user_list = [];
let g_remove_anony_user_list = [];

export default {
    components: {
        Header,
        NavHelpBar,
    },
    data() {
        return {
            ranking_list: [],
        }
    },
    async mounted() {
        this.checkToken();
        await this.getUserList();
        this.removeAnonyAcount();
        const descending_order_ranklist = this.descendingOrderRanking();
        this.userSortRanking(descending_order_ranklist);
    },
    methods: {
        checkToken() {
            if (this.$session.has("token")) {
                const group_bool = this.$session.get("user_group");
                this.getGroup(group_bool);
            }
            else {
                router.push("/signin");
            }
        },
        getGroup(group_bool) {
            //偶数の実名グループ
            if (group_bool) {
                g_user_group = "real_name"
            }
            //奇数の匿名グループ
            else {
                g_user_group = "anonymous"
            }
        },
        async getUserList() {
            await axios
                .get("/api/get-user/" + g_user_group)
                .then((res) => {
                    g_user_list = res.data;
                })
                .catch((e) => {
                    console.log(e);
                });
        },
        removeAnonyAcount() {
            let remove_anony_account_list = [];
            for (let index in g_user_list) {
                if (g_user_list[index].user_name != "匿名" && g_user_list[index].user_name != "") {
                    remove_anony_account_list.push(g_user_list[index]);
                }
            }
            g_remove_anony_user_list = remove_anony_account_list
        },
        descendingOrderRanking() {
            let obj = g_remove_anony_user_list
            let descending_order = Object.keys(obj).map(function (key) {
                return obj[key];
            }).sort(function (a, b) {
                return (a.user_point > b.user_point) ? -1 : 1;
            });
            return descending_order
        },
        userSortRanking(user_ranking_list) {
            let ranking = 2
            let old_array = user_ranking_list
            let top_rank = {
                "user_email": old_array[0].user_email,
                "user_name": old_array[0].user_name,
                "user_point": old_array[0].user_point,
                "user_ranking": 1,
            }
            let new_array = []
            new_array.push(top_rank)
            for (let step = 1; step < old_array.length; step++) {
                if (old_array[step - 1].user_point == old_array[step].user_point) {
                    let same_rank = {
                        "user_email": old_array[step].user_email,
                        "user_name": old_array[step].user_name,
                        "user_point": old_array[step].user_point,
                        "user_ranking": new_array[step - 1].user_ranking,
                    }
                    new_array.push(same_rank)
                    ranking++;
                }
                else {
                    let rank = {
                        "user_email": old_array[step].user_email,
                        "user_name": old_array[step].user_name,
                        "user_point": old_array[step].user_point,
                        "user_ranking": ranking,
                    }
                    new_array.push(rank)
                    ranking++;
                }
            }
            this.ranking_list = new_array;
        },
    },

}
</script>