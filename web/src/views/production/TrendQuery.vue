<template>
    <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">生产数据趋势分析</span>
      </div>
        <div class="platformContainer blackComponents">
            <div id="main" style="width:100%; height:750px; backgroundColor:#3D4048;" v-loading="loading">数据图表</div>
        </div>
        <div class="staticbox" style="width:100%; height:290px;overflow:auto;">
                     <div class="platformContainer blackComponents">
                        <el-table
                            :data="tableData"
                            style="width: 100%">
                            <el-table-column
                              prop="name"
                              label="统计线名称"
                              >
                            </el-table-column>
                            <el-table-column
                              prop="cdate"
                              label="统计线日期"
                              >
                            </el-table-column>
                            <el-table-column
                              prop="comparetime"
                              label="对比时间"
                              width="180">
                            </el-table-column>
                            <el-table-column
                              prop="averag"
                              label="平均值"
                              width="180">
                            </el-table-column>
                            <el-table-column
                              prop="max"
                              label="最大值"
                              width="180">
                            </el-table-column>
                             <el-table-column
                              prop="min"
                              label="最小值"
                              width="180">
                            </el-table-column>
                          </el-table>                     
                     </div>
                   </div>
    </el-col>
  </el-row>
</template>
<script>
var moment=require('moment')
import echarts from '@/assets/js/echarts.js'
export default {
    data(){
        return {
            msg:123,
            loading:false,
            rawData:[{time1:'2015-12-31 00:00:04',value1:'3570.47',value2:'3539.18',value3:'3538.35',value4:'3580.6'},
            {time1:'2015/12/30 00:00:08',value1:'3766.73',value2:'3572.88',value3:'3538.11',value4:'3573.68'},
            {time1:'2015/12/29 00:00:12',value1:'3528.4',value2:'3563.74',value3:'3515.52',value4:'3564.17'},
            {time1:'2015/12/28 00:00:16',value1:'3635.77',value2:'3533.78',value3:'2699',value4:'3209'},
            {time1:'2015/12/25 00:00:20',value1:'3614.05',value2:'3627.91',value3:'3601.74',value4:'3635.26'},
            {time1:'2015/12/25 00:00:28',value1:'3616.05',value2:'3628.91',value3:'3603.74',value4:'3633.26'},
            {time1:'2015/12/25 00:00:32',value1:'3618.05',value2:'3629.91',value3:'3602.74',value4:'3635.26'},
            {time1:'2015/12/25 00:00:38',value1:'3614.05',value2:'3630.91',value3:'3603.74',value4:'3636.26'},
            {time1:'2015/12/25 00:00:44',value1:'3610.05',value2:'3627.91',value3:'3605.74',value4:'3635.26'},
            {time1:'2015/12/25 00:00:50',value1:'3519.05',value2:'3626.91',value3:'3606.74',value4:'3638.26'},
            {time1:'2015/12/25 00:01:00',value1:'3617.05',value2:'3624.91',value3:'3603.74',value4:'3634.26'},
            {time1:'2015/12/25 00:01:06',value1:'3615.05',value2:'3627.91',value3:'3604.74',value4:'3637.26'},
            {time1:'2015/12/25 00:01:09',value1:'3614.05',value2:'3629.91',value3:'3605.74',value4:'3636.26'},
            {time1:'2015/12/25 00:01:20',value1:'3616.05',value2:'3625.91',value3:'3603.74',value4:'3637.26'},
            ],
        yvaluemax:0,
        yvaluemin:0,
        dateclass:'day',
        singletag:'tag1',
        isload:false,
        TabControl:{
          TabControlCurrent:"",
          TabControlOptions:[
            {name:"趋势分析"},
            {name:"数据汇总分析"}
          ]
        },
         tableData: [{
            averag: 0,
            name: 'Tag1',
            cdate:moment().format('YYYY-MM-DD'),
            comparetime:'00:00:04',
            max: 0,
            min:0,

          },{
            averag: 0,
            comparetime:'00:00:04',
            cdate:moment().format('YYYY-MM-DD'),
            name: 'Tag2',
            max: 0,
            min:0
          }],
        treedata:[],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        websoc:null,
        selftime:2,
        isout:false,
        value2:'',
        dates:[],
        myChart:null,
        dataline1:[],
        dataline2:[],
        dataline3:[],
        dataline4:[],
        dataline5:[],
        dataline6:[],
        maxvalue:10,
        date1:moment().format('YYYY-MM-DD'),
        date2:moment().format('YYYY-MM-DD'),
        loading:false,
        averagevalue1:0,
        averagevalue2:0,
        averagevalue3:0,
        averagevalue4:0,
        averagevalue5:0,
        averagevalue6:0,
        dataIndex:0,
        dateset:[],
        tag1Max:0,
        tag1Min:0,
        tag2Max:0,
        tag2Min:0,
        tag3Max:0,
        tag3Min:0,
        tag4Max:0,
        tag4Min:0,
        tag5Max:0,
        tag5Min:0,
        comparetime:'00:00:04',
        }
    },
    mounted(){
        this.inintPic()
    },
    methods:{
        drawLine(dataline1,dataline2,dataline3,dataline4,dateset,yvaluemax,yvaluemin){
        if(this.myChart){
          this.myChart.dispose()
        }
        this.myChart= echarts.init(document.getElementById('main'));
        var option = {
              backgroundColor: '#3D4048',
              color:['#4472C5','#ED7C30','#80FF80','#FF8096'], 
              legend: {
                  data:dateset ,
                  inactiveColor: '#777',
                  textStyle: {
                      color: '#fff'
                  }
              },
              tooltip: {
                  trigger: 'axis',
                  axisPointer: {
                      animation: false,
                      type: 'cross',
                      lineStyle: {
                          color: '#376df4',
                          width: 2,
                          opacity: 1
                      }
                  }
              },
              toolbox: {
                      feature: {
                          dataZoom: {
                              yAxisIndex: false
                          },
                          brush: {
                              type: ['lineX', 'clear']
                          }
                      }
                  },
              brush: {
                      xAxisIndex: 'all',
                      brushLink: 'all',
                      outOfBrush: {
                      colorAlpha: 0.1
                  }
              },
              xAxis: {
              type: 'category',
              data:this.dates,
              axisLine: { lineStyle: { color: '#8392A5' } }
              },
              yAxis: [{
                type: 'value',
                name: dateset[0],
                min: yvaluemin,
                max: yvaluemax,
                position: 'left',
                axisLabel: {
                    formatter: '{value}',
                },
                axisLine: {
                    lineStyle: {
                        color: '#8392A5',
                    },
                },
              }],
              grid: {
                bottom: 80,
                top:80
              },
              animation: false,
              visualMap: {
                show: false,
                dimension: 1,
                pieces: [],  //pieces的值由动态数据决定
                outOfRange: {
                color: 'green'
              }
          },
          series: [
              {
                  name: dateset[0],
                  yAxisIndex:0, 
                  type: 'line',
                  data: dataline1,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                      width: 1,
                      color:'#8CBD47'
                  }
              },
              {
                  name: dateset[1],
                  type: 'line',
                  data: dataline2,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                      width: 1,
                      color:'#00FF66'
                  }
              },
              {
                  name: dateset[2],
                  type: 'line',
                  data: dataline3,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                      width: 1,
                      color:'#5B9A92'
                  }
              },
              {
                name: dateset[3],
                  type: 'line',
                  data: dataline4,
                  smooth: true,
                  showSymbol: false,
                  lineStyle: {
                    width: 1,
                    color:'#E28A36'
                  }
              },
              {
	          name: '平行于y轴的对比线',
            type: 'line',
            markLine: {
                name: 'cc',
                symbol:'none',//去掉箭头
                lineStyle:{
                        type:"solid",
                        color:"#FF4B5C",
                    },
                data: [[
                    { coord: [this.dates[0],0] },
                    { coord: [this.dates[0],100] }
                ]]
            }
              }
          ]
      };
    var that=this
     this.myChart.on('updateAxisPointer', function (event) {  //拉着tooltips 触发滑动事件
       if(event.axesInfo.length!=0){
         var index=event.dataIndex
        if(index>that.dataIndex){
          var arr1=that.dataline1.slice(that.dataIndex,index)
          var arr2=that.dataline2.slice(that.dataIndex,index)
          var arr3=that.dataline3.slice(that.dataIndex,index)
          var arr4=that.dataline4.slice(that.dataIndex,index)
          var index1=index-that.dataIndex
        }else{
          var arr1=that.dataline1.slice(index, that.dataIndex)
          var arr2=that.dataline2.slice(index, that.dataIndex)
          var arr3=that.dataline3.slice(index, that.dataIndex)
          var arr4=that.dataline4.slice(index, that.dataIndex)
          var index1=that.dataIndex-index
        }
        var num1=0
        var num2=0
        var num3=0
        var num4=0
        for(var i=0;i<arr1.length;i++){
            num1=num1+arr1[i]
         }
        for(var i=0;i<arr2.length;i++){
            num2=num2+arr2[i]
         }
        for(var i=0;i<arr3.length;i++){
            num3=num3+arr3[i]
         }
        for(var i=0;i<arr4.length;i++){
            num4=num4+arr4[i]
         }
         that.averagevalue1=(num1/index1).toFixed(2)
         that.averagevalue2=(num2/index1).toFixed(2)
         that.averagevalue3=(num3/index1).toFixed(2)
         that.averagevalue4=(num4/index1).toFixed(2)
         that.tag1Max=Math.max.apply(Math, arr1).toFixed(2)
         that.tag1Min=Math.min.apply(Math, arr1).toFixed(2)
         that.tag2Max=Math.max.apply(Math, arr2).toFixed(2)
         that.tag2Min=Math.min.apply(Math, arr2).toFixed(2)
         that.tag3Max=Math.max.apply(Math, arr3).toFixed(2)
         that.tag3Min=Math.min.apply(Math, arr3).toFixed(2)
         that.tag4Max=Math.max.apply(Math, arr4).toFixed(2)
         that.tag4Min=Math.min.apply(Math, arr4).toFixed(2)
         that.InitTable()
       }
     })
    this.myChart.on('legendselectchanged',function(params){
      that.myChart.setOption({
         yAxis: [{
                type: 'value',
                name: params.name,
                min: this.tag1Min,
                max: this.tag1Max,
                position: 'left',
                axisLabel: {
                    formatter: '{value}',
                },
                axisLine: {
                    lineStyle: {
                        color: '#4E6EC1',
                    },
                },
              }]
       })
    })
    this.myChart.on('click', renderBrushed); //点击绘制对比线
    function renderBrushed(params) {
      var time=params.name
      var datas=params.data
      var index=params.dataIndex
      that.dataIndex=params.dataIndex
      that.comparetime=params.name
      var maxline=[]
      maxline.push(that.dataline1[index],that.dataline2[index],that.dataline3[index],that.dataline4[index])
      var max=Math.max.apply(Math, maxline)
      that.myChart.setOption({
          series:{
	          name: '平行于y轴的对比线',
            type: 'line',
            markLine: {
                name: 'cc',
                symbol:'none',//去掉箭头
                lineStyle:{
                        type:"solid",
                        color:"#FF4B5C",
                    },
                data: [[
                    { coord: [that.comparetime,0] },
                    { coord: [that.comparetime,max] }
                ]]
            }
              }
       })
        }
        this.myChart.setOption(option);
      },
      inintPic(){
           this.dates = this.rawData.map(function (item) {
                return item.time1.slice(11, 19)
              })
              this.dataline1 = this.rawData.map(function (item) {
                  return +item.value1;
               });
              this.dataline2 = this.rawData.map(function (item) {
                  return +item.value2;
               });
              this.dataline3 = this.rawData.map(function (item) {
                  return +item.value3;
               });
              this.dataline4 = this.rawData.map(function (item) {
                  return +item.value4;
               });
           this.dateset=['2020-08-22','2020-08-23','2020-08-24','2020-08-25']
           this.yvaluemax=Math.max.apply(Math, this.dataline1).toFixed(0)//初始y轴坐标值
           this.yvaluemin=Math.min.apply(Math, this.dataline1).toFixed(0)//初始y轴坐标值
           this.drawLine(this.dataline1,this.dataline2,this.dataline3,this.dataline4,this.dateset,this.yvaluemax,this.yvaluemin)
      },
      InitTable(){
        this.tableData= [{comparetime:'00:00:04',name:'tag1',averag:0,max:0,min:0},{comparetime:'00:00:04',name:'tag2',averag:0,max:0,min:0},{comparetime:'00:00:04',name:'tag3',averag:0,max:0,min:0},{comparetime:'00:00:04',name:'tag4',averag:0,max:0,min:0}]
        if(this.makefirst){
          for(var i=0;i<this.dateset.length;i++){
            this.tableData[i].name=this.dateset[i]
            this.tableData[i].comparetime=this.comparetime
            this.tableData[i].cdate=moment(this.valuedatetime1).format('YYYY-MM-DD')
        }
        }else{
          for(var i=0;i<this.dateset.length;i++){
            this.tableData[i].cdate=this.dateset[i]
            this.tableData[i].name=this.singletag
            this.tableData[i].comparetime=this.comparetime
        }
        }
        
         this.tableData[0].averag=this.averagevalue1
         this.tableData[0].max=this.tag1Max
         this.tableData[0].min=this.tag1Min
         this.tableData[1].averag=this.averagevalue2
         this.tableData[1].max=this.tag2Max
         this.tableData[1].min=this.tag2Min
         this.tableData[2].averag=this.averagevalue3
         this.tableData[2].max=this.tag3Max
         this.tableData[2].min=this.tag3Min
         this.tableData[3].averag=this.averagevalue4
         this.tableData[3].max=this.tag4Max
         this.tableData[3].min=this.tag4Min
         this.tableData=this.tableData.slice(0, this.dateset.length)
      },
    }
}
</script>
<style scoped>
.staticbox .platformContainer{
  margin-bottom: 0px;
  padding:15px 0px;
}
.staticbox .cardContainer{
  padding-left:0px;
}
</style>