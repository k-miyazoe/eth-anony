import Swal from "sweetalert2";

const api_url = process.env.VUE_APP_API_URL

const User = class {
  //コンストラクタにuser_nameは必要あるか?
  constructor(user, user_name) {
    this.user = user
    this.user_name = user_name
  };
  //未完成
  getUserData() {
    axios
      .put(api_url + "/api/users/" + this.user)
      .then((res) => {
        return res.data;
      })
      .catch((e) => {
        console.log(e);
      });
  }
  //引数を確認する objを受け取る[未]
  sendPoint() {
    let update_obj = this.createPutObject()
    this.axios
      .put(api_url + "/api/users/" + this.user, update_obj)
      .then((res) => {
        //pointを受け取りました表示
        console.log(res);
      })
      .catch((e) => {
        console.log(e);
      });
  }
  //objを受けとる
  sendEther() {
    send_object = this.userObject
    send_object.ether_stock = send_object.ether_stock + 1;
    console.log(ether_point)
    this.axios.put(api_url + "/api/users/" + this.userId, send_object)
      .then((res) => {
        //etherを受け取りました表示
        console.log(res);
      })
      .catch((e) => {
        console.log(e);
      });
  }
};

const Question = class {
  //objごと渡す事で可変長引数にする
  constructor(question, axios, user_id) {
    this.question = question
    this.axios = axios
    this.user_id = user_id
  };
  //質問を取得[全体 or 未解決] 関数作成
  getall(){
    console.log('質問取得')
  };
  //一部を取得
  getOne(){
    console.log('一部を取得')
  };
  post() {
    this.axios
      .post(api_url + "/api/create-question/", this.question)
      .then(() => {
        console.log('質問投稿しました')
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
  };
  successMessage() {
    Swal.fire(
      'Goo job!',
      'success',
    )
  };
  //test未確認
  pointUp() {
     this.axios
        .post(api_url + "/api/point-up/" + this.user_id)
        .then(() => {
            console.log("point up")
        })
        .catch((e) => {
            console.log(e)
        });
  };
};

const Answer = class {
};

export {User, Question};