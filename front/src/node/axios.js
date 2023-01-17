import Axios from "axios";
import Cookies from "js-cookie";

function setHeader() {
  const csrftoken = Cookies.get("csrftoken");
  const axios = Axios.create({
    //baseURL: process.env.VUE_APP_API_URL,
    //baseURL: "http://localhost:8001/",
    baseURL: "https://eagle4.fu.is.saga-u.ac.jp/question-board-saga/",
    timeout: 2500,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
      //Authorization: jwt,
    },
  });
  return axios;
}

//関数をexport
export default {
  setHeader,
};
