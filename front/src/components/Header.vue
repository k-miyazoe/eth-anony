<template>
  <div>
    <v-app-bar color="#00B0FF" dense dark elevation="10">
      <v-toolbar-title>
        質問掲示板 - プログラミング概論
      </v-toolbar-title>
      <v-spacer />
      <v-btn>
        <router-link to='/mypage'>
          マイページ
        </router-link>
      </v-btn>
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
  }),
  mounted() {
    this.setURLParameter();
  },
  methods: {
    setURLParameter() {
      this.$session.start();
      if (this.$session.has("token")) {
        console.log('Header.vue set uid', this.$session.get('user_id'))
        this.uid = this.$session.get('user_id')
      }
    },
  },

}

</script>
