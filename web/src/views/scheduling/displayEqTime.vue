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
            <div id="container" style="width:100%;height:600px;"></div>
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
            innerData:[],
            outData:[],
            options:[],
            pucode:'1006',
            ProductEquipmentTableData:[]
        }
    },
    mounted(){
        this.getPUName()
        this.getEqlist()
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
        getPUEQTableData(){
            var params={
                tableName:'ProductEquipment',
                PUCode:this.pucode
            }
            this.axios.get("/api/CUID",{params: params}).then(res => {
                if(res.data.code === "200"){
                    this.ProductEquipmentTableData = res.data.data.rows
                }else{
                    this.$message({
                    type: 'info',
                    message: res.data.message
                    });
                }
            })
        },
        getEqlist(){ //渲染展示的设备
            this.getPUEQTableData()
            var params={
                tableName:'ZYTask',
                PUCode:this.pucode
            }
            this.axios('/api/CUID',{params:params}).then((res) => {
                var arr=res.data.data.rows
                this.innerData = []
                this.outData = []
                this.yxeqlist=[]
                this.ProductEquipmentTableData.forEach((item,index) => {
                   var barList = []
                   arr.forEach(value => {
                       if(item.EQPCode === value.EQPCode){
                           barList.push({
                               "startTime":value.PlanStartTime,
                               "endTime":value.PlanEndTime,
                               "colorNum":index,
                               "item":value.BatchID,
                               "BrandName":value.BrandName
                           })
                       }
                   })
                   this.innerData.push({
                       "plant":item.EQPCode,
                       "list":barList
                   })
                })
                if(this.echarts){
                    this.echarts.dispose()
                }
                this.showPic()
            })

        },
        showPic(){
            this.$nextTick(() => {
                this.echarts = echarts.init(document.getElementById('container'));
                let data=this.innerData
                let seriesData = [];
                let yAxisData_plant = []; //设备名称

                data.forEach((item, index) => {
                    yAxisData_plant.push(item.plant);
                    let bgColor;
                    item.list.forEach((listItem, listIndex) => {
                        switch (listItem.colorNum) {
                            case 0:
                                bgColor = 'rgba(0,187,255,.4)';
                                break;
                            case 1:
                                bgColor = 'rgba(255,207,107,.4)';
                                break;
                            case 2:
                                bgColor = 'rgba(80,227,194,.4)';
                                break;
                            case 3:
                                bgColor = 'rgba(255,115,115,.4)';
                                break;
                            default:
                                bgColor = 'rgba(0,187,255,.4)'
                        }
                        let startTime = new Date(listItem.startTime).getTime();
                        let endTime = new Date(listItem.endTime).getTime();
                        seriesData.push({
                            name: listItem.item,
                            BrandName:listItem.BrandName,
                            value: [
                                listIndex,
                                startTime,
                                endTime,
                            ],
                            itemStyle: {
                                normal: {
                                    color: bgColor
                                }
                            }
                        });
                    })

                });

                var option = {
                        backgroundColor: '#fff',
                        tooltip: {
                            formatter: function (params) {
                                return "批次号："+params.data.name + "<br>" +
                                        "品名："+params.data.BrandName + "<br>"+
                                        "计划开始时间：" + moment(params.value[1]).format("YYYY-MM-DD HH:mm:ss")+"<br>"+
                                        "计划结束时间：" + moment(params.value[2]).format("YYYY-MM-DD HH:mm:ss")
                            }
                        },
                        grid: {
                            top: 48,
                            left: 120,
                            right: 50,
                            bottom: 50,
                            height:500
                        },
                        dataZoom: [{
                            type: 'slider',
                            filterMode: 'weakFilter',
                            showDataShadow: false,
                            top: 570,
                            height: 10,
                            borderColor: 'transparent',
                            backgroundColor: '#e2e2e2',
                            handleIcon: 'M10.7,11.9H9.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4h1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7v-1.2h6.6z M13.3,22H6.7v-1.2h6.6z M13.3,19.6H6.7v-1.2h6.6z', // jshint ignore:line
                            handleSize: 20,
                            handleStyle: {
                                shadowBlur: 6,
                                shadowOffsetX: 1,
                                shadowOffsetY: 2,
                                shadowColor: '#aaa'
                            },
                            labelFormatter: ''
                        }, {
                            type: 'inside',
                            filterMode: 'weakFilter'
                        }],
                        xAxis: {
                            type: 'time',
                            scale: true,
                            position: 'top',
                            splitNumber: 7,
                            axisLabel: {
                                show: true,
                                textStyle: {color: '#ffffff'},
                                interval: 0,
                                margin: 15,
                                fontSize: 14,
                                formatter:function (value, index) {
                                    var date = new Date(value);
                                    var texts = [date.getFullYear(),(date.getMonth() + 1), date.getDate()].join('/');
                                    return texts;
                                }
                            },
                            axisLine: {show: false,},
                            splitLine: {
                                show: true,
                                lineStyle: {color: 'rgba(233,233,233,0.1)'}
                            },
                            axisTick: {
                                lineStyle: {
                                    color: '#fff'
                                }
                            }
                        },
                        yAxis: {
                            axisLine: {
                                onZero: false,
                                show: false
                            },
                            axisLabel: {
                                show: true,
                                textStyle: {color: '#ffffff'},
                                fontSize: 14
                            },
                            splitLine: {
                                show: true,
                                lineStyle: {color: 'rgba(233,233,233,0.1)'}
                            },
                            inverse: true,
                            data: yAxisData_plant
                        },
                        series: [{
                            type: 'custom',
                            renderItem: function (params, api) {
                                var categoryIndex = api.value(0);
                                var start = api.coord([api.value(1), categoryIndex]);
                                var end = api.coord([api.value(2), categoryIndex]);
                                var height = api.size([0, 1])[1] * 0.6;
                                var rectShape = echarts.graphic.clipRectByRect({
                                    x: start[0],
                                    y: start[1] - 5,
                                    width: end[0] - start[0],
                                    height: 10
                                }, {
                                    x: params.coordSys.x,
                                    y: params.coordSys.y,
                                    width: params.coordSys.width,
                                    height: params.coordSys.height
                                });

                                return rectShape && {
                                    type: 'rect',
                                    shape: rectShape,
                                    style: api.style()
                                };

                            },
                            encode: {
                                x: [1, 2],
                                y: 0
                            },
                            data: seriesData
                        }]
                    }
                this.echarts.setOption(option);
            })
            
        }
    }
}
</script>
<style scoped>

</style>