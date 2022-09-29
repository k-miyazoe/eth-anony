<template>
  <div>
    <v-app-bar color="#00B0FF" dense dark elevation="10">
      <v-toolbar-title>
        質問掲示板 - プログラミング概論
      </v-toolbar-title>
      <v-spacer />
      <div v-if="login_status">
        <v-btn>
          <router-link to='/mypage'>
            マイページ
          </router-link>
        </v-btn>
      </div>
      <div v-else>
        <v-btn>
          <router-link to='/signin'>
            サインイン
          </router-link>
        </v-btn>
        <v-btn>
          <router-link to='/signup'>
            サインアップ
          </router-link>
        </v-btn>
      </div>
    </v-app-bar>
    <div style="padding: 15px;"></div>
  </div>
</template>

<script>
export default {
  components: {
  },
  data: () => ({
    uid: 0,
    login_status: false,
  }),
  mounted() {
    this.setURLParameter();
  },
  methods: {
    setURLParameter() {
      if (this.$session.has("token")) {
        console.log('Header.vue set uid', this.$session.get('user_id'))
        this.uid = this.$session.get('user_id')
        this.login_status = true;
      }
    },
  },

}

</script>
