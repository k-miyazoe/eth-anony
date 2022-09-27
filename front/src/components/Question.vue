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
                <v-form>
                  <v-text-field type="password" v-model="eth_password" :counter="20" label="パスワード" :rules="rules.password"
                    maxlength="20" required/>
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
import header from "/src/node/axios";
import { User,Question } from "/src/node/class";

const axios = header.setHeader();
let user_id = 0;
let user_eth_address = "";
let user_group = null;
let user_point = 0;
let UserClass = null;
const Web3 = require("web3");
const web3 = new Web3(process.env.VUE_APP_GETH_API);
const miner = process.env.VUE_APP_MINER;

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
      eth_password: "",
      question_obj: {
        "user": this.$session.get('user_id'),
        "question_user_name": this.$session.get("user_name"),
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
    this.getUserPoint();
  },
  methods: {
    checkToken() {
      if (!this.$session.has("token")) {
        router.push("/signin");
      }
      user_id = this.$session.get('user_id');
      user_eth_address = this.$session.get('user_eth_address');
      user_group = this.$session.get("user_group");
      UserClass = new User(user_id, axios);
    },
    async getUserPoint() {
      const user_data = await UserClass.getUserData();
      //なぜundefineかわからない
      console.log('user', UserClass.getUserData());
      //これがゴール
      //user_point = user_data.user_point
      //console.log('user_point', user_data.user_point);
      //return user_data.user_point;
    },
    async postQuestion() {
      this.loading = true;
      let flag = null;
      const question = new Question(axios);
      //trueになっている
      console.log('1 point消費', this.checkHasPoint());
      flag = await question.pointDown(user_id, this.checkHasPoint());//ここの処理が動いていることがそもそもよくない
      console.log('2 eth消費');
      await this.ethDown(user_eth_address, 1, this.eth_password,flag);//ok
      console.log('3 質問投稿[undefine]', flag);
      flag = question.post(this.question_obj,flag);
      console.log('4 成功か', flag);
      question.successMessage(flag);
      this.loading = false;
      router.push('/');
    },
    //質問によるetherを消費
    async ethDown(question_user_eth_address, eth, question_user_eth_password,flag) {
      //Bグループの場合 スルーする
      if(!user_group){
        return true;
      }
      //ポイント処理がうまく行っていないならば
      else if(!flag){
        return false;
      }
      else if (this.canQuestion() && flag) {
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
            return true;
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
            return false;
          });
      }
    },
    //質問できるか判定 boolean
    async canQuestion() {
      const can_question = await this.getHasEth(user_eth_address,1);
      if(can_question <= 0) {
        Swal.fire({
          icon: "warning",
          title: "Error",
          text: "ETHが足りていません",
          showConfirmButton: false,
          showCloseButton: false,
          timer: 1000,
        });
        return false;
      } else {
        return true;
      }
    },
    //計算後のetherを返す
    async getHasEth(address,check_ether) {
      let has_ether = 0;
      await web3.eth.getBalance(address)
        .then((ether) => {
          has_ether = ether;
        })
      return has_ether - check_ether;
    },
    checkHasPoint() {
      //user_pointが定義されていない なぜかuser_pointが1になっている
      //sessionで取得した情報は更新されない! バグの危険性
      //user_pointを変更
      console.log("check point",user_point);
      if (user_point <= 0) {
        Swal.fire({
          icon: "warning",
          title: "Error",
          text: "error",
          showConfirmButton: false,
          showCloseButton: false,
          timer: 3000,
        });
        return false;
      } else {
        return true;
      }
    },
    async log() {
      // await this.ethDown(user_eth_address, 1, "testether1");
      // await this.initialEth(user_eth_address,100);
    },
  }
}
</script>