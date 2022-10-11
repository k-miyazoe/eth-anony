import Axios from "axios";
import Cookies from "js-cookie";

function setHeader() {
  const csrftoken = Cookies.get("csrftoken");
  const axios = Axios.create({
    baseURL: process.env.VUE_APP_API_URL,
    //baseURL: "http://localhost:8040",
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
