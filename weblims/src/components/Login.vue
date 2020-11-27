<template>
  <div class="login" :style="conheight">
    <div class='container loginbox'>
      <div class="logintop">实验室信息管理系统</div>
      <div class="logininfo">
          <el-form :model="ruleForm" status-icon ref="ruleForm" :rules="rules" label-width="80px">
            <el-form-item label="登录名称" prop="loginname">
              <el-input v-model="ruleForm.loginname" autocomplete="off" @change='clearRemind'></el-input>
            </el-form-item>
            <el-form-item label="登录密码" prop="loginpass">
              <el-input v-model="ruleForm.loginpass" autocomplete="off" @change='clearRemind'></el-input>
            </el-form-item>
          </el-form>
          <div class="remindme"><el-checkbox v-model="checkedlogin" @change='remindKey'><span style="color:#333;">记住密码</span></el-checkbox></div>
    </div>
    <div class="subbutton" @click="loginIn">登录</div>
    </div>
  </div>
</template>

<script>
var moment=require('moment')
export default {
  name: 'Login',
  data () {
     var validateLoginname = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入登录名称'));
        } else {
          callback();
        }
      };
     var validateLoginpass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入登录密码'));
        } else {
          callback();
        }
      };
    return {
      ruleForm:{
        loginpass:'',
        loginname:''
      },
      conheight:{
        height:''
      },
      checkedlogin:false,
      rules: {
          loginname: [
            { validator: validateLoginname, trigger: 'blur' }
          ],
          loginpass: [
            { validator: validateLoginpass, trigger: 'blur' }
          ]
       }
    }
  },
  created(){
     window.addEventListener('resize', this.getHeight);
     this.getHeight()
  },
  mounted(){
    //登录默认勾选
    if(localStorage.getItem('Name') && localStorage.getItem('WorkNumber')){
    this.ruleForm={
      loginpass:localStorage.getItem('WorkNumber'),
      loginname:localStorage.getItem('Name')
    }
    this.checkedlogin=true
    }
  },
  methods: {
     getHeight(){
          this.conheight.height=window.innerHeight+'px';
       },
    clearRemind(){ //修改密码用户名清除原先勾选
      this.checkedlogin=false
    },
    remindKey(){ //勾选记住密码
      if(this.checkedlogin){
        if(this.ruleForm.loginname && this.ruleForm.loginpass){
            localStorage.setItem('Name',this.ruleForm.loginname)
            localStorage.setItem('WorkNumber',this.ruleForm.loginpass)
        }else{
            this.$message({
              type:'info',
              message:'请输入你的用户名密码'
            })
        }
      }else{
          localStorage.removeItem('Name')
          localStorage.removeItem('WorkNumber')
      }
    },
    loginIn() { //登录操作
      var params={
         WorkNumber:this.ruleForm.loginname,
         password:this.ruleForm.loginpass
      }
      this.axios.post('/api/account/userloginauthentication',this.qs.stringify(params)).then((res) => {
         if(res.data == "OK"){
           this.$message({
              showClose: true,
              message: "登录成功",
              type: 'success'
          });
          sessionStorage.setItem('Name',this.ruleForm.loginname)
          sessionStorage.setItem('WorkNumber',this.ruleForm.loginpass)
          sessionStorage.setItem('LastLoginTime',moment(new Date()).format('YYYY-MM-DD HH:mm:ss'))
          this.$router.push('/')
      }else{
        this.$message({
              showClose: true,
              message: res.data,
              type: 'error'
          });
      }
    })
  }
}
}
</script>

<style scoped>
   .login {
    width:100%;
    background:#0A9168 url('../assets/image/bg.jpg') no-repeat fixed top;
  }
  .loginbox{
    width:400px;
    height:275px;
    background-color:rgba(255, 255,255, 0.4);
    opacity: 0.8;
    position:fixed;
    top:50%;
    left: 50%;
    transform: translate(-50%,-50%)
  }
  .logintop{
    height: 60px;
    line-height: 80px;
    font-size: 18px;
    text-align:center;
    color:#333;
  }
  .logininfo{
    width: 80%;
    margin:20px 20px 5px;
  }
  .subbutton{
    position: absolute;
    top:275px;
    left:190px;
    border-radius: 25px;
    width: 50px;
    height: 50px;
    line-height: 50px;
    text-align: center;
    cursor: pointer;
    background-color: rgb(142, 142, 214);
  }
  .remindme{
    margin-left:80px;
  }
</style>
