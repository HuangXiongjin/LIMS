<template>
  <el-row :gutter="15">
    <el-col :span='24'>
      <div class="page-title"><span>批物料平衡统计</span></div>
      <el-row :gutter="15">
        <el-col :span="5">
          <div class="platformContainer">
            <p class="marginBottom">选择要查询的品名</p>
            <el-input class="marginBottom" v-model="productName" placeholder="关键字搜索" @change="handleChangeProductName"></el-input>
            <el-tag class="marginBottom marginRight cursor-pointer" v-for="(item,index) in results" :key="index" v-bind:effect="item.BrandName===BrandName?'dark':'plain'" @click="clickBrandTag(item.BrandName,item.BrandCode)">{{item.BrandName}}</el-tag>
          </div>
        </el-col>
        <el-col :span="19">
          <div class="platformContainer">
            <el-form :inline="true">
              <el-form-item label="查询月份">
                <el-date-picker type="month" v-model="searchDate" size="small" format="yyyy-MM" value-format="yyyy-MM" :editable="false" :clearable="false" style="width: 160px;" @change="getChartData"></el-date-picker>
              </el-form-item>
            </el-form>
            <ve-histogram :data="chartData" :extend="chartExtend"></ve-histogram>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>
<script>
var moment = require('moment');
export default {
  data() {
    return {
      scheduleTableData:[],
      results:[],
      productName:"",
      BrandName:"",
      BrandCode:"",
      searchDate:moment().format("YYYY-MM"),
      chartExtend:{
        'yAxis.0':{
          name: 'kg',
        },
        series:{
          barMaxWidth: 50
        }
      },
      chartData: {
        columns: ['批次号', '物料总重量'],
        rows:[]
      }
    }
  },
  mounted(){
    this.getScheduleTableData()
  },
  methods: {
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
    handleChangeProductName(queryString){
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
      this.BrandName = BrandName
      this.BrandCode = BrandCode
      this.getChartData()
    },
    getChartData(){
      var that = this
      var params = {
        BrandCode: this.BrandCode,
        month: this.searchDate,
      }
      this.axios.get("/api/materielbalance",{
        params: params
      }).then(res => {
        if(res.data.code === "200"){
          that.chartData.rows = res.data.data.row
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
