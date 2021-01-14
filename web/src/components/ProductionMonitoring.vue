<template>
  <el-container>
    <el-header style="height: 10%;position: relative;">
      <p style="position: absolute;top: 40%;left: 15px;">{{ currentTime }}</p>
      <p style="position: absolute;top: 40%;right: 13.5%;">{{ wea }}</p>
      <p style="position: absolute;top: 40%;right: 8.5%;color: #15CC48;">{{ tem }}</p>
      <p style="position: absolute;top: 40%;right: 1.5%;color: #10d4c5;">空气:{{ air_level }}</p>
    </el-header>
    <el-main>
      <el-row :gutter="15" style="height: 100%;">
        <el-col :span="6" style="height: 100%;">
          <div style="height: 30%;margin-bottom:5%;">
            <p class="text-size-14 marginBottom">车间产量统计</p>
            <ve-histogram :data="yieldChartData" :extend="chartsExtend" :colors="chartColor" height="85%"></ve-histogram>
          </div>
          <div style="height: 30%;margin-bottom:5%;">
            <p class="text-size-14">设备状态</p>
            <el-col :span="12">
              <ve-ring :data="EqStatusChartData1" :extend="ringExtend" :settings="ringSettings" :colors="color1" width="100%" height="60%"></ve-ring>
              <p class="text-size-12 text-center" style="color:#04E09E;">运行</p>
            </el-col>
            <el-col :span="12">
              <ve-ring :data="EqStatusChartData2" :extend="ringExtend" :settings="ringSettings" :colors="color2" width="100%" height="60%"></ve-ring>
              <p class="text-size-12 text-center" style="color: #F6E714;">维修</p>
            </el-col>
            <el-col :span="12">
              <ve-ring :data="EqStatusChartData3" :extend="ringExtend" :settings="ringSettings" :colors="color3" width="100%" height="60%"></ve-ring>
              <p class="text-size-12 text-center" style="color: #E07204;">巡检</p>
            </el-col>
            <el-col :span="12">
              <ve-ring :data="EqStatusChartData4" :extend="ringExtend" :settings="ringSettings" :colors="color4" width="100%" height="60%"></ve-ring>
              <p class="text-size-12 text-center color-lightgreen">保养</p>
            </el-col>
          </div>
          <div style="height: 30%;">
            <p class="text-size-14 marginBottom">能耗曲线</p>
            <ve-line :data="lineChartData" :extend="chartsExtend" :colors="lineColor" height="85%"></ve-line>
          </div>
        </el-col>
        <el-col :span="12" style="height: 100%;">
          <div style="height: 50%;margin-bottom:5%;">
            <el-col :span="24" style="height: 100%;">
              <ve-gauge :data="gaugeChartData" :extend="gaugeExtend" height="85%"></ve-gauge>
            </el-col>
          </div>
          <div style="height: 30%;margin-bottom:5%;">
            <el-col :span="6" style="text-align: right;">
              <p class="text-size-12 marginBottom">需求订单量</p>
              <p class="text-size-20 marginBottom" style="color: #04E09E;">25456</p>
              <p class="text-size-12 marginBottom">需求匹配率</p>
              <p class="text-size-20" style="color: #F6E714;">78%</p>
            </el-col>
            <el-col :span="18" style="height: 100%;">
              <ve-histogram :data="yieldChartData" :extend="chartsExtend" :colors="chartColor" height="85%"></ve-histogram>
            </el-col>
          </div>
        </el-col>
        <el-col :span="6" style="height: 100%;">
          <div style="height: 50%;margin-bottom:5%;">
            <p class="text-size-14">累计生产批次</p>
            <p class="text-size-36" style="color: #04E09E;">620376</p>
            <p class="text-size-12 color-grayblack">累计品种 <span class="text-size-20" style="color: #F6E714;">126</span></p>
            <ve-pie :data="planChartData" :extend="pieExtend" :settings="pieSettings" height="85%"></ve-pie>
          </div>
          <div style="height: 40%;">
            <p class="text-size-14">生产时长</p>
          </div>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
  var moment = require('moment');
  export default {
    name: "ProductionMonitoring",
    data(){
      return {
        websock:null,
        websockVarData:{},
        currentTime:"",
        wea:"",
        tem:"",
        air_level:"",
        chartsExtend:{
          legend:{
            show:false
          },
          yAxis:{
            show:false,
          },
          xAxis:{
            show:false
          },
          grid:{
            left:0,
            top:0,
            right:0,
            bottom:0,
            containLabel:false,
          },
          series:{
            barMaxWidth:12,
            itemStyle:{
              barBorderRadius:8
            },
            symbolSize:0,
            lineStyle:{
              shadowColor:"#818143"
            }
          }
        },
        yieldChartData:{
          columns: ['时间', '产量'],
          rows: [
            { '时间': '1/1', '产量': 1393},
            { '时间': '1/2', '产量': 3530},
            { '时间': '1/3', '产量': 2923},
            { '时间': '1/4', '产量': 1723},
            { '时间': '1/5', '产量': 3792},
            { '时间': '1/6', '产量': 4593}
          ]
        },
        ringSettings:{
          radius: ['60%', '80%'],
          offsetY: "50%"
        },
        ringExtend:{
          legend:{
            show:false
          },
          series:{
            labelLine: {
              show: false
            },
            left:0,
            top: 0,
            right:0,
            bottom:0,
            label:{
              show:false
            },
          },
        },
        pieSettings:{
          offsetY: "50%",
        },
        pieExtend:{
          legend:{
            show:false
          },
          series:{
            labelLine: {
              show: false
            },
            left:0,
            top: 0,
            right:0,
            bottom:0,
            label:{
              show:true,
              position:"inside",
              fontSize:10
            },
            radius: ['0', '70%'],
          },
        },
        chartColor:["#04E09E"],
        color1:["#04E09E","#c5f5d2"],
        color2:["#F6E714","#f1edb4"],
        color3:["#E07204","#f3d9bf"],
        color4:["#10d4c5","#c2f1ed"],
        EqStatusChartData1:{
          columns: ['状态', '设备数量'],
          rows: [
            { '状态': '运行', '设备数量': 1393 },
            { '状态': '其他', '设备数量': 530 },
          ]
        },
        EqStatusChartData2:{
          columns: ['状态', '设备数量'],
          rows: [
            { '状态': '维修', '设备数量': 322 },
            { '状态': '其他', '设备数量': 3530 },
          ]
        },
        EqStatusChartData3:{
          columns: ['状态', '设备数量'],
          rows: [
            { '状态': '巡检', '设备数量': 945 },
            { '状态': '其他', '设备数量': 4530 },
          ]
        },
        EqStatusChartData4:{
          columns: ['状态', '设备数量'],
          rows: [
            { '状态': '保养', '设备数量': 542 },
            { '状态': '其他', '设备数量': 3530 },
          ]
        },
        lineColor:["#04E09E","#F6E714"],
        lineChartData:{
          columns: ['时间', '昨日', '今日'],
          rows: [
            { '时间': '1', '昨日': 164, '今日': 245},
            { '时间': '2', '昨日': 199, '今日': 151},
            { '时间': '3', '昨日': 244, '今日': 154},
            { '时间': '4', '昨日': 345, '今日': 541},
            { '时间': '5', '昨日': 541, '今日': 366},
            { '时间': '6', '昨日': 514, '今日': 641},
          ]
        },
        planChartData:{
          columns: ['状态', '批数'],
          rows: []
        },
        gaugeExtend:{
          series:{
            axisLine:{
              lineStyle:{
                width:6,
                color:[[0, "#707070"],[1, "#707070"]]
              }
            },
            splitLine:{
              show:false,
            },
            axisTick:{
              show:false,
            },
            axisLabel:{
              show:false,
            }
          }
        },
        gaugeChartData:{
          columns: ['type', 'value'],
          rows: [
            { type: '执行中', value: 40},
          ]
        }
      }
    },
    created(){
      this.initWebSocket()
      let _this = this
      this.timer = setInterval(() =>{
        _this.currentTime = moment(new Date()).format('YYYY-MM-DD HH:mm:ss');
      },1000);
    },
    mounted(){
      this.getWeather()
      this.getBrandNum()
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
      initWebSocket(){ //初始化weosocket
        // this.websock = new WebSocket('ws://' + location.host + '/socket');
        this.websock = new WebSocket('ws://127.0.0.1:5002/socket');
        this.websock.onmessage = this.websocketonmessage;
        this.websock.onopen = this.websocketonopen;
        this.websock.onerror = this.websocketonerror;
        this.websock.onclose = this.websocketclose;
      },
      websocketonopen(){ //连接建立之后执行send方法发送数据
        this.websocketsend();
      },
      websocketonerror(){//连接建立失败重连
        console.log("websocket连接失败")
      },
      websocketonmessage(e){ //数据接收
        this.websockVarData = JSON.parse(e.data)
        console.log(this.websockVarData)
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
      getWeather(){
        let that = this
        this.axios.get("https://www.tianqiapi.com/api/?version=v1&appid=38126558&appsecret=9X3cD127").then(res => {
          console.log(res.data)
          that.wea = res.data.data[0].wea
          that.tem = res.data.data[0].tem
          that.air_level = res.data.data[0].air_level
        })
      },
      getBrandNum(){
        var that = this
        var params = {
          tableName:"PlanManager"
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if (res.data.code === "200") {
            //统计状态
            var PlanStatus1 = 0
            var PlanStatus2 = 0
            var PlanStatus3 = 0
            var PlanStatus4 = 0
            var PlanStatus5 = 0
            var PlanStatus6 = 0
            var PlanStatus7 = 0
            var PlanStatus8 = 0
            res.data.data.rows.forEach(item =>{
              if(item.PlanStatus === "待审核"){
                PlanStatus1 = PlanStatus1 + 1
              }
              if(item.PlanStatus === "审核未通过"){
                PlanStatus2 = PlanStatus2 + 1
              }
              if(item.PlanStatus === "待下发"){
                PlanStatus3 = PlanStatus3 + 1
              }
              if(item.PlanStatus === "待执行"){
                PlanStatus4 = PlanStatus4 + 1
              }
              if(item.PlanStatus === "撤回"){
                PlanStatus5 = PlanStatus5 + 1
              }
              if(item.PlanStatus === "待备料"){
                PlanStatus6 = PlanStatus6 + 1
              }
              if(item.PlanStatus === "物料发送中"){
                PlanStatus7 = PlanStatus7 + 1
              }
              if(item.PlanStatus === "物料发送完成"){
                PlanStatus8 = PlanStatus8 + 1
              }
            })
            that.planChartData.rows = [
              {"状态":"待审核","批数":PlanStatus1},
              {"状态":"审核未通过","批数":PlanStatus2},
              {"状态":"待下发","批数":PlanStatus3},
              {"状态":"待执行","批数":PlanStatus4},
              {"状态":"撤回","批数":PlanStatus5},
              {"状态":"待备料","批数":PlanStatus6},
              {"状态":"发送物料中","批数":PlanStatus7},
              {"状态":"发送物料完成","批数":PlanStatus8},
            ]
          }
        })
      }
    }
  }
</script>
<style scoped>
  .el-container{
    background: url("../assets/img/monitor_bg.jpg");
    background-repeat: no-repeat;
    background-size: 100% 100%;
    color: #ffffff;
  }
</style>
