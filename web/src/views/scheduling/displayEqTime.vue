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
            <div id="container" style="width:100%;height:660px;"></div>
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
            innerData:[],
            yAxisData_plant:[],
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
            this.innerData = []
            let that = this
            var params={
                tableName:'ProductEquipment',
                PUCode:this.pucode
            }
            this.axios.get("/api/CUID",{params: params}).then(res => {
                if(res.data.code === "200"){
                    this.ProductEquipmentTableData = res.data.data.rows
                    this.ProductEquipmentTableData.forEach(item => {
                      // that.yAxisData_plant.push(item.EQPCode)
                      that.innerData.push({
                         "plant":item.EQPCode
                      })
                    })
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
            let that = this
            var params={
                tableName:'ZYTask',
                PUCode:this.pucode
            }
            this.axios('/api/CUID',{params:params}).then((res) => {
                var arr=res.data.data.rows
                that.innerData.forEach((item,index) =>{
                   var barList = []
                   arr.forEach(value => {
                       if(value.EQPCode === item.plant){
                           barList.push({
                               "startTime":value.PlanStartTime,
                               "endTime":value.PlanEndTime,
                               "colorNum":index,
                               "item":value.BatchID,
                               "BrandName":value.BrandName,
                               "EQPName":value.EQPName,
                               "EQPCode":value.EQPCode,
                           })
                       }
                   })
                  item.list = barList
                })
                if(that.echarts){
                    that.echarts.dispose()
                }
                that.showPic()
            })

        },
        showPic(){
            let that = this
            this.$nextTick(() => {
                that.echarts = echarts.init(document.getElementById('container'));
                let data=this.innerData
                let seriesData = [];
                data.forEach((item, index) => {
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
                            EQPCode:listItem.EQPCode,
                            EQPName:listItem.EQPName,
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
                      tooltip: {
                          formatter: function (params) {
                              return "批次号："+params.data.name + "<br>" +
                                      "品名："+params.data.BrandName + "<br>"+
                                      "设备："+params.data.EQPCode + "-" +params.data.EQPName + "<br>"+
                                      "计划开始时间：" + moment(params.value[1]).format("YYYY-MM-DD HH:mm:ss")+"<br>"+
                                      "计划结束时间：" + moment(params.value[2]).format("YYYY-MM-DD HH:mm:ss")
                          }
                      },
                      grid: {
                          top: 50,
                          left: 100,
                          right: 50,
                          bottom: 60,
                          height:500
                      },
                      dataZoom: [{
                          type: 'slider',
                          filterMode: 'weakFilter',
                          showDataShadow: false,
                          top: 600,
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
                          position:'top',
                          axisLabel: {
                              show: true,
                              formatter:function (value, index) {
                                  var date = new Date(value);
                                  var texts = [date.getFullYear(),(date.getMonth() + 1), date.getDate()].join('-');
                                  return texts;
                              }
                          },
                      },
                      yAxis: {
                          data: that.yAxisData_plant.reverse(),
                          inverse:true,
                          //网格样式
                          splitLine: {
                              show: true,
                          }
                      },
                      series: [{
                          type: 'custom',
                          renderItem: function (params, api) {
                              var categoryIndex = api.value(0);//这里使用 api.value(0) 取出当前 dataItem 中第一个维度的数值。
                              var start = api.coord([api.value(1), categoryIndex]); // 这里使用 api.coord(...) 将数值在当前坐标系中转换成为屏幕上的点的像素值。
                              var end = api.coord([api.value(2), categoryIndex]);
                              var height = api.size([0, 1])[1];

                              return {
                                  type: 'rect',// 表示这个图形元素是矩形。还可以是 'circle', 'sector', 'polygon' 等等。
                                  shape: echarts.graphic.clipRectByRect({ // 矩形的位置和大小。
                                      x: start[0],
                                      y: start[1] - height / 2,
                                      width: end[0] - start[0],
                                      height: height
                                  }, { // 当前坐标系的包围盒。
                                      x: params.coordSys.x,
                                      y: params.coordSys.y,
                                      width: params.coordSys.width,
                                      height: params.coordSys.height
                                  }),
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
                that.echarts.setOption(option);
            })
            
        },
    }
}
</script>
<style scoped>

</style>
