<template>
    <el-row>
        <el-col :span='24' class="platformContainer">批次设备运行展示</el-col>
        <el-col :span='24' class="platformContainer">
            <el-select v-model="pucode" placeholder="请选择" @change='getEqlist' class="marginBottom">
                <el-option
                v-for="(item,index) in options"
                :key="index"
                :label="item.label"
                :value="item.value">
                </el-option>
            </el-select>
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
            EndTime:[],
            options:[],
            pucode:''

        }
    },
    mounted(){
        this.getPUName()
    },
    methods:{
            //获取工艺段
        getPUName(){
            var params={
                tableName:'ProcessUnit',
            }
            this.axios.get('/api/CUID',{params:params}).then((res) => {
                var arr=res.data.data.rows
                this.options=arr.map((item) => {
                    return {
                        value:item.PUCode,
                        label:item.PUCode+item.PUName
                    }
                })
            })
        },
        getEqlist(){ //渲染展示的设备
            var params={
                tableName:'EquipmentBatchRunTime',
                limit:10,
                offset:0,
                PUCode:this.pucode
            }
            this.axios('/api/CUID',{params:params}).then((res) => {
                var arr=res.data.data.rows
                this.startTime = []
                this.EndTime = []
                arr.forEach((item) => {
                    this.startTime.push(moment(item.StartTime).format('YYYY-MM-DD HH:mm:ss'))
                    this.EndTime.push(moment(item.EndTime).format('YYYY-MM-DD HH:mm:ss'))
                    this.yxeqlist.push(item.EQPCode+item.EQPName)
                })
                if(this.echarts){
                    this.echarts.dispose()
                }
                this.showPic()
            })

        },
        showPic(){
        this.echarts = echarts.init(document.getElementById('container'));
        var option = {
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
                type: 'category',
                data:this.yxeqlist
        
            },
            tooltip: {
                trigger: 'axis',
                formatter: function(params) {
                    var res = params[0].name + "</br>"
                    var date0 = params[0].data;
                    var date1 = params[1].data;
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
                    data:this.startTime
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
                    data:this.EndTime

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