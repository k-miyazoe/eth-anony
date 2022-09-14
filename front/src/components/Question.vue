<template>
  <v-app>
    <Header />
    <v-main>
      <NavHelpBar />
      <v-container>
        <v-card class="mt-12">
          <v-card-title>
            <span class="headline">質問フォーム</span>
          </v-card-title>

          <v-layout row fill-height justify-center align-center v-if="loading">
            <v-progress-circular :size="50" color="primary" indeterminate />
          </v-layout>

          <!-- 質門投稿フォーム -->
          <v-form v-else ref="form" v-model="valid" lazy-validation>
            <!--title-->
            <v-textarea v-model="question_obj.question_title" label="質問タイトル*" :rules="rules.question_title" required
              clearable clear-icon="mdi-close-circle" rows="1" outlined>
            </v-textarea>
            <!--content-->
            <v-textarea v-model="question_obj.question_content" label="質問内容*" :rules="rules.question_content" required
              clearable clear-icon="mdi-close-circle" auto-grow outlined>
            </v-textarea>
            <!--sorce code-->
            <v-textarea v-model="question_obj.question_source_code" label="ソースコード[任意]" clearable
              clear-icon="mdi-close-circle" auto-grow outlined>
            </v-textarea>
            <v-dialog v-model="dialog" width="500">
              <template v-slot:activator="{ on, attrs }">
                <v-btn dark v-bind="attrs" v-on="on" :disabled="!valid">
                  質問する
                </v-btn>
              </template>

              <v-card>
                <v-card-title>
                  質問について
                </v-card-title>
                <v-card-text>
                  質問は削除できません．あとから編集することは可能です．
                  閲覧者が理解できる質問になっていますか？
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" @click="postQuestion">
                    質問を送信する
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-form>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>
<script>
import router from "../router";
import VueLoading from 'vue-loading-template'
import Header from "../components/Header.vue";
import NavHelpBar from "../components/NavigationHelpBar.vue"
import header from "/src/node/axios";
import { User, Question } from "/src/node/class";

const axios = header.setHeader();
const user_id = this.$session.get('user_id');

export default {
  components: {
    VueLoading,
    Header,
    NavHelpBar,
  },
  data() {
    return {
      loading: false,
      dialog: false,
      valid: true,
      question_obj: {
        "user": user_id,
        "question_user_name": this.$session.get("user_name")
      },
      rules: {
        question_title: [
          (v) => !!v || "質問タイトルは必須です",
        ],
        question_content: [
          (v) => !!v || "質問内容は必須です",
        ],
      },
    };
  },
  mounted() {
    this.checkToken();
    this.getUserInfo();
  },
  methods: {
    //初期化処理
    checkToken() {
      this.$session.start();
      if (!this.$session.has("token")) {
        router.push("/signin");
      }
    },
    //user_nameは必要ないかも
    getUserInfo() {
      const user = new User(user_id, this.$session.get("user_name"));
    },

    //イベント処理
    //質問をする 
    postQuestion() {
      this.loading = true
      const question = new Question(this.question_obj, axios, user_id);
      question.post();
      question.successMessage();
      question.pointUp();
      this.loading = false
      router.push('/')
    },
  }
}
</script>