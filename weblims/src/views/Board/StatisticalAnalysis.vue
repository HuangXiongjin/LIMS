<template>
    <el-row :gutter="20" class="container mgt24" style="height:750px;">
        <el-col :span='24' class="padt8 mgb24">
            <el-row>
                <el-col :span='3' class="mgr15 boxshadow">
                    <el-select v-model="searchObj.category" placeholder="品名" @change='getCategory'>
                        <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                        </el-option>
                    </el-select>
                </el-col>
            </el-row>
        </el-col>
        <el-col :span='12' style="height:38%;" class="mgb24"><div class="box" id='box1'></div></el-col>
        <el-col :span='12' style="height:38%;" class="mgb24"><div class="box" id='box2'></div></el-col>
        <el-col :span='24' style="height:45%;" class="padtop50">
            <div class="box" id='box3'>
                <el-table
                    :data="batchTableData.data"
                    size='small'
                    highlight-current-row
                    style="width: 100%"
                   >
                  <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                </el-table>
                <div class="paginationClass">
                        <el-pagination background  layout="total, prev, pager, next, jumper"
                        :total="batchTableData.total"
                        :current-page="batchTableData.offset"
                        :page-size="batchTableData.limit"
                        @size-change="handleSizeChange"
                        @current-change="handleCurrentChange">
                        </el-pagination>
                </div>
            </div>
        </el-col>
    </el-row>
