import Axios from "axios";
import Cookies from "js-cookie";

function setHeader() {
  const csrftoken = Cookies.get("csrftoken");
  const axios = Axios.create({
    //baseURL: process.env.VUE_APP_API_URL,
    //おそらくここがeagle4.cc.xxx/question-board-saga/になる
    baseURL: "http://localhost:8040",
    //baseURL: "http://eth-anony-back:9990",
    timeout: 2500,
    headers: {
      "Content-Type": "application/json",
      //Authorization: jwt,
      "X-CSRFToken": csrftoken,
    },
  });
  return axios;
}

//関数をexport
export default {
  setHeader,
};
