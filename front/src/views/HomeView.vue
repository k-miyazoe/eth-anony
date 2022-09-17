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
import axios from "axios";

const api_url = process.env.VUE_APP_API_URL;
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
    this.getUnresolvedQuestion()
  },
  methods: {
    //3つのゲット関数は引数に文字列を与えてやれば、一つの関数で済む
    getUnresolvedQuestion() {
      axios
        .get(api_url + "/api/get-question/unresolved/")
        .then((res) => {
          this.unresolved_question = res.data;
        })
        .catch((e) => {
          console.log(e);
        });
    },
    getResolvedQuestion() {
      axios
        .get(api_url + "/api/get-question/resolved/")
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
        .get(api_url + "/api/get-question/")
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