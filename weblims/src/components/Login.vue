<template>
  <div class="login">
    <div class='container loginbox'>
      <div class="logintop">实验室信息管理系统</div>
      <div class="logininfo">
          <el-form :model="ruleForm" status-icon ref="ruleForm" :rules="rules" label-width="80px" class="demo-ruleForm">
            <el-form-item label="登录名称" prop="loginname">
              <el-input v-model="ruleForm.loginname" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="登录密码" prop="loginpass">
              <el-input v-model="ruleForm.loginpass" autocomplete="off"></el-input>
            </el-form-item>
          </el-form>
          <div class="remindme"><el-checkbox v-model="checkedlogin">记住密码</el-checkbox></div>
    </div>
    <div class="subbutton" @click="loginIn">登录</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
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
      msg: 'Welcome to Your Vue.js App',
      ruleForm:{
        loginpass:'',
        loginname:''
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
  methods: {
    loginIn() {
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
    height:800px;
    background-color:#0A9168;
  }
  .loginbox{
    width:400px;
    height:300px;
    background-color: aquamarine;
    opacity: 0.8;
    position: absolute;
    top:50%;
    left: 50%;
    transform: translate(-50%,-50%)
  }
  .logintop{
    height: 60px;
    line-height: 80px;
    font-size: 18px;
    text-align:center;
    color: rgb(42, 44, 43);
  }
  .logininfo{
    width: 80%;
    margin:20px 20px 5px;
  }
  .subbutton{
    position: absolute;
    top:275px;
    left:175px;
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
