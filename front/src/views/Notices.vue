<template>
    <v-app>
        <Header />
        <v-main>
            <NavHelpBar />
            <h1>お知らせ</h1>
            <v-spacer />
            <v-container fluid>
                <v-card>
                    <v-card-title class="red">重要</v-card-title>
                    <v-card-text>成績評価の際は匿名アカウントから実名アカウントにポイントを全て集めてください．実名アカウントのポイント順で成績加点がもらえます．</v-card-text>
                    <v-card-text>12/9からは偶数番号の人は実名アカウントで、奇数番号の人は匿名アカウントで質問・回答してください</v-card-text>
                </v-card>
                <v-card>
                    <v-card-subtitle class="green">修正済み</v-card-subtitle>
                    <v-card-text>質問を解決できない不具合を修正[12/9]</v-card-text>
                    <v-card-text>長文の質問で高評価・低評価・解決を押せない不具合修正[12/9]</v-card-text>
                </v-card>
                <v-card>
                    <v-card-subtitle class="yellow">確認している不具合</v-card-subtitle>
                    <v-card-text>ユーザーIDを正しく指定しているがポイントを送金できない不具合[1名]</v-card-text>
                    <v-card-text>回答した直後に回答が即時反映されない不具合</v-card-text>
                </v-card>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import Header from "../components/Header.vue";
import NavHelpBar from "../components/NavigationHelpBar.vue";

export default {
    components: {
        Header,
        NavHelpBar,
    },

}
</script>

<style>

</style>