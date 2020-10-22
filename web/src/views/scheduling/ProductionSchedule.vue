<template>
  <el-row :gutter="15">
    <el-col :span="24">
      <el-collapse class="marginBottom">
        <el-collapse-item title="多条件查询生产日程安排">
          <el-form :model="ZYTaskTableData.searchField" :inline="true" label-width="120px">
            <el-form-item label="批次号">
              <el-input v-model="ZYTaskTableData.searchField.BatchID"></el-input>
            </el-form-item>
            <el-form-item label="品名">
              <el-select v-model="ZYTaskTableData.searchField.BrandName" placeholder="请选择" style="width:200px">
                <el-option v-for="item in scheduleData" :key="item.ID" :label="item.BrandName" :value="item.BrandName">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="工艺段">
              <el-select v-model="ZYTaskTableData.searchField.PUName" placeholder="请选择" style="width:200px" @change="getEqTableData">
                <el-option v-for="item in optionsPUName" :key="item.ID" :label="item.PUName" :value="item.PUName">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="设备">
               <el-select v-model="ZYTaskTableData.searchField.EQPCode" placeholder="请选择" style="width:200px">
                <el-option v-for="item in optionsProductEquipment" :key="item.value" :label="item.EQPCode+ '-' +item.EQPName" :value="item.EQPCode">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="计划开始时间">
               <el-date-picker v-model="ZYTaskTableData.searchField.PlanStartTime" value-format="yyyy-MM-dd" type="date" placeholder="选择日期" style="width:200px"></el-date-picker>
            </el-form-item>
            <el-form-item label="计划结束时间">
               <el-date-picker v-model="ZYTaskTableData.searchField.PlanEndTime" value-format="yyyy-MM-dd" type="date" placeholder="选择日期" style="width:200px"></el-date-picker>
            </el-form-item>
            <el-form-item label="实际开始时间">
               <el-date-picker v-model="ZYTaskTableData.searchField.ActBeginTime" value-format="yyyy-MM-dd" type="date" placeholder="选择日期" style="width:200px"></el-date-picker>
            </el-form-item>
            <el-form-item label="实际结束时间">
               <el-date-picker v-model="ZYTaskTableData.searchField.ActEndTime" value-format="yyyy-MM-dd" type="date" placeholder="选择日期" style="width:200px"></el-date-picker>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="small" @click="resetSearchField">重置</el-button>
              <el-button type="primary" size="small" @click="getSelectedEq">查询</el-button>
            </el-form-item>
          </el-form>
        </el-collapse-item>
      </el-collapse>
    </el-col>
    <el-col :span="4">
      <div class="platformContainer">
        <p>设备计划生产时间线</p>
        <el-timeline>
          <el-timeline-item
            v-for="(item, index) in eqTimeLineData"
            :key="index"
            :timestamp="item.time">
            <span>{{ item.StartBC }}班</span>{{item.label}} <span>{{ item.EQPName }}</span>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-col>
    <el-col :span="20">
      <div class="platformContainer">
        <el-table :data="ZYTaskTableData.data" border size="small">
          <el-table-column type="selection"></el-table-column>
          <el-table-column prop="BatchID" label="批次号"></el-table-column>
          <el-table-column prop="BrandName" label="品名"></el-table-column>
          <el-table-column prop="PlanQuantity" label="批次重量"></el-table-column>
          <el-table-column prop="PUName" label="工艺段名称"></el-table-column>
          <el-table-column prop="EQPCode" label="设备编码"></el-table-column>
          <el-table-column prop="EQPName" label="设备名称"></el-table-column>
          <el-table-column prop="PlanStartTime" label="计划开始时间"></el-table-column>
          <el-table-column prop="PlanEndTime" label="计划结束时间"></el-table-column>
          <el-table-column prop="ActBeginTime" label="实际开始时间"></el-table-column>
          <el-table-column prop="ActEndTime" label="实际结束时间"></el-table-column>
          <el-table-column prop="StartBC" label="开始运行班次"></el-table-column>
          <el-table-column prop="EndBC" label="结束运行班次"></el-table-column>
        </el-table>
      </div>
    </el-col>
  </el-row>
