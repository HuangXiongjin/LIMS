import App from './App'
import Vue from 'vue'
import router from './router'

Vue.config.productionTip = false

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI)

import axios from 'axios'
Vue.prototype.axios = axios
import qs from 'qs'
Vue.prototype.qs=qs

import './assets/css/common.css'

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
