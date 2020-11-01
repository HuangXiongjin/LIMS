<template>
    <el-row>
        <el-col :span='24' class="platformContainer">批次设备运行展示</el-col>
        <el-col :span='24' class="platformContainer"><el-button  @click="showPic">click</el-button></el-col>
         <el-col :span='24' class="platformContainer">
           <div style="height:40px;fontSize:16px;fontWeight:700;">已选设备列表</div>
              <el-table
                  :data="eqlistTableData.data"
                  highlight-current-row
                  size='small'
                  border
                  ref="eqlistmultipleTable"
                  @row-click='getBatchID'
                  style="width: 100%">
                  <el-table-column v-for="item in eqlistableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="eqlistTableData.total"
                  :current-page="eqlistTableData.offset"
                  :page-size="eqlistTableData.limit"
                  @size-change="eqlistHandleSizeChange"
                  @current-change="eqlistHandleCurrentChange">
                  </el-pagination>
            </div>
        </el-col>
        <el-col :span='24' class="platformContainer">
            <div id="container" style="width:100%;height:700px;"></div>
        </el-col>
    </el-row>
</template>
<script>
import echarts from'@/assets/js/echarts.js'
var moment=require("moment")
export default {
    data(){
        return {
            echarts:null,
            eqlistTableData:{ //下发批次列表
                tableName:"PlanManager",
                data:[],
                limit: 10,
                offset: 1,
                total: 0,
                },
            eqlistableconfig:[{prop:'BatchID',label:'批次号'},{prop:'BrandCode',label:'品名编码'},{prop:'BrandName',label:'品名'}],//选择设备列表
            yxeqlist:[],
            startTime:[],
            EndTime:[]

        }
    },
    mounted(){
        this.getEchartsData()
    },
    destroyed(){
        this.echarts.dispose()
    },
    methods:{
        getBatchID(e){
            var BatchID=e.BatchID
            var params={
                tableName:'EquipmentBatchRunTime',
                limit:10,
                offset:0,
                BatchID:BatchID
            }
            this.axios('/api/CUID',{params:params}).then((res) => {
                var arr=res.data.data.rows
                if(this.echarts){
                    this.echarts.dispose()
                }
                this.yxeqlist=arr.map((item) => {
                    return item.PUName
                })
                this.startTime=arr.map((item) => {
                    return new Date(moment(item.startTime).format("YYYY/MM/DD HH:mm:ss"))
                })
                this.EndTime=arr.map((item) => {
                    return new Date(moment(item.EndTime).format("YYYY/MM/DD HH:mm:ss"))
                })
                this.showPic(this.yxeqlist,this.startTime,this.EndTime)
            })

        },
        getEchartsData(){
            var params={
                tableName:'EquipmentBatchRunTime',
                limit:10,
                offset:0,
            }
            this.axios.get('/api/CUID',{params:params}).then((res) => {
                if(res.data.code === "200"){
                    var data = res.data.data
                    this.eqlistTableData.data = data.rows
                    this.eqlistTableData.total = data.total
                }
                },err=>{
                    console.log("请求错误")
                })
        },
        eqlistHandleSizeChange(limit){ //已选设备 每页条数切换
            this.eqlistTableData.limit = limit
            this.getEchartsData()
        },
        eqlistHandleCurrentChange(offset) { //已选设备 页码切换
            this.eqlistTableData.offset = offset
            this.getEchartsData()
        },
        showPic(yxeqlist,startTime,EndTime){
        this.echarts = echarts.init(document.getElementById('container'));
        var option = {
            title: {
                text: '项目实施进度表',
                left: 10
            },
            legend: {
                y: 'top',
                data: ['计划时间']  //修改的地方1
        
            },
            grid: {
                containLabel: true,
                left: 20
            },
            xAxis: {
                type: 'time',
            },
        
            yAxis: {
                data:yxeqlist
        
            },
            tooltip: {
                trigger: 'axis',
                formatter: function(params) {
                    var res = params[0].name + "</br>"
                    var date0 = params[1].data;
                    var date1 = params[0].data;
                    date0 = date0.getFullYear() + "-" + (date0.getMonth() + 1) + "-" + date0.getDate()+"--"+date0.getHours()+":"+date0.getMinutes()+":"+date0.getSeconds();
                    date1 = date1.getFullYear() + "-" + (date1.getMonth() + 1) + "-" + date1.getDate()+"--"+date1.getHours()+":"+date1.getMinutes()+":"+date1.getSeconds();
                    res += params[0].seriesName + "~" + params[1].seriesName + ":</br>" + date0 + "~" + date1 + "</br>"
                    return res;
                }
            },
            series: [
        
                {
                    name: '计划开始时间',
                    type: 'bar',
                    stack: 'test1',
                    barWidth:30,
                    itemStyle: {
                        normal: {
                            color: 'rgba(0,0,0,0)'
                        }
                    },
                    data:startTime
                },
                {
                    name: '计划时间',
                    type: 'bar',
                    stack: 'test1',
                    barWidth:30,
                    //修改地方2
                    itemStyle: {
                        normal: {
                            color: 'lightblue'
                        }
                    },
                    data:EndTime

                }
            ]
        };
        this.echarts.setOption(option);
        }
    }
}
</script>
<style scoped>

</style>