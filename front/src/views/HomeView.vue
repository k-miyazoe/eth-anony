<template>
  <v-app>
    <Header />
    <v-main>
      <v-row class="justify-center">
        <v-btn @click="routerPushCreateQuestion">質問する</v-btn>
      </v-row>
      <v-container fluid>
        <v-card v-for="item in unresolved_question" :key="item.id" class="pa-md-4 mx-lg-auto" width="750px">
          <v-card-text>
            <router-link :to="{ name: 'question-detail', params: { id: item.id } }">
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
import Header from "../components/Header.vue";
import header from "/src/node/axios";
const axios = header.setHeader();
let g_group = null;
let user_group = "everyone";

export default {
  components: {
    Header,
  },
  data() {
    return {
      tab: null,
      unresolved_question: {},
      resolved_question: {},
      my_question: {},
      items: [],
    }
  },
  mounted() {
    this.checkToken();
    this.getUnresolvedQuestion();
  },
  methods: {
    checkToken() {
      if (this.$session.has("token")) {
        g_group = this.$session.get("user_group");
        this.getGroup();
        console.log('グループ', user_group)
      }
    },
    getGroup() {
      //偶数の実名グループ
      if (g_group) {
        user_group = "real_name"
      }
      //奇数の匿名グループ
      else {
        user_group = "anonymous"
      }
    },
    //groupを追加
    //3つのゲット関数は引数に文字列を与えてやれば、一つの関数で済む
    getUnresolvedQuestion() {
      axios
        .get("/api/get-question/unresolved/" + user_group)
        .then((res) => {
          this.unresolved_question = res.data;
        })
        .catch((e) => {
          console.log(e);
        });
    },
    getResolvedQuestion() {
      axios
        .get("/api/get-question/resolved/")
        .then((res) => {
          console.log(res.data);
          this.resolved_question = res.data
        })

        .catch((e) => {
          console.log(e);
        });
    },
    //未完成
    getMyQuestion() {
      axios
        .get("/api/get-question/")
        .then((res) => {
          console.log(res.data);
          //res.dateを保持する
        })
        .catch((e) => {
          console.log(e);
        });
    },
    routerPushCreateQuestion() {
      this.$router.push('/create-question')
    },
  },
}
</script>