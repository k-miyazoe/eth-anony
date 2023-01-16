<template>
    <v-app>
        <Header />
        <v-main>
            <NavHelpBar />
            <h1>お知らせ</h1>
            <v-spacer />
            <v-container fluid>
                <v-card class="pa-md-4 mx-lg-auto" width="750px">
                    <v-card-title class="red">重要</v-card-title>
                    <v-card-text>・成績評価の際は匿名アカウントから実名アカウントにポイントを全て集めてください．実名アカウントのポイント順で成績加点がもらえます．次回の期限日までに実名アカウントに集めていない場合救済措置はありません．</v-card-text>
                    <v-card-text>・12/9からは偶数番号の人は<font color="#ff0000">匿名アカウント</font>で、奇数番号の人は<font color="#ff0000">
                            実名アカウント</font>で質問・回答してください</v-card-text>
                    <v-card-text>・100point以下の人は、成績加点はありません.</v-card-text>
                    <v-card-text>・ユーザーIDにスペースが含まれていると送金できない不具合が生じます[現在2名確認]</v-card-text>
                </v-card>
                <v-card class="pa-md-4 mx-lg-auto" width="750px">
                    <v-card-subtitle class="green">修正済み</v-card-subtitle>
                    <v-card-text>・質問を解決できない不具合を修正[12/9]</v-card-text>
                    <v-card-text>・長文の質問で高評価・低評価・解決を押せない不具合修正[12/9]</v-card-text>
                </v-card>
                <v-card class="pa-md-4 mx-lg-auto" width="750px">
                    <v-card-subtitle class="yellow">確認している不具合</v-card-subtitle>
                    <v-card-text>・ユーザーIDを正しく指定しているがポイントを送金できない不具合[2名]</v-card-text>
                    <v-card-text>・上記の二名は100point分余分にあるので、ランキング計算の際は-100pointで計算します</v-card-text>
                    <v-card-text>・回答した直後に回答が即時反映されない不具合</v-card-text>
                </v-card>
                <v-card class="pa-md-4 mx-lg-auto" width="750px">
                    <v-card-subtitle class="blue">新機能の追加</v-card-subtitle>
                    <v-card-text>・新機能が反映されていない場合は、chromeのシークレットモードで掲示板を利用してください</v-card-text>
                    <v-card-text>・実名アカウントのみの作成ページを追加[匿名アカウントから実名アカウントに送金できない不具合がある人用]</v-card-text>
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