<template>
    <el-row :gutter="15">
        <el-col :span="4">
            <div class="platformContainer">
                <p class="marginBottom">请选择要展示的品名</p>
                <el-input class="marginBottom" v-model="productName" placeholder="关键字搜索" @change="handleChangeProductName"></el-input>
                <el-tag class="marginBottom marginRight cursor-pointer" v-for="(item,index) in results" :key="index" v-bind:effect="item.BrandName===BrandActive?'dark':'plain'" @click="clickBrandTag(item.BrandName,item.BrandCode)">{{item.BrandName}}</el-tag>
            </div>
        </el-col>
        <el-col :span='20'>
            <el-row>
                <el-col :span='24'>
                    <p class="platformContainer" v-if="BrandActive">当前展示的品名：{{BrandActive}}</p>
                </el-col>
                <el-col :span='24'>
                    <div class="platformContainer" style="backgroundColor:#fff;">
                        <el-form :inline="true" :model="formInline">
                                <el-form-item label="计划单号">
                                    <el-select v-model="formInline.CurrentBrandNum" placeholder="计划单号" @change="onSubmit">
                                        <el-option v-for="(item,index) in selectBrandNum" :key='index'  :label='item.BrandCodelabel'  :value="item.BrandCodevalue" ></el-option>
                                    </el-select>
                                </el-form-item>
                        </el-form>
                        <div id="main" style="width:100%; height:750px;" v-loading="loading">排产进度表</div>
                    </div>
                </el-col>
            </el-row>
        </el-col>
    </el-row>
</template>
<script>
import echarts from '@/assets/js/echarts.js'
export default {
    data(){
        return {
            datesection:'月',
            loading:false,
            productName:'',
            results:[],
            BrandActive:'',
            BrandCode:'',
            PUCode:'',
            PUName:'',
            inProcessList:[],
            fileList: [],
            ActiveIndex:10,
            FileName:'',
            scheduleTableData:[],
            formInline: {CurrentBrandNum: '45'},
            selectBrandNum:[],
            ydata:[],
            PlanStartTime:[],
            PlanEndTime:[]
        }
    },
     created(){
      this.getScheduleTableData()
      this.onSubmit() //初始化展示效果添加
    },
    methods: {
        onSubmit(){
           var params = {
                tableName: "PlanManager",
                PlanNum:this.formInline.CurrentBrandNum
                }
            this.axios.get("/api/CUID",{
                params: params
            }).then(res => {
                var arr=res.data.data.rows
                this.ydata=arr.map((res) => {
                    return res.BatchID
                })
                this.PlanStartTime=arr.map((res) => {
                    return new Date(res.PlanBeginTime.replace('-', '/'))
                })
                this.PlanEndTime=arr.map((res) => {
                    return new Date(res.PlanEndTime.replace('-', '/'))
                })
                this.drawPic(this.ydata,this.PlanStartTime,this.PlanEndTime)
        })
        },
        drawPic(ydata,planstarttime,planendtime) {
            var myCharts = echarts.init(document.getElementById('main'));
            var option = {
                title: {
                    text: '排产进度表',
                    left: 10,
                    textStyle: {
                      color: '#666'  //设置title文字颜色
                  }
                },
                legend: {
                    y: 'top',
                    data: ['计划完成时间'], //修改的地方1,
                    textStyle: {
                      color: '#666' //设置图例文字颜色
                  }
                },
                grid: {
                    containLabel: true,
                    left: 20,
                    bottom:10
                },
                xAxis: {
                    name:'时间',
                    type: 'time',
                    axisLine: { lineStyle: { color: '#666' } } //控制x轴坐标文字颜色
                },
                yAxis: {
                    name:'批次',
                    data:[...ydata],
                    axisLine: { lineStyle: { color: '#666' } }  //控制y轴坐标文字颜色
                },
                tooltip: {
                    trigger: 'axis',
                    formatter: function(params) {
                        var res = params[0].name + "</br>"
                        var date0 = params[0].data;
                        var date1 = params[1].data;
                        date0 = date0.getFullYear() + "-" + (date0.getMonth() + 1) + "-" + (date0.getDate().toString().padStart(2,0))+ "  " + (date0.getHours().toString().padStart(2,0))+':'+(date0.getMinutes().toString().padStart(2,0))+':'+(date0.getSeconds().toString().padStart(2,0));
                        date1 = date1.getFullYear() + "-" + (date1.getMonth() + 1) + "-" + (date1.getDate().toString().padStart(2,0))+ "  " + (date1.getHours().toString().padStart(2,0))+':'+(date1.getMinutes().toString().padStart(2,0))+':'+(date1.getSeconds().toString().padStart(2,0));
                        res += params[0].seriesName + "~" + params[1].seriesName + ":</br>" + date0 + "~" + date1 + "</br>"
                        return res;
                    }

                },
                series: [
                    {
                        name: '计划开始时间',
                        type: 'bar',
                        stack: 'test1',
                        itemStyle: {
                            normal: {
                                color: 'rgba(0,0,0,0)'
                            }
                        },
                        data:planstarttime,
                        barMaxWidth: 30,
                    },
                    {
                        name: '计划完成时间',
                        type: 'bar',
                        stack: 'test1',
                        //修改地方2
                        itemStyle: {
                            normal: {
                                color: '#06ACB5'
                            }
                        },
                        data:planendtime,
                        barMaxWidth:20,
                    }
                ]
            };
            myCharts.setOption(option);
        },
        getScheduleTableData(){ //获取品名
        var that = this
        var params = {
          tableName: "ProductRule",
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
            that.scheduleTableData = res.data.data.rows
            that.results = that.scheduleTableData
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      },
        handleChangeProductName(queryString){ //左侧模糊查询
            if(queryString != ""){
            this.results = this.scheduleTableData.filter((string) =>{
                return Object.keys(string).some(function(key) {
                return String(string[key]).toLowerCase().indexOf(queryString) > -1
                })
            })
            }else{
            this.results = this.scheduleTableData
            }
      },
       clickBrandTag(BrandName,BrandCode){
        this.BrandActive = BrandName
        this.BrandCode = BrandCode
        this.selectBrandNum=[{BrandCodelabel:'',BrandCodevalue:''}]
        this.formInline.CurrentBrandNum=''
        this.getBrandCode(BrandName)
      },
       getBrandCode(BrandName){ //查询当前品名绑定的工序
        var that = this
        var params = {
          tableName: "product_plan",
          BrandName:BrandName,
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res => {
          if(res.data.code === "200"){
           var arr=res.data.data.rows
           this.selectBrandNum=arr.map((res, index) => {
               return {BrandCodelabel:res.PlanNum,BrandCodevalue:res.PlanNum}
           })
          }else{
            that.$message({
              type: 'info',
              message: res.data.message
            });
          }
        })
      }
    },
}
</script>
<style scoped>

</style>