</template>
<script>
import echarts from '@/assets/js/echarts.js'
export default {
  name:"ProductionSchedule",
  data(){
    return {
      scheduleData:[],
      optionsPUName:[],
      optionsProductEquipment:[],
      ZYTaskTableData:{
        tableName:"ZYTask",
        data:[],
        searchField:{
          BatchID:"",
          BrandName:"",
          PUName:"",
          EQPCode:"",
          PlanStartTime:"",
          PlanEndTime:"",
          ActBeginTime:"",
          ActEndTime:"",
          StartBC:"",
          EndBC:"",
        }
      },
      eqTimeLineData:[]
    }
  },
  created(){
    this.getScheduleTableData()
    this.getPUNameTableData()
    this.getEqTableData()
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
          that.scheduleData = res.data.data.rows
        }else{
          that.$message({
            type: 'info',
            message: res.data.message
          });
        }
      })
    },
    getPUNameTableData(){ //获取工序
      var that = this
      var params = {
        tableName: "ProcessUnit",
      }
      this.axios.get("/api/CUID",{
        params: params
      }).then(res => {
        if(res.data.code === "200"){
          that.optionsPUName = res.data.data.rows
        }else{
          that.$message({
            type: 'info',
            message: res.data.message
          });
        }
      })
    },
    getEqTableData(){ //获取设备
      var that = this
      var params = {
        tableName: "ProductEquipment",
        PUName: this.ZYTaskTableData.searchField.PUName,
      }
      this.axios.get("/api/CUID",{
        params: params
      }).then(res => {
        if(res.data.code === "200"){
          that.optionsProductEquipment = res.data.data.rows
        }else{
          that.$message({
            type: 'info',
            message: res.data.message
          });
        }
      })
    },
    getSelectedEq(){ // 查询绑定设备
      var params={
        tableName:this.ZYTaskTableData.tableName,
        BatchID:this.ZYTaskTableData.searchField.BatchID,
        BrandName:this.ZYTaskTableData.searchField.BrandName,
        PUName:this.ZYTaskTableData.searchField.PUName,
        EQPCode:this.ZYTaskTableData.searchField.EQPCode,
        PlanStartTime:this.ZYTaskTableData.searchField.PlanStartTime,
        PlanEndTime:this.ZYTaskTableData.searchField.PlanEndTime,
        ActBeginTime:this.ZYTaskTableData.searchField.ActBeginTime,
        ActEndTime:this.ZYTaskTableData.searchField.ActEndTime,
        StartBC:this.ZYTaskTableData.searchField.StartBC,
        EndBC:this.ZYTaskTableData.searchField.EndBC
      }
      this.axios.get('/api/CUID',{params:params}).then(res => {
        if(res.data.code === "200"){
          var data = res.data.data
          this.ZYTaskTableData.data = data.rows
          this.ZYTaskTableData.data.forEach(item =>{
            this.eqTimeLineData.push(
              {time:item.PlanStartTime,label:"计划开始",StartBC:item.StartBC,EQPName:item.EQPName},
              {time:item.PlanEndTime,label:"计划结束",EndBC:item.EndBC,EQPName:item.EQPName},
            )
          })
        }
      },error=>{
        console.log("请求错误")
      })
    },
    resetSearchField(){
      this.ZYTaskTableData.searchField = {
        BatchID:"",
        BrandName:"",
        PUName:"",
        EQPCode:"",
        PlanStartTime:"",
        PlanEndTime:"",
        ActBeginTime:"",
        ActEndTime:"",
        StartBC:"",
        EndBC:"",
      }
    }
  },
}
</script>
<style scoped>

</style>
