<template>
  <v-app>
    <Header />
    <!-- <v-btn color="primary" @click="log">
      log button
    </v-btn> -->
    <v-main>
      <NavHelpBar />
      <SubTitle />
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
                <v-btn color="success" v-bind="attrs" v-on="on" :disabled="!valid">
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
                <v-form>
                  <v-text-field type="password" v-model="eth_password" :counter="10" label="パスワード"
                    :rules="rules.password" maxlength="10" required />
                </v-form>
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
import Swal from "sweetalert2";
import VueLoading from 'vue-loading-template'
import Header from "../components/Header.vue";
import NavHelpBar from "../components/NavigationHelpBar.vue"
import SubTitle from "../components/SubTitle.vue";
import header from "/src/node/axios";
import { User, Question } from "/src/node/class";

const axios = header.setHeader();

let user_id = 0;
let user_name = "";
let user_eth_address = "";
let user_group = null;
let user_point = 0;
let UserClass = null;

const Web3 = require("web3");
const web3 = new Web3("https://eagle4.fu.is.saga-u.ac.jp/geth-docker/");
const miner = "0x7A5601125AC4CC81647E61c0347Ef58E2Cf8cf02";
let g_question_flag = true;

export default {
  components: {
    VueLoading,
    Header,
    NavHelpBar,
    SubTitle
  },
  data() {
    return {
      loading: false,
      dialog: false,
      valid: true,
      eth_password: "",
      question_obj: {
        "user": 0,
        "question_user_name": "",
        "question_eth_address": "",
        "question_group": null,
      },
      rules: {
        question_title: [
          (v) => !!v || "質問タイトルは必須です",
        ],
        question_content: [
          (v) => !!v || "質問内容は必須です",
        ],
        password: [
          (v) => !!v || "パスワードを入力してください",
        ],
      },
    };
  },
  mounted() {
    this.checkToken();
    this.checkGeth();
  },
  methods: {
    checkToken() {
      if (!this.$session.has("token")) {
        router.push("/signin");
      }
      user_id = this.$session.get('user_id');
      user_name = this.$session.get("user_name");
      user_eth_address = this.$session.get('user_eth_address');
      user_group = this.$session.get("user_group");
      UserClass = new User(user_id, axios);
    },
    //ok
    checkGeth() {
      web3.eth.personal.getAccounts().then(
        (data) => {
          console.log("geth 起動中");
        },
        (err) => {
          console.log("geth 停止中", err);
          this.valid = false;
        }
      );
    },
    async postQuestion() {
      this.loading = true;
      const question = new Question(axios);
      await this.getHasEth(user_eth_address, 1);
      await this.ethDown(user_eth_address, 1, this.eth_password, g_question_flag);
      this.quesiotnInit();//追加
      question.post(this.question_obj, g_question_flag);
      await question.pointDown(user_id);
      this.questionResult(g_question_flag);
    },
    async getHasEth(address, check_ether) {
      await web3.eth.getBalance(address)
        .then((has_ether) => {
          console.log('所持eth', has_ether)
          g_question_flag = (has_ether - check_ether > 0)
        })
    },
    //質問によるetherを消費 eth_passが正しくない場合false 単体ok
    async ethDown(question_user_eth_address, eth, question_user_eth_password, flag) {
      if (flag) {
        const from = await web3.utils.toChecksumAddress(question_user_eth_address);
        const to = await web3.utils.toChecksumAddress(miner);
        const transaction = {
          from: from,
          to: to,
          value: eth,
          gasPrice: 0,
        };
        await web3.eth.personal
          .unlockAccount(from, question_user_eth_password, 15000)
          .then(() => {
            web3.eth.sendTransaction(transaction);
            console.log("質問によるethの消費");
          })
          .catch(() => {
            Swal.fire({
              icon: "warning",
              title: "Error",
              text: "パスワードが正しくない可能性があります",
              showConfirmButton: false,
              showCloseButton: false,
              timer: 3000,
            });
            g_question_flag = false;
          });
      }
    },
    //質問のobjectの初期化
    quesiotnInit() {
      this.question_obj.user = user_id;
      this.question_obj.question_user_name = user_name;
      //追加
      this.question_obj.question_eth_address = user_eth_address;
      this.question_obj.question_group = user_group;
    },
    questionResult(result) {
      if (result) {
        Swal.fire("質問を投稿しました", "success");
        router.push('/signin');
      } else {
        Swal.fire({
          icon: "warning",
          title: "Error",
          text: "質問できませんでした",
          showConfirmButton: false,
          showCloseButton: false,
          timer: 3000,
        });
        this.loading = false;
      }
    },
    async log() {
    },
  }
}
</script>