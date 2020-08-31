<template>
  <el-row :gutter="15">
      <el-col class='SysMonbg MainContain'></el-col>
  </el-row>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "SystemMonitor",
    data(){
      return {
        websock:null,
        websockVarData:{},
        LS1Bit:"",
        LS2Bit:"",
        LST1Bit:"",
        LST2Bit:"",
        formParameters:{
          HZLQ1:"",
          HZLQ2:"",
          HZLD1:"",
          HZLD2:"",
        },
      }
    },
    created(){
      // this.initWebSocket()
    },
    mounted(){

    },
    watch:{

    },
    computed:{ //计算属性

    },
    destroyed() {
      if(this.websock){
        this.websock.close() //离开路由之后断开websocket连接
      }
    },
    methods: {
      move(e){
        let odiv = e.target; //获取目标元素
        if(odiv.attributes.hasOwnProperty("data-move")){
          //算出鼠标相对元素的位置
          let disX = e.clientX - odiv.offsetLeft;
          let disY = e.clientY - odiv.offsetTop;
          document.onmousemove = (e)=>{ //鼠标按下并移动的事件
            //用鼠标的位置减去鼠标相对元素的位置，得到元素的位置
            let left = e.clientX - disX - 8;
            let top = e.clientY - disY;
            //绑定元素位置到positionX和positionY上面
            this.positionX = top;
            this.positionY = left;
            //移动当前元素
            odiv.style.left = left + 'px';
            odiv.style.top = top + 'px';
          };
          document.onmouseup = (e) => {
            document.onmousemove = null;
            document.onmouseup = null;
          };
        }
      },
      // initWebSocket(){ //初始化weosocket
      //   // this.websock = new WebSocket('ws://' + location.host + '/socket');
      //   this.websock = new WebSocket('ws://127.0.0.1:5002/socket');
      //   this.websock.onmessage = this.websocketonmessage;
      //   this.websock.onopen = this.websocketonopen;
      //   this.websock.onerror = this.websocketonerror;
      //   this.websock.onclose = this.websocketclose;
      // },
      websocketonopen(){ //连接建立之后执行send方法发送数据
        this.websocketsend();
      },
      websocketonerror(){//连接建立失败重连
        console.log("websocket连接失败")
      },
      websocketonmessage(e){ //数据接收
        this.websockVarData = JSON.parse(e.data)
        this.LS1Bit = parseInt(this.websockVarData["PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_108"],10).toString(2).split("")
        this.LS2Bit = parseInt(this.websockVarData["PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_111"],10).toString(2).split("")
        this.LST1Bit = parseInt(this.websockVarData["PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_127"],10).toString(2).split("")
        this.LST2Bit = parseInt(this.websockVarData["PLC.KG1.Global.KG2_KG1.Stu_Equ_x.Stu_Equ_128"],10).toString(2).split("")
      },
      websocketsend(Data){//数据发送
        this.websock.send(Data);
      },
      websocketclose(e){  //关闭
        console.log("websocket关闭")
      },
      closesocket(){
        this.websock.close()
      },
      runControl(value,type){
        this.$confirm('您是否要对'+value+'执行'+type+'操作', '提示', {
          distinguishCancelAndClose:true,
          center:true,
          type: 'warning'
        }).then(()  => {
          this.axios.post("/api/run",{
            params: {
              EquipmentCode:value,
              Status:type,
            }
          }).then(res =>{
            if(res.data.code === "20001"){
              this.$message({
                showClose: true,
                type: 'success',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          });
        });
      },
      editHZ(value,HZ){
        this.$confirm('您是否要对'+value+'的频率进行修改', '提示', {
          distinguishCancelAndClose:true,
          center:true,
          type: 'warning'
        }).then(()  => {
          this.axios.post("/api/status",{
            params: {
              EquipmentCode:value,
              HZ:HZ,
            }
          }).then(res =>{
            if(res.data.code === "20001"){
              this.$message({
                showClose: true,
                type: 'success',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          });
        });
      },
      faultReset(value){
        this.$confirm('您是否要对'+value+'进行故障复位', '提示', {
          distinguishCancelAndClose:true,
          center:true,
          type: 'warning'
        }).then(()  => {
          this.axios.post("/api/fault",{
            params: {
              EquipmentCode:value,
            }
          }).then(res =>{
            if(res.data.code === "20001"){
              this.$message({
                showClose: true,
                type: 'success',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          });
        });
      },
      changeConservationSwitch(){
        var SwitchState = ""
        var SwitchParams = ""
        if(this.websockVarData['LS_JN_FLAG'] === "1"){
          SwitchState = "开"
          SwitchParams = "on"
          this.websockVarData['LS_JN_FLAG'] = "0"
        }else if(this.websockVarData['LS_JN_FLAG'] === "0"){
          SwitchState = "关"
          SwitchParams = "off"
          this.websockVarData['LS_JN_FLAG'] = "1"
        }
        this.$confirm('您是否要进行'+ SwitchState +'节能模式的操作？', '提示', {
          distinguishCancelAndClose:true,
          center:true,
          type: 'warning'
        }).then(()  => {
          var params = {
              switch:SwitchParams,
            }
          this.axios.post("/api/reset",this.qs.stringify(params)).then(res =>{
            if(res.data.code === "20001"){
              this.$message({
                showClose: true,
                type: 'success',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          });
        });
      },
      startReseting(){
        this.$confirm('您确认要复位吗？', '提示', {
          distinguishCancelAndClose:true,
          center:true,
          type: 'warning'
        }).then(()  => {
          var params = {
              reset:"yes",
            }
          this.axios.post("/api/reset",this.qs.stringify(params)).then(res =>{
            if(res.data.code === "20001"){
              this.$message({
                showClose: true,
                type: 'success',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          });
        });
      }
    }
  }
</script>
<style>
  .SysMonbg{
      background:#34383E url('../../assets/img/Containerbgc.png') no-repeat scroll center center;
      cursor: move;
  }
  .MainContain{
    position: relative;
    width: 1450px;
    height: 887px;
  }
</style>