</template>
<script>
import echarts from '@/assets/js/echarts.js'
var moment=require('moment')
export default {
    data(){

        return {
           searchObj:{category:'巴戟胶囊'},
           options: [{
                value: '选项1',
                label: '物料一'
                },{
                value: '选项2',
                label: '物料二'
                }],
           batchTableData:{ //展示的列表
                data:[
                    {Name:'玉米淀粉',VerifyDate:'2020-10-23',VerifyUser:'lig',ProductType:'辅料',Status:'质检',ProductNumber:'YM-11'},
                    {Name:'玉米淀粉',VerifyDate:'2020-10-24',VerifyUser:'lig',ProductType:'辅料',Status:'质检',ProductNumber:'YM-09'},
                    {Name:'玉米淀粉',VerifyDate:'2020-08-23',VerifyUser:'lig',ProductType:'辅料',Status:'质检',ProductNumber:'YM-21'},
                    {Name:'玉米淀粉',VerifyDate:'2020-11-21',VerifyUser:'lig',ProductType:'辅料',Status:'质检',ProductNumber:'YM-06'},
                    {Name:'玉米淀粉',VerifyDate:'2020-12-03',VerifyUser:'lig',ProductType:'辅料',Status:'质检',ProductNumber:'YM-07'},
                    
                  ],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
           echartspie:null,
           myecharts:null,
           yData:[45,27,36,21,35,33,40,45],
           xData:["请验审核","取样", "接收", "分发","质检","报告","质检审核","放行"],
           pieData:[{value:45, name:'请验审核'},{value:27, name:'取样'},{value:36, name:'接收'},{value:21, name:'分发'},{value:35, name:'质检'},
                    {value:33, name:'报告'},{value:40, name:'质检审核'},{value:45, name:'放行'}],
           batchtableconfig:[{prop:'Name',label:"样本品名"},{prop:'ProductNumber',label:'样本批次'},{prop:'VerifyDate',label:'登记时间',width:210},{prop:'VerifyUser',label:'登记人'},{prop:'ProductType',label:'类型'},{prop:'Status',label:'状态'}],//批次列表
        }
    },
    mounted(){
        this.drawpic()
        this.drawpie()
        this.getSelectOption()
    },
    beforeDestroy(){
            this.myecharts.clear()
            this.myecharts.dispose()
            this.myecharts=null
            this.echartspie.clear()
            this.echartspie.dispose()
            this.echartspie=null
    },
    methods: {
        getCategory(e){
            if(e=='玉米淀粉'){
                this.yData=[30,25,25,20,35,30,40,27]
                this.xData=["请验审核","取样", "接收", "分发","质检","报告","质检审核","放行"]
                this.pieData=[{value:30, name:'请验审核'},{value:25, name:'接收'},{value:20, name:'分发'},{value:35, name:'质检'},
                    {value:30, name:'报告'},,{value:25, name:'取样'},{value:27, name:'放行'},{value:40, name:'质检审核'}]
            }else if(e=='巴戟胶囊'){
                this.yData=[45,27,36,21,35,33,40,45]
                this.xData=["请验审核","取样", "接收", "分发","质检","报告","质检审核","放行"]
                this.pieData=[{value:45, name:'请验审核'},{value:21, name:'分发'},{value:35, name:'质检'},,{value:27, name:'取样'},{value:36, name:'接收'},
                    {value:33, name:'报告'},{value:40, name:'质检审核'},{value:45, name:'放行'}]
            }else if(e=='血府逐淤片'){
                this.yData=[43,28,15,24,35,37,49,33]
                this.xData=["请验审核","取样", "接收", "分发","质检","报告","质检审核","放行"]
                this.pieData=[{value:43, name:'请验审核'},{value:28, name:'取样'},{value:35, name:'质检'},
                    {value:37, name:'报告'},{value:49, name:'质检审核'},{value:15, name:'接收'},{value:24, name:'分发'},{value:33, name:'放行'}]
            }else{
                this.yData=[23,27,35,20,55,30,40,50]
                this.xData=["请验审核","取样", "接收", "分发","质检","报告","质检审核","放行"]
                this.pieData=[{value:23, name:'请验审核'},{value:27, name:'取样'},{value:35, name:'接收'},{value:20, name:'分发'},{value:55, name:'质检'},
                    {value:30, name:'报告'},{value:40, name:'质检审核'},{value:50, name:'放行'}]
            }
            this.drawpic()
            this.drawpie()
            
        },
        selectStatus(){ //点击tab行图表显示详细的信息

        },
          handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
            this.selectStatus()
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
            this.selectStatus()
        },
         getSelectOption() { //获取下拉列表选项
           this.axios.get('/lims/AllProduct').then((res) => {
               if(res.data.code=='1000'){
                  this.options=res.data.data.map((item) => {
                      return {
                          value:item,
                          label:item
                      }
                  })
               }

           })
        },
         drawpic(){ //绘制柱状图
            if(this.myecharts!==null){
                this.myecharts.clear()
                this.myecharts.dispose()
                this.myecharts=null
            }
            this.myecharts=echarts.init(document.getElementById('box1'))
            var xData = this.xData;
            var yData = this.yData
            var option = {
                backgroundColor: '#061326',
                "grid": {
                    "top": "15%",
                    "left": "-5%",
                    "bottom": "5%",
                    "right": "5%",
                    "containLabel": true
                },
                tooltip:{
                show:true 
                },
                animation: false,
                "xAxis": [{
                    "type": "category",
                    "data": xData,
                    "axisTick": {
                        "alignWithLabel": true
                    },
                    "nameTextStyle": {
                        "color": "#82b0ec"
                    },
                    "axisLine": {
                        show: false,
                        "lineStyle": {
                            "color": "#82b0ec"
                        }
                    },
                    "axisLabel": {
                        "textStyle": {
                            "color": "#fff"
                        },
                        margin: 30
                    }
                }],
                "yAxis": [{
                    show: false,
                    "type": "value",
                    "axisLabel": {
                        "textStyle": {
                            "color": "#fff"
                        },
                    },
                    "splitLine": {
                        "lineStyle": {
                            "color": "#0c2c5a"
                        }
                    },
                    "axisLine": {
                        "show": false
                    }
                }],
                "series": [{
                        "name": "",
                        type: 'pictorialBar',
                        symbolSize: [40, 10],
                        symbolOffset: [0, -6],
                        symbolPosition: 'end',
                        z: 12,
                        // "barWidth": "0",
                        "label": {
                            "normal": {
                                "show": true,
                                "position": "top",
                                // "formatter": "{c}%"
                                fontSize: 25,
                                fontWeight: 'bold',
                                color: '#34DCFF'
                            }
                        },
                        color: "#2DB1EF",
                        data: yData
                    },
                    {
                        name: '',
                        type: 'pictorialBar',
                        symbolSize: [40, 10],
                        symbolOffset: [0, 7],
                        // "barWidth": "20",
                        z: 12,
                        "color": "#2DB1EF",
                        "data": yData
                    },
                    {
                        name: '',
                        type: 'pictorialBar',
                        symbolSize: [50, 15],
                        symbolOffset: [0, 12],
                        z: 10,
                        itemStyle: {
                            normal: {
                                color: 'transparent',
                                borderColor: '#2EA9E5',
                                borderType: 'solid',
                                borderWidth: 1
                            }
                        },
                        data: yData
                    },
                    {
                        name: '',
                        type: 'pictorialBar',
                        symbolSize: [70, 20],
                        symbolOffset: [0, 18],
                        z: 10,
                        itemStyle: {
                            normal: {
                                color: 'transparent',
                                borderColor: '#19465D',
                                borderType: 'solid',
                                borderWidth: 2
                            }
                        },
                        data: yData
                    },
                    {
                        type: 'bar',
                        //silent: true,
                        "barWidth": "40",
                        barGap: '10%', // Make series be overlap
                        barCateGoryGap: '10%',
                        itemStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 0.7, [{
                                        offset: 0,
                                        color: "#38B2E6"
                                    },
                                    {
                                        offset: 1,
                                        color: "#0B3147"
                                    }
                                ]),
                                opacity: .8
                            },
                        },
                        data: yData
                    }
                ]
            };
            
            this.myecharts.setOption(option)
        },
        drawpie(){
            if(this.echartspie!==null){
                this.echartspie.clear()
                this.echartspie.dispose()
                this.echartspie=null
            }
            this.echartspie=echarts.init(document.getElementById('box2'))
            var option = {
            color: ['#37a2da','#32c5e9','#23d699','#ffdb5c','#ff9f7f','#fb7293','#FF3366','#8378ea'],
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            toolbox: {
                show : true,
            
            },
            legend: {
                type:"scroll",
                orient: 'vertical',
                left:'10%',
                align:'left',
                top:'middle',
                textStyle: {
                    color:'#222'
                },
                height:150
            },
            series : [
                {
                    name:'样本状态',
                    type:'pie',
                    radius : [0, 100],
                    data:this.pieData,
                    label: {
                        normal: {
                        position: 'inner',
                        show : true
                        }
                  }
                }
            ]
        };
        this.echartspie.setOption(option)
        }
    },
}
</script>
<style scoped>
  .box{
      background-color:#FFFF99;
      height: 100%;
  }
  #box3{
      background-color: #fff;
  }
</style>