import Swal from "sweetalert2";

const User = class {
  constructor(user_id, axios) {
    this.user_id = user_id;
    this.axios = axios;
  }
  //ok .vueで利用できない問題
  getUserData() {
    this.axios
      .get("/api/users/" + this.user_id)
      .then((res) => {
        return res.data;
      })
      .catch((e) => {
        console.log(e);
      });
  }
  sendPoint(point_get_user) {
    this.axios
      .put("/api/point-up/" + point_get_user)
      .then(() => {
        console.log("ポイントを追加しました");
      })
      .catch((e) => {
        console.log(e);
      });
  }
  //backendの方も未完成
  sendEther(ether_get_user) {
    this.axios
      .put("/api/users/" + ether_get_user)
      .then(() => {
        console.log("ether get");
      })
      .catch((e) => {
        console.log(e);
      });
  }
};

const Question = class {
  constructor(axios) {
    this.axios = axios;
  }
  //質問を取得[全体 or 未解決] 未使用未完成
  getAll() {
    console.log("質問取得");
  }
  //一部を取得 ここは未使用
  async getOne(question_id) {
    await this.axios
      .get("/api/get-question/" + question_id)
      .then((res) => {
        console.log("class res.data", res.data);
        return res.data;
      })
      .catch((e) => {
        console.log(e);
      });
  }
  post(question, flag) {
    if (flag) {
      this.axios
        .post("/api/create-question/", question)
        .then(() => {
          console.log("質問投稿しました");
          return true;
        })
        .catch(() => {
          Swal.fire({
            icon: "warning",
            title: "Error",
            text: "入力が正しくありません",
            showConfirmButton: false,
            showCloseButton: false,
            timer: 3000,
          });
          return false;
        });
    } else {
      return false;
    }
  }
  successMessage(flag) {
    if (flag) {
      Swal.fire("Goo job!", "success");
    } else {
      Swal.fire({
        icon: "warning",
        title: "Error",
        text: "質問できませんでした!",
        showConfirmButton: false,
        showCloseButton: false,
        timer: 3000,
      });
    }
  }
  pointUp(question_user_id) {
    this.axios
      .put("/api/point-up/" + question_user_id)
      .then(() => {
        console.log("point up");
      })
      .catch((e) => {
        console.log(e);
      });
  }
  //質問した際のpointダウン 返り値なし
  async pointDown(question_user_id) {
    await this.axios
      .put("/api/point-down/" + question_user_id)
      .then(() => {
        console.log("point down");
      })
      .catch((e) => {
        console.log(e);
      });
  }
  //質問の回答数追加
  addNumberOfAnswers(question_id, flag) {
    if (flag) {
      this.axios
        .put("/api/add-num-answer/" + question_id)
        .then((res) => {
          console.log(res);
        })
        .catch((e) => {
          console.log(e);
        });
    }
  }
  //new
  //質問者 高評価point
  rewardPoint() {
    console.log("reward");
  }
  likeQuestion() {
    console.log("like question");
  }
  //質問解決 未完成
  resolvedQuestion(now_user_id, question_user_id, answer, best_answer) {
    //質問者の場合
    if (now_user_id == question_user_id) {
      //回答が存在する場合
      //ここのifのじょうけんがうまくいってない
      if (answer.length != 0) {
        //ベストアンサーが存在しているなら
        if (best_answer) {
          //解決処理
          const resolve = {
            user: question_user_id,
            question_status: true,
          };
          this.axios
            .put("/api/update-question/" + this.question_id, resolve)
            .then(() => {
              Swal.fire("質問が解決されました!", "success");
            })
            .catch((e) => {
              console.log(e);
            });
        }
        //ベストアンサーが存在してない場合
        else {
          Swal.fire({
            icon: "warning",
            title: "Error",
            text: "ベストアンサーが存在しません．ベストアンサーを選択してください!",
            showConfirmButton: false,
            showCloseButton: false,
            timer: 3000,
          });
        }
      }
      //回答がない場合
      else {
        Swal.fire({
          icon: "warning",
          title: "Error",
          text: "回答が存在しません.自己解決した場合、自身で回答を作成してください",
          showConfirmButton: false,
          showCloseButton: false,
          timer: 3000,
        });
      }
    }
    //質問者以外
    else {
      Swal.fire({
        icon: "warning",
        title: "Error",
        text: "質問者のみ有効です！",
        showConfirmButton: false,
        showCloseButton: false,
        timer: 3000,
      });
    }
  }
  //質問解決取り消し 未完成
  releaseResolvedQuestion() { }
};

const Answer = class {
  //コンストラクタのひきすうにquestion_idがあってもいい
  constructor(axios) {
    this.axios = axios;
  }
  getAnswer(question_id) {
    this.axios
      .get("/api/get-answer/" + question_id)
      .then((res) => {
        return res.data;
      })
      .catch((e) => {
        console.log(e);
      });
  }
  hasBestAnswer(answer) {
    let best_answer_decision = false;
    for (let item of answer) {
      if (item.answer_best == true) {
        console.log("ベストアンサーあり");
        best_answer_decision = true;
      }
    }
    return best_answer_decision;
  }
  postAnswer(answer, flag) {
    if (flag) {
      this.axios
        .post("/api/create-answer/", answer)
        .then((res) => {
          console.log(res);
          Swal.fire(
            '回答を投稿しました!',
            'success',
          )
        })
        .catch(() => {
          Swal.fire({
            icon: "warning",
            title: "Error",
            text: "入力が正しくありません",
            showConfirmButton: false,
            showCloseButton: false,
            timer: 3000,
          });
        });
    }
  }
  pointDown(answer_user_id, flag) {
    if (flag) {
      this.axios
        .put("/api/point-down/" + answer_user_id)
        .then(() => {
          console.log("point down");
          return true;
        })
        .catch((e) => {
          console.log(e);
          return false;
        });
    } else {
      return false;
    }
  }
};

export { User, Question, Answer };
